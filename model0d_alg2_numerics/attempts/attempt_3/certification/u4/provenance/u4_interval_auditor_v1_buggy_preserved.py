#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path
import numpy as np
P=100

def sha256(path: Path):
    h=hashlib.sha256();
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def op2(a,b,fn,rounding):
    with localcontext() as c:
        c.prec=P; c.rounding=rounding
        return fn(a,b)
def addd(a,b,r): return op2(a,b,lambda x,y:x+y,r)
def subd(a,b,r): return op2(a,b,lambda x,y:x-y,r)
def muld(a,b,r): return op2(a,b,lambda x,y:x*y,r)
def divd(a,b,r): return op2(a,b,lambda x,y:x/y,r)
class I:
    __slots__=('lo','hi')
    def __init__(self,lo,hi=None): self.lo=Decimal(lo); self.hi=Decimal(lo if hi is None else hi); assert self.lo<=self.hi

def add(x,y): return I(addd(x.lo,y.lo,ROUND_FLOOR), addd(x.hi,y.hi,ROUND_CEILING))
def neg(x): return I(-x.hi,-x.lo)
def sub(x,y): return add(x,neg(y))
def mul(x,y):
    lows=[muld(a,b,ROUND_FLOOR) for a in (x.lo,x.hi) for b in (y.lo,y.hi)]
    highs=[muld(a,b,ROUND_CEILING) for a in (x.lo,x.hi) for b in (y.lo,y.hi)]
    return I(min(lows),max(highs))
def div(x,y):
    if y.lo<=0<=y.hi: raise ZeroDivisionError('interval denominator contains zero')
    lows=[divd(a,b,ROUND_FLOOR) for a in (x.lo,x.hi) for b in (y.lo,y.hi)]
    highs=[divd(a,b,ROUND_CEILING) for a in (x.lo,x.hi) for b in (y.lo,y.hi)]
    return I(min(lows),max(highs))
def sq(x): return mul(x,x)
def dot(a,b):
    z=I(0)
    for x,y in zip(a,b): z=add(z,mul(x,y))
    return z
def vsub(a,b): return [sub(x,y) for x,y in zip(a,b)]
def vadd(a,b): return [add(x,y) for x,y in zip(a,b)]
def dec_float_exact(x): return Decimal.from_float(float(x))
def seg(a,d):
    s=dot(d,d); b=dot(a,d); a2=dot(a,a); bs=add(b,s)
    if s.lo==0 and s.hi==0: return a2,'degenerate',I(0),s,b
    if b.lo>=0: return a2,'endpoint0',I(0),s,b
    if bs.hi<=0: return dot(vadd(a,d),vadd(a,d)),'endpoint1',I(1),s,b
    if s.lo>0 and b.hi<0 and bs.lo>0:
        lam=div(neg(b),s); return sub(a2,div(sq(b),s)),'interior',lam,s,b
    raise RuntimeError(f'uncertified segment regime: s=[{s.lo},{s.hi}], b=[{b.lo},{b.hi}], b+s=[{bs.lo},{bs.hi}]')
def js(i): return {'lo':str(i.lo),'hi':str(i.hi)}
def certify(config_path,state_path):
    cfg=json.loads(Path(config_path).read_text(),parse_float=Decimal,parse_int=Decimal); m=cfg['model']; K=int(m['K']); q=int(m['q']); N=int(m['N'])
    a=np.load(state_path); Q=q*K; z1=np.asarray(a['z1'],np.float64).reshape(-1); z2=np.asarray(a['z2'],np.float64).reshape(-1)
    starts=[[I(v) for v in row] for row in m['starts']]
    f1=[[I(dec_float_exact(v)) for v in row] for row in z1[:Q].reshape(K,q)]
    f2=[[I(dec_float_exact(v)) for v in row] for row in z2.reshape(K,q)]
    T=[[starts[0]]+f1,[starts[1]]+f2]
    lo=[I(v) for v in m['workspace_lower']]; hi=[I(v) for v in m['workspace_upper']]; vmax=[I(v) for v in m['vmax']]; dt=I(m['dt']); radii=[I(v) for v in m['radii']]; clear=add(add(radii[0],radii[1]),I(m['delta_uav']))
    vals={'initial_workspace':[],'workspace':[],'speed':[],'obstacle':[],'uav':[]}; inconclusive=[]
    for i in range(N):
      for j in range(q): vals['initial_workspace'] += [(sub(T[i][0][j],lo[j]),[i,0,j,'lower']),(sub(hi[j],T[i][0][j]),[i,0,j,'upper'])]
      for k in range(1,K+1):
        for j in range(q): vals['workspace'] += [(sub(T[i][k][j],lo[j]),[i,k,j,'lower']),(sub(hi[j],T[i][k][j]),[i,k,j,'upper'])]
      lim2=sq(mul(vmax[i],dt))
      for k in range(K):
        st=vsub(T[i][k+1],T[i][k]); vals['speed'].append((sub(lim2,dot(st,st)),[i,k]))
    init_a=vsub(T[0][0],T[1][0]); init_uav=sub(dot(init_a,init_a),sq(clear))
    delta_obs=[I(v) for v in m['delta_obs']]
    for i in range(N):
      for oi,ob in enumerate(m['obstacles']):
        center=[I(v) for v in ob['center']]; rho=add(add(I(ob['radius']),radii[i]),delta_obs[i])
        for k in range(K):
          aa=vsub(T[i][k],center); dd=vsub(T[i][k+1],T[i][k])
          M,reg,lam,s,b=seg(aa,dd); vals['obstacle'].append((sub(M,sq(rho)),[i,oi,k,reg,js(lam)]))
    for k in range(K):
      aa=vsub(T[0][k],T[1][k]); r1=vsub(T[0][k+1],T[1][k+1]); dd=vsub(r1,aa)
      M,reg,lam,s,b=seg(aa,dd); vals['uav'].append((sub(M,sq(clear)),[0,1,k,reg,js(lam),js(M)]))
    failures=[]
    for fam,seq in vals.items():
      for iv,meta in seq:
        if iv.lo < 0: failures.append([fam,meta,js(iv)])
    if init_uav.lo<0: failures.append(['initial_uav',[0,1],js(init_uav)])
    mins={fam:min(seq,key=lambda x:x[0].lo) if seq else None for fam,seq in vals.items()}
    return {
      'method':'U4-E2 independent validated decimal interval audit','precision_decimal_digits':P,
      'input':{'config_sha256':sha256(Path(config_path)),'final_state_sha256':sha256(Path(state_path))},
      'semantics':{'saved_binary64':'exact singleton Decimal.from_float','model_constants':'exact JSON decimal literals','rounding':'directed ROUND_FLOOR / ROUND_CEILING','safety_tolerance_used':False},
      'initial_uav_squared_margin_interval':js(init_uav),
      'minimum_intervals':{fam:(None if item is None else {'interval':js(item[0]),'meta':item[1]}) for fam,item in mins.items()},
      'expected_counts':{fam:len(seq) for fam,seq in vals.items()},
      'regime_evaluation_complete':True,
      'failure_count':len(failures),'failures':failures,
      'INTERVAL_SAFETY_AUDIT_PASS':len(failures)==0
    }
def main():
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--state',required=True);p.add_argument('--output',required=True);a=p.parse_args(); r=certify(Path(a.config),Path(a.state));Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({'INTERVAL_SAFETY_AUDIT_PASS':r['INTERVAL_SAFETY_AUDIT_PASS'],'uav_min':r['minimum_intervals']['uav']},indent=2))
if __name__=='__main__': main()
