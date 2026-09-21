import json
from pathlib import Path
import numpy as np
import src.sunsun_algorithm2 as alg
from src.config import ModelConfig
from src.diagnostics import LocalOracleDiagnostics
from src.local_nlp import LocalSolveResult
ROOT=Path(__file__).resolve().parents[1]
class FakeLocal:
 def __init__(self,agent,cfg,ops):self.agent=agent;self.cfg=cfg;self.ops=ops;self.n_constraints=1
 def solve(self,z0,u_old,xi_old_half,y_old_half,rho):return LocalSolveResult(self.agent,np.asarray(z0,float).copy(),np.zeros(1),0.0,True,'SYNTHETIC_OK',0,0.0,{})
 def eval_source_objective(self,z):return 0.0
def _diag(agent,accepted=True,code=None):return LocalOracleDiagnostics(agent,True,'SYNTHETIC',0,0.0,True,0.0,1e-12,True,{}, {},[],[],True,[],[],[],{},[],{},[],[],0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,True,True,True,accepted,code,[] if code is None else [code])
def _cfg_with_caps(max_outer=1,max_inner=1):
 r=json.loads((ROOT/'configs'/'baseline_2uav_0obs.json').read_text());r['algorithm']['max_outer_iterations']=max_outer;r['algorithm']['max_inner_iterations']=max_inner;return ModelConfig(r)
def _install_fake_locals(monkeypatch):monkeypatch.setattr(alg,'build_local_nlp',lambda agent,cfg,ops:FakeLocal(agent,cfg,ops))
def _zero_res(*a,**k):return {'R1':0.0,'R2':0.0,'R3':0.0,'R1_matrix':0.0,'R2_matrix':0.0,'R1_crosscheck_abs':0.0,'R2_crosscheck_abs':0.0}
def test_common_local_oracle_abort_occurs_before_a5(monkeypatch):
 cfg=_cfg_with_caps();_install_fake_locals(monkeypatch);calls={'diag':0}
 def fd(local,result,*a,**k):calls['diag']+=1;return _diag(local.agent,local.agent==2,None if local.agent==2 else 'FIRST_BLOCK_ORACLE_FAILED')
 monkeypatch.setattr(alg,'local_oracle_diagnostics',fd);monkeypatch.setattr(alg,'_a5_edge_update',lambda *a,**k:(_ for _ in ()).throw(AssertionError('A5 must not run')));r=alg.run_algorithm2(cfg);assert calls['diag']==2 and r.termination_reason=='LOCAL_ORACLE_ABORT' and r.primary_cause=='FIRST_BLOCK_ORACLE_FAILED';assert r.state.outer_r==0 and r.state.inner_t==0
def test_success_on_final_permitted_inner_iteration_is_not_inner_cap_exhaustion(monkeypatch):
 cfg=_cfg_with_caps();_install_fake_locals(monkeypatch);monkeypatch.setattr(alg,'local_oracle_diagnostics',lambda local,result,*a,**k:_diag(local.agent));monkeypatch.setattr(alg,'_residuals',_zero_res);monkeypatch.setattr(alg,'_outer_stop_predicate',lambda *a,**k:False);r=alg.run_algorithm2(cfg);assert r.termination_reason=='MAX_OUTER_ITERATIONS' and 'MAX_INNER_ITERATIONS' not in r.all_causes and r.state.inner_t==1
def test_inner_cap_exhaustion_returns_last_complete_inner_snapshot(monkeypatch):
 cfg=_cfg_with_caps();_install_fake_locals(monkeypatch);monkeypatch.setattr(alg,'local_oracle_diagnostics',lambda local,result,*a,**k:_diag(local.agent));monkeypatch.setattr(alg,'_residuals',lambda *a,**k:{'R1':1.,'R2':1.,'R3':1.,'R1_matrix':1.,'R2_matrix':1.,'R1_crosscheck_abs':0.,'R2_crosscheck_abs':0.});r=alg.run_algorithm2(cfg);assert r.termination_reason=='MAX_INNER_ITERATIONS' and r.primary_cause=='MAX_INNER_ITERATIONS' and r.state.inner_t==1
def test_nonfinite_update_is_explicit_failure_and_not_accepted_state(monkeypatch):
 cfg=_cfg_with_caps();_install_fake_locals(monkeypatch);monkeypatch.setattr(alg,'local_oracle_diagnostics',lambda local,result,*a,**k:_diag(local.agent));monkeypatch.setattr(alg,'_a5_edge_update',lambda cfg,rho,*a,**k:np.full(cfg.Q,np.nan));r=alg.run_algorithm2(cfg);assert r.termination_reason=='UPDATE_ABORT' and r.primary_cause=='NUMERICAL_NAN_INF' and r.state.inner_t==0
def test_backend_construction_failure_uses_common_finalization(monkeypatch):
 cfg=_cfg_with_caps();monkeypatch.setattr(alg,'build_local_nlp',lambda *a,**k:(_ for _ in ()).throw(RuntimeError('x')));r=alg.run_algorithm2(cfg);assert r.termination_reason=='SOLVER_BACKEND_FAILURE' and r.history[-1]['phase']=='finalization'
def test_input_admissibility_failure_uses_common_finalization(monkeypatch):
 cfg=_cfg_with_caps();cfg.raw['model']['starts'][0]=[99.,99.];_install_fake_locals(monkeypatch);r=alg.run_algorithm2(cfg);assert r.termination_reason=='INPUT_ADMISSIBILITY_FAILED' and r.history[-1]['phase']=='finalization'
