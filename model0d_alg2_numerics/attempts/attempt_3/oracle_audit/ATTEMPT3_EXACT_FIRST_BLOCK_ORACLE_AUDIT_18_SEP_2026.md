# Attempt 3 — exact first-block oracle audit

**Scientific date:** 18 September 2026  
**Closure synchronization:** 19 September 2026  
**Research:** Constraint Consensus-Based Dynamics for Decentralized Path Planning in UAV Swarms  
**Scope:** post-hoc audit of immutable saved Attempt-3 evidence. **No simulation rerun, no solver rerun, no retuning.**

## 1. Question

The finite experiment accepted local first-block candidates through frozen feasibility, multiplier, complementarity, stationarity-residual and descent diagnostics. Sun--Sun Assumption 3 is stronger: each accepted first-block point must be an **exact stationary point** of the current first-block problem and satisfy exact augmented-Lagrangian nonincrease.

The audit question is therefore:

> Can the exact binary64 first-block iterates that were actually used by Attempt 3 satisfy the exact normal-cone stationarity and nonincrease conditions?

A single exact counterexample at one accepted first-block update is sufficient to answer **no** for the historical execution.

## 2. Evidence point selected

Both official repetitions contain the same non-timing evidence at

\[
(r,t,a)=(1,1,2).
\]

For agent 2, the frozen baseline has no obstacle rows, no guardian UAV--UAV row, and no foreign-copy A1 row. Its local feasible set contains only source workspace and speed inequalities. At the first inner update,

\[
\rho^1=4,\qquad y_2^{1,0}=0,\qquad \xi_2^{1,0}=0,
\]

and the auxiliary trajectory is the stationary source-2 initialization. Therefore the first-block objective is

\[
\phi_2(z_2)=f_2(z_2)+2\|z_2-u^0\|^2.
\]

The archived event does not serialize the full first-block primal vector directly. It does, however, serialize all independently recomputed affine workspace rows. For the first two source-2 y-coordinates, the upper-workspace rows are

\[
\operatorname{fl}(p_{2,y}^{1}-3)=-4.995670274728392,
\]

\[
\operatorname{fl}(p_{2,y}^{2}-3)=-4.982681099161541.
\]

This is enough for an exact IEEE-754 rounding-cell proof. No unique reconstruction of a hidden binary64 coordinate is assumed.

## 3. Exact rounding-cell reconstruction

Enumerating the binary64 values that reproduce the two logged affine rows gives

\[
p_{2,y}^{1}\in\{-1.995670274728392,\,-1.9956702747283919,\,-1.9956702747283916,\,-1.9956702747283914,\,-1.9956702747283912\},
\]

and

\[
p_{2,y}^{2}\in\{-1.9826810991615411,\,-1.982681099161541,\,-1.9826810991615407,\,-1.9826810991615405,\,-1.9826810991615402\}.
\]

An independent derivation uses exact rounding cells instead of candidate enumeration and produces the same extrema.

For the first coordinate of every source-2 x-position, the corresponding upper workspace row is exactly `-3.0`. Hence

\[
|p_{2,x}^{k}|\le 2^{-52}
\]

for the coordinates needed below; this is the exact closed rounding-cell enclosure and is deliberately conservative at tie endpoints.

## 4. Exact inactivity of every constraint that can contribute to the chosen normal component

Consider the coordinate \(p_{2,y}^{1}\). Only three local constraint groups can depend on it:

1. the two workspace facets at sample 1;
2. the speed constraint for segment \(k=0\);
3. the speed constraint for segment \(k=1\).

The workspace inequalities are strict because every consistent value above lies strictly in \((-3,3)\).

The exact worst-case upper bounds for the speed rows, using the complete binary64/rounding-cell uncertainty compatible with the log, are

\[
g_{2,0}^{\mathrm{spd}}
\le
-\frac{11408475177437967442479836660827}
{20282409603651670423947251286016}
\approx -0.5624812534790724<0,
\]

and

\[
g_{2,1}^{\mathrm{spd}}
\le
-\frac{2851358345159962184494201477051}
{5070602400912917605986812821504}
\approx -0.5623312813180935<0.
\]

