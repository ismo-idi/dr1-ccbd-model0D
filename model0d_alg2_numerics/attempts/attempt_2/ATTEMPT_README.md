# Attempt 2 — activity-aware finite diagnostic

> **Naming update — 17 September 2026.** Attempt 2 is the current name of the historical Attempt 2A; the next planned attempt is Attempt 3. [Naming and evidence-preservation map](../../provenance/ATTEMPT_NAMING_17_SEP_2026.md). Dated campaign conclusions and historical identifiers retain their original scope.


**Primary runs:** `runs/attempt2a_run1/`, `runs/attempt2a_run2/`.  
**Recorded date:** 13 September 2026.  
**Outcome:** cap reached at `(r,t)=(1,100)`; no completed outer iteration; TCC and actual-source safety-clearance checks failed.

Read the [canonical final campaign report](../../FINAL_SIMULATION_CAMPAIGN_REPORT_13_SEP_2026.md), [diagnostic amendment](ATTEMPT2A_PROTOCOL_AMENDMENT_13_SEP_2026.md), [original report](ATTEMPT2A_BASELINE_REPORT_13_SEP_2026.md) and [machine summary](ATTEMPT2A_MACHINE_SUMMARY.json). Source, configuration, tests, evidence and figures are this attempt's exact snapshot.

The original delivery was cumulative: its `runs/baseline_run1/2`, `plots/` and Step-3 records are unchanged historical copies of Attempt 1. They do not count as new experiments. Attempt 2 figures are in `plots_attempt2a/`; its verification is in `verification_attempt2a/`.

The original report's phrase “actual sources collide” (§8.1) is superseded by **required safety-clearance violation of planned trajectories**: minimum separation 0.286132 m, required clearance 0.4 m, body-radius sum 0.2 m. Its “false rejection” phrase is superseded by **rejection under the original diagnostic, removed under a disclosed amended diagnostic**. The original proposals for Attempt 2A.1/2B remain unexecuted, and no Model 1 is defined by them. These clarifications preserve original evidence rather than rewriting it.

Large summaries/event logs are losslessly compressed. Follow the root [reproducibility guide](../../REPRODUCIBILITY.md). Use this attempt's source when reproducing Attempt 2; it does not reproduce Attempt 1's original acceptance rule. No new run is authorized now.

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
