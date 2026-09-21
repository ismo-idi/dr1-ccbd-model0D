import copy
import json
from pathlib import Path

import numpy as np

import src.sunsun_algorithm2 as alg
from src.config import ModelConfig, load_config
from src.diagnostics import LocalOracleDiagnostics
from src.local_nlp import LocalSolveResult

ROOT = Path(__file__).resolve().parents[1]


class FakeLocal:
    def __init__(self, agent, cfg, ops):
        self.agent = agent
        self.cfg = cfg
        self.ops = ops
        self.n_constraints = 1

    def solve(self, z0, u_old, xi_old_half, y_old_half, rho):
        return LocalSolveResult(
            agent=self.agent,
            z=np.asarray(z0, float).copy(),
            mu=np.zeros(1),
            phi=0.0,
            backend_success=True,
            backend_status="SYNTHETIC_OK",
            backend_iterations=0,
            backend_elapsed_s=0.0,
            raw_stats={},
        )

    def eval_source_objective(self, z):
        return 0.0


def _diag(agent, accepted=True, code=None):
    return LocalOracleDiagnostics(
        agent=agent,
        backend_success=True,
        backend_status="SYNTHETIC",
        backend_iterations=0,
        backend_elapsed_s=0.0,
        finite=True,
        constraint_value_crosscheck_abs=0.0,
        constraint_value_crosscheck_limit=1e-12,
        constraint_value_crosscheck_pass=True,
        feasibility_max_by_family={},
        feasibility_pass_by_family={},
        raw_g=[],
        raw_mu_backend=[],
        multiplier_mapping_available=True,
        diagnostic_mu=[],
        differentiable_rows=[],
        omitted_rows=[],
        omitted_reasons={},
        near_active_rows=[],
        nonsmooth_blocking_rows=[],
        R_dual=0.0,
        R_dual_normalized=0.0,
        R_comp=0.0,
        R_stat=0.0,
        R_stat_normalized=0.0,
        R_desc=0.0,
        descent_limit=0.0,
        pass_dual=True,
        pass_comp=True,
        pass_stat=True,
        pass_desc=True,
        accepted=accepted,
        failure_code=code,
        failure_codes=[] if code is None else [code],
    )


def _cfg_with_caps(max_outer=1, max_inner=1):
    raw = json.loads((ROOT / "configs" / "baseline_2uav_0obs.json").read_text())
    raw["algorithm"]["max_outer_iterations"] = max_outer
    raw["algorithm"]["max_inner_iterations"] = max_inner
    return ModelConfig(raw)  # synthetic control-flow test: intentionally bypass frozen config validator


def _install_fake_locals(monkeypatch):
    monkeypatch.setattr(alg, "build_local_nlp", lambda agent, cfg, ops: FakeLocal(agent, cfg, ops))


def test_common_local_oracle_abort_occurs_before_a5(monkeypatch):
    cfg = _cfg_with_caps()
    _install_fake_locals(monkeypatch)
    calls = {"diag": 0}

    def fake_diag(local, result, *args, **kwargs):
        calls["diag"] += 1
        return _diag(local.agent, accepted=(local.agent == 2), code=None if local.agent == 2 else "FIRST_BLOCK_ORACLE_FAILED")

    monkeypatch.setattr(alg, "local_oracle_diagnostics", fake_diag)
    monkeypatch.setattr(alg, "_a5_edge_update", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("A5 must not run after local barrier failure")))
    result = alg.run_algorithm2(cfg)
    assert calls["diag"] == 2
    assert result.termination_reason == "LOCAL_ORACLE_ABORT"
    assert result.primary_cause == "FIRST_BLOCK_ORACLE_FAILED"
    assert result.state is not None
    assert result.state.outer_r == 0 and result.state.inner_t == 0


def test_success_on_final_permitted_inner_iteration_is_not_inner_cap_exhaustion(monkeypatch):
    cfg = _cfg_with_caps(max_outer=1, max_inner=1)
    _install_fake_locals(monkeypatch)
    monkeypatch.setattr(alg, "local_oracle_diagnostics", lambda local, result, *a, **k: _diag(local.agent))
    monkeypatch.setattr(alg, "_residuals", lambda *a, **k: {
        "R1": 0.0, "R2": 0.0, "R3": 0.0,
        "R1_matrix": 0.0, "R2_matrix": 0.0,
        "R1_crosscheck_abs": 0.0, "R2_crosscheck_abs": 0.0,
    })
    monkeypatch.setattr(alg, "_outer_stop_predicate", lambda *a, **k: False)
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "MAX_OUTER_ITERATIONS"
    assert "MAX_INNER_ITERATIONS" not in result.all_causes
    assert result.state is not None
    assert result.state.outer_r == 1 and result.state.inner_t == 1


