from pathlib import Path
import numpy as np
from src.config import load_config
from src.tcc import assemble_tcc
ROOT=Path(__file__).resolve().parents[1]
def test_BtB_and_exact_split_elimination():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);np.testing.assert_allclose(ops.B.T@ops.B,2.*np.eye(cfg.Q));r=np.random.default_rng(20260911);s=r.normal(size=cfg.Q);z1=np.concatenate([r.normal(size=cfg.Q),s.copy()]);z2=s.copy();u=s.copy();np.testing.assert_allclose(ops.target_rows(z1,z2,u),0.);np.testing.assert_allclose(ops.direct_tcc_difference(z1,z2),0.)
