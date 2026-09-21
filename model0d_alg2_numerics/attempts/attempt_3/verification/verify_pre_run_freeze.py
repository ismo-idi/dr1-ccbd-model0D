#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, difflib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXPECTED_UNCHANGED={
 'run_experiment.py':'555881830578179db1c3b8e48a309a5e4276004595c7732d59fec065cc552823',
 'src/__init__.py':'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
 'src/diagnostics.py':'4bcef4c418c46d6938f4e50b4c1ec0b39811e821f3d017a7f657837e7945e84a',
 'src/geometry.py':'bbcee181c372d462e2b56dcbe4bee831a2f13fe9f97298eb6747c719e5ba47a8',
 'src/io_utils.py':'c448d2108f0b846c9c2897a8a20a3cac7c702547d08812fb0299fbaa8b778239',
 'src/local_nlp.py':'789bc9da93e593d9ff62ab874fe20e50188b2800d3fab6815badb0275adee504',
 'src/sunsun_algorithm2.py':'dfdc931ae1e1ce17d37e8e7b886cb313047c30cfab405ba4a3be253b61719024',
 'src/tcc.py':'852af3aea5228a9efba8d87a8ba66d4856b4755a0f840d11defa4e71f834658f',
}
ATTEMPT2_CONFIG_PY_SHA='3d035be4ac0ca7e82e1a7063193ae12274bad957ce5d751fa21b3684910145ae'

def sha(p:Path)->str:
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

checks={}
checks['unchanged_source_hashes']={p:{'expected':h,'actual':sha(ROOT/p),'pass':sha(ROOT/p)==h} for p,h in EXPECTED_UNCHANGED.items()}
checks['attempt2_config_py_reference']={
 'expected':ATTEMPT2_CONFIG_PY_SHA,
 'actual':sha(ROOT/'provenance/attempt2_config_py_reference.py'),
}
checks['attempt2_config_py_reference']['pass']=checks['attempt2_config_py_reference']['actual']==ATTEMPT2_CONFIG_PY_SHA

old_py=(ROOT/'provenance/attempt2_config_py_reference.py').read_text().splitlines()
new_py=(ROOT/'src/config.py').read_text().splitlines()
changes=[]
for line in difflib.unified_diff(old_py,new_py,lineterm=''):
 if line.startswith(('+++','---','@@')): continue
 if line.startswith('+') or line.startswith('-'): changes.append(line)
checks['config_py_only_cap_line_changed']={
 'changes':changes,
 'pass': changes==['-        "max_inner_iterations": 100,','+        "max_inner_iterations": 1000,']
}

old=json.loads((ROOT/'provenance/attempt2_baseline_config_reference.json').read_text())
new=json.loads((ROOT/'configs/baseline_2uav_0obs.json').read_text())

def leafdiff(a,b,path=''):
 out=[]
 if isinstance(a,dict) and isinstance(b,dict):
  for k in sorted(set(a)|set(b)):
   p=f'{path}.{k}' if path else k
   if k not in a: out.append((p,'<MISSING>',b[k]))
   elif k not in b: out.append((p,a[k],'<MISSING>'))
   else: out.extend(leafdiff(a[k],b[k],p))
 elif isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
  for i,(x,y) in enumerate(zip(a,b)): out.extend(leafdiff(x,y,f'{path}[{i}]'))
 elif a!=b: out.append((path,a,b))
 return out
D=leafdiff(old,new)
nonmeta=[d for d in D if d[0] != 'description' and not d[0].startswith('attempt3')]
checks['baseline_config_scientific_diff']={
 'all_differences':[{'path':p,'old':a,'new':b} for p,a,b in D],
 'nonmetadata_differences':[{'path':p,'old':a,'new':b} for p,a,b in nonmeta],
 'pass':nonmeta==[('algorithm.max_inner_iterations',100,1000)]
}
checks['attempt3_metadata']={
 'value':new.get('attempt3'),
 'pass': new.get('attempt3')=={
    'attempt_id':'attempt_3','route':'finite_cap_isolation','source_attempt':'attempt_2',
    'single_experimental_change':'algorithm.max_inner_iterations: 100 -> 1000',
    'parent_branch_head':'79cd3aa4bfeabc12ea3eeb2649b1e3d341ce6f1c',
    'fresh_process_repetitions':2,'outcome_driven_retuning_permitted':False,
 }
}
checks['runs_directory_empty']={'entries':sorted(p.name for p in (ROOT/'runs').iterdir()),'pass':not any((ROOT/'runs').iterdir())}
checks['baseline_cap_frozen']={'value':new['algorithm']['max_inner_iterations'],'pass':new['algorithm']['max_inner_iterations']==1000}
checks['wall_clock_unchanged']={'value':new['algorithm']['wall_clock_cap_s'],'pass':new['algorithm']['wall_clock_cap_s']==600.0}
checks['no_retry_unchanged']={'value':new['algorithm']['retry_count'],'pass':new['algorithm']['retry_count']==0}
checks['overall_pass']=all(v.get('pass',True) for k,v in checks.items() if isinstance(v,dict))
print(json.dumps(checks,indent=2,sort_keys=True))
raise SystemExit(0 if checks['overall_pass'] else 1)
