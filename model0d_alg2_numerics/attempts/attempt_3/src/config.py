"""Configuration loading and frozen-protocol validation for Model 0-D numerics."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


class ConfigurationError(ValueError):
    pass


@dataclass(frozen=True)
class ModelConfig:
    raw: dict[str, Any]

    @property
    def m(self):
        return self.raw["model"]

    @property
    def a(self):
        return self.raw["algorithm"]

    @property
    def t(self):
        return self.raw["thresholds"]

    @property
    def b(self):
        return self.raw["backend"]

    @property
    def N(self) -> int:
        return int(self.m["N"])

    @property
    def q(self) -> int:
        return int(self.m["q"])

    @property
    def K(self) -> int:
        return int(self.m["K"])

    @property
    def Q(self) -> int:
        return self.q * self.K

    @property
    def dt(self) -> float:
        return float(self.m["dt"])

    @property
    def starts(self) -> np.ndarray:
        return np.asarray(self.m["starts"], dtype=float)

    @property
    def goals(self) -> np.ndarray:
        return np.asarray(self.m["goals"], dtype=float)

    @property
    def radii(self) -> np.ndarray:
        return np.asarray(self.m["radii"], dtype=float)

    @property
    def vmax(self) -> np.ndarray:
        return np.asarray(self.m["vmax"], dtype=float)

    @property
    def alpha(self) -> np.ndarray:
        return np.asarray(self.m["alpha"], dtype=float)

    @property
    def beta_obj(self) -> np.ndarray:
        return np.asarray(self.m["beta_obj"], dtype=float)

    @property
    def workspace_lower(self) -> np.ndarray:
        return np.asarray(self.m["workspace_lower"], dtype=float)

    @property
    def workspace_upper(self) -> np.ndarray:
        return np.asarray(self.m["workspace_upper"], dtype=float)

    @property
    def a1_lower(self) -> np.ndarray:
        return np.asarray(self.m["a1_lower"], dtype=float)

    @property
    def a1_upper(self) -> np.ndarray:
        return np.asarray(self.m["a1_upper"], dtype=float)

    @property
    def delta_uav(self) -> float:
        return float(self.m["delta_uav"])

    @property
    def delta_obs(self) -> np.ndarray:
        return np.asarray(self.m["delta_obs"], dtype=float)

    @property
    def obstacles(self) -> list[dict[str, Any]]:
        return list(self.m["obstacles"])

    @property
    def uav_clearance(self) -> float:
        return float(self.radii[0] + self.radii[1] + self.delta_uav)

    def obstacle_clearance(self, i: int, obstacle: dict[str, Any]) -> float:
        return float(obstacle["radius"] + self.radii[i] + self.delta_obs[i])


# Researcher-approved protocol v1.0, 11 September 2026.
# These are experiment-wrapper constants, deliberately locked before outcome inspection.
_FROZEN_COMMON: dict[str, Any] = {
    "schema_version": "1.0",
    "repository_branch": "Model-0_24-Aug-2026",
    "implementation_base_commit": "de49211ddd924e4751b7303ec3f1f2949b16bb23",
    "protocol_file": "MODEL0D_NUMERICAL_PROTOCOL_AND_READINESS_V1_0_11_SEP_2026.md",
    "seed": 20260911,
    "model": {
        "N": 2,
        "q": 2,
        "K": 8,
        "dt": 0.5,
        "workspace_lower": [-3.0, -3.0],
        "workspace_upper": [3.0, 3.0],
        "a1_lower": [-3.5, -3.5],
        "a1_upper": [3.5, 3.5],
        "starts": [[-2.0, 0.0], [0.0, -2.0]],
        "goals": [[2.0, 0.0], [0.0, 2.0]],
        "radii": [0.1, 0.1],
        "vmax": [1.5, 1.5],
        "alpha": [20.0, 20.0],
        "beta_obj": [1.0, 1.0],
        "delta_uav": 0.2,
        "delta_obs": [0.1, 0.1],
    },
    "tcc": {
        "guardian_pair_1_2": 1,
        "source_2_copy_holders": [1, 2],
        "source_2_equality_edge": [1, 2],
        "reduction_tree_edge": [1, 2],
    },
    "algorithm": {
        "beta0": 1.0,
        "vartheta": 2.0,
        "omega": 0.5,
        "lambda_initial": 0.0,
        "lambda_lower": -100.0,
        "lambda_upper": 100.0,
        "eps1_scale": 0.0001,
        "eps2_scale": 0.0001,
        "eps3_scale": 0.000001,
        "max_outer_iterations": 20,
        "max_inner_iterations": 1000,
        "wall_clock_cap_s": 600.0,
        "retry_count": 0,
    },
    "backend": {
        "name": "casadi_ipopt",
        "ipopt.tol": 1e-9,
        "ipopt.constr_viol_tol": 1e-9,
        "ipopt.dual_inf_tol": 1e-8,
        "ipopt.compl_inf_tol": 1e-8,
        "ipopt.max_iter": 500,
        "ipopt.acceptable_iter": 0,
        "ipopt.hessian_approximation": "limited-memory",
        "ipopt.bound_relax_factor": 0.0,
        "ipopt.print_level": 0,
        "print_time": False,
    },
    "thresholds": {
        "tau_W": 1e-8,
        "tau_spd": 1e-8,
        "tau_obs": 1e-8,
        "tau_uav": 1e-8,
        "tau_A1": 1e-8,
        "tau_s": 1e-12,
        "inactive_factor": 100.0,
        "near_factor": 10.0,
        "dual_normalized": 1e-8,
        "complementarity": 1e-6,
        "stationarity_normalized": 1e-6,
        "descent_relative": 1e-10,
        "integrity_relative": 1e-12,
        "tcc_eq": 1e-6,
        "target": 1e-6,
        "physical_numeric_margin": 1e-7,
        "outer_xi": 1e-6,
        "repro_atol": 1e-10,
        "repro_rtol": 1e-10,
    },
}

_FROZEN_OBSTACLES: dict[str, list[dict[str, Any]]] = {
    "baseline_2uav_0obs": [],
    "obstacle_2uav_1obs": [{"center": [1.0, 0.0], "radius": 0.35}],
}


def _compare_exact(actual: Any, expected: Any, path: str, errors: list[str]) -> None:
    """Recursively compare protocol-controlled values without tolerance retuning."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            errors.append(f"{path} must be an object")
            return
        for key, exp in expected.items():
            if key not in actual:
                errors.append(f"{path}.{key} missing")
            else:
                _compare_exact(actual[key], exp, f"{path}.{key}", errors)
        return
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            errors.append(f"{path} must equal {expected!r}")
            return
        for idx, (act, exp) in enumerate(zip(actual, expected, strict=True)):
            _compare_exact(act, exp, f"{path}[{idx}]", errors)
        return
    # JSON number equality is intentional here: these values are the frozen protocol literals.
    if actual != expected:
        errors.append(f"{path}={actual!r}, expected frozen value {expected!r}")


