# Model 0-D — Attempt 3 Finite-Cap Isolation Protocol Freeze

**Date:** 18 September 2026  
**Role:** DAILY WORKER  
**Researcher / final scientific decision-maker:** Ismaël Assoumane Idi  
**Repository / branch:** `ismo-idi/CCBO_Model1` / `Model-0_24-Aug-2026`  
**Live branch HEAD rechecked before freeze:** `79cd3aa4bfeabc12ea3eeb2649b1e3d341ce6f1c` (`Finalize post-meeting harmonization structure and timetable status`)  
**Source numerical implementation:** current Attempt 2 package (`model0d_alg2_numerics/attempts/attempt_2/`)  
**Status:** **CHECKPOINT A FROZEN — NO ATTEMPT-3 EXPERIMENT HAS BEEN EXECUTED**

## 1. Scientific question

Attempt 3 tests one question only:

> Holding the Attempt-2 physical problem, TCC architecture, activity-aware finite multiplier diagnostic, backend, Algorithm-2 parameters, tolerances, stopping criteria, failure rules, and acceptance rules fixed, was the previously frozen `max_inner_iterations = 100` budget insufficient for the inner process to reach the already-existing acceptance conditions?

This is a finite experimental question. A success would not prove general convergence of Sun–Sun Algorithm 2; a failure would not disprove the algorithm, TCC, or Model 0-D.

## 2. Single experimental change

The sole scientific/executable change relative to Attempt 2 is

```text
algorithm.max_inner_iterations: 100 -> 1000
```

The Attempt-3 `src/config.py` is byte-identical to the Attempt-2 executable source after changing this one literal only. The exact unified diff is stored in `verification/attempt2_to_attempt3_config_py.diff`.

The baseline JSON also changes its human-readable description and adds an `attempt3` provenance object. Those metadata changes do not modify the model or numerical algorithm. The pre-run verifier confirms that the only non-metadata scientific configuration difference is the inner cap.

## 3. Why 1000 is frozen

`1000` is selected **before any Attempt-3 outcome exists** as a bounded 10× extension of the exact cap that stopped Attempt 2. It is large enough to test whether the 100-iteration ceiling was the immediate finite limitation without creating an open-ended “run until it works” experiment.

Attempt 2 required approximately 32 s for 100 inner iterations in its recorded environment. A purely linear timing extrapolation would be approximately 320 s for 1000 iterations, which is below the unchanged 600 s run wall-clock cap. This estimate is only a planning rationale: no linear runtime claim is made. If the unchanged 600 s wall-clock limit terminates Attempt 3 before 1000 iterations, `TIMEOUT` is a valid experimental result and the cap will not be increased again.

## 4. Quantities deliberately unchanged

The following remain inherited from Attempt 2 without outcome-driven retuning:

- physical scenario: 2 UAVs, 2D, 0 obstacles, the same crossing starts/goals;
- `K = 8`, `dt = 0.5 s`, 4 s horizon;
- workspace `[-3,3]^2`, A1 box `[-3.5,3.5]^2`;
- radii `0.1 m` each, UAV safety buffer `0.2 m`, required center clearance `0.4 m`;
- maximum speeds `1.5 m/s` each;
- objective weights `alpha = 20`, `beta_obj = 1` per UAV;
- TCC guardian/copy/equality/reduction-tree architecture;
- stationary exact-TCC initialization;
- activity-aware finite multiplier diagnostic introduced in Attempt 2, including preservation of raw backend multipliers;
- `beta0=1`, `vartheta=2`, `beta^1=2`, `omega=0.5`, `rho^r=2 beta^r`;
- outer multiplier initialization and safeguard `[-100,100]`;
- inner schedules `eps1=1e-4/r`, `eps2=1e-4/r`, `eps3=1e-6/r`;
- `max_outer_iterations=20`;
- `wall_clock_cap_s=600`;
- local IPOPT cap `500` iterations;
- `retry_count=0`;
- CasADi/IPOPT backend and every backend option;
- all local feasibility, dual, complementarity, stationarity, descent, algebraic-integrity, TCC, target, physical-postcheck and outer-stop thresholds;
- failure precedence and common-finalization semantics;
- requirement that physical postchecks use actual source trajectories, not guardian foreign copies;
- U3 remains `CONDITIONAL`; U4 remains `UNSELECTED`;
- exact certification language and claim boundaries.

