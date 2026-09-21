import casadi as ca
def test_ipopt_upper_bound_multiplier_sign():
    x=ca.MX.sym('x');nlp={'x':x,'f':(x-2)**2,'g':x-1};solver=ca.nlpsol('scalar_sign_test','ipopt',nlp,{'ipopt.print_level':0,'print_time':False,'ipopt.bound_relax_factor':0.0});sol=solver(x0=0.0,lbg=-ca.inf,ubg=0.0);xv=float(sol['x']);mu=float(sol['lam_g']);assert abs(xv-1.0)<=1e-7;assert mu>=0.0;assert abs(2.0*(xv-2.0)+mu)<=1e-6
