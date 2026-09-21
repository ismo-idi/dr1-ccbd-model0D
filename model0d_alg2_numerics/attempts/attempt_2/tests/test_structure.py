from pathlib import Path
import numpy as np

from src.config import load_config
from src.local_nlp import build_local_nlp
from src.tcc import assemble_tcc, stationary_exact_tcc_initialization

ROOT = Path(__file__).resolve().parents[1]


def test_frozen_dimensions_and_initialization():
    cfg = load_config(ROOT / 'configs' / 'baseline_2uav_0obs.json')
    ops = assemble_tcc(cfg)
    assert cfg.Q == 16
    assert ops.d1 == 32
    assert ops.d2 == 16
    assert ops.M_eq == 1
    assert ops.m == 32
    z1, z2, u = stationary_exact_tcc_initialization(cfg, ops)
    assert z1.shape == (32,)
    assert z2.shape == (16,)
    assert u.shape == (16,)
    np.testing.assert_allclose(ops.direct_tcc_difference(z1, z2), 0.0)
    np.testing.assert_allclose(ops.target_rows(z1, z2, u), 0.0)


def test_local_constraint_counts_baseline():
    cfg = load_config(ROOT / 'configs' / 'baseline_2uav_0obs.json')
    ops = assemble_tcc(cfg)
    l1 = build_local_nlp(1, cfg, ops)
    l2 = build_local_nlp(2, cfg, ops)
    # UAV1: W 32 + speed 8 + guardian UAV-pair 8 + A1 32 = 80
    assert l1.n_constraints == 80
    # UAV2: W 32 + speed 8 = 40
    assert l2.n_constraints == 40
    assert sum(m.family == 'uav' for m in l1.metas) == 8
    assert sum(m.family == 'uav' for m in l2.metas) == 0
    assert sum(m.family == 'A1' for m in l1.metas) == 32
    assert sum(m.family == 'A1' for m in l2.metas) == 0


def test_fixed_prefix_selector_and_architecture_legality():
    cfg = load_config(ROOT / 'configs' / 'baseline_2uav_0obs.json')
    ops = assemble_tcc(cfg)
    z1, z2, u = stationary_exact_tcc_initialization(cfg, ops)
    # Free coordinates exclude p_i^0; insertion reconstructs it from frozen data.
    from src.diagnostics import source_trajectories
    p1, p2 = source_trajectories(cfg, ops, z1, z2)
    np.testing.assert_allclose(p1[0], cfg.starts[0])
    np.testing.assert_allclose(p2[0], cfg.starts[1])
    np.testing.assert_allclose(p1[1:], ops.source1_from_z1(z1).reshape(cfg.K, cfg.q))
    np.testing.assert_allclose(p2[1:], ops.source2_from_z2(z2).reshape(cfg.K, cfg.q))
    # W is strictly inside B, and the unique equality/reduction edge is legal.
    assert np.all(cfg.a1_lower < cfg.workspace_lower)
    assert np.all(cfg.workspace_upper < cfg.a1_upper)
    assert cfg.raw['tcc']['source_2_equality_edge'] == [1, 2]
    assert cfg.raw['tcc']['reduction_tree_edge'] == [1, 2]
    assert len({(1, 2)}) == 1  # E^all cardinality for N=2


def test_stationary_exact_lift_is_feasible_for_both_local_domains_and_a1():
    cfg = load_config(ROOT / 'configs' / 'baseline_2uav_0obs.json')
    ops = assemble_tcc(cfg)
    l1 = build_local_nlp(1, cfg, ops)
    l2 = build_local_nlp(2, cfg, ops)
    z1, z2, u = stationary_exact_tcc_initialization(cfg, ops)
    g1 = l1.eval_g(z1)
    g2 = l2.eval_g(z2)
    assert np.max(g1) <= 0.0
    assert np.max(g2) <= 0.0
    assert np.all(u.reshape(cfg.K, cfg.q) >= cfg.a1_lower)
    assert np.all(u.reshape(cfg.K, cfg.q) <= cfg.a1_upper)
    np.testing.assert_allclose(ops.target_rows(z1, z2, u), 0.0, atol=0.0, rtol=0.0)
