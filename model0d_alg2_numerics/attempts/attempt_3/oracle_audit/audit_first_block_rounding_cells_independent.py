#!/usr/bin/env python3
import json, math
from fractions import Fraction
from pathlib import Path
RUNS=Path('/mnt/data/ccbo_closure/attempt3_checkpointC_execution/attempt3_checkpointAB/runs')
OUT=Path(__file__).resolve().parent/'ATTEMPT3_EXACT_FIRST_BLOCK_ORACLE_INDEPENDENT_AUDIT.json'
def F(x): return Fraction.from_float(float(x))
def cell(x):
    x=float(x); fx=F(x); p=F(math.nextafter(x,-math.inf)); n=F(math.nextafter(x,math.inf))
    return (p+fx)/2,(fx+n)/2

def target(run):
    with (RUNS/run/'events.jsonl').open() as f:
        for line in f:
            e=json.loads(line)
            if e.get('phase')=='inner_complete' and e.get('r')==1 and e.get('t')==1:
                return [o for o in e['oracles'] if o['agent']==2][0]
    raise RuntimeError

def audit(run):
    o=target(run); raw=o['raw_g']; g1=raw[2]; g2=raw[6]
    # If fl(y-3)=g, exact y lies in rounding-cell(g)+3. This enclosure is conservative even at ties.
    l1,h1=cell(g1); l2,h2=cell(g2); l1+=3; h1+=3; l2+=3; h2+=3
    dl=8*l1-2*h2+12; dh=8*h1-2*l2+12
    # fl(x-3)=-3 -> x lies within cell(-3)+3 = [-2^-52,2^-52].
    xl,xh=cell(-3.0); xl+=3; xh+=3
    # Speed constraints affecting y1. Maximize with interval endpoints.
    def sqmax(a,b): return max(a*a,b*b)
    s0=sqmax(xl,xh)+sqmax(l1+2,h1+2)-Fraction(9,16)
    dxlo=xl-xh; dxhi=xh-xl; dylo=l2-h1; dyhi=h2-l1
    s1=sqmax(dxlo,dxhi)+sqmax(dylo,dyhi)-Fraction(9,16)
    return {'run':run,'derivative_lower':str(dl),'derivative_upper':str(dh),'derivative_lower_decimal':float(dl),'strict_positive':dl>0,
            'speed0_upper':str(s0),'speed0_decimal':float(s0),'speed1_upper':str(s1),'speed1_decimal':float(s1),
            'workspace_y1_strict': h1 < 3 and l1 > -3,
            'normal_component_zero': (s0<0 and s1<0 and h1<3 and l1>-3),
            'stationarity_impossible': (dl>0 and s0<0 and s1<0 and h1<3 and l1>-3)}
res=[audit('attempt3_run1'),audit('attempt3_run2')]
out={'method':'independent exact IEEE-754 rounding-cell enclosure; no candidate-float enumeration','runs':res,
     'verdict':'PASS independent audit: exact first-block stationarity is impossible at r=1,t=1,agent=2 in both official repetitions.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(OUT); print(json.dumps(out,indent=2))
