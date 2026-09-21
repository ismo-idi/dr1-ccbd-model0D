from pathlib import Path
import numpy as np
from src.config import load_config
from src.diagnostics import physical_postcheck_numeric
from src.tcc import assemble_tcc,stationary_exact_tcc_initialization
ROOT=Path(__file__).resolve().parents[1]
def test_physical_postcheck_uses_actual_source_trajectories_not_foreign_copy():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);z1,z2,_=stationary_exact_tcc_initialization(cfg,ops);base=physical_postcheck_numeric(cfg,ops,z1,z2);bad=z1.copy();bad[cfg.Q:]=np.tile(np.array([3.5,3.5]),cfg.K);assert physical_postcheck_numeric(cfg,ops,bad,z2)==base
def test_expected_physical_cardinalities_baseline():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);z1,z2,_=stationary_exact_tcc_initialization(cfg,ops);r=physical_postcheck_numeric(cfg,ops,z1,z2);assert r['expected_cardinality']=={'W':64,'spd':16,'obs':0,'uav':8};assert r['evaluation_complete'] is True
