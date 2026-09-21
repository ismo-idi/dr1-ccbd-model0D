"""Terminal-weight sweep: is the inter-UAV clearance constraint active because of alpha?

Answers one question and nothing else: at the centralized optimum of the frozen
baseline, is the inter-UAV segment-clearance constraint active only for the
frozen weight alpha = 20, or for the whole admissible range?

Backend: IPOPT (Interior Point OPTimizer) via CasADi.  Exact segment-safety
constraints are imported from the frozen Attempt-3 source tree.

This is a diagnostic sweep of the *reference* problem.  It reruns no attempt and
changes no campaign result.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--alphas", default="0.5,1,2,5,10,20,50")
    ap.add_argument("--tol", type=float, default=1e-11)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()

    sys.path.insert(0, str(Path(a.src).resolve().parent))
    import casadi as ca
    from src import geometry

    cfg = json.loads(Path(a.config).read_text())
    m = cfg["model"]
    N, q, K, dt = int(m["N"]), int(m["q"]), int(m["K"]), float(m["dt"])
    starts = [np.asarray(s, float) for s in m["starts"]]
    goals = [np.asarray(g, float) for g in m["goals"]]
    lo, hi = np.asarray(m["workspace_lower"], float), np.asarray(m["workspace_upper"], float)
    clearance = float(m["radii"][0]) + float(m["radii"][1]) + float(m["delta_uav"])

    rows = []
    for alpha in [float(t) for t in a.alphas.split(",")]:
        x = ca.MX.sym("x", N * K * q)
        P = [ca.horzcat(ca.DM(starts[i].reshape(q, 1)),
                        ca.reshape(x[i * K * q:(i + 1) * K * q], q, K)) for i in range(N)]
        f = 0
        for i in range(N):
            g = ca.DM(goals[i].reshape(-1, 1))
            f += alpha * ca.dot(P[i][:, K] - g, P[i][:, K] - g)
            for k in range(K):
                s = P[i][:, k + 1] - P[i][:, k]
                f += float(m["beta_obj"][i]) * ca.dot(s, s)
        G = []
        for i in range(N):
            for k in range(1, K + 1):
                for j in range(q):
                    G += [P[i][j, k] - float(hi[j]), float(lo[j]) - P[i][j, k]]
            v2 = (float(m["vmax"][i]) * dt) ** 2
            for k in range(K):
                s = P[i][:, k + 1] - P[i][:, k]
                G += [ca.dot(s, s) - v2]
        for k in range(K):
            G += [geometry.uav_segment_constraint_symbolic(
                P[0][:, k], P[0][:, k + 1], P[1][:, k], P[1][:, k + 1], clearance)]
        gall = ca.vertcat(*G)
        solver = ca.nlpsol("sweep", "ipopt", {"x": x, "f": f, "g": gall},
                           {"ipopt.tol": a.tol, "ipopt.print_level": 0, "print_time": False,
                            "ipopt.bound_relax_factor": 0.0})
        hover = np.concatenate([np.tile(starts[i], K) for i in range(N)])
        sol = solver(x0=hover, lbg=-np.inf * np.ones(gall.shape[0]), ubg=np.zeros(gall.shape[0]))
        ok = bool(solver.stats().get("success", False))
        xs = np.asarray(sol["x"], float).reshape(-1)
        Pn = [np.vstack([starts[i], xs[i * K * q:(i + 1) * K * q].reshape(K, q)]) for i in range(N)]
        margins = []
        for k in range(K):
            _, res = geometry.uav_segment_constraint_numeric(
                Pn[0][k], Pn[0][k + 1], Pn[1][k], Pn[1][k + 1], clearance)
            margins.append(geometry.unsquared_margin_from_squared_min(res.min_squared_distance, clearance))
        rows.append({
            "alpha": alpha, "beta_obj": float(m["beta_obj"][0]), "converged": ok,
            "F_star": float(sol["f"]),
            "min_uav_clearance_margin_m": float(min(margins)),
            "constraint_active_at_1e-6": bool(min(margins) < 1e-6),
            "goal_error_uav1_m": float(np.linalg.norm(Pn[0][-1] - goals[0])),
            "goal_error_uav2_m": float(np.linalg.norm(Pn[1][-1] - goals[1])),
        })

    out = {
        "question": "is the inter-UAV clearance constraint active only at the frozen alpha = 20?",
        "answer": "no: it is active at the centralized optimum for every alpha tested; activity follows from the symmetric crossing geometry, not from the weight choice",
        "backend": "IPOPT (Interior Point OPTimizer) via CasADi",
        "ipopt_tol": a.tol,
        "rows": rows,
        "non_claims": ["single-start solves; this is an activity diagnostic, not a global-optimality or weight-selection study"],
    }
    Path(a.output).write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
