import casadi as ca
import numpy as np
from scipy.optimize import minimize_scalar
from src.geometry import segment_min_squared_numeric,segment_min_squared_symbolic,obstacle_segment_constraint_numeric,uav_segment_constraint_numeric
def test_symbolic_and_numeric_exact_value_agree_random_cases():
 a=ca.MX.sym('a',2);d=ca.MX.sym('d',2);f=ca.Function('seg_value_test',[a,d],[segment_min_squared_symbolic(a,d)]);rng=np.random.default_rng(20260911);cases=[(np.array([2.,-1.]),np.zeros(2))]+[(rng.normal(size=2),rng.normal(size=2)) for _ in range(100)]
 for av,dv in cases:np.testing.assert_allclose(float(f(av,dv)),segment_min_squared_numeric(av,dv).min_squared_distance,atol=2e-12,rtol=2e-12)
def test_guarded_value_matches_independent_bounded_scalar_minimization():
 rng=np.random.default_rng(19092026)
 for _ in range(60):
  a=rng.normal(size=2);d=rng.normal(size=2);r=segment_min_squared_numeric(a,d);direct=minimize_scalar(lambda lam:float(np.dot(a+lam*d,a+lam*d)),bounds=(0.,1.),method='bounded',options={'xatol':1e-14});dc=min(float(direct.fun),float(np.dot(a,a)),float(np.dot(a+d,a+d)));assert abs(r.min_squared_distance-dc)<=2e-10
def test_obstacle_and_uav_wrapper_values_match_generic_segment_geometry():
 c=.55;go,ro=obstacle_segment_constraint_numeric([-1.,1.],[1.,1.],[0.,0.],c);assert ro.regime=='interior';np.testing.assert_allclose(ro.min_squared_distance,1.,atol=1e-14);np.testing.assert_allclose(go,c*c-1.,atol=1e-14);gu,ru=uav_segment_constraint_numeric([-1.,1.],[1.,1.],[0.,0.],[0.,0.],c);assert ru.regime=='interior';np.testing.assert_allclose(ru.min_squared_distance,1.,atol=1e-14);np.testing.assert_allclose(gu,c*c-1.,atol=1e-14)
