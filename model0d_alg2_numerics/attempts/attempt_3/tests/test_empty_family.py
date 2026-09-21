from pathlib import Path
from src.config import load_config
from src.diagnostics import physical_postcheck_numeric
from src.tcc import assemble_tcc,stationary_exact_tcc_initialization
ROOT=Path(__file__).resolve().parents[1]
def test_zero_obstacle_family_semantics():
 cfg=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');ops=assemble_tcc(cfg);z1,z2,_=stationary_exact_tcc_initialization(cfg,ops);result=physical_postcheck_numeric(cfg,ops,z1,z2);obs=result['families']['obs'];assert result['expected_cardinality']['obs']==0;assert obs['aggregate_violation']==0.0;assert obs['minimum_margin']=='NOT_APPLICABLE_EMPTY_FAMILY';assert obs['numeric_pass'] is True
