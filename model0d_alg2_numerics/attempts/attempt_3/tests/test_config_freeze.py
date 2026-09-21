import json
from pathlib import Path
import pytest
from src.config import ConfigurationError,ModelConfig,load_config,validate_frozen_2uav_protocol
ROOT=Path(__file__).resolve().parents[1]
def test_both_approved_configs_pass_exact_freeze():
 b=load_config(ROOT/'configs'/'baseline_2uav_0obs.json');o=load_config(ROOT/'configs'/'obstacle_2uav_1obs.json');assert b.raw['scenario_id']=='baseline_2uav_0obs';assert o.raw['scenario_id']=='obstacle_2uav_1obs';assert b.obstacles==[];assert o.obstacles==[{'center':[1.0,0.0],'radius':0.35}]
def test_protocol_threshold_drift_is_rejected():
 r=json.loads((ROOT/'configs'/'baseline_2uav_0obs.json').read_text());r['thresholds']['tcc_eq']=1e-4
 with pytest.raises(ConfigurationError,match='tcc_eq'):validate_frozen_2uav_protocol(ModelConfig(r))
def test_scenario_data_drift_is_rejected():
 r=json.loads((ROOT/'configs'/'baseline_2uav_0obs.json').read_text());r['model']['goals'][0][0]=1.9
 with pytest.raises(ConfigurationError,match='goals'):validate_frozen_2uav_protocol(ModelConfig(r))
def test_unapproved_scenario_is_rejected():
 r=json.loads((ROOT/'configs'/'baseline_2uav_0obs.json').read_text());r['scenario_id']='unapproved'
 with pytest.raises(ConfigurationError,match='outside the approved bounded campaign'):validate_frozen_2uav_protocol(ModelConfig(r))

def test_attempt3_cap_is_frozen_at_1000_and_attempt_metadata_is_present():
    cfg = load_config(ROOT / 'configs' / 'baseline_2uav_0obs.json')
    assert cfg.a['max_inner_iterations'] == 1000
    assert cfg.raw['attempt3']['attempt_id'] == 'attempt_3'
    assert cfg.raw['attempt3']['route'] == 'finite_cap_isolation'
    assert cfg.raw['attempt3']['source_attempt'] == 'attempt_2'
    assert cfg.raw['attempt3']['fresh_process_repetitions'] == 2
    assert cfg.raw['attempt3']['outcome_driven_retuning_permitted'] is False


def test_attempt3_cap_drift_is_rejected():
    raw = json.loads((ROOT / 'configs' / 'baseline_2uav_0obs.json').read_text())
    raw['algorithm']['max_inner_iterations'] = 999
    with pytest.raises(ConfigurationError, match='max_inner_iterations'):
        validate_frozen_2uav_protocol(ModelConfig(raw))