Therefore **every local inequality that depends on \(p_{2,y}^{1}\) is strictly inactive**.
All other agent-2 inequalities are independent of this coordinate. Consequently every exact normal

\[
n\in N_{X_2}(z_2^{1,1})
\]

has

\[
\boxed{n_{p_{2,y}^{1}}=0.}
\]

Equivalently, a sufficiently small motion in both \(\pm p_{2,y}^{1}\) directions remains locally feasible while all other coordinates are fixed, so no exact normal can have a component along that coordinate.

## 5. Exact first-block gradient contradiction

For this first-block problem, with \(p_{2,y}^{0}=-2\), terminal/regularization weights from the frozen scenario, and \(\rho^1=4\), the derivative in the selected coordinate is

\[
\frac{\partial\phi_2}{\partial p_{2,y}^{1}}
=
8p_{2,y}^{1}-2p_{2,y}^{2}+12.
\]

Over **every** binary64 pair compatible with the immutable logged workspace rows, exact rational arithmetic gives

\[
\boxed{
\frac{558383}{1125899906842624}
\le
\frac{\partial\phi_2}{\partial p_{2,y}^{1}}
\le
\frac{558393}{1125899906842624}
}
\]

or numerically

\[
4.95943730527415\times10^{-10}
\le
\frac{\partial\phi_2}{\partial p_{2,y}^{1}}
\le
4.95952612311612\times10^{-10}.
\]

The lower bound is strictly positive. Since every admissible exact normal has zero component in the same coordinate,

\[
0\notin \nabla\phi_2(z_2^{1,1})+N_{X_2}(z_2^{1,1}).
\]

Thus the exact first-block stationarity part of Sun--Sun Assumption 3 **fails** at this accepted update.

## 6. Exact nonincrease at the same update

The second part of Assumption 3 is checked separately rather than inferred from the logged finite `R_desc=0`.

At the stationary initialization,

\[
\phi_2(z_2^{1,0})=320.
\]

Using exact rational outward bounds induced by the archived binary64 workspace rows for all 16 free source-2 coordinates gives

\[
55.15977310579321\ldots
\le
\phi_2(z_2^{1,1})
\le
55.15977310579322\ldots <320.
\]

Therefore exact nonincrease passes, with certified decrease greater than \(264.8402268942\).

The failure is specifically **exact stationarity**, not descent.

## 7. Repetition and sufficiency

The relevant non-timing evidence is identical in `attempt3_run1` and `attempt3_run2`; the two independent audit scripts reproduce the same exact bounds for both official repetitions.

Sun--Sun Assumption 3 requires the first-block oracle condition at every required first-block update. Therefore one proven failure is sufficient:

\[
\boxed{
\text{Historical Attempt 3 does not satisfy original exact Sun--Sun Assumption 3 as executed.}
}
\]

No audit of later first-block points can reverse this conclusion.

## 8. Final status consequence

This result **does not** invalidate TCC, the Sun--Sun source algorithm, the frozen finite protocol, U3, U4, or the numerical utility of Attempt 3. It establishes the correct certification boundary for the historical binary64 execution:

```text
FINITE_FIRST_BLOCK_EXACT_ORACLE_CERTIFIED = false
SUNSUN_ALGORITHMICALLY_CERTIFIED          = false
FULLY_CERTIFIED_MODEL0D_SUNSUN_RESULT     = false
```

The run remains a reproducible finite numerical Model-0D/TCC success under the frozen finite wrapper, with TCC consistency and exact deterministic physical-safety certification. A future theorem-faithful exact/certified first-block oracle or a separately proved inexact extension is future work and is **not** part of this presentation-stage closure.

## 9. Machine-checkable evidence

- `audit_exact_first_block.py`: exact dyadic candidate enumeration and exact rational objective/constraint bounds.
- `ATTEMPT3_EXACT_FIRST_BLOCK_ORACLE_AUDIT_RESULTS.json`: primary results for both official repetitions.
- `audit_first_block_rounding_cells_independent.py`: independent exact IEEE-754 rounding-cell derivation without candidate enumeration.
- `ATTEMPT3_EXACT_FIRST_BLOCK_ORACLE_INDEPENDENT_AUDIT.json`: independent result.

No solver or simulation is called by either audit script.
