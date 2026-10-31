import numpy as np


def target_resampling_gaussian(series, multiplier=1, seed=42):
    """Lightweight synthetic target augmentation with Gaussian perturbation.

    This is intentionally a simple research baseline. It is not residual
    bootstrap and is not presented as clinically realistic generative data.
    """
    rng = np.random.default_rng(seed)
    y = np.asarray(series, dtype=float)
    if len(y) < 3 or multiplier <= 0:
        return np.array([], dtype=float)
    diffs = np.diff(y)
    scale = np.std(diffs) if np.std(diffs) > 0 else 1.0
    samples = []
    for _ in range(int(multiplier * len(y))):
        base = y[rng.integers(0, len(y))]
        perturb = rng.normal(0, scale * 0.35)
        samples.append(max(0.0, base + perturb))
    return np.asarray(samples)


def residual_bootstrap(series, multiplier=1, seed=42):
    """Backward-compatible alias for the historical V1 augmentation function."""
    return target_resampling_gaussian(series, multiplier=multiplier, seed=seed)


def targeted_high_intensity(series, multiplier=1, quantile=0.8, seed=42):
    """Oversample high-intensity target values as a stress-test ablation."""
    rng = np.random.default_rng(seed)
    y = np.asarray(series, dtype=float)
    if multiplier <= 0:
        return np.array([], dtype=float)
    threshold = np.quantile(y, quantile)
    high = y[y >= threshold]
    if len(high) == 0:
        return np.array([], dtype=float)
    idx = rng.integers(0, len(high), size=int(multiplier * len(y)))
    return high[idx]
