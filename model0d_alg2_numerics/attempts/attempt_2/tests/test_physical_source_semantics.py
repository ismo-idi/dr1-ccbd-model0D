from pathlib import Path

import numpy as np

from src.config import load_config
from src.diagnostics import physical_postcheck_numeric
from src.tcc import assemble_tcc, stationary_exact_tcc_initialization

ROOT = Path(__file__).resolve().parents[1]


def test_physical_postcheck_uses_actual_source_trajectories_not_foreign_copy():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    ops = assemble_tcc(cfg)
    z1, z2, _ = stationary_exact_tcc_initialization(cfg, ops)
    baseline = physical_postcheck_numeric(cfg, ops, z1, z2)
    assert baseline["evaluation_complete"] is True
    # Corrupt only UAV1's foreign copy of source 2. Physical postcheck must not change.
    z1_bad_copy = z1.copy()
    z1_bad_copy[cfg.Q:] = np.tile(np.array([3.5, 3.5]), cfg.K)
    changed = physical_postcheck_numeric(cfg, ops, z1_bad_copy, z2)
    assert changed == baseline


def test_expected_physical_cardinalities_baseline():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    ops = assemble_tcc(cfg)
    z1, z2, _ = stationary_exact_tcc_initialization(cfg, ops)
    result = physical_postcheck_numeric(cfg, ops, z1, z2)
    assert result["expected_cardinality"] == {"W": 64, "spd": 16, "obs": 0, "uav": 8}
    assert result["evaluation_complete"] is True
