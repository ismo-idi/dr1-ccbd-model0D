from pathlib import Path

from src.config import load_config
from src.sunsun_algorithm2 import _residual_crosscheck_pass

ROOT = Path(__file__).resolve().parents[1]


def test_residual_crosscheck_pass_and_failure():
    cfg = load_config(ROOT / "configs" / "baseline_2uav_0obs.json")
    good = {
        "R1": 2.0, "R1_matrix": 2.0, "R1_crosscheck_abs": 1e-15,
        "R2": 3.0, "R2_matrix": 3.0, "R2_crosscheck_abs": 1e-15,
    }
    ok, _ = _residual_crosscheck_pass(cfg, good)
    assert ok
    bad = dict(good)
    bad["R1_crosscheck_abs"] = 1e-5
    ok, _ = _residual_crosscheck_pass(cfg, bad)
    assert not ok
