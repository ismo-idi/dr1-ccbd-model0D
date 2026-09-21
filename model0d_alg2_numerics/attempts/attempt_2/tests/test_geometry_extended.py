import casadi as ca
import numpy as np
from scipy.optimize import minimize_scalar

from src.geometry import segment_min_squared_numeric, segment_min_squared_symbolic


def test_symbolic_and_numeric_exact_value_agree_random_cases():
    a = ca.MX.sym("a", 2)
    d = ca.MX.sym("d", 2)
    f = ca.Function("seg_value_test", [a, d], [segment_min_squared_symbolic(a, d)])
    rng = np.random.default_rng(20260911)
    cases = [(np.array([2.0, -1.0]), np.zeros(2))]
    cases += [(rng.normal(size=2), rng.normal(size=2)) for _ in range(100)]
    for av, dv in cases:
        numeric = segment_min_squared_numeric(av, dv).min_squared_distance
        symbolic = float(f(av, dv))
        np.testing.assert_allclose(symbolic, numeric, atol=2e-12, rtol=2e-12)


def test_guarded_value_matches_independent_bounded_scalar_minimization():
    rng = np.random.default_rng(19092026)
    for _ in range(60):
        a = rng.normal(size=2)
        d = rng.normal(size=2)
        result = segment_min_squared_numeric(a, d)
        direct = minimize_scalar(
            lambda lam: float(np.dot(a + lam * d, a + lam * d)),
            bounds=(0.0, 1.0),
            method="bounded",
            options={"xatol": 1e-14},
        )
        # The bounded routine does not necessarily evaluate exact interval endpoints,
        # so the independent constrained scalar check must include both endpoints.
        f0 = float(np.dot(a, a))
        f1 = float(np.dot(a + d, a + d))
        direct_constrained = min(float(direct.fun), f0, f1)
        assert abs(result.min_squared_distance - direct_constrained) <= 2e-10


def test_obstacle_and_uav_wrapper_values_match_generic_segment_geometry():
    from src.geometry import obstacle_segment_constraint_numeric, uav_segment_constraint_numeric
    clearance = 0.55
    # Obstacle: segment from (-1,1) to (1,1), center at origin -> interior distance 1.
    g_obs, res_obs = obstacle_segment_constraint_numeric([-1.0, 1.0], [1.0, 1.0], [0.0, 0.0], clearance)
    assert res_obs.regime == 'interior'
    np.testing.assert_allclose(res_obs.min_squared_distance, 1.0, atol=1e-14)
    np.testing.assert_allclose(g_obs, clearance**2 - 1.0, atol=1e-14)
    # UAV relative motion is the same generic scalar segment problem.
    g_uav, res_uav = uav_segment_constraint_numeric(
        [-1.0, 1.0], [1.0, 1.0], [0.0, 0.0], [0.0, 0.0], clearance
    )
    assert res_uav.regime == 'interior'
    np.testing.assert_allclose(res_uav.min_squared_distance, 1.0, atol=1e-14)
    np.testing.assert_allclose(g_uav, clearance**2 - 1.0, atol=1e-14)
