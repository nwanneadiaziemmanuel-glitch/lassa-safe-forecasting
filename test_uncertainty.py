import numpy as np

from src.uncertainty import coverage, interval_score


def test_interval_score_and_coverage():
    y = np.array([1.0, 2.0, 3.0])
    lo = np.array([0.0, 1.0, 2.0])
    hi = np.array([2.0, 3.0, 4.0])
    assert coverage(y, lo, hi) == 1.0
    assert interval_score(y, lo, hi) > 0
