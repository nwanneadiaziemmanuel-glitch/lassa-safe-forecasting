import numpy as np


def residual_bootstrap_interval(pred, residuals, alpha=0.05, seed=42):
    """Construct an empirical residual-bootstrap prediction interval."""
    rng = np.random.default_rng(seed)
    pred = np.asarray(pred, dtype=float)
    residuals = np.asarray(residuals, dtype=float)
    if residuals.size == 0:
        raise ValueError("Residuals are required.")
    draws = rng.choice(residuals, size=(2000, len(pred)), replace=True)
    sims = pred[None, :] + draws
    lo = np.quantile(sims, alpha / 2, axis=0)
    hi = np.quantile(sims, 1 - alpha / 2, axis=0)
    return lo, hi


def coverage(y, lo, hi):
    y, lo, hi = map(np.asarray, (y, lo, hi))
    return float(np.mean((y >= lo) & (y <= hi)))


def interval_score(y, lo, hi, alpha=0.05):
    """Mean interval score for one prediction interval level."""
    y, lo, hi = map(np.asarray, (y, lo, hi))
    width = hi - lo
    below = (lo - y) * (y < lo) * (2 / alpha)
    above = (y - hi) * (y > hi) * (2 / alpha)
    return float(np.mean(width + below + above))