def test_inner_cap_exhaustion_returns_last_complete_inner_snapshot(monkeypatch):
    cfg = _cfg_with_caps(max_outer=1, max_inner=1)
    _install_fake_locals(monkeypatch)
    monkeypatch.setattr(alg, "local_oracle_diagnostics", lambda local, result, *a, **k: _diag(local.agent))
    monkeypatch.setattr(alg, "_residuals", lambda *a, **k: {
        "R1": 1.0, "R2": 1.0, "R3": 1.0,
        "R1_matrix": 1.0, "R2_matrix": 1.0,
        "R1_crosscheck_abs": 0.0, "R2_crosscheck_abs": 0.0,
    })
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "MAX_INNER_ITERATIONS"
    assert result.primary_cause == "MAX_INNER_ITERATIONS"
    assert result.state is not None
    assert result.state.outer_r == 1 and result.state.inner_t == 1


def test_nonfinite_update_is_explicit_failure_and_not_accepted_state(monkeypatch):
    cfg = _cfg_with_caps(max_outer=1, max_inner=1)
    _install_fake_locals(monkeypatch)
    monkeypatch.setattr(alg, "local_oracle_diagnostics", lambda local, result, *a, **k: _diag(local.agent))
    monkeypatch.setattr(alg, "_a5_edge_update", lambda cfg, rho, *a, **k: np.full(cfg.Q, np.nan))
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "UPDATE_ABORT"
    assert result.primary_cause == "NUMERICAL_NAN_INF"
    assert result.state is not None
    assert result.state.outer_r == 0 and result.state.inner_t == 0


def test_backend_construction_failure_uses_common_finalization(monkeypatch):
    cfg = _cfg_with_caps()
    monkeypatch.setattr(alg, "build_local_nlp", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("synthetic build failure")))
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "SOLVER_BACKEND_FAILURE"
    assert result.primary_cause == "SOLVER_BACKEND_FAILURE"
    assert result.history[-1]["phase"] == "finalization"


def test_input_admissibility_failure_uses_common_finalization(monkeypatch):
    cfg = _cfg_with_caps()
    cfg.raw["model"]["starts"][0] = [99.0, 99.0]
    _install_fake_locals(monkeypatch)
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "INPUT_ADMISSIBILITY_FAILED"
    assert result.primary_cause == "INPUT_ADMISSIBILITY_FAILED"
    assert result.history[-1]["phase"] == "finalization"


def test_timeout_uses_common_finalization(monkeypatch):
    cfg = _cfg_with_caps()
    cfg.raw["algorithm"]["wall_clock_cap_s"] = -1.0
    _install_fake_locals(monkeypatch)
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "TIMEOUT"
    assert "TIMEOUT" in result.all_causes
    assert result.history[-1]["phase"] == "finalization"


def test_initialization_integrity_failure_uses_common_finalization(monkeypatch):
    cfg = _cfg_with_caps()
    _install_fake_locals(monkeypatch)
    monkeypatch.setattr(alg, "integrity_pass", lambda *a, **k: (False, {"synthetic": 1.0}))
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "INITIALIZATION_FAILED"
    assert "ALGEBRAIC_INTEGRITY_FAILED" in result.all_causes
    assert result.history[-1]["phase"] == "finalization"


def test_postcheck_exception_is_explicit_finalization(monkeypatch):
    cfg = _cfg_with_caps(max_outer=1, max_inner=1)
    _install_fake_locals(monkeypatch)
    monkeypatch.setattr(alg, "local_oracle_diagnostics", lambda local, result, *a, **k: _diag(local.agent))
    monkeypatch.setattr(alg, "_residuals", lambda *a, **k: {
        "R1": 0.0, "R2": 0.0, "R3": 0.0,
        "R1_matrix": 0.0, "R2_matrix": 0.0,
        "R1_crosscheck_abs": 0.0, "R2_crosscheck_abs": 0.0,
    })
    monkeypatch.setattr(alg, "physical_postcheck_numeric", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("synthetic postcheck failure")))
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "POSTCHECK_EVALUATION_FAILED"
    assert result.primary_cause == "POSTCHECK_EVALUATION_FAILED"
    assert result.history[-1]["phase"] == "finalization"


