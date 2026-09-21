import numpy as np

from src.geometry import dense_sample_min_squared, segment_min_squared_numeric


def test_guarded_segment_distance_regimes_against_dense_sampling():
    cases = [
        (np.array([2.0, 0.0]), np.array([0.0, 0.0]), 'degenerate'),
        (np.array([1.0, 0.0]), np.array([1.0, 0.0]), 'endpoint0'),
        (np.array([-2.0, 1.0]), np.array([1.0, 0.0]), 'endpoint1'),
        (np.array([-0.5, 1.0]), np.array([1.0, 0.0]), 'interior'),
    ]
    for a, d, regime in cases:
        res = segment_min_squared_numeric(a, d)
        dense = dense_sample_min_squared(a, d, samples=20001)
        assert res.regime == regime
        assert abs(res.min_squared_distance - dense) <= 1e-8
