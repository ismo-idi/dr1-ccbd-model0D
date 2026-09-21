# Model 0-D — Attempt 3 Checkpoint C Execution Record

**Date:** 18 September 2026  
**Role:** DAILY WORKER  
**Route:** A — finite-cap isolation  
**Frozen change:** `algorithm.max_inner_iterations: 100 -> 1000` only  
**Official repetitions:** `attempt3_run1`, `attempt3_run2`  
**Checkpoint-C status:** **EXECUTED — BOTH OFFICIAL REPETITIONS RETURNED `FINITE_OUTER_STOP`**

## 1. Pre-execution integrity

The live GitHub branch was rechecked immediately before execution and remained at:

`79cd3aa4bfeabc12ea3eeb2649b1e3d341ce6f1c` — `Finalize post-meeting harmonization structure and timetable status`.

The frozen Checkpoint-A/B manifest verified successfully. The pre-run freeze verifier returned `overall_pass: true`. The execution package was reconstructed from the frozen ZIP. Because ZIP does not retain an empty unlisted directory, an empty `runs/` directory was created operationally before verification; no source/configuration file was changed.

## 2. Infrastructure interruption before the official repetitions

An initial launch of the frozen Run-1 command was terminated externally by the ChatGPT container command-time limit before the program reached its own finalization path. Only `config.json` and `environment.json` had been persisted; no `events.jsonl`, `summary.json`, or `final_state.npz` existed, and no scientific result was available or inspected.

That partial artifact is preserved under `execution_provenance/infrastructure_abort_before_official_run1/`. It is **not counted as an Attempt-3 repetition**. No source/configuration file was changed. The official repetitions were then launched asynchronously so that the external command-return limit could not terminate the scientific process.

## 3. Official Run 1

Frozen command and environment were used unchanged. Direct worker output:

- termination: `FINITE_OUTER_STOP`
- primary cause: none
- all causes: empty
- elapsed time: `155.981345626 s`
- final complete state: outer `r=10`, inner `t=3`
- final `beta=4`, `rho=8`

The first outer iteration required **211 inner iterations**, which is already greater than Attempt 2's old cap of 100.

## 4. Official Run 2

Before Run 2, source/configuration SHA-256 identities were compared with the pre-Run-1 identities and showed **zero drift**. No code/configuration change or result-driven retuning occurred between repetitions.

Direct worker output:

- termination: `FINITE_OUTER_STOP`
- primary cause: none
- all causes: empty
- elapsed time: `151.483544788 s`
- final complete state: outer `r=10`, inner `t=3`
- final `beta=4`, `rho=8`

## 5. Recorded outer progression

Both official repetitions recorded the same complete-outer sequence:

| Outer r | Inner t at completion | xi norm | R_TCC,eq (m) | R_target (m) | physical numeric pass | outer predicate |
|---:|---:|---:|---:|---:|:---:|:---:|
| 1 | 211 | 9.028962e-2 | 1.276890e-1 | 9.028975e-2 | no | no |
| 2 | 202 | 1.746146e-2 | 2.469400e-2 | 1.746130e-2 | no | no |
| 3 | 164 | 3.645465e-3 | 5.155309e-3 | 3.645354e-3 | no | no |
| 4 | 121 | 7.715252e-4 | 1.090981e-3 | 7.714401e-4 | no | no |
| 5 | 79 | 1.628940e-4 | 2.302719e-4 | 1.628268e-4 | no | no |
| 6 | 42 | 3.389894e-5 | 4.786207e-5 | 3.384359e-5 | no | no |
| 7 | 18 | 6.802222e-6 | 9.533952e-6 | 6.741522e-6 | no | no |
| 8 | 8 | 1.283382e-6 | 1.700614e-6 | 1.202516e-6 | no | no |
| 9 | 5 | 3.963968e-7 | 6.408606e-7 | 4.531568e-7 | yes | yes (1st consecutive) |
| 10 | 3 | 5.181917e-7 | 7.850017e-7 | 5.550800e-7 | yes | yes (2nd consecutive) |

Total complete inner iterations across outer iterations: **853**.

## 6. Final recorded finite statuses

Both repetitions recorded exactly the same final scientific quantities:

- `NUMERICALLY_VALID = true`
- `TCC_CONSISTENT = true`
- `PHYSICAL_POSTCHECK_NUMERIC_PASS = true`
- `MODEL0D_SAFETY_CERTIFIED = false`
- `SUNSUN_ALGORITHMICALLY_CERTIFIED = false`
- `FULLY_CERTIFIED_MODEL0D_SUNSUN_RESULT = false`
- `U3 = CONDITIONAL`
- `U4 = UNSELECTED`

Final finite TCC quantities:

- `R_TCC_eq = 7.850016699224997e-07 m <= 1e-6 m`
- `R_target = 5.550800040449635e-07 m <= 1e-6 m`
- final `||xi|| = 5.181917114188811e-07 <= 1e-6`

Final ordinary-floating-point physical postcheck:

- workspace minimum margin: `1.0229604892253026 m`
- speed minimum margin: `0.21445581216584575 m`
- UAV clearance minimum margin: `5.49336685584656e-07 m`
- obstacle family: verified empty

The positive UAV margin is **very small** and remains an ordinary floating-point diagnostic only. U4 is unresolved, so this cannot be promoted to exact Model-0D safety certification.

Final objective:

- `F = 4.0157423760136215`
- goal error UAV 1: `0.023025503186993156 m`
- goal error UAV 2: `0.02664019998163306 m`

## 7. Direct repeat-agreement check

A standalone saved-output comparison, importing no solver implementation, found:

- termination reason: exact equal
- primary/all causes: exact equal
- configuration files: exact equal
- environment records: exact equal
- final-state arrays: **bit-for-bit exact equal**
- maximum final-state absolute difference: **0.0**
- event counts: `864` vs `864`
- sanitized event history (excluding timing): exact equal
- sanitized summary (excluding timing/output path): exact equal
- inherited `atol=1e-10`, `rtol=1e-10`: passed

This establishes direct same-environment repetition consistency for Checkpoint C. The broader independent scientific/saved-evidence verification and three-attempt interpretation remain Checkpoint D and have not been completed in this record.

## 8. Checkpoint-C interpretation boundary

The direct worker evidence supports the finite statement that the unchanged Attempt-2 realization, when allowed a per-outer inner cap of 1000 instead of 100, reached the inherited finite outer stop in both official repetitions. It also directly shows that outer iteration 1 required 211 inner iterations, so the previous 100-iteration cap was insufficient for that first inner solve under the same inherited configuration.

This does **not** establish a general convergence theorem, global optimality, exact Sun–Sun first-block certification, exact physical safety certification, distributed-network performance, or flight safety. No obstacle scenario or Attempt 4 is authorized or executed.

**Execution is now stopped at the Checkpoint C -> D gate.**