No obstacle scenario is part of Attempt 3.

## 5. Reproducibility design

Attempt 3 consists of **one experiment with two fresh-process repetitions**:

- `attempt3_run1`
- `attempt3_run2`

Both repetitions must use the exact same frozen source, JSON configuration, software environment and deterministic process variables. There is no inspection-driven modification between Run 1 and Run 2. The second run is a reproducibility repetition, not an “Attempt 4”.

The inherited reproducibility thresholds remain

```text
atol = 1e-10
rtol = 1e-10
```

and timing fields are not deterministic acceptance quantities.

## 6. Passive-diagnostic decision

No new per-inner-iteration source/TCC/safety instrumentation is inserted into the executable path for Attempt 3.

Reason: this is a strict cap-isolation experiment under an unchanged 600 s wall-clock cap. Additional per-iteration postchecking would change runtime and therefore introduce a second experimental factor. The existing Attempt-2 logging, finite-oracle diagnostics, residual histories, final physical source postcheck, TCC metrics, integrity checks and raw run evidence are retained unchanged.

Additional analysis may be performed **after** both runs from saved evidence, but it must not alter the execution path or acceptance criteria.

## 7. Acceptance and interpretation contract

Attempt 3 keeps the existing distinctions:

- `NUMERICALLY_VALID`: numerical/evaluator integrity only;
- finite `TCC_CONSISTENT`: direct TCC and target residuals meet their frozen numerical thresholds;
- `PHYSICAL_POSTCHECK_NUMERIC_PASS`: ordinary-floating-point physical margins on actual source trajectories meet the frozen finite tolerance;
- `MODEL0D_SAFETY_CERTIFIED`: remains unavailable while U4 is unresolved;
- `SUNSUN_ALGORITHMICALLY_CERTIFIED`: remains unavailable under the current finite first-block witness limitation;
- a backend success status, goal proximity, objective decrease, small residual trend, or one successful Attempt-3 run is not a theorem or global-optimality certificate.

A complete success on the final permitted inner iteration counts as success; reaching 1000 without satisfying the inherited inner stop is genuine cap exhaustion.

## 8. Frozen planned execution commands — NOT YET EXECUTED

From the Attempt-3 package root:

```bash
PYTHONHASHSEED=0 \
OMP_NUM_THREADS=1 \
OPENBLAS_NUM_THREADS=1 \
MKL_NUM_THREADS=1 \
python run_experiment.py \
  --config configs/baseline_2uav_0obs.json \
  --output runs/attempt3_run1
```

Then, with no code/configuration change:

```bash
PYTHONHASHSEED=0 \
OMP_NUM_THREADS=1 \
OPENBLAS_NUM_THREADS=1 \
MKL_NUM_THREADS=1 \
python run_experiment.py \
  --config configs/baseline_2uav_0obs.json \
  --output runs/attempt3_run2
```

These commands are frozen for Checkpoint C but require the researcher's separate `GO RUN` authorization.

## 9. Campaign closure rule

No parameter is retuned after seeing Attempt-3 results. No additional 2D numerical Attempt 4 is opened merely because Attempt 3 fails or is inconclusive. After the two repetitions, the next work is independent verification, three-attempt synthesis and numerical-campaign closure.

## 10. Repository publication status

This Checkpoint-A/B working package has **not** been committed or pushed to GitHub. Repository publication remains a separate authorized action; the live scientific branch is untouched by this freeze.
