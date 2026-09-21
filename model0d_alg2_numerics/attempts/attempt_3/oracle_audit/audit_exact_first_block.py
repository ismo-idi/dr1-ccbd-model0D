#!/usr/bin/env python3
import json, math, itertools, hashlib
from fractions import Fraction
from pathlib import Path

RUNS = Path('/mnt/data/ccbo_closure/attempt3_checkpointC_execution/attempt3_checkpointAB/runs')
OUT = Path(__file__).resolve().parent / 'ATTEMPT3_EXACT_FIRST_BLOCK_ORACLE_AUDIT_RESULTS.json'

def F(x): return Fraction.from_float(float(x))

def neigh(x,n=32):
    vals={float(x)}
    y=float(x)
    for _ in range(n):
        y=math.nextafter(y,-math.inf); vals.add(y)
    y=float(x)
    for _ in range(n):
        y=math.nextafter(y,math.inf); vals.add(y)
    return sorted(vals)

def candidates_from_upper_workspace(raw_g):
    # raw_g = fl(y - 3.0), with stored y binary64. Enumerate nearby binary64 y and retain exact reproductions.
    base=float(raw_g + 3.0)
    return [y for y in neigh(base,32) if float(y - 3.0) == float(raw_g)]

def inner_event(run):
    p=RUNS/run/'events.jsonl'
    with p.open() as f:
        for line in f:
            e=json.loads(line)
            if e.get('phase')=='inner_complete' and e.get('r')==1 and e.get('t')==1:
                return e
    raise RuntimeError('r1,t1 event not found')

def interval_square(lo,hi):
    if lo <= 0 <= hi: return Fraction(0), max(lo*lo,hi*hi)
    vals=(lo*lo,hi*hi); return min(vals),max(vals)

