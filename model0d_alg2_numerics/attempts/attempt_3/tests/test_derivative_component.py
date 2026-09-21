from pathlib import Path
import numpy as np
from src.config import load_config
from src.local_nlp import build_local_nlp
from src.tcc import assemble_tcc,stationary_exact_tcc_initialization
ROOT=Path(__file__).resolve().parents[1]
def _central_jac(fun,x,h=1e-6):
 x=np.asarray(x,float);f0=np.asarray(fun(x),float).reshape(-1);J=np.empty((f0.size,x.size))
 for j in range(x.size):
  xp=x.copy();xm=x.copy();xp[j]+=h;xm[j]-=h;J[:,j]=(np.asarray(fun(xp),float).reshape(-1)-np.asarray(fun(xm),float).reshape(-1))/(2*h)
 return J
def _central_grad(fun,x,h=1e-6):
 x=np.asarray(x,float);g=np.empty(x.size)
 for j in range(x.size):
  xp=x.copy();xm=x.copy();xp[j]+=h;xm[j]-=h;g[j]=(float(fun(xp))-float(fun(xm)))/(2*h)
 return g
def test_non_switching_local_jacobian_and_phi_gradient_match_finite_differences():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);local=build_local_nlp(1,cfg,ops);z1,_,u=stationary_exact_tcc_initialization(cfg,ops);P1=np.column_stack([np.linspace(-1.9,-1.2,cfg.K),np.zeros(cfg.K)]);z=z1.copy();z[:cfg.Q]=P1.reshape(-1);assert np.max(np.abs(local.eval_jac(z)-_central_jac(local.eval_g,z)))<=2e-6;xi=np.zeros(cfg.Q);y=np.zeros(cfg.Q);rho=4.0;assert np.max(np.abs(local.eval_grad_phi(z,u,xi,y,rho)-_central_grad(lambda zz:local.eval_phi(zz,u,xi,y,rho),z)))<=2e-5
