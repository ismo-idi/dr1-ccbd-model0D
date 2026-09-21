from pathlib import Path

import numpy as np

from src.config import load_config
from src.diagnostics import local_oracle_diagnostics
from src.local_nlp import build_local_nlp
from src.tcc import assemble_tcc, stationary_exact_tcc_initialization

ROOT = Path(__file__).resolve().parents[1]


def test_initial_hover_first_block_backend_returns_finite_accepted_components():
    """Component test only: one first-block solve, not an Algorithm-2 baseline run."""
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    ops = assemble_tcc(cfg)
    l1 = build_local_nlp(1, cfg, ops)
    l2 = build_local_nlp(2, cfg, ops)
    z1, z2, u = stationary_exact_tcc_initialization(cfg, ops)
    xi = np.zeros(ops.m)
    y = np.zeros(ops.m)
    rho = 4.0
    r1 = l1.solve(z1, u, xi[:cfg.Q], y[:cfg.Q], rho)
    r2 = l2.solve(z2, u, xi[cfg.Q:], y[cfg.Q:], rho)
    d1 = local_oracle_diagnostics(l1, r1, z1, u, xi[:cfg.Q], y[:cfg.Q], rho)
    d2 = local_oracle_diagnostics(l2, r2, z2, u, xi[cfg.Q:], y[cfg.Q:], rho)
    assert r1.backend_success and r2.backend_success
    assert d1.finite and d2.finite
    assert d1.multiplier_mapping_available and d2.multiplier_mapping_available
    assert d1.accepted, d1.to_dict()
    assert d2.accepted, d2.to_dict()
