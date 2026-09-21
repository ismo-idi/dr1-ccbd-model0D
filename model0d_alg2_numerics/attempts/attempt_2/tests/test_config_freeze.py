import copy
import json
from pathlib import Path

import pytest

from src.config import ConfigurationError, ModelConfig, load_config, validate_frozen_2uav_protocol

ROOT = Path(__file__).resolve().parents[1]


def test_both_approved_configs_pass_exact_freeze():
    base = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    obs = load_config(ROOT / "configs" / "obstacle_2uav_1obs.json")
    assert base.raw["scenario_id"] == "baseline_2uav_0obs"
    assert obs.raw["scenario_id"] == "obstacle_2uav_1obs"
    assert base.obstacles == []
    assert obs.obstacles == [{"center": [1.0, 0.0], "radius": 0.35}]


def test_protocol_threshold_drift_is_rejected():
    raw = json.loads((ROOT / "configs" / "baseline_2uav_0obs.json").read_text())
    raw["thresholds"]["tcc_eq"] = 1e-4
    with pytest.raises(ConfigurationError, match="tcc_eq"):
        validate_frozen_2uav_protocol(ModelConfig(raw))


def test_scenario_data_drift_is_rejected():
    raw = json.loads((ROOT / "configs" / "baseline_2uav_0obs.json").read_text())
    raw["model"]["goals"][0][0] = 1.9
    with pytest.raises(ConfigurationError, match="goals"):
        validate_frozen_2uav_protocol(ModelConfig(raw))


def test_unapproved_scenario_is_rejected():
    raw = json.loads((ROOT / "configs" / "baseline_2uav_0obs.json").read_text())
    raw["scenario_id"] = "unapproved"
    with pytest.raises(ConfigurationError, match="outside the approved bounded campaign"):
        validate_frozen_2uav_protocol(ModelConfig(raw))
