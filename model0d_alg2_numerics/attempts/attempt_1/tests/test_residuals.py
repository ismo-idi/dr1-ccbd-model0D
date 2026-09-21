from pathlib import Path
import numpy as np

from src.config import load_config
from src.sunsun_algorithm2 import _residuals
from src.tcc import assemble_tcc

ROOT = Path(__file__).resolve().parents[1]


def test_R1_R2_peer_to_peer_match_matrix_forms():
    cfg = load_config(ROOT / 'configs' / 'baseline_2uav_0obs.json')
    ops = assemble_tcc(cfg)
    rng = np.random.default_rng(20260911)
    z1 = rng.normal(size=ops.d1)
    z2 = rng.normal(size=ops.d2)
    u_old = rng.normal(size=ops.Q)
    u_new = rng.normal(size=ops.Q)
    xi_old = rng.normal(size=ops.m)
    xi_new = rng.normal(size=ops.m)
    vals = _residuals(ops, 4.0, z1, z2, u_old, u_new, xi_old, xi_new)
    assert vals['R1_crosscheck_abs'] <= 1e-12
    assert vals['R2_crosscheck_abs'] <= 1e-12


def test_R3_is_complete_half_row_norm():
    cfg = load_config(ROOT / 'configs' / 'baseline_2uav_0obs.json')
    ops = assemble_tcc(cfg)
    rng = np.random.default_rng(9)
    z1 = rng.normal(size=ops.d1)
    z2 = rng.normal(size=ops.d2)
    u_old = rng.normal(size=ops.Q)
    u_new = rng.normal(size=ops.Q)
    xi_old = rng.normal(size=ops.m)
    xi_new = rng.normal(size=ops.m)
    vals = _residuals(ops, 4.0, z1, z2, u_old, u_new, xi_old, xi_new)
    expected = np.linalg.norm(ops.target_rows(z1, z2, u_new) + xi_new)
    np.testing.assert_allclose(vals['R3'], expected, atol=1e-14, rtol=1e-14)
