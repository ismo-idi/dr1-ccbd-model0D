# Attempt 3 — final closure report

**Scientific closure:** 18 September 2026  
**Repository synchronization:** 19 September 2026  
**Researcher / final scientific authority:** Ismaël Assoumane Idi  
**Branch baseline used by the experiment:** `79cd3aa4bfeabc12ea3eeb2649b1e3d341ce6f1c`  
**Scenario:** `N=2`, `q=2`, `K=8`, zero obstacles, frozen crossing geometry  
**No Attempt-3 rerun was performed during U3/U4/oracle closure.**

## 1. Controlled scientific question

Attempt 3 was the final authorized numerical attempt. Relative to Attempt 2, the sole scientific/executable change was

```text
max_inner_iterations: 100 -> 1000
```

Everything else was inherited: physical problem, TCC architecture, solver/backend, diagnostics, tolerances, update equations, maximum outer iterations, 600 s wall-clock cap, and zero retries. The question was whether the Attempt-2 cap of 100 inner iterations was an active blocker under the frozen scenario.

## 2. Reproducible execution result

Two fresh-process official repetitions completed successfully:

| Run | Termination | Final `(r,t)` | Elapsed |
|---|---|---:|---:|
| `attempt3_run1` | `FINITE_OUTER_STOP` | `(10,3)` | 155.981345626 s |
| `attempt3_run2` | `FINITE_OUTER_STOP` | `(10,3)` | 151.483544788 s |

The saved final-state arrays are byte-identical and have SHA-256

```text
d444e1d5df70c64639f5a3f0de1445bc82150ec9797a7b9533a76feebed58e46
```

The sanitized histories/summaries agree after timing fields are excluded. The pre-official synchronous process killed by the external execution infrastructure is preserved separately as an infrastructure abort and is not counted as a scientific repetition.

## 3. Outer progression

| `r` | terminating inner `t` | `||xi||` | `R_TCC,eq` (m) | `R_target` (m) | finite physical postcheck | frozen outer predicate |
|---:|---:|---:|---:|---:|:---:|:---:|
| 1 | 211 | 9.028962253367044e-2 | 1.2768898917888183e-1 | 9.028975013124303e-2 | false | false |
| 2 | 202 | 1.7461463312267986e-2 | 2.4694004025418662e-2 | 1.746129770102144e-2 | false | false |
| 3 | 164 | 3.645464643064285e-3 | 5.155309106016253e-3 | 3.6453540279768504e-3 | false | false |
| 4 | 121 | 7.715252249663599e-4 | 1.0909810971517794e-3 | 7.714401319423628e-4 | false | false |
| 5 | 79 | 1.628939614843912e-4 | 2.302719353329657e-4 | 1.628268469908902e-4 | false | false |
| 6 | 42 | 3.389893843838477e-5 | 4.786206784085708e-5 | 3.384359273188062e-5 | false | false |
| 7 | 18 | 6.802221596989993e-6 | 9.533951795113956e-6 | 6.741521965830736e-6 | false | false |
| 8 | 8 | 1.283381764762773e-6 | 1.7006142757418199e-6 | 1.2025158865596899e-6 | false | false |
| 9 | 5 | 3.963968424180342e-7 | 6.408605500628833e-7 | 4.5315684074440574e-7 | true | true (1st) |
| 10 | 3 | 5.181917114188811e-7 | 7.850016699224997e-7 | 5.550800040449635e-7 | true | true (2nd) |

Total complete inner iterations: **853**.

Because the first outer solve required 211 inner iterations, the old Attempt-2 cap of 100 is directly shown to have been insufficient for this frozen scenario. This is a scenario-specific finite result, not a convergence theorem.

## 4. Final finite numerical state

At `(r,t)=(10,3)`:

```text
R1 = 9.780703313666428e-06
R2 = 2.6597130100645397e-15
R3 = 4.157895314285983e-08
```

The `r=10` thresholds are `1e-5`, `1e-5`, `1e-7`, so all pass. Direct finite agreement also passes:

```text
R_TCC_eq  = 7.850016699224997e-07 m < 1e-6 m
R_target  = 5.550800040449635e-07 m < 1e-6 m
||xi||    = 5.181917114188811e-07
```

Integrity:

```text
R_id      = 2.994713704459715e-22
R_rhobeta = 0
```

Objective/terminal diagnostics:

```text
F            = 4.0157423760136215
f1           = 2.0078734359074213
f2           = 2.0078689401062
goal_error_1 = 0.023025503186993156 m
goal_error_2 = 0.02664019998163306 m
```

These objective values are descriptive. No global-optimality conclusion follows.

## 5. U4 — exact deterministic physical safety

Ordinary floating-point postchecking gave a smallest required-clearance margin of approximately `+5.49336685584656e-7 m`, which was too close to zero to convert into an exact-safety claim by tolerance alone.

The researcher approved U4-E1 exact-rational certification and an independent U4-E2 directed-rounding interval audit. Both official saved trajectories pass complete U4 evaluation.

The critical exact UAV squared-margin is

\[
\frac{2359246339737244210484930680683636361274901726413405985560497}
{5368394241616423559259674901405253777730294016954048679647169740800}>0.
\]

Therefore

```text
MODEL0D_SAFETY_CERTIFIED = true
U4 = RESOLVED_FOR_ATTEMPT3_BY_U4_E1_WITH_U4_E2_INDEPENDENT_AUDIT
```

