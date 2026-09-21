# Reproducing the Model 0-D 2-UAV / 0-Obstacle Sun--Sun Algorithm-2 Baseline

**Purpose:** exact reproduction guide for the researcher, independent auditor, or another technically competent reviewer.  
**Reference Step-3 code state:** Step-2-approved implementation present at branch commit `bd4b7f19d687cf78976d3c99501ca1a75c4c91ce`.  
**Expected Step-3 outcome:** reproducible `LOCAL_ORACLE_ABORT` / `FIRST_BLOCK_ORACLE_FAILED` at attempted `(r,t)=(1,17)`, with last complete snapshot `(1,16)`.  
**Important:** reproducing the same failure is not a claim of successful convergence.

---

## 1. Obtain the exact repository state

Use the repository

```text
https://github.com/ismo-idi/CCBO_Model1
```

and branch

```text
Model-0_24-Aug-2026
```

For the exact Step-3 code used here, check out

```text
bd4b7f19d687cf78976d3c99501ca1a75c4c91ce
```

then enter

```bash
cd model0d_alg2_numerics
```

Do not use `old-main/` as current scientific authority.

---

## 2. Required software identity

The reference execution used:

```text
Python      3.13.5
NumPy       2.3.5
SciPy       1.17.0
Matplotlib  3.10.8
CasADi      3.7.2
IPOPT       CasADi IPOPT plugin
Linux       x86_64
```

Exact numerical reproducibility across different IPOPT builds, BLAS libraries, processors or operating systems is not promised merely because package version numbers match. Record all differences if reproducing elsewhere.

---

## 3. Verify the configuration and implementation hashes

The baseline configuration must hash to

```text
a9120c15840c8ec1605f8ce5d21d946ac1734672bde044ea1e9bacbc55750784  configs/baseline_2uav_0obs.json
```

Reference core hashes:

```text
555881830578179db1c3b8e48a309a5e4276004595c7732d59fec065cc552823  run_experiment.py
3d035be4ac0ca7e82e1a7063193ae12274bad957ce5d751fa21b3684910145ae  src/config.py
af629c69912fec45a15e9e8c73562cfbb5565db9692d2ad2de6baaced160db84  src/diagnostics.py
bbcee181c372d462e2b56dcbe4bee831a2f13fe9f97298eb6747c719e5ba47a8  src/geometry.py
c448d2108f0b846c9c2897a8a20a3cac7c702547d08812fb0299fbaa8b778239  src/io_utils.py
789bc9da93e593d9ff62ab874fe20e50188b2800d3fab6815badb0275adee504  src/local_nlp.py
dfdc931ae1e1ce17d37e8e7b886cb313047c30cfab405ba4a3be253b61719024  src/sunsun_algorithm2.py
852af3aea5228a9efba8d87a8ba66d4856b4755a0f840d11defa4e71f834658f  src/tcc.py
```

Example:

```bash
sha256sum configs/baseline_2uav_0obs.json run_experiment.py src/*.py
```

Do not continue as an exact reproduction if these differ without recording the difference.

---

## 4. Set the deterministic process environment

Run in a fresh shell:

```bash
export PYTHONHASHSEED=0
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
```

The harness independently checks these values before creating the experiment output directory.

---

## 5. Optional but recommended preflight

The Step-2 checkpoint passed 53 component tests. Re-run them before reproducing Step 3:

```bash
python3 -m pytest -q
```

Expected reference result:

```text
53 passed
```

A failure here means you are not reproducing the verified launch state and should investigate before running the experiment.

---

## 6. Ensure clean output directories

The output path must not already exist. Use new directories, for example:

```bash
rm -rf runs/repro_run1 runs/repro_run2
```

Do not delete historical evidence directories merely to obtain a clean name; choose new names when preserving prior evidence matters.

---

## 7. Run the first baseline process

```bash
python3 run_experiment.py \
  --config configs/baseline_2uav_0obs.json \
  --output runs/repro_run1
```

Reference terminal signature:

```text
scenario_id:        baseline_2uav_0obs
termination_reason: LOCAL_ORACLE_ABORT
primary_cause:      FIRST_BLOCK_ORACLE_FAILED
```

Inspect `runs/repro_run1/summary.json`. The reference run stopped at attempted local solve `(r,t)=(1,17)` and saved `(r,t)=(1,16)` as the last complete snapshot.

---

## 8. Run the second baseline in a new Python process

Do not call the solver twice from one long-lived Python interpreter. Start a second command:

```bash
python3 run_experiment.py \
  --config configs/baseline_2uav_0obs.json \
  --output runs/repro_run2
```

Reference behavior should be the same failure signature.

---

## 9. Reproducibility criterion

The approved protocol requires

\[
\max|x^{(1)}-x^{(2)}|\le10^{-10}
\]

with relative tolerance `1e-10` for final accepted arrays/scalars. For the Step-3 reference execution, the two saved last-complete states were actually bit-for-bit identical:

```text
maximum final-state absolute difference = 0.0
```

Timing values are not expected to be identical.

---

## 10. Independent verification script

Step 3 adds

```text
analysis/verify_step3_baseline.py
```

which deliberately does not import the solver implementation. Run:

```bash
python3 analysis/verify_step3_baseline.py \
  --config configs/baseline_2uav_0obs.json \
  --run1 runs/repro_run1 \
  --run2 runs/repro_run2 \
  --output-dir verification_reproduction
```

It independently recomputes:

- physical source trajectories;
- objective and goal errors;
- direct and split TCC residuals;
- workspace/speed/UAV margins;
- the \(\lambda+\beta\xi+y\) identity;
- reproducibility of persisted arrays;
- agreement with each run's persisted summary.

---

## 11. Reference numerical signature

At the reference run's last complete snapshot `(r,t)=(1,16)`:

```text
R1          = 0.37669732341234324
R2          = 1.5328517645723046e-15
R3          = 0.01745669812479472
R_TCC_eq    = 0.3029946622823656
R_target    = 0.21424958036318856
F           = 4.324447512461001
R_id        = 8.268646384127626e-17
R_rhobeta   = 0.0
```

Reference numerical physical minimum margins:

```text
workspace = 1.024844720443907 m
speed     = 1.0491674196089207e-10 m
obstacle  = NOT_APPLICABLE_EMPTY_FAMILY
UAV       = 0.100849953505317 m
```

At the rejected UAV-1 candidate `(1,17)`:

```text
backend_status        = Solved_To_Acceptable_Level
R_dual_normalized     = 9.56248038286337e-08   # threshold 1e-8 -> FAIL
R_comp                = 3.148423710168679e-07 # threshold 1e-6 -> PASS
R_stat_normalized     = 1.1976452902038308e-07 # threshold 1e-6 -> PASS
R_desc                = 0.0                    # PASS
```

The most negative diagnostic multiplier was row 30, `a1:W:k8:dim1:upper`:

```text
mu = -9.56248038286337e-08
g  = -2.9999999927837857
```

---

## 12. Interpretation rules

Do not change the reference conclusion by relabeling statuses:

- `IPOPT success` is not the finite first-block acceptance condition;
- the rejected run is not a successful baseline;
- the saved snapshot is not a completed outer solution;
- ordinary floating-point physical margins do not resolve U4;
- this experiment does not make `SUNSUN_ALGORITHMICALLY_CERTIFIED` available;
- do not run the obstacle scenario as if the baseline gate passed.

Any change to thresholds, multiplier handling, backend options, retry logic or algorithm path creates a **new protocol/implementation experiment** and must be documented as such rather than described as exact reproduction of Step 3.
