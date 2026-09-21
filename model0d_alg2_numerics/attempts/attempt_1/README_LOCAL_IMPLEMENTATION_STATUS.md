# Model 0-D Algorithm-2 numerics — local Step-2 verification state

**Date:** 11 September 2026  
**Status:** LOCAL / UNCOMMITTED / UNAUDITED IMPLEMENTATION WORK  
**Repository traceability baseline:** `de49211ddd924e4751b7303ec3f1f2949b16bb23`  
**Protocol:** researcher-approved `MODEL0D_NUMERICAL_PROTOCOL_AND_READINESS_V1_0_11_SEP_2026.md`

This local directory contains the smallest approved 2-UAV TCC / Sun--Sun
Algorithm-2 implementation together with the completed pre-baseline component
verification package.

Step 2 has passed locally. The complete component suite currently contains 53
tests and checks structure, dimensions, exact TCC split, exact segment geometry,
backend multiplier sign/order, stationary-lift feasibility, local derivative
consistency, Algorithm-2 algebraic updates, residual reductions, empty-family
semantics, physical source-trajectory postchecks, protocol/configuration locks,
deterministic execution guards, failure precedence, all major finalization exit
classes, non-finite logging, and the hover-initialized local first-block backend
interface.

No complete Model-0D Algorithm-2 baseline run has been executed or inspected in
this Step-2 package. The `runs/` directory is intentionally empty. One first-block
solve per UAV at the accepted hover initialization was executed strictly as the
protocol-required backend/component check; it was not interpreted as a baseline
experiment result.

Nothing in this Step-2 state has been committed. Per researcher instruction, any
future GitHub commit requires a fresh explicit permission request.

Scientific claim boundary remains:

- finite oracle diagnostics do not establish exact Sun--Sun source-oracle compliance;
- U3 remains conditional;
- U4 remains unselected;
- ordinary floating-point physical margins cannot establish `MODEL0D_SAFETY_CERTIFIED`;
- passing Step 2 establishes implementation readiness for the first bounded baseline
  experiment, not numerical validation of Model 0-D or the Sun--Sun convergence theory.