def load_config(path: str | Path) -> ModelConfig:
    p = Path(path)
    raw = json.loads(p.read_text(encoding="utf-8"))
    cfg = ModelConfig(raw)
    validate_frozen_2uav_protocol(cfg)
    return cfg


def validate_frozen_2uav_protocol(cfg: ModelConfig) -> None:
    """Reject silent drift from every researcher-approved bounded-campaign setting."""
    errors: list[str] = []
    raw = cfg.raw
    scenario_id = raw.get("scenario_id")
    if scenario_id not in _FROZEN_OBSTACLES:
        errors.append(f"scenario_id {scenario_id!r} is outside the approved bounded campaign")
    _compare_exact(raw, {k: v for k, v in _FROZEN_COMMON.items() if k != "model"}, "config", errors)

    if not isinstance(raw.get("model"), dict):
        errors.append("config.model must be an object")
    else:
        expected_model = dict(_FROZEN_COMMON["model"])
        if scenario_id in _FROZEN_OBSTACLES:
            expected_model["obstacles"] = _FROZEN_OBSTACLES[scenario_id]
        _compare_exact(raw["model"], expected_model, "config.model", errors)

    # Redundant semantic checks retained for readable failure diagnosis.
    if raw.get("model"):
        if not np.all(cfg.workspace_lower < cfg.workspace_upper):
            errors.append("workspace bounds invalid")
        if not np.all(cfg.a1_lower < cfg.workspace_lower) or not np.all(cfg.workspace_upper < cfg.a1_upper):
            errors.append("A1 box must strictly contain workspace")
        if float(cfg.a["beta0"]) < 0.25:
            errors.append("beta0 must be >=1/4")
        if float(cfg.a["vartheta"]) <= 1.0:
            errors.append("vartheta must be >1")
        if not (0.0 <= float(cfg.a["omega"]) < 1.0):
            errors.append("omega must lie in [0,1)")
        if not (float(cfg.a["lambda_lower"]) < float(cfg.a["lambda_upper"])):
            errors.append("lambda safeguard box invalid")

    if errors:
        raise ConfigurationError("; ".join(errors))
