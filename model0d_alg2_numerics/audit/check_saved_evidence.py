from pathlib import Path
import hashlib,json,re
import numpy as np
H=Path(__file__).parent
out={}
def clean(x):
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items() if k not in ['elapsed_s','backend_elapsed_s']}
 if isinstance(x,list):return [clean(v) for v in x]
 return x
def closest(P,Q):
 vals=[]
 for k in range(len(P)-1):
  a=P[k]-Q[k];d=(P[k+1]-Q[k+1])-a;s=d@d;u=float(np.clip(-(a@d)/s,0,1)) if s else 0.;dist=float(np.linalg.norm(a+u*d));vals.append({'k':k,'lambda':u,'distance':dist})
 return min(vals,key=lambda x:x['distance'])
for tag,runprefix,mf in [('step3','baseline','verification_step3/STEP3_SHA256_MANIFEST.txt'),('attempt2a','attempt2a','verification_attempt2a/ATTEMPT2A_SHA256_MANIFEST.txt')]:
 root=H.parent/'attempts'/({'step3':'attempt_1','attempt2a':'attempt_2'}[tag]);fails=[];count=0
 for line in (root/mf).read_text().splitlines():
  m=re.match(r'^([a-f0-9]{64})\s+(.+?)(?:\s+\d+ bytes)?$',line)
  if not m:continue
  sha,p=m.groups();f=root/p.lstrip('*');count+=1
  if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=sha:fails.append(p)
 assert not fails,fails
 sums=[];events=[];states=[];metrics=[]
 for nr in [1,2]:
  rd=root/'runs'/f'{runprefix}_run{nr}';su=json.loads((rd/'summary.json').read_text());ev=[json.loads(x) for x in (rd/'events.jsonl').read_text().splitlines()];st=np.load(rd/'final_state.npz',allow_pickle=False);env=json.loads((rd/'environment.json').read_text());cfg=json.loads((root/'configs/baseline_2uav_0obs.json').read_text());mo=cfg['model'];K=mo['K'];q=mo['q'];Q=K*q
  for fn,sha in env['implementation_files_sha256'].items():assert hashlib.sha256((root/fn).read_bytes()).hexdigest()==sha,(tag,fn)
  assert hashlib.sha256((root/'configs/baseline_2uav_0obs.json').read_bytes()).hexdigest()==env['config_sha256']
  for k in st.files:assert np.array_equal(st[k].reshape(-1),np.asarray(su['state'][k]).reshape(-1)),k
  assert clean(ev)==clean(su['history'])
  P=np.vstack([mo['starts'][0],st['z1'][:Q].reshape(K,q)]);S=np.vstack([mo['starts'][1],st['z2'].reshape(K,q)]);C=np.vstack([mo['starts'][1],st['z1'][Q:].reshape(K,q)])
  dist=closest(P,S);guard=closest(P,C);clear=sum(mo['radii'])+mo['delta_uav'];F=sum(mo['alpha'][i]*np.sum((X[-1]-mo['goals'][i])**2)+mo['beta_obj'][i]*np.sum(np.diff(X,axis=0)**2) for i,X in enumerate([P,S]));target=np.r_[st['z1'][Q:]-st['u'],st['z2']-st['u']]
  vals={'objective':float(F),'TCC':float(np.linalg.norm(st['z1'][Q:]-st['z2'])),'target':float(np.linalg.norm(target)),'R3':float(np.linalg.norm(target+st['xi'])),'source_closest':dist,'source_margin':dist['distance']-clear,'body_clearance':dist['distance']-sum(mo['radii']),'guardian_margin':guard['distance']-clear,'integrity':float(np.linalg.norm(st['lambda_outer']+st['beta']*st['xi']+st['y'])),'outer':int(st['outer_r'].item()),'inner':int(st['inner_t'].item()),'outer_complete_events':sum(e['phase']=='outer_complete' for e in ev),'termination':su['termination_reason']}
  fm=su['final_metrics'];assert abs(F-fm['objective']['F'])<1e-12;assert abs(vals['TCC']-fm['tcc']['R_TCC_eq'])<1e-12;assert abs(vals['target']-fm['tcc']['R_target'])<1e-12;assert abs(vals['source_margin']-fm['physical']['families']['uav']['minimum_margin'])<1e-12
  inner=[e for e in ev if e['phase']=='inner_complete'];assert abs(vals['R3']-inner[-1]['residuals']['R3'])<1e-12
  # Recompute sign/complementarity tests directly from persisted raw/diagnostic multipliers.
  for e in ev:
   for d in e.get('oracles',[]):
    mu=np.array(d['diagnostic_mu']);g=np.array(d['raw_g']);raw=np.array(d['raw_mu_backend']);den=max(1,float(np.max(np.abs(mu))));dual=float(np.max(np.maximum(-mu,0))/den);comp=float(np.max(np.abs(mu*g)))
    assert abs(dual-d['R_dual_normalized'])<1e-12 and abs(comp-d['R_comp'])<1e-12
    if tag=='attempt2a':
     mask=g < -1e-6;assert np.array_equal(mu,np.where(mask,0,raw));assert set(np.flatnonzero(mask))==set(d['inactive_zeroed_rows'])
  metrics.append(vals);sums.append(su);events.append(ev);states.append(st)
 assert clean(sums[0])==clean(sums[1]);assert clean(events[0])==clean(events[1]);assert all(np.array_equal(states[0][k],states[1][k]) for k in states[0].files)
 out[tag]={'manifest_entries_matched':count,'run_source_and_config_hashes':'PASS','stored_repeats_identical_excluding_timing':True,'saved_states_match_summaries':True,'metrics':metrics[0]}
# Confirm all historical run data preserved unchanged in newer package.
a=H.parent/'attempts/attempt_2';b=H.parent/'attempts/attempt_1';historical=list((b/'runs').rglob('*'));assert all((a/p.relative_to(b)).read_bytes()==p.read_bytes() for p in historical if p.is_file())
out['historical_run_data_preserved']=True
(H/'independent_saved_evidence_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
