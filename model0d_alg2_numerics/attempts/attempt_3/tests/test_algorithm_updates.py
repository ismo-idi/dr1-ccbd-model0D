from pathlib import Path
import numpy as np
from src.config import load_config
from src.diagnostics import integrity_pass
from src.sunsun_algorithm2 import _a5_edge_update,_outer_parameter_update,_slack_dual_update
ROOT=Path(__file__).resolve().parents[1]
def test_a5_is_symmetric_average_then_a1_projection():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');Q=cfg.Q;u=_a5_edge_update(cfg,4.0,np.full(Q,5.0),np.full(Q,4.0),np.zeros(Q),np.zeros(Q),np.zeros(Q),np.zeros(Q));np.testing.assert_allclose(u,3.5)
def test_slack_dual_update_satisfies_exact_identity_numerically():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');rng=np.random.default_rng(20260911);lam=rng.normal(size=32);y0=rng.normal(size=32);c=rng.normal(size=32);xi,y=_slack_dual_update(lam,2.0,4.0,y0,c);np.testing.assert_allclose(lam+2.0*xi+y,0.0,atol=3e-15,rtol=0.0);ok,vals=integrity_pass(cfg,lam,2.0,xi,y,4.0);assert ok,vals
def test_first_penalty_rule_with_xi0_zero_is_preserved():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');lam=np.zeros(32);beta=2.0;xi0=np.zeros(32);_,bs,rs=_outer_parameter_update(cfg,lam,beta,np.zeros(32),xi0);assert bs==beta and rs==2*bs;xn=np.zeros(32);xn[0]=1e-12;_,bg,rg=_outer_parameter_update(cfg,lam,beta,xn,xi0);assert bg==cfg.a['vartheta']*beta and rg==2*bg
def test_outer_lambda_projection_uses_frozen_safeguard_box():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ln,_,_=_outer_parameter_update(cfg,np.full(32,99.0),2.0,np.full(32,10.0),np.ones(32)*100.0);np.testing.assert_allclose(ln,100.0)
