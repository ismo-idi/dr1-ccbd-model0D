from pathlib import Path

import numpy as np

from src.config import load_config
from src.diagnostics import integrity_pass
from src.sunsun_algorithm2 import _a5_edge_update, _outer_parameter_update, _slack_dual_update

ROOT = Path(__file__).resolve().parents[1]


def test_a5_is_symmetric_average_then_a1_projection():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    Q = cfg.Q
    s1 = np.full(Q, 5.0)
    s2 = np.full(Q, 4.0)
    zeros = np.zeros(Q)
    u = _a5_edge_update(cfg, 4.0, s1, s2, zeros, zeros, zeros, zeros)
    # Average 4.5 lies outside B=[-3.5,3.5]^2, so every component projects to 3.5.
    np.testing.assert_allclose(u, 3.5)


def test_slack_dual_update_satisfies_exact_identity_numerically():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    rng = np.random.default_rng(20260911)
    lam = rng.normal(size=32)
    y0 = rng.normal(size=32)
    c = rng.normal(size=32)
    beta = 2.0
    rho = 4.0
    xi, y = _slack_dual_update(lam, beta, rho, y0, c)
    np.testing.assert_allclose(lam + beta * xi + y, 0.0, atol=3e-15, rtol=0.0)
    ok, vals = integrity_pass(cfg, lam, beta, xi, y, rho)
    assert ok, vals


def test_first_penalty_rule_with_xi0_zero_is_preserved():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    lam = np.zeros(32)
    beta = 2.0
    xi0 = np.zeros(32)
    _, beta_same, rho_same = _outer_parameter_update(cfg, lam, beta, np.zeros(32), xi0)
    assert beta_same == beta
    assert rho_same == 2 * beta_same
    xi_nonzero = np.zeros(32)
    xi_nonzero[0] = 1e-12
    _, beta_grow, rho_grow = _outer_parameter_update(cfg, lam, beta, xi_nonzero, xi0)
    assert beta_grow == cfg.a["vartheta"] * beta
    assert rho_grow == 2 * beta_grow


def test_outer_lambda_projection_uses_frozen_safeguard_box():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    lam = np.full(32, 99.0)
    xi = np.full(32, 10.0)
    lam_next, _, _ = _outer_parameter_update(cfg, lam, 2.0, xi, np.ones(32) * 100.0)
    np.testing.assert_allclose(lam_next, 100.0)
