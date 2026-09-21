#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import numpy as np


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20), b''): h.update(b)
    return h.hexdigest()

def ffloat(x) -> Fraction:
    n,d=float(x).as_integer_ratio(); return Fraction(n,d)

def fdec(x: Decimal) -> Fraction:
    return Fraction(x)

def dot(a,b): return sum((x*y for x,y in zip(a,b)), Fraction(0))
def vec_sub(a,b): return [x-y for x,y in zip(a,b)]
def vec_add(a,b): return [x+y for x,y in zip(a,b)]

def seg_min_sq(a,d):
    s=dot(d,d); b=dot(a,d); a2=dot(a,a)
    if s == 0: return a2, Fraction(0), 'degenerate', s, b
    if b >= 0: return a2, Fraction(0), 'endpoint0', s, b
    if b <= -s:
        ad=vec_add(a,d); return dot(ad,ad), Fraction(1), 'endpoint1', s, b
    lam=-b/s
    return a2-b*b/s, lam, 'interior', s, b

def frac_obj(x: Fraction): return {'numerator':str(x.numerator),'denominator':str(x.denominator)}
def decstr(x: Fraction, digits=50):
    with localcontext() as c:
        c.prec=digits
        return str(Decimal(x.numerator)/Decimal(x.denominator))

def sqrt_decimal_fraction(x: Fraction, digits=50):
    if x < 0: return None
    with localcontext() as c:
        c.prec=digits
        return str((Decimal(x.numerator)/Decimal(x.denominator)).sqrt())