def test_timeout_uses_common_finalization(monkeypatch):
 cfg=_cfg_with_caps();cfg.raw['algorithm']['wall_clock_cap_s']=-1.;_install_fake_locals(monkeypatch);r=alg.run_algorithm2(cfg);assert r.termination_reason=='TIMEOUT' and 'TIMEOUT' in r.all_causes
def test_initialization_integrity_failure_uses_common_finalization(monkeypatch):
 cfg=_cfg_with_caps();_install_fake_locals(monkeypatch);monkeypatch.setattr(alg,'integrity_pass',lambda *a,**k:(False,{'x':1.}));r=alg.run_algorithm2(cfg);assert r.termination_reason=='INITIALIZATION_FAILED' and 'ALGEBRAIC_INTEGRITY_FAILED' in r.all_causes
def test_postcheck_exception_is_explicit_finalization(monkeypatch):
 cfg=_cfg_with_caps();_install_fake_locals(monkeypatch);monkeypatch.setattr(alg,'local_oracle_diagnostics',lambda local,result,*a,**k:_diag(local.agent));monkeypatch.setattr(alg,'_residuals',_zero_res);monkeypatch.setattr(alg,'physical_postcheck_numeric',lambda *a,**k:(_ for _ in ()).throw(RuntimeError('x')));r=alg.run_algorithm2(cfg);assert r.termination_reason=='POSTCHECK_EVALUATION_FAILED' and r.primary_cause=='POSTCHECK_EVALUATION_FAILED'
def test_finite_outer_stop_requires_two_consecutive_complete_outer_passes(monkeypatch):
 cfg=_cfg_with_caps(2,1);_install_fake_locals(monkeypatch);monkeypatch.setattr(alg,'local_oracle_diagnostics',lambda local,result,*a,**k:_diag(local.agent));monkeypatch.setattr(alg,'_residuals',_zero_res);monkeypatch.setattr(alg,'_outer_stop_predicate',lambda *a,**k:True);r=alg.run_algorithm2(cfg);assert r.termination_reason=='FINITE_OUTER_STOP';ev=[e for e in r.history if e.get('phase')=='outer_complete'];assert [e['consecutive_outer_passes'] for e in ev]==[1,2]
def test_residual_crosscheck_failure_aborts_before_snapshot_acceptance(monkeypatch):
 cfg=_cfg_with_caps();_install_fake_locals(monkeypatch);monkeypatch.setattr(alg,'local_oracle_diagnostics',lambda local,result,*a,**k:_diag(local.agent));bad=_zero_res();bad.update({'R1_matrix':1.,'R1_crosscheck_abs':1.});monkeypatch.setattr(alg,'_residuals',lambda *a,**k:bad);r=alg.run_algorithm2(cfg);assert r.termination_reason=='UPDATE_ABORT' and r.primary_cause=='ALGEBRAIC_INTEGRITY_FAILED' and r.state.inner_t==0
def test_outer_parameter_integrity_failure_has_explicit_update_abort(monkeypatch):
 cfg=_cfg_with_caps();_install_fake_locals(monkeypatch);monkeypatch.setattr(alg,'local_oracle_diagnostics',lambda local,result,*a,**k:_diag(local.agent));monkeypatch.setattr(alg,'_residuals',_zero_res);monkeypatch.setattr(alg,'_outer_stop_predicate',lambda *a,**k:False);monkeypatch.setattr(alg,'_outer_parameter_update',lambda cfg,lam,beta,xi,prev:(np.asarray(lam),beta,999.));r=alg.run_algorithm2(cfg);assert r.termination_reason=='UPDATE_ABORT' and r.primary_cause=='ALGEBRAIC_INTEGRITY_FAILED'
def test_incomplete_physical_evaluator_is_postcheck_failure_not_safety_violation(monkeypatch):
 cfg=_cfg_with_caps();_install_fake_locals(monkeypatch);monkeypatch.setattr(alg,'local_oracle_diagnostics',lambda local,result,*a,**k:_diag(local.agent));monkeypatch.setattr(alg,'_residuals',_zero_res);monkeypatch.setattr(alg,'physical_postcheck_numeric',lambda *a,**k:{'evaluation_complete':False,'PHYSICAL_POSTCHECK_NUMERIC_PASS':False,'families':{}});monkeypatch.setattr(alg,'_outer_stop_predicate',lambda *a,**k:False);r=alg.run_algorithm2(cfg);assert 'POSTCHECK_EVALUATION_FAILED' in r.all_causes and 'PHYSICAL_VIOLATION_DETECTED' not in r.all_causes and r.statuses['NUMERICALLY_VALID'] is False
def test_inner_loop_timeout_branch_uses_common_finalization(monkeypatch):
    cfg=_cfg_with_caps(max_outer=1,max_inner=2);cfg.raw['algorithm']['wall_clock_cap_s']=1.0;_install_fake_locals(monkeypatch);values=iter([0.0,0.0,2.0,2.0,2.0]);monkeypatch.setattr(alg.time,'monotonic',lambda:next(values,2.0));result=alg.run_algorithm2(cfg);assert result.termination_reason=='TIMEOUT';assert result.history[-1]['phase']=='finalization'
