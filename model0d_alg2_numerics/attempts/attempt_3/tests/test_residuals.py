from pathlib import Path
import numpy as np
from src.config import load_config
from src.sunsun_algorithm2 import _residuals
from src.tcc import assemble_tcc
ROOT=Path(__file__).resolve().parents[1]
def test_R1_R2_peer_to_peer_match_matrix_forms():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);r=np.random.default_rng(20260911);v=_residuals(ops,4.,r.normal(size=ops.d1),r.normal(size=ops.d2),r.normal(size=ops.Q),r.normal(size=ops.Q),r.normal(size=ops.m),r.normal(size=ops.m));assert v['R1_crosscheck_abs']<=1e-12 and v['R2_crosscheck_abs']<=1e-12
def test_R3_is_complete_half_row_norm():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);r=np.random.default_rng(9);z1=r.normal(size=ops.d1);z2=r.normal(size=ops.d2);uo=r.normal(size=ops.Q);un=r.normal(size=ops.Q);xo=r.normal(size=ops.m);xn=r.normal(size=ops.m);v=_residuals(ops,4.,z1,z2,uo,un,xo,xn);np.testing.assert_allclose(v['R3'],np.linalg.norm(ops.target_rows(z1,z2,un)+xn),atol=1e-14,rtol=1e-14)
