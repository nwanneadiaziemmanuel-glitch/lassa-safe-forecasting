import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from .features import make_features


def make_model(random_state=42):
    return GradientBoostingRegressor(
        random_state=random_state,
        n_estimators=100,
        max_depth=2,
        learning_rate=0.05,
        loss="huber",
    )


def seasonal_naive(df, horizon=1, target="confirmed_cases"):
    """Predict y[t+h] using the observation 52 weeks before the target."""
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    # At origin t, the target is t+h. The seasonal analogue is t+h-52.
    return df[target].shift(52 - horizon)


def historical_seasonal_mean(train, target_week, target="confirmed_cases"):
    hist = train.loc[train["epi_week"] == target_week, target]
    return float(hist.mean()) if len(hist) else float(train[target].mean())


def direct_target(df, horizon, target="confirmed_cases"):
    """Return the future target aligned to the current forecast origin."""
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    return df[target].shift(-horizon)


def fit_predict(train_df, test_df, feature_cols, horizon=1, target="confirmed_cases"):
    """Fit using only targets that are fully before the test period."""
    combined = pd.concat([train_df, test_df], ignore_index=True)
    combined_feat, _ = make_features(combined, target)
    cutoff = len(train_df)
    train_feat = combined_feat.iloc[:cutoff].copy()
    test_feat = combined_feat.iloc[cutoff:].copy()

    y_future = direct_target(combined_feat, horizon, target)
    test_start = pd.to_datetime(test_df["week_start_date"]).min()
    target_date = pd.to_datetime(combined["week_start_date"]).shift(-horizon)

    train_mask = (
        (pd.to_datetime(combined["week_start_date"]) < test_start)
        & (target_date < test_start)
        & train_feat[feature_cols].notna().all(axis=1)
        & y_future.notna()
    )
    model = make_model()
    model.fit(train_feat.loc[train_mask, feature_cols], y_future.loc[train_mask])

    test_valid = test_feat[feature_cols].notna().all(axis=1) & y_future.iloc[cutoff:].notna()
    pred = np.full(len(test_feat), np.nan)
    pred[test_valid] = model.predict(test_feat.loc[test_valid, feature_cols])
    return pred, model


def evaluate(y_true, y_pred):
    mask = np.isfinite(y_true) & np.isfinite(y_pred)
    return {
        "n": int(mask.sum()),
        "MAE": float(mean_absolute_error(np.asarray(y_true)[mask], np.asarray(y_pred)[mask])),
        "RMSE": float(mean_squared_error(np.asarray(y_true)[mask], np.asarray(y_pred)[mask]) ** 0.5),
    }


def rolling_year_evaluation(df, target_years=(2022, 2023, 2024, 2025), horizon=1):
    """Year-based expanding temporal holdout with leakage-controlled targets.

    This is an expanding historical holdout, not a full rolling-origin study.
    Training targets are restricted to outcomes occurring before the evaluation
    year's first week, preventing future-period target leakage.
    """
    rows = []
    work = df.sort_values("week_start_date").reset_index(drop=True).copy()

    for year in target_years:
        train = work[work["epi_year"] < year].copy()
        test = work[work["epi_year"] == year].copy()
        combined = pd.concat([train, test], ignore_index=True)
        feat, cols = make_features(combined)
        y_future = direct_target(combined, horizon)
        dates = pd.to_datetime(combined["week_start_date"])
        test_start = pd.to_datetime(test["week_start_date"]).min()
        target_dates = dates.shift(-horizon)

        train_mask = (
            (dates < test_start)
            & (target_dates < test_start)
            & feat[cols].notna().all(axis=1)
            & y_future.notna()
        )
        test_mask = (
            (combined["epi_year"] == year)
            & (target_dates.dt.year == year)
            & feat[cols].notna().all(axis=1)
            & y_future.notna()
        )

        model = make_model()
        model.fit(feat.loc[train_mask, cols], y_future.loc[train_mask])
        pred = model.predict(feat.loc[test_mask, cols])
        truth = y_future.loc[test_mask].to_numpy()
        metrics = evaluate(truth, pred)
        rows.append(
            {
                "horizon": horizon,
                "target_year": year,
                "model": "gradient_boosting_v1_1",
                **metrics,
            }
        )
    return pd.DataFrame(rows)
