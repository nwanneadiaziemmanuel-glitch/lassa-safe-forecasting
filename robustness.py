
import numpy as np
import pandas as pd

def mask_latest_signal(df, target="confirmed_cases", weeks=1):
    out = df.copy()
    out.loc[out.index[-weeks:], target] = np.nan
    return out

def inject_random_missingness(df, frac=0.2, target="confirmed_cases", seed=42):
    rng = np.random.default_rng(seed)
    out = df.copy()
    n = max(1, int(len(out)*frac))
    idx = rng.choice(out.index, size=n, replace=False)
    out.loc[idx, target] = np.nan
    return out

def add_feature_noise(values, pct=0.15, seed=42):
    rng = np.random.default_rng(seed)
    x = np.asarray(values, dtype=float)
    return x + rng.normal(0, np.maximum(1, np.abs(x))*pct, size=len(x))
