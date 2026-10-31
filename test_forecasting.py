import pandas as pd

from src.forecasting import direct_target, seasonal_naive


def test_horizon_target_alignment():
    df = pd.DataFrame({"confirmed_cases": [1, 2, 3, 4, 5]})
    assert direct_target(df, 1).iloc[:4].tolist() == [2.0, 3.0, 4.0, 5.0]
    assert pd.isna(direct_target(df, 1).iloc[4])
    assert direct_target(df, 2).iloc[:3].tolist() == [3.0, 4.0, 5.0]
    assert direct_target(df, 2).iloc[3:].isna().all()


def test_seasonal_naive_alignment():
    df = pd.DataFrame({"confirmed_cases": list(range(60))})
    assert seasonal_naive(df, 1).iloc[52] == 1
    assert seasonal_naive(df, 4).iloc[52] == 4
