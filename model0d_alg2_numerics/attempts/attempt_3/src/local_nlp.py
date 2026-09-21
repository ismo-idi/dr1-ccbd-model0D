"""UAV-local first-block NLPs for the frozen N=2 TCC baseline.

Implements Decision-15 (S7)-(S9) with CasADi/IPOPT. The backend solve is
never itself treated as oracle certification; diagnostics.py independently
recomputes the required finite acceptance quantities.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import time

import casadi as ca
import numpy as np

from .config import ModelConfig
from .geometry import obstacle_segment_constraint_symbolic, uav_segment_constraint_symbolic
from .tcc import TCCOperators


@dataclass(frozen=True)
class ConstraintMeta:
    row: int
    family: str  # W, spd, obs, uav, A1
    label: str
    interval: int | None = None
    obstacle_index: int | None = None


@dataclass
class LocalSolveResult:
    agent: int
    z: np.ndarray
    mu: np.ndarray
    phi: float
    backend_success: bool
    backend_status: str
    backend_iterations: int | None
    backend_elapsed_s: float
    raw_stats: dict[str, Any]


@dataclass
class LocalNLP:
    agent: int
    cfg: ModelConfig
    ops: TCCOperators
    solver: Any
    metas: list[ConstraintMeta]
    g_fun: Any
    jac_fun: Any
    phi_fun: Any
    grad_phi_fun: Any
    source_objective_fun: Any

    @property
    def d(self) -> int:
        return self.ops.d1 if self.agent == 1 else self.ops.d2

    @property
    def n_constraints(self) -> int:
        return len(self.metas)

    def parameter_vector(self, u_old, xi_old_half, y_old_half, rho: float) -> np.ndarray:
        return np.concatenate([
            np.asarray(u_old, float).reshape(-1),
            np.asarray(xi_old_half, float).reshape(-1),
            np.asarray(y_old_half, float).reshape(-1),
            [float(rho)],
        ])

    def solve(self, z0, u_old, xi_old_half, y_old_half, rho: float) -> LocalSolveResult:
        p = self.parameter_vector(u_old, xi_old_half, y_old_half, rho)
        args = {
            "x0": np.asarray(z0, float).reshape(-1),
            "p": p,
            "lbg": np.full(self.n_constraints, -np.inf),
            "ubg": np.zeros(self.n_constraints),
        }
        tic = time.monotonic()
        try:
            sol = self.solver(**args)
            elapsed = time.monotonic() - tic
            stats = dict(self.solver.stats())
            z = np.asarray(sol["x"], float).reshape(-1)
            mu = np.asarray(sol["lam_g"], float).reshape(-1)
            phi = float(sol["f"])
            return LocalSolveResult(
                agent=self.agent,
                z=z,
                mu=mu,
                phi=phi,
                backend_success=bool(stats.get("success", False)),
                backend_status=str(stats.get("return_status", "UNKNOWN")),
                backend_iterations=int(stats["iter_count"]) if "iter_count" in stats else None,
                backend_elapsed_s=float(elapsed),
                raw_stats=stats,
            )
        except Exception as exc:  # final classification is handled by the harness
            elapsed = time.monotonic() - tic
            return LocalSolveResult(
                agent=self.agent,
                z=np.asarray(z0, float).reshape(-1).copy(),
                mu=np.full(self.n_constraints, np.nan),
                phi=float("nan"),
                backend_success=False,
                backend_status=f"EXCEPTION:{type(exc).__name__}:{exc}",
                backend_iterations=None,
                backend_elapsed_s=float(elapsed),
                raw_stats={"exception": repr(exc)},
            )

    def eval_g(self, z) -> np.ndarray:
        return np.asarray(self.g_fun(np.asarray(z, float).reshape(-1)), float).reshape(-1)

    def eval_jac(self, z) -> np.ndarray:
        return np.asarray(self.jac_fun(np.asarray(z, float).reshape(-1)), float)

    def eval_phi(self, z, u_old, xi_old_half, y_old_half, rho: float) -> float:
        p = self.parameter_vector(u_old, xi_old_half, y_old_half, rho)
        return float(self.phi_fun(np.asarray(z, float).reshape(-1), p))

    def eval_grad_phi(self, z, u_old, xi_old_half, y_old_half, rho: float) -> np.ndarray:
        p = self.parameter_vector(u_old, xi_old_half, y_old_half, rho)
        return np.asarray(self.grad_phi_fun(np.asarray(z, float).reshape(-1), p), float).reshape(-1)

    def eval_source_objective(self, z) -> float:
        return float(self.source_objective_fun(np.asarray(z, float).reshape(-1)))


def _trajectory_matrix(free, start: np.ndarray, q: int, K: int):
    free_mat = ca.reshape(free, q, K)
    p0 = ca.DM(np.asarray(start, float).reshape(q, 1))
    return ca.horzcat(p0, free_mat)  # q x (K+1)


def _objective(P, goal: np.ndarray, alpha: float, beta_obj: float, K: int):
    g = ca.DM(np.asarray(goal, float).reshape(-1, 1))
    val = alpha * ca.dot(P[:, K] - g, P[:, K] - g)
    for k in range(K):
        step = P[:, k + 1] - P[:, k]
        val += beta_obj * ca.dot(step, step)
    return val


def _append(g_list, metas, expr, family: str, label: str, interval=None, obstacle_index=None):
    row = len(g_list)
    g_list.append(expr)
    metas.append(ConstraintMeta(row, family, label, interval, obstacle_index))


def build_local_nlp(agent: int, cfg: ModelConfig, ops: TCCOperators) -> LocalNLP:
    if agent not in (1, 2):
        raise ValueError("agent must be 1 or 2")
    Q, q, K = cfg.Q, cfg.q, cfg.K
    d = ops.d1 if agent == 1 else ops.d2
    z = ca.MX.sym(f"z{agent}", d)
    param = ca.MX.sym(f"param{agent}", 3 * Q + 1)
    u_old = param[:Q]
    xi_old = param[Q:2 * Q]
    y_old = param[2 * Q:3 * Q]
    rho = param[-1]

    if agent == 1:
        source_free = z[:Q]
        incident = z[Q:2 * Q]  # S_{1<-2} z_1
        foreign2 = z[Q:2 * Q]
        P_source = _trajectory_matrix(source_free, cfg.starts[0], q, K)
        P_foreign2 = _trajectory_matrix(foreign2, cfg.starts[1], q, K)
        source_idx = 0
    else:
        source_free = z[:Q]
        incident = z[:Q]  # S_{2<-2} z_2
        P_source = _trajectory_matrix(source_free, cfg.starts[1], q, K)
        P_foreign2 = None
        source_idx = 1

    f_source = _objective(
        P_source, cfg.goals[source_idx], float(cfg.alpha[source_idx]),
        float(cfg.beta_obj[source_idx]), K,
    )
    q_half = incident - u_old + xi_old
    phi = f_source + ca.dot(y_old, q_half) + 0.5 * rho * ca.dot(q_half, q_half)

    g_list: list[Any] = []
    metas: list[ConstraintMeta] = []

    # Source-owned workspace rows: axis-aligned H-representation with unit normals.
    lo, hi = cfg.workspace_lower, cfg.workspace_upper
    for k in range(1, K + 1):
        pk = P_source[:, k]
        for j in range(q):
            _append(g_list, metas, pk[j] - float(hi[j]), "W", f"a{agent}:W:k{k}:dim{j}:upper")
            _append(g_list, metas, float(lo[j]) - pk[j], "W", f"a{agent}:W:k{k}:dim{j}:lower")

    # Source-owned squared speed rows.
    vmax_step_sq = float(cfg.vmax[source_idx] * cfg.dt) ** 2
    for k in range(K):
        step = P_source[:, k + 1] - P_source[:, k]
        _append(g_list, metas, ca.dot(step, step) - vmax_step_sq, "spd", f"a{agent}:spd:k{k}", interval=k)

    # Source-owned obstacle segment rows (empty for the baseline, generic for later approved scenario).
    for oi, obs in enumerate(cfg.obstacles):
        clearance = cfg.obstacle_clearance(source_idx, obs)
        for k in range(K):
            expr = obstacle_segment_constraint_symbolic(
                P_source[:, k], P_source[:, k + 1], obs["center"], clearance
            )
            _append(g_list, metas, expr, "obs", f"a{agent}:obs:o{oi}:k{k}", interval=k, obstacle_index=oi)

    # Guardian-owned pair rows. gamma({1,2})=1, so only UAV 1 owns them.
    if agent == 1:
        clearance = cfg.uav_clearance
        for k in range(K):
            expr = uav_segment_constraint_symbolic(
                P_source[:, k], P_source[:, k + 1],
                P_foreign2[:, k], P_foreign2[:, k + 1],
                clearance,
            )
            _append(g_list, metas, expr, "uav", f"a1:uav:1-2:k{k}", interval=k)

        # A1 only on the foreign source-2 copy, not source-1.
        blo, bhi = cfg.a1_lower, cfg.a1_upper
        for k in range(1, K + 1):
            pk = P_foreign2[:, k]
            for j in range(q):
                _append(g_list, metas, pk[j] - float(bhi[j]), "A1", f"a1:A1:copy2:k{k}:dim{j}:upper")
                _append(g_list, metas, float(blo[j]) - pk[j], "A1", f"a1:A1:copy2:k{k}:dim{j}:lower")

    g = ca.vertcat(*g_list)
    jac = ca.jacobian(g, z)
    grad_phi = ca.gradient(phi, z)

    ipopt_opts = {k: v for k, v in cfg.b.items() if k != "name"}
    opts = dict(ipopt_opts)
    nlp = {"x": z, "p": param, "f": phi, "g": g}
    solver = ca.nlpsol(f"local_agent_{agent}", "ipopt", nlp, opts)

    return LocalNLP(
        agent=agent,
        cfg=cfg,
        ops=ops,
        solver=solver,
        metas=metas,
        g_fun=ca.Function(f"g_agent_{agent}", [z], [g]),
        jac_fun=ca.Function(f"jac_agent_{agent}", [z], [jac]),
        phi_fun=ca.Function(f"phi_agent_{agent}", [z, param], [phi]),
        grad_phi_fun=ca.Function(f"grad_phi_agent_{agent}", [z, param], [grad_phi]),
        source_objective_fun=ca.Function(f"f_source_agent_{agent}", [z], [f_source]),
    )
