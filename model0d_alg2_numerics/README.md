# Model 0-D numerical campaign — final three-attempt closure

> **Current closure — 19 September 2026.** Attempts 1–3 are complete. Attempt 2 is the current name of historical Attempt 2A; raw `attempt2a_*` identifiers are preserved as evidence. The 13 September report remains the historical closure of Attempts 1–2 and is superseded only as a **current campaign-status document**, not rewritten.

Start with [the final three-attempt report](FINAL_SIMULATION_CAMPAIGN_REPORT_18_SEP_2026.md).

| Location | Purpose |
|---|---|
| [Final three-attempt report](FINAL_SIMULATION_CAMPAIGN_REPORT_18_SEP_2026.md) | Current results, chronology, U3/U4 closure, terminal exact first-block audit and final status vector |
| [Historical Attempts 1–2 report](FINAL_SIMULATION_CAMPAIGN_REPORT_13_SEP_2026.md) | Immutable dated interpretation before Attempt 3 |
| [Attempt 1](attempts/attempt_1/ATTEMPT_README.md) | Original finite diagnostic; abort at attempted inner iteration 17; last complete state 16 |
| [Attempt 2](attempts/attempt_2/ATTEMPT_README.md) | Activity-aware finite diagnostic amendment; inner cap 100; TCC incomplete; required-clearance violation |
| [Attempt 3](attempts/attempt_3/FINAL_ATTEMPT3_CLOSURE_REPORT_18_SEP_2026.md) | Cap-isolation attempt; two official repetitions; U3/U4 post-certification; terminal exact oracle audit |
| [Attempt-3 exact first-block audit](attempts/attempt_3/ATTEMPT3_EXACT_FIRST_BLOCK_ORACLE_AUDIT_18_SEP_2026.md) | Exact proof that historical binary64 Assumption-3 stationarity fails at `r=1,t=1,a=2` |
| [Attempt-3 independent oracle audit](attempts/attempt_3/ATTEMPT3_EXACT_FIRST_BLOCK_ORACLE_INDEPENDENT_AUDIT_18_SEP_2026.md) | Independent exact rounding-cell verification |
| [Reproducibility](REPRODUCIBILITY.md) | Historical archive restoration and reproduction guidance |
| [Attempt naming map](provenance/ATTEMPT_NAMING_17_SEP_2026.md) | Attempt-2 / Attempt-2A evidence naming |

## Final controlled campaign outcome

Attempt 3 changed only

```text
max_inner_iterations: 100 -> 1000
```

relative to Attempt 2. Both official fresh-process repetitions reached `FINITE_OUTER_STOP` at `(r,t)=(10,3)`. The first outer solve required 211 inner iterations, directly showing that cap 100 was an active blocker for this frozen scenario. Final arrays are bit-identical across repetitions.

Final finite agreement:

```text
R_TCC_eq = 7.850016699224997e-07 m
R_target = 5.550800040449635e-07 m
```

Both are below the frozen `1e-6 m` thresholds.

U4 exact-rational certification plus the corrected independent interval audit proves `MODEL0D_SAFETY_CERTIFIED = true` for the immutable deterministic saved source trajectory. U3 is resolved by the actual Algorithm-2 multiplier-sequence/MFCQ theorem.

The final exact first-block audit then proves a different limitation: at the first accepted agent-2 first-block update, the exact gradient component is bounded below by

\[
\frac{558383}{1125899906842624}>0,
\]

while every exact normal has zero component in that coordinate. Therefore original Sun–Sun Assumption-3 stationarity fails for the historical binary64 execution. Exact nonincrease passes at the same point.

## Final claim boundary

```text
NUMERICALLY_VALID                     = true
TCC_CONSISTENT                        = true
MODEL0D_SAFETY_CERTIFIED              = true
U3                                    = resolved
U4                                    = resolved for Attempt 3
SUNSUN_ALGORITHMICALLY_CERTIFIED      = false
FULLY_CERTIFIED_MODEL0D_SUNSUN_RESULT = false
```

This is a successful finite numerical Model-0D/TCC result under the frozen experimental wrapper, **not** a theorem-certified exact execution of Sun–Sun Algorithm 2. The code remains single-process orchestration, not deployed distributed execution or flight validation. The zero-obstacle Attempt-3 scenario does not validate nonempty-obstacle performance.

No Attempt 4 or outcome-driven retuning belongs to this presentation-stage campaign.

---

**Obstacle scenario — pre-registered, not executed (independent-audit correction, 20 September 2026).** The one-obstacle configuration `obstacle_2uav_1obs.json` was frozen before any baseline outcome was inspected and gated on baseline success. The gate never opened within the campaign budget, so it was never executed and Attempt 3 ran with an empty obstacle registry. The pre-registration is retained as evidence. The consequence is that the exact segment-to-obstacle constraint family, its multiplier family and the guarded fixed-centre closest-point branches are specified, unit-tested and **unexercised end to end**; a verified empty family passes vacuously and supports no nonempty-obstacle conclusion.
