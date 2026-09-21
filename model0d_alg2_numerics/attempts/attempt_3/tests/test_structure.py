from pathlib import Path
import numpy as np
from src.config import load_config
from src.local_nlp import build_local_nlp
from src.tcc import assemble_tcc,stationary_exact_tcc_initialization
ROOT=Path(__file__).resolve().parents[1]
def test_frozen_dimensions_and_initialization():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);assert (cfg.Q,ops.d1,ops.d2,ops.M_eq,ops.m)==(16,32,16,1,32);z1,z2,u=stationary_exact_tcc_initialization(cfg,ops);assert z1.shape==(32,) and z2.shape==(16,) and u.shape==(16,);np.testing.assert_allclose(ops.direct_tcc_difference(z1,z2),0.);np.testing.assert_allclose(ops.target_rows(z1,z2,u),0.)
def test_local_constraint_counts_baseline():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);l1=build_local_nlp(1,cfg,ops);l2=build_local_nlp(2,cfg,ops);assert l1.n_constraints==80 and l2.n_constraints==40;assert sum(m.family=='uav' for m in l1.metas)==8 and sum(m.family=='uav' for m in l2.metas)==0;assert sum(m.family=='A1' for m in l1.metas)==32 and sum(m.family=='A1' for m in l2.metas)==0
def test_fixed_prefix_selector_and_architecture_legality():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);z1,z2,u=stationary_exact_tcc_initialization(cfg,ops);from src.diagnostics import source_trajectories;p1,p2=source_trajectories(cfg,ops,z1,z2);np.testing.assert_allclose(p1[0],cfg.starts[0]);np.testing.assert_allclose(p2[0],cfg.starts[1]);assert cfg.raw['tcc']['source_2_equality_edge']==[1,2] and cfg.raw['tcc']['reduction_tree_edge']==[1,2]
def test_stationary_exact_lift_is_feasible_for_both_local_domains_and_a1():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);l1=build_local_nlp(1,cfg,ops);l2=build_local_nlp(2,cfg,ops);z1,z2,u=stationary_exact_tcc_initialization(cfg,ops);assert np.max(l1.eval_g(z1))<=0 and np.max(l2.eval_g(z2))<=0;assert np.all(u.reshape(cfg.K,cfg.q)>=cfg.a1_lower) and np.all(u.reshape(cfg.K,cfg.q)<=cfg.a1_upper);np.testing.assert_allclose(ops.target_rows(z1,z2,u),0.,atol=0.,rtol=0.)