def certify(config_path: Path, state_path: Path):
    # Exact decimal literals from JSON.
    cfg=json.loads(config_path.read_text(), parse_float=Decimal, parse_int=Decimal)
    m=cfg['model']; K=int(m['K']); q=int(m['q']); N=int(m['N'])
    assert N==2 and q in (2,3)
    arr=np.load(state_path)
    z1=np.asarray(arr['z1'],dtype=np.float64).reshape(-1)
    z2=np.asarray(arr['z2'],dtype=np.float64).reshape(-1)
    Q=q*K
    assert z1.size >= Q and z2.size == Q
    starts=[[fdec(v) for v in row] for row in m['starts']]
    free1=[[ffloat(v) for v in z1[:Q].reshape(K,q)[k]] for k in range(K)]
    free2=[[ffloat(v) for v in z2.reshape(K,q)[k]] for k in range(K)]
    P=[ [starts[0]]+free1, [starts[1]]+free2 ]
    lo=[fdec(v) for v in m['workspace_lower']]; hi=[fdec(v) for v in m['workspace_upper']]
    vmax=[fdec(v) for v in m['vmax']]; dt=fdec(m['dt'])
    radii=[fdec(v) for v in m['radii']]; delta_uav=fdec(m['delta_uav'])
    clearance=radii[0]+radii[1]+delta_uav

    counts={'initial_workspace':0,'initial_uav':0,'workspace':0,'speed':0,'obstacle':0,'uav':0}
    failures=[]
    initial_workspace=[]; workspace=[]; speed=[]; uav=[]; obstacles=[]
    for i in range(N):
        for j in range(q):
            for side,margin in [('lower',P[i][0][j]-lo[j]),('upper',hi[j]-P[i][0][j])]:
                counts['initial_workspace']+=1; initial_workspace.append((margin,i,j,side))
                if margin < 0: failures.append(['initial_workspace',i,j,side])
        for k in range(1,K+1):
            for j in range(q):
                for side,margin in [('lower',P[i][k][j]-lo[j]),('upper',hi[j]-P[i][k][j])]:
                    counts['workspace']+=1; workspace.append((margin,i,k,j,side))
                    if margin < 0: failures.append(['workspace',i,k,j,side])
        lim2=(vmax[i]*dt)**2
        for k in range(K):
            step=vec_sub(P[i][k+1],P[i][k]); margin=lim2-dot(step,step)
            counts['speed']+=1; speed.append((margin,i,k))
            if margin < 0: failures.append(['speed',i,k])

    a0=vec_sub(P[0][0],P[1][0]); init_uav=dot(a0,a0)-clearance**2
    counts['initial_uav']=1
    if init_uav < 0: failures.append(['initial_uav',0,1])

    # No obstacle hard-coding: support exact spherical/circular center/radius family if present.
    delta_obs=[fdec(v) for v in m['delta_obs']]
    for i in range(N):
        for oi,obs in enumerate(m['obstacles']):
            center=[fdec(v) for v in obs['center']]
            rho=fdec(obs['radius'])+radii[i]+delta_obs[i]
            for k in range(K):
                a=vec_sub(P[i][k],center); d=vec_sub(P[i][k+1],P[i][k])
                M,lam,reg,s,b=seg_min_sq(a,d); margin=M-rho**2
                counts['obstacle']+=1; obstacles.append((margin,i,oi,k,reg,lam,M,rho,s,b))
                if margin < 0: failures.append(['obstacle',i,oi,k])

    for k in range(K):
        a=vec_sub(P[0][k],P[1][k])
        rel1=vec_sub(P[0][k+1],P[1][k+1]); d=vec_sub(rel1,a)
        M,lam,reg,s,b=seg_min_sq(a,d); margin=M-clearance**2
        counts['uav']+=1; uav.append((margin,k,reg,lam,M,s,b))
        if margin < 0: failures.append(['uav',0,1,k])

    wi=min(initial_workspace,key=lambda x:x[0]); ww=min(workspace,key=lambda x:x[0]); ws=min(speed,key=lambda x:x[0]); wu=min(uav,key=lambda x:x[0])
    result={
      'method':'U4-E1 exact-rational physical safety certification',
      'input':{'config':str(config_path),'final_state':str(state_path),'config_sha256':sha256(config_path),'final_state_sha256':sha256(state_path)},
      'semantics':{'saved_binary64':'exact dyadic rationals via as_integer_ratio','model_constants':'exact JSON decimal literals','safety_tolerance_used':False,'source_trajectories_only':True},
      'expected_counts':counts,
      'evaluation_complete':True,
      'failure_count':len(failures),'failures':failures,
      'initial_workspace_min':{'margin_exact':frac_obj(wi[0]),'margin_decimal':decstr(wi[0]),'uav':wi[1]+1,'dim':wi[2],'side':wi[3]},
      'initial_uav_squared_margin':{'margin_exact':frac_obj(init_uav),'margin_decimal':decstr(init_uav)},
      'workspace_min':{'margin_exact':frac_obj(ww[0]),'margin_decimal':decstr(ww[0]),'uav':ww[1]+1,'k':ww[2],'dim':ww[3],'side':ww[4]},
      'speed_min_squared_margin':{'margin_exact':frac_obj(ws[0]),'margin_decimal':decstr(ws[0]),'uav':ws[1]+1,'k':ws[2]},
      'obstacle_family':{'count':counts['obstacle'],'status':'VACUOUS_EMPTY_FAMILY' if counts['obstacle']==0 else ('PASS' if all(x[0]>=0 for x in obstacles) else 'FAIL')},
      'uav_min_squared_margin':{'margin_exact':frac_obj(wu[0]),'margin_decimal':decstr(wu[0]),'pair':[1,2],'k':wu[1],'regime':wu[2],'lambda_exact':frac_obj(wu[3]),'lambda_decimal':decstr(wu[3]),'min_squared_distance_exact':frac_obj(wu[4]),'min_squared_distance_decimal':decstr(wu[4]),'clearance_exact':frac_obj(clearance),'clearance_decimal':decstr(clearance),'min_distance_decimal_for_readability':sqrt_decimal_fraction(wu[4]),'unsquared_margin_decimal_for_readability':None},
      'MODEL0D_SAFETY_CERTIFIED': len(failures)==0,
      'U4':'RESOLVED_BY_U4_E1_EXACT_RATIONAL' if len(failures)==0 else 'RESOLVED_WITH_CERTIFIED_VIOLATION'
    }
    with localcontext() as c:
        c.prec=60
        md=(Decimal(wu[4].numerator)/Decimal(wu[4].denominator)).sqrt()
        cr=Decimal(clearance.numerator)/Decimal(clearance.denominator)
        result['uav_min_squared_margin']['unsquared_margin_decimal_for_readability']=str(md-cr)
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--config',required=True); ap.add_argument('--state',required=True); ap.add_argument('--output',required=True)
    a=ap.parse_args(); r=certify(Path(a.config),Path(a.state)); Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); print(json.dumps({'MODEL0D_SAFETY_CERTIFIED':r['MODEL0D_SAFETY_CERTIFIED'],'uav_min_squared_margin_decimal':r['uav_min_squared_margin']['margin_decimal'],'uav_k':r['uav_min_squared_margin']['k'],'regime':r['uav_min_squared_margin']['regime']},indent=2))
if __name__=='__main__': main()
