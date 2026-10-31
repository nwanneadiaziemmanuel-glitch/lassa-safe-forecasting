
import numpy as np
import pandas as pd

LAGS = [1,2,3,4,8,13,26,52]
ROLLING_WINDOWS = [4,8,13,26,52]

def make_features(df, target="confirmed_cases"):
    x = df.copy().sort_values("week_start_date").reset_index(drop=True)
    for lag in LAGS:
        x[f"lag_{lag}"] = x[target].shift(lag)
    for w in ROLLING_WINDOWS:
        # shift first: the current target is never used in its own predictor.
        x[f"rollmean_{w}"] = x[target].shift(1).rolling(w).mean()
    angle = 2*np.pi*x["epi_week"]/53.0
    x["epi_sin"] = np.sin(angle)
    x["epi_cos"] = np.cos(angle)
    feature_cols = [f"lag_{l}" for l in LAGS] + [f"rollmean_{w}" for w in ROLLING_WINDOWS] + ["epi_sin","epi_cos"]
    return x, feature_cols
