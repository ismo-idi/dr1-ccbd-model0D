from pathlib import Path
import numpy as np
from src.config import load_config
from src.diagnostics import local_oracle_diagnostics
from src.local_nlp import LocalSolveResult,build_local_nlp
from src.tcc import assemble_tcc,stationary_exact_tcc_initialization
ROOT=Path(__file__).resolve().parents[1]
def test_objective_is_source_counted_once_and_foreign_copy_does_not_duplicate_it():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);l=build_local_nlp(1,cfg,ops);z1,_,_=stationary_exact_tcc_initialization(cfg,ops);f0=l.eval_source_objective(z1);z=z1.copy();z[cfg.Q:]=np.linspace(-3.,3.,cfg.Q);assert f0==l.eval_source_objective(z)
def test_metadata_rows_are_complete_sequential_and_guardian_localized():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);l1=build_local_nlp(1,cfg,ops);l2=build_local_nlp(2,cfg,ops);assert [m.row for m in l1.metas]==list(range(l1.n_constraints));assert [m.row for m in l2.metas]==list(range(l2.n_constraints));assert sum(m.family=='uav' for m in l1.metas)==cfg.K;assert sum(m.family=='uav' for m in l2.metas)==0
def test_predefined_obstacle_scenario_builds_generic_obstacle_rows_without_execution():
 cfg=load_config(ROOT/'configs'/'obstacle_2uav_1obs.json');ops=assemble_tcc(cfg);l1=build_local_nlp(1,cfg,ops);l2=build_local_nlp(2,cfg,ops);assert sum(m.family=='obs' for m in l1.metas)==cfg.K;assert sum(m.family=='obs' for m in l2.metas)==cfg.K;assert l1.n_constraints==88;assert l2.n_constraints==48
def test_missing_multiplier_vector_is_explicitly_unavailable_not_reconstructed():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);l=build_local_nlp(2,cfg,ops);_,z2,u=stationary_exact_tcc_initialization(cfg,ops);xi=np.zeros(cfg.Q);y=np.zeros(cfg.Q);r=LocalSolveResult(2,z2.copy(),np.zeros(l.n_constraints-1),l.eval_phi(z2,u,xi,y,4.0),True,'SYNTHETIC',0,0.0,{});d=local_oracle_diagnostics(l,r,z2,u,xi,y,4.0);assert not d.accepted and not d.multiplier_mapping_available and d.failure_code=='MULTIPLIER_DIAGNOSTIC_UNAVAILABLE'
def test_hover_pair_rows_are_omitted_only_when_strictly_inactive():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);l=build_local_nlp(1,cfg,ops);z1,_,u=stationary_exact_tcc_initialization(cfg,ops);xi=np.zeros(cfg.Q);y=np.zeros(cfg.Q);r=LocalSolveResult(1,z1.copy(),np.zeros(l.n_constraints),l.eval_phi(z1,u,xi,y,4.0),True,'SYNTHETIC',0,0.0,{});d=local_oracle_diagnostics(l,r,z1,u,xi,y,4.0);rows=[m.row for m in l.metas if m.family=='uav'];assert set(rows).issubset(set(d.omitted_rows));assert not set(rows).intersection(d.nonsmooth_blocking_rows)
def test_backend_failure_with_nonfinite_multiplier_preserves_simultaneous_causes():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);l=build_local_nlp(2,cfg,ops);_,z2,u=stationary_exact_tcc_initialization(cfg,ops);xi=np.zeros(cfg.Q);y=np.zeros(cfg.Q);r=LocalSolveResult(2,z2.copy(),np.full(l.n_constraints,np.nan),float('nan'),False,'SYNTHETIC_FAILURE',None,0.0,{});d=local_oracle_diagnostics(l,r,z2,u,xi,y,4.0);assert 'NUMERICAL_NAN_INF' in d.failure_codes and 'SOLVER_BACKEND_FAILURE' in d.failure_codes;assert d.failure_code=='NUMERICAL_NAN_INF' and not d.accepted
def test_independent_constraint_value_recompute_detects_solver_graph_mismatch():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);l=build_local_nlp(2,cfg,ops);_,z2,u=stationary_exact_tcc_initialization(cfg,ops);xi=np.zeros(cfg.Q);y=np.zeros(cfg.Q);orig=l.g_fun;l.g_fun=lambda z:np.asarray(orig(z),float).reshape(-1)+np.r_[1e-4,np.zeros(l.n_constraints-1)];r=LocalSolveResult(2,z2.copy(),np.zeros(l.n_constraints),l.eval_phi(z2,u,xi,y,4.0),True,'SYNTHETIC',0,0.0,{});d=local_oracle_diagnostics(l,r,z2,u,xi,y,4.0);assert not d.constraint_value_crosscheck_pass and 'ALGEBRAIC_INTEGRITY_FAILED' in d.failure_codes and not d.accepted