def test_finite_outer_stop_requires_two_consecutive_complete_outer_passes(monkeypatch):
    cfg = _cfg_with_caps(max_outer=2, max_inner=1)
    _install_fake_locals(monkeypatch)
    monkeypatch.setattr(alg, "local_oracle_diagnostics", lambda local, result, *a, **k: _diag(local.agent))
    monkeypatch.setattr(alg, "_residuals", lambda *a, **k: {
        "R1": 0.0, "R2": 0.0, "R3": 0.0,
        "R1_matrix": 0.0, "R2_matrix": 0.0,
        "R1_crosscheck_abs": 0.0, "R2_crosscheck_abs": 0.0,
    })
    monkeypatch.setattr(alg, "_outer_stop_predicate", lambda *a, **k: True)
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "FINITE_OUTER_STOP"
    outer_events = [e for e in result.history if e.get("phase") == "outer_complete"]
    assert len(outer_events) == 2
    assert outer_events[0]["consecutive_outer_passes"] == 1
    assert outer_events[1]["consecutive_outer_passes"] == 2
    assert result.history[-1]["phase"] == "finalization"


def test_inner_loop_timeout_branch_uses_common_finalization(monkeypatch):
    cfg = _cfg_with_caps(max_outer=1, max_inner=2)
    cfg.raw["algorithm"]["wall_clock_cap_s"] = 1.0
    _install_fake_locals(monkeypatch)
    # start_time=0, outer boundary still 0, inner boundary exceeds cap.
    values = iter([0.0, 0.0, 2.0, 2.0, 2.0])
    monkeypatch.setattr(alg.time, "monotonic", lambda: next(values, 2.0))
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "TIMEOUT"
    assert result.history[-1]["phase"] == "finalization"


def test_residual_crosscheck_failure_aborts_before_snapshot_acceptance(monkeypatch):
    cfg = _cfg_with_caps(max_outer=1, max_inner=1)
    _install_fake_locals(monkeypatch)
    monkeypatch.setattr(alg, "local_oracle_diagnostics", lambda local, result, *a, **k: _diag(local.agent))
    monkeypatch.setattr(alg, "_residuals", lambda *a, **k: {
        "R1": 0.0, "R2": 0.0, "R3": 0.0,
        "R1_matrix": 1.0, "R2_matrix": 0.0,
        "R1_crosscheck_abs": 1.0, "R2_crosscheck_abs": 0.0,
    })
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "UPDATE_ABORT"
    assert result.primary_cause == "ALGEBRAIC_INTEGRITY_FAILED"
    assert any(e.get("phase") == "residual_integrity_abort" for e in result.history)
    assert result.state is not None
    assert result.state.outer_r == 0 and result.state.inner_t == 0


def test_outer_parameter_integrity_failure_has_explicit_update_abort(monkeypatch):
    cfg = _cfg_with_caps(max_outer=1, max_inner=1)
    _install_fake_locals(monkeypatch)
    monkeypatch.setattr(alg, "local_oracle_diagnostics", lambda local, result, *a, **k: _diag(local.agent))
    monkeypatch.setattr(alg, "_residuals", lambda *a, **k: {
        "R1": 0.0, "R2": 0.0, "R3": 0.0,
        "R1_matrix": 0.0, "R2_matrix": 0.0,
        "R1_crosscheck_abs": 0.0, "R2_crosscheck_abs": 0.0,
    })
    monkeypatch.setattr(alg, "_outer_stop_predicate", lambda *a, **k: False)
    monkeypatch.setattr(alg, "_outer_parameter_update", lambda cfg, lam, beta, xi, xi_prev: (np.asarray(lam), beta, 999.0))
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "UPDATE_ABORT"
    assert result.primary_cause == "ALGEBRAIC_INTEGRITY_FAILED"
    assert result.history[-1]["phase"] == "finalization"
    assert result.history[-1]["phase_detail"] == "outer_parameter_update"


def test_incomplete_physical_evaluator_is_postcheck_failure_not_safety_violation(monkeypatch):
    cfg = _cfg_with_caps(max_outer=1, max_inner=1)
    _install_fake_locals(monkeypatch)
    monkeypatch.setattr(alg, "local_oracle_diagnostics", lambda local, result, *a, **k: _diag(local.agent))
    monkeypatch.setattr(alg, "_residuals", lambda *a, **k: {
        "R1": 0.0, "R2": 0.0, "R3": 0.0,
        "R1_matrix": 0.0, "R2_matrix": 0.0,
        "R1_crosscheck_abs": 0.0, "R2_crosscheck_abs": 0.0,
    })
    monkeypatch.setattr(alg, "physical_postcheck_numeric", lambda *a, **k: {
        "evaluation_complete": False,
        "PHYSICAL_POSTCHECK_NUMERIC_PASS": False,
        "families": {},
    })
    monkeypatch.setattr(alg, "_outer_stop_predicate", lambda *a, **k: False)
    result = alg.run_algorithm2(cfg)
    assert result.termination_reason == "MAX_OUTER_ITERATIONS"
    assert "POSTCHECK_EVALUATION_FAILED" in result.all_causes
    assert "PHYSICAL_VIOLATION_DETECTED" not in result.all_causes
    assert result.statuses["NUMERICALLY_VALID"] is False
