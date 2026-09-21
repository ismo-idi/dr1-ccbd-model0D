from pathlib import Path

import numpy as np

from src.config import load_config
from src.diagnostics import local_oracle_diagnostics
from src.local_nlp import LocalSolveResult, build_local_nlp
from src.tcc import assemble_tcc, stationary_exact_tcc_initialization

ROOT = Path(__file__).resolve().parents[1]


def test_objective_is_source_counted_once_and_foreign_copy_does_not_duplicate_it():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    ops = assemble_tcc(cfg)
    local1 = build_local_nlp(1, cfg, ops)
    z1, _, _ = stationary_exact_tcc_initialization(cfg, ops)
    f0 = local1.eval_source_objective(z1)
    z1_changed_copy = z1.copy()
    z1_changed_copy[cfg.Q:] = np.linspace(-3.0, 3.0, cfg.Q)
    f1 = local1.eval_source_objective(z1_changed_copy)
    assert f0 == f1


def test_metadata_rows_are_complete_sequential_and_guardian_localized():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    ops = assemble_tcc(cfg)
    l1 = build_local_nlp(1, cfg, ops)
    l2 = build_local_nlp(2, cfg, ops)
    assert [m.row for m in l1.metas] == list(range(l1.n_constraints))
    assert [m.row for m in l2.metas] == list(range(l2.n_constraints))
    assert sum(m.family == "uav" for m in l1.metas) == cfg.K
    assert sum(m.family == "uav" for m in l2.metas) == 0


def test_predefined_obstacle_scenario_builds_generic_obstacle_rows_without_execution():
    cfg = load_config(ROOT / "configs" / "obstacle_2uav_1obs.json")
    ops = assemble_tcc(cfg)
    l1 = build_local_nlp(1, cfg, ops)
    l2 = build_local_nlp(2, cfg, ops)
    assert sum(m.family == "obs" for m in l1.metas) == cfg.K
    assert sum(m.family == "obs" for m in l2.metas) == cfg.K
    assert l1.n_constraints == 88
    assert l2.n_constraints == 48


def test_missing_multiplier_vector_is_explicitly_unavailable_not_reconstructed():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    ops = assemble_tcc(cfg)
    local = build_local_nlp(2, cfg, ops)
    _, z2, u = stationary_exact_tcc_initialization(cfg, ops)
    xi = np.zeros(cfg.Q)
    y = np.zeros(cfg.Q)
    result = LocalSolveResult(
        agent=2,
        z=z2.copy(),
        mu=np.zeros(local.n_constraints - 1),
        phi=local.eval_phi(z2, u, xi, y, 4.0),
        backend_success=True,
        backend_status="SYNTHETIC",
        backend_iterations=0,
        backend_elapsed_s=0.0,
        raw_stats={},
    )
    diag = local_oracle_diagnostics(local, result, z2, u, xi, y, 4.0)
    assert diag.accepted is False
    assert diag.multiplier_mapping_available is False
    assert diag.failure_code == "MULTIPLIER_DIAGNOSTIC_UNAVAILABLE"


def test_hover_pair_rows_are_omitted_only_when_strictly_inactive():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    ops = assemble_tcc(cfg)
    local = build_local_nlp(1, cfg, ops)
    z1, _, u = stationary_exact_tcc_initialization(cfg, ops)
    xi = np.zeros(cfg.Q)
    y = np.zeros(cfg.Q)
    result = LocalSolveResult(
        agent=1,
        z=z1.copy(),
        mu=np.zeros(local.n_constraints),
        phi=local.eval_phi(z1, u, xi, y, 4.0),
        backend_success=True,
        backend_status="SYNTHETIC",
        backend_iterations=0,
        backend_elapsed_s=0.0,
        raw_stats={},
    )
    diag = local_oracle_diagnostics(local, result, z1, u, xi, y, 4.0)
    pair_rows = [m.row for m in local.metas if m.family == "uav"]
    assert set(pair_rows).issubset(set(diag.omitted_rows))
    assert not set(pair_rows).intersection(diag.nonsmooth_blocking_rows)


def test_backend_failure_with_nonfinite_multiplier_preserves_simultaneous_causes():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    ops = assemble_tcc(cfg)
    local = build_local_nlp(2, cfg, ops)
    _, z2, u = stationary_exact_tcc_initialization(cfg, ops)
    xi = np.zeros(cfg.Q)
    y = np.zeros(cfg.Q)
    result = LocalSolveResult(
        agent=2,
        z=z2.copy(),
        mu=np.full(local.n_constraints, np.nan),
        phi=float("nan"),
        backend_success=False,
        backend_status="SYNTHETIC_FAILURE",
        backend_iterations=None,
        backend_elapsed_s=0.0,
        raw_stats={},
    )
    diag = local_oracle_diagnostics(local, result, z2, u, xi, y, 4.0)
    assert "NUMERICAL_NAN_INF" in diag.failure_codes
    assert "SOLVER_BACKEND_FAILURE" in diag.failure_codes
    assert diag.failure_code == "NUMERICAL_NAN_INF"
    assert diag.accepted is False


def test_independent_constraint_value_recompute_detects_solver_graph_mismatch():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    ops = assemble_tcc(cfg)
    local = build_local_nlp(2, cfg, ops)
    _, z2, u = stationary_exact_tcc_initialization(cfg, ops)
    xi = np.zeros(cfg.Q)
    y = np.zeros(cfg.Q)
    original = local.g_fun
    local.g_fun = lambda z: np.asarray(original(z), float).reshape(-1) + np.r_[1e-4, np.zeros(local.n_constraints - 1)]
    result = LocalSolveResult(
        agent=2,
        z=z2.copy(),
        mu=np.zeros(local.n_constraints),
        phi=local.eval_phi(z2, u, xi, y, 4.0),
        backend_success=True,
        backend_status="SYNTHETIC",
        backend_iterations=0,
        backend_elapsed_s=0.0,
        raw_stats={},
    )
    diag = local_oracle_diagnostics(local, result, z2, u, xi, y, 4.0)
    assert diag.constraint_value_crosscheck_pass is False
    assert "ALGEBRAIC_INTEGRITY_FAILED" in diag.failure_codes
    assert diag.accepted is False
