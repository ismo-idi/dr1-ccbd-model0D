#!/usr/bin/env python3
"""Independent Step-3 verifier for the frozen 2-UAV/0-obstacle baseline.

This deliberately does not import the solver implementation.  It reads only the
frozen JSON configuration and persisted run artifacts, recomputes the reported
source-trajectory objective, TCC residuals, integrity identity, physical margins,
and cross-run reproducibility with NumPy/Python.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _segment_min_distance(a: np.ndarray, b: np.ndarray) -> float:
    d = b - a
    s = float(np.dot(d, d))
    if s == 0.0:
        return float(np.linalg.norm(a))
    lam = float(np.clip(-np.dot(a, d) / s, 0.0, 1.0))
    return float(np.linalg.norm(a + lam * d))


def _trajectory(start: list[float], flat: np.ndarray, K: int, q: int) -> np.ndarray:
    return np.vstack([np.asarray(start, dtype=float), np.asarray(flat, dtype=float).reshape(K, q)])


def recompute_one(config: dict[str, Any], run_dir: Path) -> dict[str, Any]:
    m = config["model"]
    K, q = int(m["K"]), int(m["q"])
    Q = K * q
    state = np.load(run_dir / "final_state.npz")
    z1 = state["z1"].astype(float)
    z2 = state["z2"].astype(float)
    u = state["u"].astype(float)
    xi = state["xi"].astype(float)
    y = state["y"].astype(float)
    lam = state["lambda_outer"].astype(float)
    beta = float(state["beta"][0])
    rho = float(state["rho"][0])

    p1 = _trajectory(m["starts"][0], z1[:Q], K, q)
    p2 = _trajectory(m["starts"][1], z2[:Q], K, q)
    copy2 = _trajectory(m["starts"][1], z1[Q:2*Q], K, q)
    uP = u.reshape(K, q)

    alpha = np.asarray(m["alpha"], dtype=float)
    beta_obj = np.asarray(m["beta_obj"], dtype=float)
    goals = np.asarray(m["goals"], dtype=float)
    vals = []
    goal_errors = []
    step_sums = []
    for i, P in enumerate((p1, p2)):
        ge2 = float(np.dot(P[-1] - goals[i], P[-1] - goals[i]))
        ss = float(np.sum(np.diff(P, axis=0) ** 2))
        vals.append(float(alpha[i] * ge2 + beta_obj[i] * ss))
        goal_errors.append(float(np.sqrt(ge2)))
        step_sums.append(ss)

    direct_tcc = copy2[1:].reshape(-1) - p2[1:].reshape(-1)
    half1 = copy2[1:].reshape(-1) - u
    half2 = p2[1:].reshape(-1) - u
    target = np.concatenate([half1, half2])

    lo = np.asarray(m["workspace_lower"], dtype=float)
    hi = np.asarray(m["workspace_upper"], dtype=float)
    vmax = np.asarray(m["vmax"], dtype=float)
    dt = float(m["dt"])
    workspace_margins: list[float] = []
    speed_margins: list[float] = []
    for i, P in enumerate((p1, p2)):
        for k in range(1, K + 1):
            workspace_margins.extend((hi - P[k]).tolist())
            workspace_margins.extend((P[k] - lo).tolist())
        for k in range(K):
            speed_margins.append(float(vmax[i] * dt - np.linalg.norm(P[k+1] - P[k])))

    clearance = float(m["radii"][0] + m["radii"][1] + m["delta_uav"])
    uav_margins: list[float] = []
    for k in range(K):
        a0 = p1[k] - p2[k]
        a1 = p1[k+1] - p2[k+1]
        uav_margins.append(_segment_min_distance(a0, a1) - clearance)

    identity = float(np.linalg.norm(lam + beta * xi + y))
    rho_beta = float(abs(rho - 2.0 * beta))

    summary = _read_json(run_dir / "summary.json")
    events = [json.loads(x) for x in (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()]
    abort = next(e for e in events if e.get("phase") == "local_oracle_abort")
    oracle1 = next(o for o in abort["oracles"] if o["agent"] == 1)
    oracle2 = next(o for o in abort["oracles"] if o["agent"] == 2)

    independent = {
        "termination_reason": summary["termination_reason"],
        "primary_cause": summary["primary_cause"],
        "last_complete_outer_r": int(state["outer_r"][0]),
        "last_complete_inner_t": int(state["inner_t"][0]),
        "objective": {"f1": vals[0], "f2": vals[1], "F": sum(vals), "goal_error_1": goal_errors[0], "goal_error_2": goal_errors[1], "squared_step_sum_1": step_sums[0], "squared_step_sum_2": step_sums[1]},
        "tcc": {"R_TCC_eq": float(np.linalg.norm(direct_tcc)), "R_target": float(np.linalg.norm(target))},
        "integrity": {"R_id": identity, "R_rhobeta": rho_beta},
        "physical_margins": {
            "workspace_min": float(min(workspace_margins)),
            "speed_min": float(min(speed_margins)),
            "obstacle_family_cardinality": 0,
            "uav_min": float(min(uav_margins)),
            "workspace_count": len(workspace_margins),
            "speed_count": len(speed_margins),
            "uav_count": len(uav_margins),
        },
        "failure": {
            "r": int(abort["r"]), "t": int(abort["t"]),
            "agent1": {k: oracle1[k] for k in ["backend_status","backend_success","backend_iterations","R_dual_normalized","R_comp","R_stat_normalized","R_desc","pass_dual","pass_comp","pass_stat","pass_desc","accepted","failure_codes"]},
            "agent2": {k: oracle2[k] for k in ["backend_status","backend_success","backend_iterations","R_dual_normalized","R_comp","R_stat_normalized","R_desc","pass_dual","pass_comp","pass_stat","pass_desc","accepted","failure_codes"]},
        },
    }

    # Compare key independently recomputed numbers to the persisted report.
    rep = summary["final_metrics"]
    checks = {
        "F": abs(independent["objective"]["F"] - rep["objective"]["F"]),
        "R_TCC_eq": abs(independent["tcc"]["R_TCC_eq"] - rep["tcc"]["R_TCC_eq"]),
        "R_target": abs(independent["tcc"]["R_target"] - rep["tcc"]["R_target"]),
        "R_id": abs(identity - rep["integrity"]["R_id"]),
        "R_rhobeta": abs(rho_beta - rep["integrity"]["R_rhobeta"]),
        "workspace_min": abs(independent["physical_margins"]["workspace_min"] - rep["physical"]["families"]["W"]["minimum_margin"]),
        "speed_min": abs(independent["physical_margins"]["speed_min"] - rep["physical"]["families"]["spd"]["minimum_margin"]),
        "uav_min": abs(independent["physical_margins"]["uav_min"] - rep["physical"]["families"]["uav"]["minimum_margin"]),
    }
    independent["reported_crosscheck_absolute_errors"] = checks
    independent["reported_crosscheck_pass_1e-12"] = bool(max(checks.values()) <= 1e-12)
    return independent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--run1", required=True, type=Path)
    ap.add_argument("--run2", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    cfg = _read_json(args.config)
    v1 = recompute_one(cfg, args.run1)
    v2 = recompute_one(cfg, args.run2)
    (out / "independent_run1_verification.json").write_text(json.dumps(v1, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "independent_run2_verification.json").write_text(json.dumps(v2, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    a = np.load(args.run1 / "final_state.npz")
    b = np.load(args.run2 / "final_state.npz")
    arrays = {}
    all_exact = True
    max_abs = 0.0
    for key in a.files:
        exact = bool(np.array_equal(a[key], b[key]))
        d = float(np.max(np.abs(a[key] - b[key]))) if a[key].size else 0.0
        arrays[key] = {"exact_equal": exact, "max_abs_difference": d}
        all_exact = all_exact and exact
        max_abs = max(max_abs, d)
    s1 = _read_json(args.run1 / "summary.json")
    s2 = _read_json(args.run2 / "summary.json")
    repro = {
        "termination_reason_equal": s1["termination_reason"] == s2["termination_reason"],
        "primary_cause_equal": s1["primary_cause"] == s2["primary_cause"],
        "all_causes_equal": s1["all_causes"] == s2["all_causes"],
        "final_state_arrays": arrays,
        "all_final_state_arrays_exact_equal": all_exact,
        "maximum_final_state_absolute_difference": max_abs,
        "protocol_repro_atol": cfg["thresholds"]["repro_atol"],
        "protocol_repro_rtol": cfg["thresholds"]["repro_rtol"],
        "reproducibility_pass": bool(all_exact and s1["termination_reason"] == s2["termination_reason"] and s1["primary_cause"] == s2["primary_cause"] and s1["all_causes"] == s2["all_causes"]),
        "note": "Wall-clock/backend elapsed times are intentionally excluded from deterministic equality requirements.",
    }
    (out / "reproducibility_comparison.json").write_text(json.dumps(repro, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Compact inner-iteration CSV from run1.
    events = [json.loads(x) for x in (args.run1 / "events.jsonl").read_text(encoding="utf-8").splitlines()]
    with (out / "inner_iteration_metrics_run1.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["r","t","R1","R2","R3","a1_R_dual_norm","a1_R_comp","a1_R_stat_norm","a2_R_dual_norm","a2_R_comp","a2_R_stat_norm"])
        for e in events:
            if e.get("phase") != "inner_complete":
                continue
            o1, o2 = e["oracles"]
            res=e["residuals"]
            w.writerow([e["r"],e["t"],res["R1"],res["R2"],res["R3"],o1["R_dual_normalized"],o1["R_comp"],o1["R_stat_normalized"],o2["R_dual_normalized"],o2["R_comp"],o2["R_stat_normalized"]])

    print(json.dumps({"run1": v1, "repro": repro}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
