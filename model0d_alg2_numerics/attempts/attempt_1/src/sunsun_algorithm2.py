"""Finite experimental harness for the selected Sun--Sun Algorithm 2.

This is the approved N=2 Model 0-D/TCC realization. It preserves the exact
update equations but keeps finite experiment/certification semantics separate
from source theorem claims.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import time
from typing import Any, Callable

import numpy as np

from .config import ModelConfig
from .diagnostics import (
    LocalOracleDiagnostics,
    integrity_pass,
    local_oracle_diagnostics,
    physical_postcheck_numeric,
    tcc_metrics,
)
from .local_nlp import LocalNLP, build_local_nlp
from .tcc import TCCOperators, assemble_tcc, project_a1, stationary_exact_tcc_initialization


FAILURE_PRIORITY = [
    "INPUT_ADMISSIBILITY_FAILED",
    "NUMERICAL_NAN_INF",
    "LINEAR_ALGEBRA_FAILURE",
    "SOLVER_BACKEND_FAILURE",
    "MULTIPLIER_DIAGNOSTIC_UNAVAILABLE",
    "ORACLE_UNCERTIFIED_NONSMOOTH",
    "FIRST_BLOCK_ORACLE_FAILED",
    "ALGEBRAIC_INTEGRITY_FAILED",
    "POSTCHECK_EVALUATION_FAILED",
    "PHYSICAL_VIOLATION_DETECTED",
    "TCC_NOT_ACCEPTED",
    "MAX_INNER_ITERATIONS",
    "MAX_OUTER_ITERATIONS",
    "TIMEOUT",
]


@dataclass
class RunState:
    z1: np.ndarray
    z2: np.ndarray
    u: np.ndarray
    xi: np.ndarray
    y: np.ndarray
    lambda_outer: np.ndarray
    beta: float
    rho: float
    outer_r: int
    inner_t: int


@dataclass
class RunResult:
    scenario_id: str
    termination_reason: str
    primary_cause: str | None
    all_causes: list[str]
    state: RunState | None
    history: list[dict[str, Any]]
    final_metrics: dict[str, Any]
    statuses: dict[str, bool | str]
    elapsed_s: float

    def to_serializable(self) -> dict[str, Any]:
        d = asdict(self)
        if self.state is not None:
            for key in ("z1", "z2", "u", "xi", "y", "lambda_outer"):
                d["state"][key] = getattr(self.state, key).tolist()
        return d


def _primary(causes: list[str]) -> str | None:
    unique = list(dict.fromkeys(causes))
    for code in FAILURE_PRIORITY:
        if code in unique:
            return code
    return unique[0] if unique else None


def _initial_admissibility(cfg: ModelConfig) -> tuple[bool, list[str]]:
    causes: list[str] = []
    for i, p in enumerate(cfg.starts):
        if np.any(p < cfg.workspace_lower) or np.any(p > cfg.workspace_upper):
            causes.append("INPUT_ADMISSIBILITY_FAILED")
        for obs in cfg.obstacles:
            clearance = cfg.obstacle_clearance(i, obs)
            if np.linalg.norm(p - np.asarray(obs["center"], float)) < clearance:
                causes.append("INPUT_ADMISSIBILITY_FAILED")
    if np.linalg.norm(cfg.starts[0] - cfg.starts[1]) < cfg.uav_clearance:
        causes.append("INPUT_ADMISSIBILITY_FAILED")
    return not causes, causes


def _objective_metrics(local1: LocalNLP, local2: LocalNLP, z1, z2) -> dict[str, float]:
    f1 = local1.eval_source_objective(z1)
    f2 = local2.eval_source_objective(z2)
    cfg = local1.cfg
    free1 = np.asarray(z1[: cfg.Q], float).reshape(cfg.K, cfg.q)
    free2 = np.asarray(z2[: cfg.Q], float).reshape(cfg.K, cfg.q)
    P1 = np.vstack([cfg.starts[0], free1])
    P2 = np.vstack([cfg.starts[1], free2])
    p1K = P1[-1]
    p2K = P2[-1]
    step_sq_1 = float(np.sum(np.sum(np.diff(P1, axis=0) ** 2, axis=1)))
    step_sq_2 = float(np.sum(np.sum(np.diff(P2, axis=0) ** 2, axis=1)))
    goal_sq_1 = float(np.dot(p1K - cfg.goals[0], p1K - cfg.goals[0]))
    goal_sq_2 = float(np.dot(p2K - cfg.goals[1], p2K - cfg.goals[1]))
    return {
        "f1": float(f1),
        "f2": float(f2),
        "F": float(f1 + f2),
        "goal_error_1": float(np.sqrt(goal_sq_1)),
        "goal_error_2": float(np.sqrt(goal_sq_2)),
        "terminal_tracking_term_1": float(cfg.alpha[0] * goal_sq_1),
        "terminal_tracking_term_2": float(cfg.alpha[1] * goal_sq_2),
        "squared_step_sum_1": step_sq_1,
        "squared_step_sum_2": step_sq_2,
        "step_regularization_term_1": float(cfg.beta_obj[0] * step_sq_1),
        "step_regularization_term_2": float(cfg.beta_obj[1] * step_sq_2),
    }


def _residuals(ops: TCCOperators, rho: float, z1, z2, u_old, u_new, xi_old, xi_new) -> dict[str, float]:
    Q = ops.Q
    dxi = np.asarray(xi_old, float).reshape(-1) - np.asarray(xi_new, float).reshape(-1)
    du_term = np.asarray(u_new, float).reshape(-1) - np.asarray(u_old, float).reshape(-1)
    # P2P form, one incident half-edge per agent in the N=2 baseline.
    d1 = du_term + dxi[:Q]
    d2 = du_term + dxi[Q:]
    R1_p2p = float(rho * np.sqrt(np.dot(d1, d1) + np.dot(d2, d2)))
    R2_p2p = float(rho * np.linalg.norm(dxi[:Q] + dxi[Q:]))
    c = ops.target_rows(z1, z2, u_new)
    R3 = float(np.linalg.norm(c + np.asarray(xi_new, float).reshape(-1)))

    # Independent matrix forms used as integrity cross-checks.
    dU_old_minus_new = np.asarray(u_old, float).reshape(-1) - np.asarray(u_new, float).reshape(-1)
    vec1 = ops.B @ dU_old_minus_new + dxi
    R1_matrix = float(np.linalg.norm(rho * (ops.A.T @ vec1)))
    R2_matrix = float(np.linalg.norm(rho * (ops.B.T @ dxi)))
    return {
        "R1": R1_p2p,
        "R2": R2_p2p,
        "R3": R3,
        "R1_matrix": R1_matrix,
        "R2_matrix": R2_matrix,
        "R1_crosscheck_abs": abs(R1_p2p - R1_matrix),
        "R2_crosscheck_abs": abs(R2_p2p - R2_matrix),
    }


def _a5_edge_update(cfg: ModelConfig, rho: float, s1, s2, xi1_old, xi2_old, y1_old, y2_old) -> np.ndarray:
    """Exact A5 symmetric average-and-project update for the unique N=2 edge."""
    psi1 = np.asarray(s1, float).reshape(-1) + np.asarray(xi1_old, float).reshape(-1) + np.asarray(y1_old, float).reshape(-1) / float(rho)
    psi2 = np.asarray(s2, float).reshape(-1) + np.asarray(xi2_old, float).reshape(-1) + np.asarray(y2_old, float).reshape(-1) / float(rho)
    return project_a1(cfg, 0.5 * (psi1 + psi2))


def _slack_dual_update(lambda_r, beta_r: float, rho: float, y_old, c) -> tuple[np.ndarray, np.ndarray]:
    """Exact Decision-15 (S11)-(S12) update in real-arithmetic form."""
    lam = np.asarray(lambda_r, float).reshape(-1)
    y0 = np.asarray(y_old, float).reshape(-1)
    c = np.asarray(c, float).reshape(-1)
    xi_new = -(lam + y0 + float(rho) * c) / (float(beta_r) + float(rho))
    y_new = y0 + float(rho) * (c + xi_new)
    return xi_new, y_new


def _outer_parameter_update(cfg: ModelConfig, lambda_r, beta_r: float, xi_r, xi_prev_outer) -> tuple[np.ndarray, float, float]:
    """Exact safeguarded lambda and adaptive beta update for the experiment wrapper."""
    lam = np.asarray(lambda_r, float).reshape(-1)
    xi = np.asarray(xi_r, float).reshape(-1)
    xi_prev = np.asarray(xi_prev_outer, float).reshape(-1)
    lam_next = np.clip(lam + float(beta_r) * xi, float(cfg.a["lambda_lower"]), float(cfg.a["lambda_upper"]))
    beta_next = float(beta_r) if np.linalg.norm(xi) <= float(cfg.a["omega"]) * np.linalg.norm(xi_prev) else float(cfg.a["vartheta"]) * float(beta_r)
    rho_next = 2.0 * beta_next
    return lam_next, beta_next, rho_next


def _residual_crosscheck_pass(cfg: ModelConfig, residual: dict[str, float]) -> tuple[bool, dict[str, float]]:
    """Check P2P residual reductions against independently assembled matrix forms."""
    rel = float(cfg.t["integrity_relative"])
    lim1 = rel * max(1.0, abs(residual["R1"]), abs(residual["R1_matrix"]))
    lim2 = rel * max(1.0, abs(residual["R2"]), abs(residual["R2_matrix"]))
    details = {
        "R1_crosscheck_limit": lim1,
        "R2_crosscheck_limit": lim2,
        "R1_crosscheck_abs": residual["R1_crosscheck_abs"],
        "R2_crosscheck_abs": residual["R2_crosscheck_abs"],
    }
    ok = residual["R1_crosscheck_abs"] <= lim1 and residual["R2_crosscheck_abs"] <= lim2
    return bool(ok), details


def _outer_stop_predicate(cfg: ModelConfig, xi, tcc: dict[str, float], physical: dict[str, Any], integrity_ok: bool, last_oracles: list[LocalOracleDiagnostics]) -> bool:
    return bool(
        np.linalg.norm(xi) <= float(cfg.t["outer_xi"])
        and tcc["R_TCC_eq"] <= float(cfg.t["tcc_eq"])
        and tcc["R_target"] <= float(cfg.t["target"])
        and integrity_ok
        and all(d.accepted for d in last_oracles)
        and bool(physical.get("PHYSICAL_POSTCHECK_NUMERIC_PASS", False))
    )


def _final_metrics(cfg, ops, local1, local2, state: RunState | None, last_oracles=None) -> tuple[dict[str, Any], dict[str, bool | str], list[str]]:
    if state is None:
        return {}, {
            "NUMERICALLY_VALID": False,
            "TCC_CONSISTENT": False,
            "PHYSICAL_POSTCHECK_NUMERIC_PASS": False,
            "MODEL0D_SAFETY_CERTIFIED": False,
            "SUNSUN_ALGORITHMICALLY_CERTIFIED": False,
        }, []
    causes: list[str] = []
    vals: dict[str, Any] = {}
    try:
        vals["objective"] = _objective_metrics(local1, local2, state.z1, state.z2)
        vals["tcc"] = tcc_metrics(ops, state.z1, state.z2, state.u)
        vals["physical"] = physical_postcheck_numeric(cfg, ops, state.z1, state.z2)
        integ_ok, integ = integrity_pass(cfg, state.lambda_outer, state.beta, state.xi, state.y, state.rho)
        vals["integrity"] = integ
    except Exception as exc:
        causes.append("POSTCHECK_EVALUATION_FAILED")
        vals["postcheck_exception"] = repr(exc)
        integ_ok = False

    finite_state = all(np.all(np.isfinite(v)) for v in (state.z1, state.z2, state.u, state.xi, state.y, state.lambda_outer))
    if not finite_state:
        causes.append("NUMERICAL_NAN_INF")

    tcc_pass = False
    phys_pass = False
    if "tcc" in vals:
        tcc_pass = vals["tcc"]["R_TCC_eq"] <= float(cfg.t["tcc_eq"]) and vals["tcc"]["R_target"] <= float(cfg.t["target"])
        if not tcc_pass:
            causes.append("TCC_NOT_ACCEPTED")
    physical_complete = False
    if "physical" in vals:
        physical_complete = bool(vals["physical"].get("evaluation_complete", False))
        phys_pass = bool(vals["physical"].get("PHYSICAL_POSTCHECK_NUMERIC_PASS", False))
        if not physical_complete:
            causes.append("POSTCHECK_EVALUATION_FAILED")
        elif not phys_pass:
            causes.append("PHYSICAL_VIOLATION_DETECTED")

    tcc_finite = bool("tcc" in vals and all(np.isfinite(v) for v in vals["tcc"].values()))
    numeric_valid = bool(
        finite_state and integ_ok and tcc_finite and physical_complete
        and "postcheck_exception" not in vals
    )
    statuses: dict[str, bool | str] = {
        "NUMERICALLY_VALID": numeric_valid,
        "TCC_CONSISTENT": tcc_pass,
        "PHYSICAL_POSTCHECK_NUMERIC_PASS": phys_pass,
        "MODEL0D_SAFETY_CERTIFIED": False,
        "SUNSUN_ALGORITHMICALLY_CERTIFIED": False,
        "FULLY_CERTIFIED_MODEL0D_SUNSUN_RESULT": False,
        "U3": "CONDITIONAL",
        "U4": "UNSELECTED",
    }
    if last_oracles is not None:
        vals["last_local_oracles"] = [d.to_dict() for d in last_oracles]
    return vals, statuses, causes


def run_algorithm2(cfg: ModelConfig, event_callback: Callable[[dict[str, Any]], None] | None = None) -> RunResult:
    """Execute the finite approved experiment wrapper.

    The caller controls when this is actually invoked. Component verification may
    build and test pieces of this function without inspecting a complete baseline
    outcome. Every runtime exit is routed through one common finalization helper.
    """
    start_time = time.monotonic()
    history: list[dict[str, Any]] = []

    def emit(event: dict[str, Any]):
        history.append(event)
        if event_callback is not None:
            event_callback(event)

    # Assembly/backend construction failures must be explicit rather than escaping
    # the reproducible failure contract as an uncaught exception.
    try:
        ops = assemble_tcc(cfg)
        local1 = build_local_nlp(1, cfg, ops)
        local2 = build_local_nlp(2, cfg, ops)
    except Exception as exc:
        causes = ["SOLVER_BACKEND_FAILURE"]
        emit({
            "phase": "finalization",
            "termination_reason": "SOLVER_BACKEND_FAILURE",
            "primary_cause": "SOLVER_BACKEND_FAILURE",
            "all_causes": causes,
            "exception": repr(exc),
            "last_complete_snapshot": None,
        })
        return RunResult(
            cfg.raw.get("scenario_id", "UNKNOWN"),
            "SOLVER_BACKEND_FAILURE",
            "SOLVER_BACKEND_FAILURE",
            causes,
            None,
            history,
            {},
            {
                "NUMERICALLY_VALID": False,
                "TCC_CONSISTENT": False,
                "PHYSICAL_POSTCHECK_NUMERIC_PASS": False,
                "MODEL0D_SAFETY_CERTIFIED": False,
                "SUNSUN_ALGORITHMICALLY_CERTIFIED": False,
            },
            time.monotonic() - start_time,
        )

    def finish(
        termination_reason: str,
        causes: list[str],
        state: RunState | None,
        last_oracles: list[LocalOracleDiagnostics] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> RunResult:
        metrics, statuses, post_causes = _final_metrics(cfg, ops, local1, local2, state, last_oracles)
        all_causes = list(dict.fromkeys([c for c in causes + post_causes if c]))
        primary = _primary(all_causes)
        event: dict[str, Any] = {
            "phase": "finalization",
            "termination_reason": termination_reason,
            "primary_cause": primary,
            "all_causes": all_causes,
            "last_complete_snapshot": None if state is None else {
                "outer_r": state.outer_r,
                "inner_t": state.inner_t,
            },
            "statuses": statuses,
        }
        if extra:
            event.update(extra)
        emit(event)
        return RunResult(
            cfg.raw["scenario_id"], termination_reason, primary, all_causes,
            state, history, metrics, statuses, time.monotonic() - start_time,
        )

    admissible, causes = _initial_admissibility(cfg)
    if not admissible:
        return finish("INPUT_ADMISSIBILITY_FAILED", causes, None)

    z1, z2, u = stationary_exact_tcc_initialization(cfg, ops)
    xi_outer_prev = np.zeros(ops.m)  # xi^0
    beta = float(cfg.a["beta0"]) * float(cfg.a["vartheta"])  # beta^1
    rho = 2.0 * beta
    lam = np.full(ops.m, float(cfg.a["lambda_initial"]))
    xi = np.zeros(ops.m)
    y = -lam - beta * xi
    last_complete_state = RunState(
        z1.copy(), z2.copy(), u.copy(), xi.copy(), y.copy(), lam.copy(),
        beta, rho, 0, 0,
    )
    consecutive_outer_passes = 0
    last_oracles: list[LocalOracleDiagnostics] = []

    for r in range(1, int(cfg.a["max_outer_iterations"]) + 1):
        if time.monotonic() - start_time > float(cfg.a["wall_clock_cap_s"]):
            return finish("TIMEOUT", ["TIMEOUT"], last_complete_state, last_oracles)

        # Warm start from the previous complete outer primal/slack output; reset y
        # exactly to the Algorithm-1 initialization identity.
        if r == 1:
            z1_r0, z2_r0, u_r0 = z1.copy(), z2.copy(), u.copy()
            xi_r0 = np.zeros(ops.m)
        else:
            z1_r0, z2_r0, u_r0 = z1.copy(), z2.copy(), u.copy()
            xi_r0 = xi.copy()
        y_r0 = -lam - beta * xi_r0
        z1, z2, u, xi, y = z1_r0, z2_r0, u_r0, xi_r0, y_r0
        rho = 2.0 * beta
        init_ok, init_integ = integrity_pass(cfg, lam, beta, xi, y, rho)
        init_finite = all(np.all(np.isfinite(v)) for v in (z1, z2, u, xi, y, lam))
        if not init_ok or not init_finite:
            init_causes: list[str] = []
            if not init_finite:
                init_causes.append("NUMERICAL_NAN_INF")
            if not init_ok:
                init_causes.append("ALGEBRAIC_INTEGRITY_FAILED")
            return finish(
                "INITIALIZATION_FAILED", init_causes, last_complete_state, last_oracles,
                {"initialization_integrity": init_integ},
            )

        inner_completed = False
        for t in range(1, int(cfg.a["max_inner_iterations"]) + 1):
            if time.monotonic() - start_time > float(cfg.a["wall_clock_cap_s"]):
                return finish("TIMEOUT", ["TIMEOUT"], last_complete_state, last_oracles)

            Q = ops.Q
            xi1_old, xi2_old = xi[:Q].copy(), xi[Q:].copy()
            y1_old, y2_old = y[:Q].copy(), y[Q:].copy()
            z1_old, z2_old, u_old, xi_old = z1.copy(), z2.copy(), u.copy(), xi.copy()

            # UAV-local first block, followed by a logical all-agent acceptance barrier.
            res1 = local1.solve(z1_old, u_old, xi1_old, y1_old, rho)
            res2 = local2.solve(z2_old, u_old, xi2_old, y2_old, rho)
            d1 = local_oracle_diagnostics(local1, res1, z1_old, u_old, xi1_old, y1_old, rho)
            d2 = local_oracle_diagnostics(local2, res2, z2_old, u_old, xi2_old, y2_old, rho)
            last_oracles = [d1, d2]
            if not (d1.accepted and d2.accepted):
                oracle_causes = [code for d in last_oracles for code in d.failure_codes]
                emit({
                    "phase": "local_oracle_abort", "r": r, "t": t,
                    "oracles": [d.to_dict() for d in last_oracles],
                })
                return finish("LOCAL_ORACLE_ABORT", oracle_causes, last_complete_state, last_oracles)

            z1 = res1.z.copy()
            z2 = res2.z.copy()

            # A5 symmetric edge update.
            s1 = ops.copy2_from_z1(z1)
            s2 = ops.source2_from_z2(z2)
            u = _a5_edge_update(cfg, rho, s1, s2, xi1_old, xi2_old, y1_old, y2_old)

            # Exact slack and inner-dual updates.
            c = ops.target_rows(z1, z2, u)
            xi, y = _slack_dual_update(lam, beta, rho, y, c)

            integ_ok, integ = integrity_pass(cfg, lam, beta, xi, y, rho)
            update_finite = bool(np.all(np.isfinite(np.concatenate([z1, z2, u, xi, y]))))
            if not update_finite or not integ_ok:
                update_causes: list[str] = []
                if not update_finite:
                    update_causes.append("NUMERICAL_NAN_INF")
                if not integ_ok:
                    update_causes.append("ALGEBRAIC_INTEGRITY_FAILED")
                return finish(
                    "UPDATE_ABORT", update_causes, last_complete_state, last_oracles,
                    {"update_integrity": integ, "r": r, "t": t},
                )

            residual = _residuals(ops, rho, z1, z2, u_old, u, xi_old, xi)
            residual_ok, residual_integrity = _residual_crosscheck_pass(cfg, residual)
            if not residual_ok:
                emit({
                    "phase": "residual_integrity_abort", "r": r, "t": t,
                    "residuals": residual, "crosscheck": residual_integrity,
                })
                return finish(
                    "UPDATE_ABORT", ["ALGEBRAIC_INTEGRITY_FAILED"],
                    last_complete_state, last_oracles,
                )

            snapshot = RunState(
                z1.copy(), z2.copy(), u.copy(), xi.copy(), y.copy(), lam.copy(),
                beta, rho, r, t,
            )
            last_complete_state = snapshot
            emit({
                "phase": "inner_complete", "r": r, "t": t,
                "residuals": residual,
                "residual_crosscheck": residual_integrity,
                "integrity": integ,
                "oracles": [d1.to_dict(), d2.to_dict()],
            })

            eps1 = float(cfg.a["eps1_scale"]) / r
            eps2 = float(cfg.a["eps2_scale"]) / r
            eps3 = float(cfg.a["eps3_scale"]) / r
            if residual["R1"] <= eps1 and residual["R2"] <= eps2 and residual["R3"] <= eps3:
                inner_completed = True
                break

        if not inner_completed:
            # A complete iteration at t=max that passed the stop test would already
            # have broken above; reaching here is genuine cap exhaustion.
            return finish(
                "MAX_INNER_ITERATIONS", ["MAX_INNER_ITERATIONS"],
                last_complete_state, last_oracles,
            )

        # Complete outer output and finite reporting predicates.
        current_state = RunState(
            z1.copy(), z2.copy(), u.copy(), xi.copy(), y.copy(), lam.copy(),
            beta, rho, r, t,
        )
        last_complete_state = current_state
        try:
            current_tcc = tcc_metrics(ops, z1, z2, u)
            current_phys = physical_postcheck_numeric(cfg, ops, z1, z2)
            current_integ_ok, current_integ = integrity_pass(cfg, lam, beta, xi, y, rho)
            current_obj = _objective_metrics(local1, local2, z1, z2)
        except Exception as exc:
            return finish(
                "POSTCHECK_EVALUATION_FAILED", ["POSTCHECK_EVALUATION_FAILED"],
                current_state, last_oracles, {"exception": repr(exc)},
            )

        pass_outer = _outer_stop_predicate(
            cfg, xi, current_tcc, current_phys, current_integ_ok, last_oracles,
        )
        consecutive_outer_passes = consecutive_outer_passes + 1 if pass_outer else 0
        emit({
            "phase": "outer_complete", "r": r, "t": t,
            "objective": current_obj, "tcc": current_tcc, "physical": current_phys,
            "integrity": current_integ, "xi_norm": float(np.linalg.norm(xi)),
            "beta": beta, "rho": rho,
            "lambda_norm": float(np.linalg.norm(lam)), "y_norm": float(np.linalg.norm(y)),
            "outer_predicate": pass_outer,
            "consecutive_outer_passes": consecutive_outer_passes,
        })

        if consecutive_outer_passes >= 2:
            return finish("FINITE_OUTER_STOP", [], current_state, last_oracles)

        # Published Algorithm-2 outer updates; current output is already logged and
        # remains distinct from next-iteration parameters.
        lam_next, beta_next, rho_next = _outer_parameter_update(
            cfg, lam, beta, xi, xi_outer_prev,
        )
        xi_outer_prev = xi.copy()
        lam = lam_next
        beta = float(beta_next)
        rho = float(rho_next)
        if not (
            np.all(np.isfinite(lam)) and np.isfinite(beta) and np.isfinite(rho)
            and abs(rho - 2.0 * beta) <= float(cfg.t["integrity_relative"]) * max(1.0, abs(rho), abs(2.0 * beta))
        ):
            return finish(
                "UPDATE_ABORT", ["ALGEBRAIC_INTEGRITY_FAILED"],
                current_state, last_oracles,
                {"phase_detail": "outer_parameter_update"},
            )

    return finish(
        "MAX_OUTER_ITERATIONS", ["MAX_OUTER_ITERATIONS"],
        last_complete_state, last_oracles,
    )