The obstacle family is verified empty, so this campaign does not validate nonempty-obstacle numerical performance.

The first interval-audit implementation was rejected after it failed to enclose the exact-rational result. The bug and invalid outputs are preserved. The corrected audit uses an exact sign-change operation and then encloses the exact value with strictly positive lower bound. This QA correction is part of the evidence.

## 6. U3 — actual Algorithm-2 dual-sequence condition

U3 is resolved by the researcher-approved Route-A theorem. Under a smooth feasible primal limit satisfying split-TCC MFCQ and the actual exact-source approximate-stationarity relations, an abnormal-multiplier normalization argument proves boundedness of the **actual** Algorithm-2 equality multiplier sequence. Hence a matching convergent dual subsequence exists.

At the exact Attempt-3 lift all physical inequalities are strictly inactive, A1 is strictly inactive, and the split equality block is full row rank. Therefore the MFCQ premise holds exactly at that candidate lift.

```text
U3 = RESOLVED_BY_ROUTE_A_MFCQ_ACTUAL_SEQUENCE
```

This resolves the old actual-`y` sequence-identification gap. It does not certify the finite first-block IPOPT candidates.

## 7. Exact first-block Assumption-3 audit — terminal negative result

A post-hoc audit asked whether the historical binary64 first-block iterates themselves satisfy original Sun--Sun Assumption 3 exactly. No solver or simulation was rerun.

At the first accepted agent-2 first-block update `(r,t,a)=(1,1,2)`, immutable affine workspace residuals and exact IEEE-754 rounding-cell semantics imply

\[
\frac{558383}{1125899906842624}
\le
\frac{\partial\phi_2}{\partial p_{2,y}^{1}}
\le
\frac{558393}{1125899906842624},
\]

whose lower endpoint is approximately `4.95943730527415e-10 > 0`.

Every constraint that can contribute to the normal component in that coordinate is exactly strictly inactive. In particular, exact worst-case speed-row upper bounds are approximately

```text
k=0: -0.5624812534790724 < 0
k=1: -0.5623312813180935 < 0
```

and the workspace rows are strict. Every exact local normal therefore has zero component along `p2_y1`. Exact stationarity is impossible:

\[
0\notin\nabla\phi_2(z_2^{1,1})+N_{X_2}(z_2^{1,1}).
\]

Exact nonincrease passes independently: an exact outward rational enclosure gives

\[
\phi_2(z_2^{1,1})<55.15977310579323<320=\phi_2(z_2^{1,0}).
\]

Thus the historical execution fails original Assumption 3 **through exact stationarity**, not through nonincrease. The independent audit, using rounding cells rather than candidate enumeration, reproduces the same conclusion in both official repetitions.

One failed required first-block call is sufficient for the historical execution.

## 8. Terminal status vector

```text
NUMERICALLY_VALID                     = true
TCC_CONSISTENT                        = true
PHYSICAL_POSTCHECK_NUMERIC_PASS       = true
MODEL0D_SAFETY_CERTIFIED              = true
U3                                    = RESOLVED_BY_ROUTE_A_MFCQ_ACTUAL_SEQUENCE
U4                                    = RESOLVED_FOR_ATTEMPT3_BY_U4_E1_WITH_U4_E2_INDEPENDENT_AUDIT
FINITE_FIRST_BLOCK_EXACT_ORACLE       = false
SUNSUN_ALGORITHMICALLY_CERTIFIED      = false
FULLY_CERTIFIED_MODEL0D_SUNSUN_RESULT = false
```

The final two `false` values are now a **proved negative status for this historical binary64 run**, not merely an uncompleted proof obligation.

## 9. Three-attempt scientific interpretation

| Attempt | Controlled state | Outcome | Principal lesson |
|---|---|---|---|
| 1 | Original finite diagnostic | stopped at `r1,t17`; last complete `t16` | original finite multiplier-sign rule rejected a strict-inactive row |
| 2 | Activity-aware finite diagnostic amendment; cap 100 | all candidate finite diagnostics pass, but cap reached; TCC incomplete; required-clearance violation | finite diagnostic blocker removed; cap/TCC/source-safety remained blockers |
| 3 | **Only cap 100 -> 1000** | reproducible finite outer stop; TCC consistent; exact saved-plan physical safety | cap 100 was active for this scenario; finite numerical success obtained; exact Assumption 3 still not satisfied by executed binary64 first block |

Attempt 2's minimum source center distance was approximately `0.286132298 m`; against required clearance `0.4 m`, this is a required-clearance violation. The combined modeled body radii were `0.2 m`, so body overlap was **not** demonstrated.

## 10. What is and is not closed

The presentation-stage three-attempt numerical campaign is closed. There is no Attempt 4 in this path and no outcome-driven retuning.

The supported presentation statement is:

> **Attempt 3 is a reproducible finite numerical Model-0D/TCC success. It reaches the frozen finite outer stop, passes finite TCC consistency and numerical-integrity requirements, and its immutable deterministic source trajectory is rigorously physically safety-certified. U3 and U4 are resolved. The historical binary64 first-block sequence, however, is proved not to satisfy original exact Sun--Sun Assumption 3, so exact Sun--Sun algorithmic/full certification remains future research.**

Future investigation of a theorem-faithful certified first-block oracle or a separately proved inexact Sun--Sun extension is explicitly deferred until after the presentation.
