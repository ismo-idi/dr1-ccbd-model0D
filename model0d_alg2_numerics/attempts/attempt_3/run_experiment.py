#!/usr/bin/env python3
"""Run one approved Model 0-D Algorithm-2 configuration.

This executable is implemented in Step 1 but must not be invoked on the
baseline until the mandatory Step-2 component verification passes.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np

from src.config import load_config
from src.io_utils import environment_record, sha256_file, validate_execution_environment, write_json, write_jsonl
from src.sunsun_algorithm2 import run_algorithm2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    cfg_path = Path(args.config).resolve()
    out = Path(args.output).resolve()

    # Validate the frozen protocol and deterministic process environment before
    # creating any experimental output directory.
    cfg = load_config(cfg_path)
    validate_execution_environment()
    out.mkdir(parents=True, exist_ok=False)
    write_json(out / "config.json", cfg.raw)
    env = environment_record()
    env["config_sha256"] = sha256_file(cfg_path)
    package_root = Path(__file__).resolve().parent
    implementation_files = [package_root / "run_experiment.py"] + sorted((package_root / "src").glob("*.py"))
    env["implementation_files_sha256"] = {
        str(path.relative_to(package_root)): sha256_file(path) for path in implementation_files
    }
    write_json(out / "environment.json", env)

    result = run_algorithm2(cfg)
    write_jsonl(out / "events.jsonl", result.history)
    write_json(out / "summary.json", result.to_serializable())
    if result.state is not None:
        np.savez_compressed(
            out / "final_state.npz",
            z1=result.state.z1,
            z2=result.state.z2,
            u=result.state.u,
            xi=result.state.xi,
            y=result.state.y,
            lambda_outer=result.state.lambda_outer,
            beta=np.array([result.state.beta]),
            rho=np.array([result.state.rho]),
            outer_r=np.array([result.state.outer_r]),
            inner_t=np.array([result.state.inner_t]),
        )

    print(json.dumps({
        "scenario_id": result.scenario_id,
        "termination_reason": result.termination_reason,
        "primary_cause": result.primary_cause,
        "all_causes": result.all_causes,
        "elapsed_s": result.elapsed_s,
        "output": str(out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
