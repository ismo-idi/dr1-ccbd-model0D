# Attempt 3 — final presentation-stage Model 0-D numerical attempt

**Scientific execution date:** 18 September 2026  
**Closure synchronization:** 19 September 2026  
**Scenario:** `baseline_2uav_0obs`  
**Status:** **CLOSED — reproducible finite numerical success under the frozen wrapper; not an exact Sun–Sun Assumption-3 execution**

## Controlled change

Attempt 3 changed exactly one scientific/executable protocol parameter relative to Attempt 2:

```text
max_inner_iterations: 100 -> 1000
```

The physical scenario, TCC structure, algorithmic update formulas, finite diagnostic thresholds, backend/options, outer cap, wall-time cap and retry policy were otherwise frozen. No obstacle case was executed in Attempt 3.

## Official execution

Two official fresh-process repetitions were executed. Both returned `FINITE_OUTER_STOP` at `(r,t)=(10,3)` after 853 complete inner iterations. The first outer iteration required 211 inner iterations, so the historical cap 100 was an active blocker for this frozen scenario. The two saved `final_state.npz` files are byte-identical.

The earlier synchronous process killed by external tool timeout occurred before the official run accounting. Its partial configuration/environment evidence is preserved in the original Checkpoint-C package and explicitly excluded from the two official repetitions.

## Final finite status

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

The first four positive results and U3/U4 resolutions do **not** override the exact first-block result. The terminal post-hoc audit proves that the historical binary64 first-block candidate at `(r,t,a)=(1,1,2)` fails original Sun–Sun Assumption-3 stationarity, while exact nonincrease passes at the same update.

## Navigation

- `ATTEMPT3_PROTOCOL_FREEZE_18_SEP_2026.md` — pre-execution scientific freeze.
- `ATTEMPT3_CHECKPOINT_AB_READINESS_18_SEP_2026.md` — readiness gate.
- `ATTEMPT3_CHECKPOINT_C_EXECUTION_RECORD_18_SEP_2026.md` — official execution provenance and run accounting.
- `FINAL_ATTEMPT3_CLOSURE_REPORT_18_SEP_2026.md` — current Attempt-3 conclusion.
- `runs/` — compact committed evidence for both official repetitions: config, environment, immutable final state and compact summary.
- `RAW_EXECUTION_EVIDENCE_MANIFEST.json` — SHA-256/size map for the complete raw `events.jsonl` and `summary.json` evidence preserved in the immutable Checkpoint-C package.
- `src/`, `tests/`, `configs/`, `verification/`, `provenance/` — frozen implementation/readiness evidence.
- `oracle_audit/` — exact negative Assumption-3 audit, independent audit, scripts and machine-readable results.
- `certification/u3/` — U3 Route-A proof and independent logical audit.
- `certification/u4/` — U4 exact-rational certificate, independent interval audit and QA provenance.

## Evidence-size policy

The complete raw Attempt-3 event and summary logs are tens of megabytes per run. To keep the repository closure navigable, the repository stores the exact source/config/test snapshot, both immutable final states, compact summaries, execution provenance and all post-certification material. The complete raw logs remain losslessly preserved in `Attempt3_CheckpointC_Execution_18SEP2026.tar.gz`; their exact SHA-256 identities and byte sizes are recorded in `RAW_EXECUTION_EVIDENCE_MANIFEST.json`.

This storage decision does not change any scientific result and does not rerun the experiment.

## Attempt 2 versus Attempt 3 — complete comparison

**Added by the independent-audit correction of 20 September 2026, so that the difference between the two attempts is unambiguous.** Every row was verified by direct file comparison.

| Item | Attempt 2 | Attempt 3 |
|---|---|---|
| `algorithm.max_inner_iterations` | `100` | **`1000`** |
| `src/config.py` | — | identical except the same cap default (`100 -> 1000`); verified by `diff`, one changed line |
| `src/geometry.py`, `src/tcc.py`, `src/local_nlp.py`, `src/sunsun_algorithm2.py`, `src/diagnostics.py`, `src/io_utils.py`, `src/__init__.py` | — | **byte-identical** |
| `run_experiment.py` | — | **byte-identical** |
| configuration: physical data, TCC structure, thresholds, backend and options, outer cap, wall-clock cap, retries | — | identical; only the cap value and descriptive metadata differ |
| tests | 56 | **58** |
| tests added | — | `test_attempt3_cap_is_frozen_at_1000_and_attempt_metadata_is_present`, `test_attempt3_cap_drift_is_rejected` — both in `tests/test_config_freeze.py`, both guarding the single experimental change |
| test source formatting | expanded | condensed — **cosmetic only**; this is why a plain `diff` of `tests/` reports every file as changed |
| Outcome | `MAX_INNER_ITERATIONS` at `(r,t)=(1,100)`; no completed outer iteration; `TCC_NOT_ACCEPTED`; `PHYSICAL_VIOLATION_DETECTED` | `FINITE_OUTER_STOP` at `(r,t)=(10,3)`; 853 complete inner iterations; TCC consistent; saved plan exactly safety-certified |
| Source-side minimum UAV clearance margin | `-0.1139 m` (**violation**) | `+5.4934e-07 m` |
| `R_TCC_eq` | `0.1258 m` | `7.850016699224997e-07 m` |

Tests do not participate in an executed run: they are pre-run component verification. The two added tests exist only to make the single experimental change tamper-evident, so they strengthen rather than weaken the single-change claim.

Note the last two rows together. In both attempts the magnitude of the source-side margin is of the order of the TCC disagreement, and only the **sign** differs. That relationship is proved and quantified in [Decision 17, Section 10](../../../decisions/17_U4_exact_physical_safety_certification.md).

## The one-obstacle scenario: pre-registered, gated, not executed

**Added by the independent-audit correction of 20 September 2026.**

`configs/obstacle_2uav_1obs.json` is present in all three attempts. The numerical protocol froze it **before any baseline outcome was inspected** (`MODEL0D_NUMERICAL_PROTOCOL_AND_READINESS_V1_0_11_SEP_2026.md`, Section 4: *"This scenario is selected before any baseline result is inspected."*) and made its execution conditional on the baseline gate. The gate never opened within the campaign budget, so the scenario was **never executed**. Attempt 3 ran with `obstacles: []`.

This is genuine **pre-registration** and is a methodological strength: it demonstrates that the obstacle case was fixed in advance rather than designed after seeing what worked. The configuration is therefore retained, not deleted.

The consequence must be stated plainly and first: the exact segment-to-obstacle machinery — the constraint family `g_{i,o,k}^{obs,seg}`, its multiplier family `xi_{i,o,k}^{obs}`, and the guarded fixed-centre closest-point branches — is **specified, unit-tested and unexercised end-to-end**. The obstacle family is verified empty in every Attempt-3 evaluator, and a verified empty family passes vacuously. No conclusion about nonempty-obstacle solver behaviour, conditioning or safety follows from this campaign.

```text
OBSTACLE_SCENARIO = PRE_REGISTERED_BEFORE_BASELINE_INSPECTION
OBSTACLE_SCENARIO_EXECUTED = false
OBSTACLE_CODE_PATH_VALIDATED_END_TO_END = false
```
