#!/usr/bin/env python3
"""Independent verifier for Attempt 2A of the 2-UAV/0-obstacle baseline.

This script deliberately does not import the solver implementation.  It reads
only persisted JSON/NPZ artifacts and recomputes the source objective, TCC
residuals, physical margins, guardian-copy safety, algebraic identity, and
cross-run reproducibility with NumPy/Python.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def trajectory(start: list[float], flat: np.ndarray, K: int, q: int) -> np.ndarray:
    return np.vstack([np.asarray(start, dtype=float), np.asarray(flat, dtype=float).reshape(K, q)])


def segment_relative_min(P: np.ndarray, Q: np.ndarray, clearance: float) -> list[dict[str, float | int]]:
    out = []
    for k in range(len(P) - 1):
        a = P[k] - Q[k]
        b = P[k + 1] - Q[k + 1]
        d = b - a
        s = float(np.dot(d, d))
        lam = 0.0 if s == 0.0 else float(np.clip(-np.dot(a, d) / s, 0.0, 1.0))
        dist = float(np.linalg.norm(a + lam * d))
        out.append({"k": k, "lambda": lam, "distance": dist, "margin": dist - clearance})
    return out


def recompute(config: dict[str, Any], run_dir: Path) -> dict[str, Any]:
    m = config["model"]
    K, q = int(m["K"]), int(m["q"])
    Q = K * q
    state = np.load(run_dir / "final_state.npz")
    z1, z2 = state["z1"].astype(float), state["z2"].astype(float)
    u = state["u"].astype(float)
    xi, y, lam = state["xi"].astype(float), state["y"].astype(float), state["lambda_outer"].astype(float)
    beta, rho = float(state["beta"][0]), float(state["rho"][0])
    p1 = trajectory(m["starts"][0], z1[:Q], K, q)
    p2 = trajectory(m["starts"][1], z2[:Q], K, q)
    copy2 = trajectory(m["starts"][1], z1[Q:2*Q], K, q)

    alpha = np.asarray(m["alpha"], float)
    beta_obj = np.asarray(m["beta_obj"], float)
    goals = np.asarray(m["goals"], float)
    objective = {}
    vals = []
    for i, P in enumerate((p1, p2)):
        terminal = float(alpha[i] * np.dot(P[-1]-goals[i], P[-1]-goals[i]))
        step = float(beta_obj[i] * np.sum(np.diff(P, axis=0)**2))
        vals.append(terminal + step)
        objective[f"terminal_tracking_term_{i+1}"] = terminal
        objective[f"step_regularization_term_{i+1}"] = step
        objective[f"goal_error_{i+1}"] = float(np.linalg.norm(P[-1]-goals[i]))
    objective.update({"f1": vals[0], "f2": vals[1], "F": sum(vals)})

    direct = copy2[1:].reshape(-1) - p2[1:].reshape(-1)
    target = np.concatenate([copy2[1:].reshape(-1)-u, p2[1:].reshape(-1)-u])

    lo, hi = np.asarray(m["workspace_lower"], float), np.asarray(m["workspace_upper"], float)
    vmax, dt = np.asarray(m["vmax"], float), float(m["dt"])
    W, spd = [], []
    for i, P in enumerate((p1,p2)):
        for k in range(1,K+1):
            W.extend((hi-P[k]).tolist()); W.extend((P[k]-lo).tolist())
        for k in range(K):
            spd.append(float(vmax[i]*dt - np.linalg.norm(P[k+1]-P[k])))
    clearance = float(m["radii"][0] + m["radii"][1] + m["delta_uav"])
    source_pair = segment_relative_min(p1,p2,clearance)
    guardian_pair = segment_relative_min(p1,copy2,clearance)
    source_min = min(source_pair, key=lambda x: x["margin"])
    guardian_min = min(guardian_pair, key=lambda x: x["margin"])

    summary = read_json(run_dir / "summary.json")
    events = [json.loads(line) for line in (run_dir/"events.jsonl").read_text(encoding="utf-8").splitlines()]
    inner = [e for e in events if e.get("phase") == "inner_complete"]
    last = inner[-1]
    t17 = next(e for e in inner if e["r"] == 1 and e["t"] == 17)
    t17o1 = next(o for o in t17["oracles"] if o["agent"] == 1)

    independent = {
        "termination_reason": summary["termination_reason"],
        "primary_cause": summary["primary_cause"],
        "all_causes": summary["all_causes"],
        "last_complete_outer_r": int(state["outer_r"][0]),
        "last_complete_inner_t": int(state["inner_t"][0]),
        "inner_complete_count": len(inner),
        "objective": objective,
        "tcc": {"R_TCC_eq": float(np.linalg.norm(direct)), "R_target": float(np.linalg.norm(target))},
        "integrity": {"R_id": float(np.linalg.norm(lam + beta*xi + y)), "R_rhobeta": float(abs(rho-2*beta))},
        "physical": {
            "workspace_min_margin": float(min(W)),
            "speed_min_margin": float(min(spd)),
            "uav_source_min": source_min,
            "guardian_source1_copy2_min": guardian_min,
            "uav_clearance": clearance,
            "obstacle_family_cardinality": 0,
        },
        "last_inner_residuals": {k: float(last["residuals"][k]) for k in ("R1","R2","R3")},
        "attempt1_failure_row_replayed_at_t17": {
            "row": 30,
            "raw_backend_mu": float(t17o1["raw_mu_backend"][30]),
            "diagnostic_mu": float(t17o1["diagnostic_mu"][30]),
            "g": float(t17o1["raw_g"][30]),
            "row_zeroed": bool(30 in t17o1.get("inactive_zeroed_rows", [])),
            "agent1_accepted": bool(t17o1["accepted"]),
            "R_dual_normalized": float(t17o1["R_dual_normalized"]),
            "R_comp": float(t17o1["R_comp"]),
            "R_stat_normalized": float(t17o1["R_stat_normalized"]),
        },
    }

    rep = summary["final_metrics"]
    checks = {
        "F": abs(independent["objective"]["F"] - rep["objective"]["F"]),
        "R_TCC_eq": abs(independent["tcc"]["R_TCC_eq"] - rep["tcc"]["R_TCC_eq"]),
        "R_target": abs(independent["tcc"]["R_target"] - rep["tcc"]["R_target"]),
        "R_id": abs(independent["integrity"]["R_id"] - rep["integrity"]["R_id"]),
        "workspace_min": abs(independent["physical"]["workspace_min_margin"] - rep["physical"]["families"]["W"]["minimum_margin"]),
        "speed_min": abs(independent["physical"]["speed_min_margin"] - rep["physical"]["families"]["spd"]["minimum_margin"]),
        "uav_min": abs(independent["physical"]["uav_source_min"]["margin"] - rep["physical"]["families"]["uav"]["minimum_margin"]),
    }
    independent["reported_crosscheck_absolute_errors"] = checks
    independent["reported_crosscheck_pass_1e-12"] = bool(max(checks.values()) <= 1e-12)
    return independent


def sanitized(obj: Any, key: str | None = None) -> Any:
    # Remove nondeterministic timing only. Keep every scientific/numerical value.
    if isinstance(obj, dict):
        return {k: sanitized(v,k) for k,v in obj.items() if k not in {"elapsed_s", "backend_elapsed_s"}}
    if isinstance(obj, list):
        return [sanitized(v,key) for v in obj]
    return obj


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--config', type=Path, required=True)
    ap.add_argument('--run1', type=Path, required=True)
    ap.add_argument('--run2', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    args=ap.parse_args(); args.output_dir.mkdir(parents=True, exist_ok=True)
    cfg=read_json(args.config)
    v1=recompute(cfg,args.run1); v2=recompute(cfg,args.run2)
    (args.output_dir/'independent_attempt2a_run1.json').write_text(json.dumps(v1,indent=2,sort_keys=True)+'\n')
    (args.output_dir/'independent_attempt2a_run2.json').write_text(json.dumps(v2,indent=2,sort_keys=True)+'\n')

    a=np.load(args.run1/'final_state.npz'); b=np.load(args.run2/'final_state.npz')
    arrays={}; exact_all=True; max_abs=0.0
    for k in a.files:
        exact=bool(np.array_equal(a[k],b[k])); diff=float(np.max(np.abs(a[k]-b[k]))) if a[k].size else 0.0
        arrays[k]={"exact_equal":exact,"max_abs_difference":diff}; exact_all &= exact; max_abs=max(max_abs,diff)
    s1=read_json(args.run1/'summary.json'); s2=read_json(args.run2/'summary.json')
    e1=[json.loads(x) for x in (args.run1/'events.jsonl').read_text().splitlines()]
    e2=[json.loads(x) for x in (args.run2/'events.jsonl').read_text().splitlines()]
    summary_equal = sanitized(s1) == sanitized(s2)
    events_equal = sanitized(e1) == sanitized(e2)
    repro={
        "termination_reason_equal": s1["termination_reason"]==s2["termination_reason"],
        "primary_cause_equal": s1["primary_cause"]==s2["primary_cause"],
        "all_causes_equal": s1["all_causes"]==s2["all_causes"],
        "sanitized_summary_exact_equal": summary_equal,
        "sanitized_event_history_exact_equal": events_equal,
        "final_state_arrays": arrays,
        "all_final_state_arrays_exact_equal": exact_all,
        "maximum_final_state_absolute_difference": max_abs,
        "protocol_repro_atol": cfg["thresholds"]["repro_atol"],
        "protocol_repro_rtol": cfg["thresholds"]["repro_rtol"],
        "reproducibility_pass": bool(exact_all and summary_equal and events_equal),
        "excluded_nondeterministic_fields": ["elapsed_s","backend_elapsed_s"],
    }
    (args.output_dir/'attempt2a_reproducibility.json').write_text(json.dumps(repro,indent=2,sort_keys=True)+'\n')
    print(json.dumps({"run1":v1,"reproducibility":repro},indent=2,sort_keys=True))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
