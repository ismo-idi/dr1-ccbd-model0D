"""Centralized reference solve of the frozen Model 0-D problem (P0).

Purpose
-------
Every quantity reported by the Attempt-3 campaign (R1, R2, R3, R_TCC_eq, ||xi||)
is *internal* to the Sun--Sun/TCC algorithm.  None of them can distinguish
"solved the physical problem (P0)" from "converged to a stationary point of the
feasibility-violation problem", which Sun--Sun Theorem 1, case 2, explicitly
permits.  This script supplies the only instrument that is external to the
method: a direct centralized solve of (P0) with the identical physical data.

It is a *validation oracle*, not a competing algorithm.  It requires a central
coordinator and does not scale; it plays the role an analytical solution plays
for a partial-differential-equation solver.

Fidelity
--------
The exact segment-safety constraints are imported from the frozen Attempt-3
source tree, so the centralized model and the distributed model evaluate the
*same* code path for the only nonconvex constraint family.  Physical data are
read from the frozen Attempt-3 configuration file.  The backend is the same
one used by the campaign: IPOPT (Interior Point OPTimizer), through CasADi.

Non-claims
----------
Multistart IPOPT (Interior Point OPTimizer) on a nonconvex feasible set is not
a proof of global optimality, and a finite number of starts is not exhaustive.
Decision Study 08 proves that Model 0-D has no general uniqueness guarantee.
The output of this script is numerical evidence on one instance.

Usage
-----
    python centralized_reference.py --config <attempt3 config.json> \
                                    --state  <attempt3 final_state.npz> \
                                    --src    <attempt3 src directory> \
                                    --starts 20 --output results.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_and_solve(cfg_raw, geometry, ca, x0, tol: float):
    """One centralized solve of (P0) from initial guess x0."""
    m = cfg_raw["model"]
    N, q, K, dt = int(m["N"]), int(m["q"]), int(m["K"]), float(m["dt"])
    starts = [np.asarray(s, float) for s in m["starts"]]
    goals = [np.asarray(g, float) for g in m["goals"]]
    alpha, beta_obj, vmax = m["alpha"], m["beta_obj"], m["vmax"]
    lo, hi = np.asarray(m["workspace_lower"], float), np.asarray(m["workspace_upper"], float)
    radii, d_uav = m["radii"], float(m["delta_uav"])
    if m["obstacles"]:
        raise SystemExit("this reference script covers the frozen zero-obstacle baseline only")

    x = ca.MX.sym("x", N * K * q)

    def traj(i):
        free = x[i * K * q:(i + 1) * K * q]
        p0 = ca.DM(starts[i].reshape(q, 1))
        return ca.horzcat(p0, ca.reshape(free, q, K))

    P = [traj(i) for i in range(N)]

    f = 0
    for i in range(N):
        g = ca.DM(goals[i].reshape(-1, 1))
        f += float(alpha[i]) * ca.dot(P[i][:, K] - g, P[i][:, K] - g)
        for k in range(K):
            s = P[i][:, k + 1] - P[i][:, k]
            f += float(beta_obj[i]) * ca.dot(s, s)

    G = []
    for i in range(N):
        for k in range(1, K + 1):
            for j in range(q):
                G += [P[i][j, k] - float(hi[j]), float(lo[j]) - P[i][j, k]]
        v2 = (float(vmax[i]) * dt) ** 2
        for k in range(K):
            s = P[i][:, k + 1] - P[i][:, k]
            G += [ca.dot(s, s) - v2]
    for i in range(N):
        for j in range(i + 1, N):
            clearance = float(radii[i]) + float(radii[j]) + d_uav
            for k in range(K):
                G += [geometry.uav_segment_constraint_symbolic(
                    P[i][:, k], P[i][:, k + 1], P[j][:, k], P[j][:, k + 1], clearance)]
    g_all = ca.vertcat(*G)

    solver = ca.nlpsol("centralized_reference", "ipopt",
                       {"x": x, "f": f, "g": g_all},
                       {"ipopt.tol": tol, "ipopt.print_level": 0, "print_time": False,
                        "ipopt.bound_relax_factor": 0.0, "ipopt.max_iter": 3000})
    sol = solver(x0=x0, lbg=-np.inf * np.ones(g_all.shape[0]), ubg=np.zeros(g_all.shape[0]))
    ok = bool(solver.stats().get("success", False))
    return ok, float(sol["f"]), np.asarray(sol["x"], float).reshape(-1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--state", required=True)
    ap.add_argument("--src", required=True, help="frozen Attempt-3 src/ directory")
    ap.add_argument("--starts", type=int, default=20)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tol", type=float, default=1e-10)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()

    sys.path.insert(0, str(Path(a.src).resolve().parent))
    import casadi as ca                      # noqa: E402
    from src import geometry                 # noqa: E402

    cfg_raw = json.loads(Path(a.config).read_text())
    m = cfg_raw["model"]
    N, q, K = int(m["N"]), int(m["q"]), int(m["K"])
    starts = [np.asarray(s, float) for s in m["starts"]]

    hover = np.concatenate([np.tile(starts[i], K) for i in range(N)])
    rng = np.random.default_rng(a.seed)
    lo, hi = np.asarray(m["workspace_lower"], float), np.asarray(m["workspace_upper"], float)
    guesses = [hover] + [np.clip(hover + rng.normal(scale=1.0, size=hover.size),
                                 np.tile(lo, N * K), np.tile(hi, N * K))
                         for _ in range(a.starts - 1)]

    values, solutions, best = [], [], None
    for idx, x0 in enumerate(guesses):
        ok, F, xs = build_and_solve(cfg_raw, geometry, ca, x0, a.tol)
        if not ok:
            continue
        values.append(F)
        solutions.append((F, xs))
        if best is None or F < best[0]:
            best = (F, xs)
    if best is None:
        raise SystemExit("no centralized start converged")

    F_star, x_star = best

    # The instance is symmetric, so several distinct minimizers may share F*.
    # Cluster the converged solutions by trajectory to count them explicitly.
    optimal = [xs for F, xs in solutions if abs(F - F_star) <= 1e-8 * max(1.0, abs(F_star))]
    clusters: list[np.ndarray] = []
    for xs in optimal:
        if not any(np.linalg.norm(xs - c) <= 1e-5 for c in clusters):
            clusters.append(xs)

    # Distributed Attempt-3 free trajectory, in the same coordinate order.
    st = np.load(a.state)
    x_tcc = np.concatenate([st["z1"][: K * q], st["z2"]])


    # Physical margins of the centralized optimum, recomputed independently.
    def free_to_full(vec, i):
        return np.vstack([starts[i], vec[i * K * q:(i + 1) * K * q].reshape(K, q)])
    x_nearest = min(clusters, key=lambda c: np.linalg.norm(x_tcc - c))
    Pc = [free_to_full(x_nearest, i) for i in range(N)]
    clearance = float(m["radii"][0]) + float(m["radii"][1]) + float(m["delta_uav"])
    margins = []
    for k in range(K):
        _, res = geometry.uav_segment_constraint_numeric(
            Pc[0][k], Pc[0][k + 1], Pc[1][k], Pc[1][k + 1], clearance)
        margins.append(geometry.unsquared_margin_from_squared_min(res.min_squared_distance, clearance))

    out = {
        "purpose": "external validation oracle for the TCC copy-space reformulation; not a competing algorithm",
        "backend": "IPOPT (Interior Point OPTimizer) via CasADi",
        "ipopt_tol": a.tol,
        "multistart": {"requested": a.starts, "converged": len(values), "seed": a.seed},
        "objective": {
            "F_star_centralized": F_star,
            "F_attempt3_distributed": 4.0157423760136215,
            "absolute_gap": 4.0157423760136215 - F_star,
            "relative_gap_percent": 100.0 * (4.0157423760136215 - F_star) / F_star,
            "distinct_converged_values_rounded_1e-9": sorted(set(np.round(values, 9).tolist())),
        },
        "distinct_global_minimizers_found": {
            "count": len(clusters),
            "separation_l2_m": (
                float(min(np.linalg.norm(clusters[i] - clusters[j])
                          for i in range(len(clusters)) for j in range(i + 1, len(clusters))))
                if len(clusters) > 1 else None),
            "note": ("Several distinct trajectories attain F* on this symmetric crossing instance. "
                     "This is a numerical instance of the non-uniqueness proved in Decision Study 08: "
                     "the objective is strictly convex, the feasible set is not."),
        },
        "trajectory_agreement_nearest_minimizer": {
            "l2_norm_difference_m": float(np.linalg.norm(x_tcc - x_nearest)),
            "max_coordinate_difference_m": float(np.max(np.abs(x_tcc - x_nearest))),
        },
        "centralized_optimum_uav_clearance_margins_m": [float(v) for v in margins],
        "centralized_optimum_min_uav_clearance_margin_m": float(min(margins)),
        "inputs": {
            "config": str(a.config), "config_sha256": sha256(Path(a.config)),
            "state": str(a.state), "state_sha256": sha256(Path(a.state)),
        },
        "environment": {
            "python": sys.version.split()[0], "platform": platform.platform(),
            "numpy": np.__version__, "casadi": ca.__version__,
        },
        "non_claims": [
            "multistart IPOPT (Interior Point OPTimizer) on a nonconvex feasible set is not a proof of global optimality",
            "a finite number of starts is not exhaustive",
            "Decision Study 08 proves Model 0-D has no general uniqueness guarantee",
            "this validates TCC exactness numerically on one instance; it certifies neither convergence nor real-UAV safety",
        ],
    }
    Path(a.output).write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
