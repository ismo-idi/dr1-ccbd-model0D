# Model 0-D — Attempt 3 Checkpoints A–B Readiness Record

**Date:** 18 September 2026  
**Role:** DAILY WORKER  
**Route:** A — finite-cap isolation  
**Status:** **READY TO RUN, WAITING FOR RESEARCHER `GO RUN`**  
**Experiment executed:** **NO**

## 1. Checkpoint A — protocol freeze

Checkpoint A is frozen in `ATTEMPT3_PROTOCOL_FREEZE_18_SEP_2026.md`.

The experimental question is limited to the finite inner budget. The cap is frozen at

```text
max_inner_iterations = 1000
```

instead of Attempt 2's `100`. No other scientific/executable parameter is changed.

The branch was rechecked immediately before finalizing this record and remained at

```text
79cd3aa4bfeabc12ea3eeb2649b1e3d341ce6f1c
Finalize post-meeting harmonization structure and timetable status
```

No GitHub write was performed.

## 2. Attempt-2 implementation inheritance

The Attempt-3 working package inherits the Attempt-2 executable source. Exact SHA-256 equality was verified for every executable file except `src/config.py`, which necessarily contains the frozen cap change.

| File | Attempt-3 SHA-256 | Relation to Attempt 2 |
|---|---|---|
| `run_experiment.py` | `555881830578179db1c3b8e48a309a5e4276004595c7732d59fec065cc552823` | exact match |
| `src/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | exact match |
| `src/diagnostics.py` | `4bcef4c418c46d6938f4e50b4c1ec0b39811e821f3d017a7f657837e7945e84a` | exact match |
| `src/geometry.py` | `bbcee181c372d462e2b56dcbe4bee831a2f13fe9f97298eb6747c719e5ba47a8` | exact match |
| `src/io_utils.py` | `c448d2108f0b846c9c2897a8a20a3cac7c702547d08812fb0299fbaa8b778239` | exact match |
| `src/local_nlp.py` | `789bc9da93e593d9ff62ab874fe20e50188b2800d3fab6815badb0275adee504` | exact match |
| `src/sunsun_algorithm2.py` | `dfdc931ae1e1ce17d37e8e7b886cb313047c30cfab405ba4a3be253b61719024` | exact match |
| `src/tcc.py` | `852af3aea5228a9efba8d87a8ba66d4856b4755a0f840d11defa4e71f834658f` | exact match |
| `src/config.py` | `8f14f4b5cd63a3dc418ab2aee51009ab08c17fcba6fb2bf9e1b993849d8c8fd6` | one-line cap change only |

The locally reconstructed exact Attempt-2 `src/config.py` reference has SHA-256

```text
3d035be4ac0ca7e82e1a7063193ae12274bad957ce5d751fa21b3684910145ae
```

which matches the hash recorded by the Attempt-2 campaign. The Attempt-2 → Attempt-3 source diff is exactly:

```diff
-        "max_inner_iterations": 100,
+        "max_inner_iterations": 1000,
```

The machine-readable verification is in `verification/pre_run_freeze_verification.json` and reports `overall_pass: true`.

## 3. Baseline JSON configuration diff

The Attempt-2 scientific baseline was compared recursively with the Attempt-3 JSON.

The only non-metadata scientific difference is:

```text
algorithm.max_inner_iterations: 100 -> 1000
```

The other JSON differences are the human-readable description and a provenance-only `attempt3` object recording route, source attempt, parent branch head, two repetitions and the prohibition on outcome-driven retuning.

No start/goal, geometry, objective, TCC, threshold, backend, wall-clock, retry or outer-loop value drift was detected.

## 4. Pre-run component verification

The inherited behavioral component suite, reconstructed from the checked Attempt-2 GitHub source, plus two Attempt-3-specific cap-freeze tests was run under the frozen deterministic process variables.

Result:

```text
58 passed in 3.06 s
```

The two added tests verify that:

1. Attempt 3 loads with `max_inner_iterations == 1000` and its provenance metadata;
2. a drift to `999` is rejected by the exact configuration validator.

`python -m compileall -q src tests run_experiment.py` also passed.

The tests include the existing first-block component checks, multiplier sign/order checks, activity-aware multiplier handling, geometry checks, derivative check, TCC split/structure checks, residual/integrity checks, actual-source physical-postcheck semantics, empty-family semantics, deterministic-environment guard and failure/control-flow behavior. Component tests may invoke isolated local NLP solves; **no complete Attempt-3 Algorithm-2 run was executed**.

Evidence:

- `verification/pytest_attempt3_pre_run.txt`
- `verification/compileall_attempt3.txt`
- `verification/pre_run_freeze_verification.json`

## 5. Execution environment

Pre-run numerical stack:

```text
Python      3.13.5
NumPy       2.3.5
SciPy       1.17.0
Matplotlib  3.10.8
CasADi      3.7.2
```

Deterministic variables:

```text
PYTHONHASHSEED=0
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
```

Current platform record:

```text
Linux 6.18.44 x86_64, glibc 2.41
```

The Attempt-2 recorded platform was `Linux 6.18.35 x86_64, glibc 2.41`. Thus the numerical Python/CasADi stack and deterministic process variables match, while the host kernel patch version is not byte-identical. This is disclosed as an environmental limitation; it is not silently treated as exact cross-attempt platform identity. The two Attempt-3 repetitions themselves will run in the same current environment and therefore still provide the planned same-environment reproducibility test.

## 6. Outcome-contamination and output-directory checks

Before any experimental execution:

```text
runs/ = EMPTY
```

The pre-run verifier confirms that no Attempt-3 run directory exists. No baseline outcome has been generated or inspected.

No new per-inner diagnostic instrumentation was inserted into the execution path, specifically to avoid altering runtime under the unchanged 600 s wall-clock cap.

## 7. Reproducibility freeze

Attempt 3 will be executed twice in two fresh Python processes with identical frozen files and environment:

```text
runs/attempt3_run1
runs/attempt3_run2
```

No code/configuration modification is permitted between the repetitions. No retry is permitted within either run. A disappointing Run 1 is not grounds to modify Run 2.

## 8. Readiness verdict

All Checkpoint-A/B gates under the worker's control pass:

```text
Scientific question frozen:                    PASS
Single factor selected/frozen:                 PASS (100 -> 1000 inner iterations)
Attempt-2 executable inheritance:              PASS
Unchanged executable source hashes:            PASS
config.py exact one-line executable diff:       PASS
Baseline JSON scientific diff gate:            PASS
Component/regression tests:                    PASS (58/58)
Python compile check:                           PASS
Deterministic variables:                       PASS
Numerical software versions:                   PASS
Attempt-3 runs directory empty:                PASS
Two-repeat reproducibility design frozen:       PASS
No result-driven retuning allowed:              PASS
Attempt-3 experiment executed:                  NO
```

### Final Checkpoint-B status

```text
READY TO RUN — WAITING FOR RESEARCHER GO RUN
```

The disclosed kernel-patch difference from the historical Attempt-2 host remains a provenance caveat, not a hidden claim of exact host identity.
