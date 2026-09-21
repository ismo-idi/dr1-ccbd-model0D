import casadi as ca
import numpy as np
def test_ipopt_constraint_multiplier_row_order_with_distinct_known_values():
 x=ca.MX.sym('x',2);g=ca.vertcat(x[0],x[1]);f=(x[0]-1)**2+2*(x[1]-1)**2;solver=ca.nlpsol('multiplier_order_test','ipopt',{'x':x,'f':f,'g':g},{'ipopt.print_level':0,'print_time':False,'ipopt.bound_relax_factor':0.0,'ipopt.tol':1e-11});sol=solver(x0=np.array([-0.5,-0.5]),lbg=np.array([-np.inf,-np.inf]),ubg=np.zeros(2));xv=np.asarray(sol['x'],float).reshape(-1);mu=np.asarray(sol['lam_g'],float).reshape(-1);np.testing.assert_allclose(xv,[0.0,0.0],atol=1e-7);np.testing.assert_allclose(mu,[2.0,4.0],atol=1e-5,rtol=1e-5)
