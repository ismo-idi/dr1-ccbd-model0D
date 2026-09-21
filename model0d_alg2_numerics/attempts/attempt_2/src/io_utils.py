"""Reproducible logging utilities for Model 0-D numerical runs."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any

import casadi
import matplotlib
import numpy
import scipy


APPROVED_EXECUTION_ENV = {
    "PYTHONHASHSEED": "0",
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
}


def validate_execution_environment() -> None:
    """Fail before an experiment if deterministic execution variables drift."""
    mismatches = []
    for key, expected in APPROVED_EXECUTION_ENV.items():
        actual = os.environ.get(key)
        if actual != expected:
            mismatches.append(f"{key}={actual!r}, expected {expected!r}")
    if mismatches:
        raise RuntimeError("Approved deterministic execution environment not active: " + "; ".join(mismatches))


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def environment_record() -> dict[str, Any]:
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": numpy.__version__,
        "scipy": scipy.__version__,
        "matplotlib": matplotlib.__version__,
        "casadi": casadi.__version__,
        "PYTHONHASHSEED": os.environ.get("PYTHONHASHSEED"),
        "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
        "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
        "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
    }


def _json_safe(value: Any) -> Any:
    """Convert non-finite numerical diagnostics to explicit categorical markers.

    Experiment logs must never contain JSON NaN/Infinity tokens. Those tokens are
    non-portable and, more importantly, would blur the distinction between an
    unavailable/failed numerical quantity and a genuine finite scalar.
    """
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, numpy.ndarray):
        return _json_safe(value.tolist())
    if isinstance(value, numpy.generic):
        return _json_safe(value.item())
    if isinstance(value, float):
        if numpy.isnan(value):
            return "NONFINITE_NAN"
        if numpy.isposinf(value):
            return "NONFINITE_POSITIVE_INFINITY"
        if numpy.isneginf(value):
            return "NONFINITE_NEGATIVE_INFINITY"
    return value


def write_json(path: str | Path, data: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(_json_safe(data), indent=2, sort_keys=True, allow_nan=False), encoding="utf-8")


def write_jsonl(path: str | Path, records: list[dict[str, Any]]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(_json_safe(record), sort_keys=True, allow_nan=False) + "\n")
