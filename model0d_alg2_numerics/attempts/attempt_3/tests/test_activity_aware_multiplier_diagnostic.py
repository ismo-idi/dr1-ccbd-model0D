from pathlib import Path
import numpy as np
from src.config import load_config
from src.diagnostics import local_oracle_diagnostics
from src.local_nlp import LocalSolveResult,build_local_nlp
from src.tcc import assemble_tcc,stationary_exact_tcc_initialization
ROOT=Path(__file__).resolve().parents[1]
def _synthetic_result(local,z,mu,phi,status='SYNTHETIC'): return LocalSolveResult(local.agent,np.asarray(z,float).copy(),np.asarray(mu,float).copy(),float(phi),True,status,0,0.0,{})
def test_strictly_inactive_workspace_negative_backend_multiplier_is_zeroed_only_for_diagnostic():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);local=build_local_nlp(2,cfg,ops);_,z2,u=stationary_exact_tcc_initialization(cfg,ops);xi=np.zeros(cfg.Q);y=np.zeros(cfg.Q);g=local.eval_g(z2);rows=[m.row for m in local.metas if m.family=='W' and g[m.row]<-1.0];assert rows;row=rows[0];mu=np.zeros(local.n_constraints);mu[row]=-1e-5;diag=local_oracle_diagnostics(local,_synthetic_result(local,z2,mu,local.eval_phi(z2,u,xi,y,4.0)),z2,u,xi,y,4.0);assert diag.raw_mu_backend[row]==-1e-5;assert diag.diagnostic_mu[row]==0.0;assert row in diag.inactive_zeroed_rows;assert diag.R_dual_normalized==0.0
def test_near_active_workspace_negative_multiplier_is_not_zeroed_and_still_fails_dual_sign_test():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);local=build_local_nlp(2,cfg,ops);_,z2,u=stationary_exact_tcc_initialization(cfg,ops);xi=np.zeros(cfg.Q);y=np.zeros(cfg.Q);z=z2.copy();z[0]=cfg.workspace_upper[0];g=local.eval_g(z);rows=[m.row for m in local.metas if m.family=='W' and abs(g[m.row])<1e-12];assert rows;row=rows[0];mu=np.zeros(local.n_constraints);mu[row]=-1e-5;diag=local_oracle_diagnostics(local,_synthetic_result(local,z,mu,local.eval_phi(z,u,xi,y,4.0)),z,u,xi,y,4.0);assert diag.diagnostic_mu[row]==-1e-5;assert row not in diag.inactive_zeroed_rows;assert diag.pass_dual is False;assert 'FIRST_BLOCK_ORACLE_FAILED' in diag.failure_codes
def test_activity_aware_zeroing_uses_existing_family_aware_buffer_without_retuning_thresholds():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');assert cfg.t['inactive_factor']==100.0;assert cfg.t['tau_W']==1e-8;assert cfg.t['dual_normalized']==1e-8;assert cfg.t['complementarity']==1e-6;assert cfg.t['stationarity_normalized']==1e-6