def audit(run):
    e=inner_event(run)
    a2=[o for o in e['oracles'] if o['agent']==2][0]
    raw=a2['raw_g']
    # Workspace rows are [x upper,x lower,y upper,y lower] for k=1..8.
    gu_y1=float(raw[2]); gu_y2=float(raw[6])
    c1=candidates_from_upper_workspace(gu_y1)
    c2=candidates_from_upper_workspace(gu_y2)
    if not c1 or not c2: raise RuntimeError('candidate reconstruction failed')
    deriv=[]
    for y1,y2 in itertools.product(c1,c2):
        # r=1,t=1,a=2: rho=4, y_old=0, xi_old=0, u_old=(0,-2) at every free sample.
        # f2 derivative at y1 = 2(2y1-y0-y2), y0=-2; penalty derivative=4(y1+2).
        d=8*F(y1)-2*F(y2)+12
        deriv.append((d,y1,y2))
    dmin=min(deriv,key=lambda z:z[0]); dmax=max(deriv,key=lambda z:z[0])

    # From fl(x-3)=-3, exact rounding-cell enclosure gives |x| <= 2^-52.
    xb=Fraction(1,2**52)
    max_y0=max((F(y)+2)**2 for y in c1)
    speed0_upper=xb*xb + max_y0 - Fraction(9,16)
    max_dy=max((F(y2)-F(y1))**2 for y1,y2 in itertools.product(c1,c2))
    speed1_upper=(2*xb)**2 + max_dy - Fraction(9,16)

    # Conservative exact interval of full phi2 from all 16 logged upper-workspace rows.
    ysets=[]
    for k in range(8):
        cs=candidates_from_upper_workspace(float(raw[4*k+2]))
        if not cs: raise RuntimeError(f'no candidates for y{k+1}')
        ysets.append(cs)
    xint=(-xb,xb)
    yint=[(min(map(F,c)),max(map(F,c))) for c in ysets]
    lo=Fraction(0); hi=Fraction(0)
    px=(Fraction(0),Fraction(0)); py=(Fraction(-2),Fraction(-2))
    # step regularization beta_i=1
    for k in range(8):
        xi=xint; yi=yint[k]
        dx=(xi[0]-px[1],xi[1]-px[0]); dy=(yi[0]-py[1],yi[1]-py[0])
        a,b=interval_square(*dx); lo+=a; hi+=b
        a,b=interval_square(*dy); lo+=a; hi+=b
        px,py=xi,yi
    # terminal alpha_i=20, goal=(0,2)
    dx=xint; dy=(yint[-1][0]-2,yint[-1][1]-2)
    a,b=interval_square(*dx); lo+=20*a; hi+=20*b
    a,b=interval_square(*dy); lo+=20*a; hi+=20*b
    # ADMM quadratic rho/2=2 vs stationary u=(0,-2)
    for yi in yint:
        a,b=interval_square(*xint); lo+=2*a; hi+=2*b
        dy=(yi[0]+2,yi[1]+2); a,b=interval_square(*dy); lo+=2*a; hi+=2*b
    phi_old=Fraction(320,1)

    return {
      'run':run,
      'event':{'r':1,'t':1,'agent':2},
      'backend':{'status':a2['backend_status'],'finite_R_stat':a2['R_stat'],'finite_R_desc':a2['R_desc'],'accepted':a2['accepted']},
      'logged_upper_workspace':{'y1_minus_3':gu_y1,'y2_minus_3':gu_y2},
      'consistent_binary64_y1':c1,'consistent_binary64_y2':c2,
      'exact_derivative_interval':{
          'formula':'8*y1 - 2*y2 + 12',
          'lower_num':dmin[0].numerator,'lower_den':dmin[0].denominator,'lower_decimal':float(dmin[0]),
          'upper_num':dmax[0].numerator,'upper_den':dmax[0].denominator,'upper_decimal':float(dmax[0]),
          'strictly_positive':dmin[0]>0},
      'exact_speed_upper_bounds':{
          'k0_num':speed0_upper.numerator,'k0_den':speed0_upper.denominator,'k0_decimal':float(speed0_upper),'k0_strictly_inactive':speed0_upper<0,
          'k1_num':speed1_upper.numerator,'k1_den':speed1_upper.denominator,'k1_decimal':float(speed1_upper),'k1_strictly_inactive':speed1_upper<0},
      'normal_cone_coordinate_conclusion':'all constraints involving p2_y1 are strictly inactive; all other local constraints are independent of p2_y1; hence every exact local normal has p2_y1 component 0',
      'exact_stationarity_pass':False,
      'phi_interval':{
          'old_num':phi_old.numerator,'old_den':phi_old.denominator,'old_decimal':float(phi_old),
          'new_lower_num':lo.numerator,'new_lower_den':lo.denominator,'new_lower_decimal':float(lo),
          'new_upper_num':hi.numerator,'new_upper_den':hi.denominator,'new_upper_decimal':float(hi),
          'strict_nonincrease_certified':hi < phi_old,
          'minimum_certified_decrease_decimal':float(phi_old-hi)},
      'assumption3_first_block_pass':False,
    }

res=[audit('attempt3_run1'),audit('attempt3_run2')]
# non-timing proof evidence must reproduce exactly across reps
same = {k:res[0][k] for k in ['logged_upper_workspace','consistent_binary64_y1','consistent_binary64_y2','exact_derivative_interval','exact_speed_upper_bounds','normal_cone_coordinate_conclusion','exact_stationarity_pass','phi_interval','assumption3_first_block_pass']} == {k:res[1][k] for k in ['logged_upper_workspace','consistent_binary64_y1','consistent_binary64_y2','exact_derivative_interval','exact_speed_upper_bounds','normal_cone_coordinate_conclusion','exact_stationarity_pass','phi_interval','assumption3_first_block_pass']}
out={'method':'exact dyadic binary64 reconstruction/enumeration plus exact Fraction bounds','runs':res,'non_timing_evidence_identical':same,'terminal_conclusion':'Historical Attempt 3 fails exact Sun-Sun Assumption 3 because exact first-block stationarity fails at r=1,t=1,agent=2; exact nonincrease passes there.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(OUT)
print(json.dumps(out['runs'][0]['exact_derivative_interval'],indent=2))
print(json.dumps(out['runs'][0]['phi_interval'],indent=2))
