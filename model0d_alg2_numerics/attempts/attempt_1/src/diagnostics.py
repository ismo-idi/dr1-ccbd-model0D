"""Independent finite diagnostics for the approved Model 0-D campaign.

These diagnostics intentionally do not upgrade finite numerical evidence into
exact Sun--Sun oracle certification or U4 physical-safety certification.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import numpy as np

from .config import ModelConfig
from .geometry import (
    obstacle_segment_constraint_numeric,
    uav_segment_constraint_numeric,
    unsquared_margin_from_squared_min,
)
from .local_nlp import LocalNLP, LocalSolveResult
from .tcc import TCCOperators


FAMILY_TAU_KEY = {
    "W": "tau_W",
    "spd": "tau_spd",
    "obs": "tau_obs",
    "uav": "tau_uav",
    "A1": "tau_A1",
}


@dataclass
class LocalOracleDiagnostics:
    agent: int
    backend_success: bool
    backend_status: str
    backend_iterations: int | None
    backend_elapsed_s: float
    finite: bool
    constraint_value_crosscheck_abs: float
    constraint_value_crosscheck_limit: float
    constraint_value_crosscheck_pass: bool
    feasibility_max_by_family: dict[str, float]
    feasibility_pass_by_family: dict[str, bool]
    raw_g: list[float]
    raw_mu_backend: list[float]
    multiplier_mapping_available: bool
    diagnostic_mu: list[float]
    differentiable_rows: list[int]
    omitted_rows: list[int]
    omitted_reasons: dict[str, str]
    near_active_rows: list[int]
    nonsmooth_blocking_rows: list[int]
    R_dual: float
    R_dual_normalized: float
    R_comp: float
    R_stat: float
    R_stat_normalized: float
    R_desc: float
    descent_limit: float
    pass_dual: bool
    pass_comp: bool
    pass_stat: bool
    pass_desc: bool
    accepted: bool
    failure_code: str | None
    failure_codes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _trajectory_from_free(start: np.ndarray, free: np.ndarray, K: int, q: int) -> np.ndarray:
    return np.vstack([np.asarray(start, float).reshape(1, q), np.asarray(free, float).reshape(K, q)])


def extract_local_trajectories(local: LocalNLP, z: np.ndarray) -> dict[str, np.ndarray]:
    cfg = local.cfg
    z = np.asarray(z, float).reshape(-1)
    if local.agent == 1:
        p1 = _trajectory_from_free(cfg.starts[0], z[: cfg.Q], cfg.K, cfg.q)
        p2_copy = _trajectory_from_free(cfg.starts[1], z[cfg.Q : 2 * cfg.Q], cfg.K, cfg.q)
        return {"source": p1, "copy2": p2_copy}
    p2 = _trajectory_from_free(cfg.starts[1], z[: cfg.Q], cfg.K, cfg.q)
    return {"source": p2}


def _segment_s_for_meta(local: LocalNLP, z: np.ndarray, row: int) -> float | None:
    meta = local.metas[row]
    tr = extract_local_trajectories(local, z)
    k = meta.interval
    if meta.family == "obs" and k is not None:
        P = tr["source"]
        d = P[k + 1] - P[k]
        return float(np.dot(d, d))
    if meta.family == "uav" and k is not None:
        p1 = tr["source"]
        p2 = tr["copy2"]
        a0 = p1[k] - p2[k]
        a1 = p1[k + 1] - p2[k + 1]
        d = a1 - a0
        return float(np.dot(d, d))
    return None


def recompute_local_constraints_numeric(local: LocalNLP, z: np.ndarray) -> np.ndarray:
    """Independent NumPy recomputation of the canonical local g(z)<=0 rows.

    This mirrors the frozen mathematical families rather than evaluating the
    CasADi solver graph. Row order is intentionally reconstructed from the
    approved canonical assembly and cross-checked against LocalNLP metadata.
    """
    cfg = local.cfg
    tr = extract_local_trajectories(local, z)
    P = tr["source"]
    source_idx = 0 if local.agent == 1 else 1
    vals: list[float] = []

    # Workspace rows in exactly the canonical upper/lower order.
    for k in range(1, cfg.K + 1):
        pk = P[k]
        for j in range(cfg.q):
            vals.append(float(pk[j] - cfg.workspace_upper[j]))
            vals.append(float(cfg.workspace_lower[j] - pk[j]))

    # Squared speed rows.
    vmax_step_sq = float(cfg.vmax[source_idx] * cfg.dt) ** 2
    for k in range(cfg.K):
        step = P[k + 1] - P[k]
        vals.append(float(np.dot(step, step) - vmax_step_sq))

    # Exact squared obstacle-segment rows.
    for obs in cfg.obstacles:
        clearance = cfg.obstacle_clearance(source_idx, obs)
        for k in range(cfg.K):
            g, _ = obstacle_segment_constraint_numeric(P[k], P[k + 1], obs["center"], clearance)
            vals.append(float(g))

    if local.agent == 1:
        P2 = tr["copy2"]
        for k in range(cfg.K):
            g, _ = uav_segment_constraint_numeric(
                P[k], P[k + 1], P2[k], P2[k + 1], cfg.uav_clearance,
            )
            vals.append(float(g))

        # A1 box on foreign source-2 free samples only.
        for k in range(1, cfg.K + 1):
            pk = P2[k]
            for j in range(cfg.q):
                vals.append(float(pk[j] - cfg.a1_upper[j]))
                vals.append(float(cfg.a1_lower[j] - pk[j]))

    arr = np.asarray(vals, dtype=float)
    if arr.size != local.n_constraints:
        raise RuntimeError(
            f"independent local constraint count {arr.size} != assembled {local.n_constraints}"
        )
    return arr


def local_oracle_diagnostics(
    local: LocalNLP,
    result: LocalSolveResult,
    z_old: np.ndarray,
    u_old: np.ndarray,
    xi_old_half: np.ndarray,
    y_old_half: np.ndarray,
    rho: float,
) -> LocalOracleDiagnostics:
    cfg = local.cfg
    t = cfg.t
    z = np.asarray(result.z, float).reshape(-1)
    g_backend = local.eval_g(z)
    g = recompute_local_constraints_numeric(local, z)
    J = local.eval_jac(z)
    grad_phi = local.eval_grad_phi(z, u_old, xi_old_half, y_old_half, rho)
    mu_backend = np.asarray(result.mu, float).reshape(-1)

    g_cross_abs = float(np.max(np.abs(g_backend - g))) if g.size else 0.0
    g_cross_scale = max(1.0, float(np.max(np.abs(g_backend))) if g_backend.size else 0.0, float(np.max(np.abs(g))) if g.size else 0.0)
    g_cross_limit = float(t["integrity_relative"]) * g_cross_scale
    g_cross_pass = bool(g_cross_abs <= g_cross_limit)

    multiplier_mapping_available = bool(mu_backend.size == g.size == len(local.metas))
    finite = bool(
        np.all(np.isfinite(z)) and np.all(np.isfinite(g_backend)) and np.all(np.isfinite(g)) and
        np.all(np.isfinite(J)) and np.all(np.isfinite(grad_phi)) and
        np.all(np.isfinite(mu_backend)) and np.isfinite(result.phi)
    )

    feasibility_max_by_family: dict[str, float] = {}
    feasibility_pass_by_family: dict[str, bool] = {}
    for fam in FAMILY_TAU_KEY:
        rows = [m.row for m in local.metas if m.family == fam]
        if not rows:
            continue
        vmax = float(np.max(np.maximum(g[rows], 0.0)))
        feasibility_max_by_family[fam] = vmax
        feasibility_pass_by_family[fam] = bool(vmax <= float(t[FAMILY_TAU_KEY[fam]]))

    # A missing or mis-sized multiplier vector is an unavailable diagnostic,
    # not permission to invent multipliers or silently reorder rows.
    if not multiplier_mapping_available:
        phi_old = local.eval_phi(z_old, u_old, xi_old_half, y_old_half, rho)
        phi_new = local.eval_phi(z, u_old, xi_old_half, y_old_half, rho)
        R_desc = max(0.0, float(phi_new - phi_old))
        descent_limit = float(t["descent_relative"]) * max(1.0, abs(phi_old), abs(phi_new))
        failure_codes = []
        if not finite:
            failure_codes.append("NUMERICAL_NAN_INF")
        if not result.backend_success:
            failure_codes.append("SOLVER_BACKEND_FAILURE")
        if not g_cross_pass:
            failure_codes.append("ALGEBRAIC_INTEGRITY_FAILED")
        failure_codes.append("MULTIPLIER_DIAGNOSTIC_UNAVAILABLE")
        return LocalOracleDiagnostics(
            agent=local.agent, backend_success=result.backend_success, backend_status=result.backend_status,
            backend_iterations=result.backend_iterations, backend_elapsed_s=result.backend_elapsed_s, finite=finite, constraint_value_crosscheck_abs=g_cross_abs, constraint_value_crosscheck_limit=g_cross_limit, constraint_value_crosscheck_pass=g_cross_pass, feasibility_max_by_family=feasibility_max_by_family,
            feasibility_pass_by_family=feasibility_pass_by_family, raw_g=g.tolist(),
            raw_mu_backend=mu_backend.tolist(), multiplier_mapping_available=False,
            diagnostic_mu=[], differentiable_rows=[], omitted_rows=[], omitted_reasons={},
            near_active_rows=[], nonsmooth_blocking_rows=[], R_dual=float("inf"),
            R_dual_normalized=float("inf"), R_comp=float("inf"), R_stat=float("inf"),
            R_stat_normalized=float("inf"), R_desc=R_desc, descent_limit=descent_limit,
            pass_dual=False, pass_comp=False, pass_stat=False, pass_desc=bool(R_desc <= descent_limit),
            accepted=False, failure_code=failure_codes[0], failure_codes=failure_codes,
        )

    mu_diag = mu_backend.copy()
    diff_rows: list[int] = []
    omitted_rows: list[int] = []
    omitted_reasons: dict[str, str] = {}
    near_active_rows: list[int] = []
    blocking: list[int] = []

    for meta in local.metas:
        row = meta.row
        if meta.family not in ("obs", "uav"):
            diff_rows.append(row)
            continue
        s = _segment_s_for_meta(local, z, row)
        assert s is not None
        family_tau = float(t[FAMILY_TAU_KEY[meta.family]])
        near_buffer = float(t["near_factor"]) * family_tau
        if g[row] >= -near_buffer:
            near_active_rows.append(row)
        if s > float(t["tau_s"]):
            diff_rows.append(row)
            continue
        inactive_buffer = float(t["inactive_factor"]) * family_tau
        if g[row] < -inactive_buffer:
            omitted_rows.append(row)
            mu_diag[row] = 0.0
            omitted_reasons[str(row)] = (
                f"{meta.label}: s={s:.17g} <= tau_s and g={g[row]:.17g} "
                f"< -inactive_buffer={-inactive_buffer:.17g}; strict-inactive local omission"
            )
        else:
            blocking.append(row)

    # Full multiplier checks use diagnostic multipliers, with justified omitted rows zeroed.
    R_dual = float(np.max(np.maximum(-mu_diag, 0.0))) if mu_diag.size else 0.0
    mu_scale = max(1.0, float(np.max(np.abs(mu_diag))) if mu_diag.size else 0.0)
    R_dual_norm = R_dual / mu_scale
    R_comp = float(np.max(np.abs(mu_diag * g))) if mu_diag.size else 0.0

    if diff_rows:
        Jd = J[diff_rows, :]
        mud = mu_diag[diff_rows]
        jtmu = Jd.T @ mud
    else:
        jtmu = np.zeros_like(grad_phi)
    stationarity_vec = grad_phi + jtmu
    R_stat = float(np.linalg.norm(stationarity_vec))
    stat_scale = max(1.0, float(np.linalg.norm(grad_phi)), float(np.linalg.norm(jtmu)))
    R_stat_norm = R_stat / stat_scale

    phi_old = local.eval_phi(z_old, u_old, xi_old_half, y_old_half, rho)
    phi_new = local.eval_phi(z, u_old, xi_old_half, y_old_half, rho)
    R_desc = max(0.0, float(phi_new - phi_old))
    descent_limit = float(t["descent_relative"]) * max(1.0, abs(phi_old), abs(phi_new))

    pass_dual = bool(R_dual_norm <= float(t["dual_normalized"]))
    pass_comp = bool(R_comp <= float(t["complementarity"]))
    pass_stat = bool(R_stat_norm <= float(t["stationarity_normalized"]))
    pass_desc = bool(R_desc <= descent_limit)
    pass_feas = bool(all(feasibility_pass_by_family.values()))

    failure_codes: list[str] = []
    # Preserve simultaneous causes in protocol priority order for the local phase.
    if not finite:
        failure_codes.append("NUMERICAL_NAN_INF")
    if not result.backend_success:
        failure_codes.append("SOLVER_BACKEND_FAILURE")
    if not g_cross_pass:
        failure_codes.append("ALGEBRAIC_INTEGRITY_FAILED")
    if blocking:
        failure_codes.append("ORACLE_UNCERTIFIED_NONSMOOTH")
    if not (pass_feas and pass_dual and pass_comp and pass_stat and pass_desc):
        failure_codes.append("FIRST_BLOCK_ORACLE_FAILED")
    failure_code = failure_codes[0] if failure_codes else None
    accepted = not failure_codes
    return LocalOracleDiagnostics(
        agent=local.agent,
        backend_success=result.backend_success,
        backend_status=result.backend_status,
        backend_iterations=result.backend_iterations,
        backend_elapsed_s=result.backend_elapsed_s,
        finite=finite,
        constraint_value_crosscheck_abs=g_cross_abs,
        constraint_value_crosscheck_limit=g_cross_limit,
        constraint_value_crosscheck_pass=g_cross_pass,
        feasibility_max_by_family=feasibility_max_by_family,
        feasibility_pass_by_family=feasibility_pass_by_family,
        raw_g=g.tolist(),
        raw_mu_backend=mu_backend.tolist(),
        multiplier_mapping_available=multiplier_mapping_available,
        diagnostic_mu=mu_diag.tolist(),
        differentiable_rows=diff_rows,
        omitted_rows=omitted_rows,
        omitted_reasons=omitted_reasons,
        near_active_rows=near_active_rows,
        nonsmooth_blocking_rows=blocking,
        R_dual=R_dual,
        R_dual_normalized=R_dual_norm,
        R_comp=R_comp,
        R_stat=R_stat,
        R_stat_normalized=R_stat_norm,
        R_desc=R_desc,
        descent_limit=descent_limit,
        pass_dual=pass_dual,
        pass_comp=pass_comp,
        pass_stat=pass_stat,
        pass_desc=pass_desc,
        accepted=accepted,
        failure_code=failure_code,
        failure_codes=failure_codes,
    )


def tcc_metrics(ops: TCCOperators, z1, z2, u) -> dict[str, float]:
    direct = ops.direct_tcc_difference(z1, z2)
    target = ops.target_rows(z1, z2, u)
    return {
        "R_TCC_eq": float(np.linalg.norm(direct)),  # unique tree edge => max=edge norm
        "R_target": float(np.linalg.norm(target)),
    }


def integrity_metrics(lambda_r, beta_r: float, xi, y, rho: float) -> dict[str, float]:
    lam = np.asarray(lambda_r, float).reshape(-1)
    xi = np.asarray(xi, float).reshape(-1)
    y = np.asarray(y, float).reshape(-1)
    return {
        "R_id": float(np.linalg.norm(lam + beta_r * xi + y)),
        "R_rhobeta": float(abs(rho - 2.0 * beta_r)),
    }


def integrity_pass(cfg: ModelConfig, lambda_r, beta_r: float, xi, y, rho: float) -> tuple[bool, dict[str, float]]:
    vals = integrity_metrics(lambda_r, beta_r, xi, y, rho)
    t = float(cfg.t["integrity_relative"])
    lam = np.asarray(lambda_r, float).reshape(-1)
    xi = np.asarray(xi, float).reshape(-1)
    y = np.asarray(y, float).reshape(-1)
    id_scale = max(1.0, float(np.linalg.norm(lam)), float(np.linalg.norm(beta_r * xi)), float(np.linalg.norm(y)))
    rb_scale = max(1.0, abs(float(rho)), abs(2.0 * float(beta_r)))
    vals["R_id_limit"] = t * id_scale
    vals["R_rhobeta_limit"] = t * rb_scale
    ok = vals["R_id"] <= vals["R_id_limit"] and vals["R_rhobeta"] <= vals["R_rhobeta_limit"]
    return bool(ok), vals


def source_trajectories(cfg: ModelConfig, ops: TCCOperators, z1, z2) -> tuple[np.ndarray, np.ndarray]:
    x1 = ops.source1_from_z1(z1).reshape(cfg.K, cfg.q)
    x2 = ops.source2_from_z2(z2).reshape(cfg.K, cfg.q)
    p1 = np.vstack([cfg.starts[0], x1])
    p2 = np.vstack([cfg.starts[1], x2])
    return p1, p2


def physical_postcheck_numeric(cfg: ModelConfig, ops: TCCOperators, z1, z2) -> dict[str, Any]:
    """Ordinary floating-point physical diagnostic on actual source trajectories.

    This function never sets MODEL0D_SAFETY_CERTIFIED; U4 remains unresolved.
    """
    p1, p2 = source_trajectories(cfg, ops, z1, z2)
    fam: dict[str, list[float]] = {"W": [], "spd": [], "obs": [], "uav": []}

    # Workspace normalized margins; box normals are unit coordinate vectors.
    for P in (p1, p2):
        for k in range(1, cfg.K + 1):
            fam["W"].extend((cfg.workspace_upper - P[k]).tolist())
            fam["W"].extend((P[k] - cfg.workspace_lower).tolist())

    for i, P in enumerate((p1, p2)):
        for k in range(cfg.K):
            fam["spd"].append(float(cfg.vmax[i] * cfg.dt - np.linalg.norm(P[k + 1] - P[k])))
        for obs in cfg.obstacles:
            clearance = cfg.obstacle_clearance(i, obs)
            for k in range(cfg.K):
                _, res = obstacle_segment_constraint_numeric(P[k], P[k + 1], obs["center"], clearance)
                fam["obs"].append(unsquared_margin_from_squared_min(res.min_squared_distance, clearance))

    for k in range(cfg.K):
        _, res = uav_segment_constraint_numeric(p1[k], p1[k + 1], p2[k], p2[k + 1], cfg.uav_clearance)
        fam["uav"].append(unsquared_margin_from_squared_min(res.min_squared_distance, cfg.uav_clearance))

    expected = {
        "W": 2 * 2 * cfg.q * cfg.K,
        "spd": 2 * cfg.K,
        "obs": 2 * len(cfg.obstacles) * cfg.K,
        "uav": cfg.K,
    }
    out: dict[str, Any] = {"expected_cardinality": expected, "families": {}}
    tau = float(cfg.t["physical_numeric_margin"])
    all_pass = True
    evaluation_complete = True
    for name, vals in fam.items():
        if len(vals) != expected[name]:
            out["families"][name] = {"status": "EVALUATION_COUNT_MISMATCH", "actual": len(vals), "expected": expected[name]}
            all_pass = False
            evaluation_complete = False
            continue
        if not vals:
            out["families"][name] = {
                "aggregate_violation": 0.0,
                "minimum_margin": "NOT_APPLICABLE_EMPTY_FAMILY",
                "numeric_pass": True,
            }
            continue
        arr = np.asarray(vals, float)
        finite = bool(np.all(np.isfinite(arr)))
        min_margin = float(np.min(arr)) if finite else float("nan")
        violation = float(np.max(np.maximum(-arr, 0.0))) if finite else float("nan")
        passed = bool(finite and min_margin >= -tau)
        if not finite:
            evaluation_complete = False
        all_pass = all_pass and passed
        out["families"][name] = {
            "aggregate_violation": violation,
            "minimum_margin": min_margin,
            "numeric_pass": passed,
        }
    out["evaluation_complete"] = bool(evaluation_complete)
    out["PHYSICAL_POSTCHECK_NUMERIC_PASS"] = bool(all_pass and evaluation_complete)
    out["MODEL0D_SAFETY_CERTIFIED"] = False
    out["certification_note"] = "U4 unresolved; ordinary floating-point margins are diagnostic only."
    return out
