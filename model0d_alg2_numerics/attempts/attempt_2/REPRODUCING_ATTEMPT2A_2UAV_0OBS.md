# Reproducing Model 0-D Baseline Attempt 2A — 2 UAVs, 0 Obstacles

**Attempt:** 2A, 13 September 2026  
**Purpose:** reproduce the original crossing baseline with the researcher-authorized activity-aware finite multiplier diagnostic.  
**Important:** this guide reproduces a **failed baseline attempt**, not an accepted/certified result.

## 1. Required artifact

Use the complete delivered Attempt-2A package and verify its SHA-256 against the value supplied with the final delivery message.

After extraction, enter the `model0d_alg2_numerics/` directory.

## 2. Reference software environment

The executed reference environment was:

```text
Python      3.13.5
NumPy       2.3.5
SciPy       1.17.0
Matplotlib  3.10.8
CasADi      3.7.2
IPOPT       through CasADi plugin
Linux       x86_64
```

For the strongest same-environment reproducibility comparison, use the same package versions and compatible IPOPT build.

Different operating systems, BLAS libraries, CasADi/IPOPT builds, or compiler stacks may produce small floating-point differences. Such a rerun can still be scientifically compared, but universal bit-for-bit identity is **not** claimed across arbitrary machines.

## 3. Deterministic process variables

Set exactly:

```bash
export PYTHONHASHSEED=0
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
```

`run_experiment.py` rejects execution if these variables are not set to the approved values.

## 4. Verify the frozen configuration and Attempt-2A source

Reference hashes:

```text
configs/baseline_2uav_0obs.json
a9120c15840c8ec1605f8ce5d21d946ac1734672bde044ea1e9bacbc55750784

src/diagnostics.py
4bcef4c418c46d6938f4e50b4c1ec0b39811e821f3d017a7f657837e7945e84a
```

Run:

```bash
sha256sum configs/baseline_2uav_0obs.json src/diagnostics.py
```

Do not edit configuration values if the goal is reproduction rather than a successor experiment.

## 5. Run the component suite first

```bash
pytest -q
```

Expected Attempt-2A package result in the reference environment:

```text
56 passed
```

Do not proceed as a claimed reproduction if component tests fail. Preserve the failures instead.

## 6. Run two fresh baseline processes

Choose output directories that do not already exist:

```bash
python run_experiment.py \
  --config configs/baseline_2uav_0obs.json \
  --output runs/repro_attempt2a_run1
```

Then launch a second fresh Python process:

```bash
python run_experiment.py \
  --config configs/baseline_2uav_0obs.json \
  --output runs/repro_attempt2a_run2
```

Do not retry within a run and do not adjust thresholds after seeing run 1.

## 7. Independently verify the result

The supplied verifier does not import the solver modules:

```bash
python analysis/verify_attempt2a.py \
  --config configs/baseline_2uav_0obs.json \
  --run1 runs/repro_attempt2a_run1 \
  --run2 runs/repro_attempt2a_run2 \
  --output-dir verification_attempt2a_reproduction
```

Review:

```text
verification_attempt2a_reproduction/independent_attempt2a_run1.json
verification_attempt2a_reproduction/independent_attempt2a_run2.json
verification_attempt2a_reproduction/attempt2a_reproducibility.json
```

## 8. Reference outcome

In the executed reference environment, both runs gave:

```text
termination_reason = MAX_INNER_ITERATIONS
primary_cause      = PHYSICAL_VIOLATION_DETECTED
last complete      = r=1, t=100
```

Reference last-inner residuals:

```text
R1 = 0.01343852896082126
R2 = 1.0401237528903013e-15
R3 = 0.0002248160621244216
```

Reference TCC values:

```text
R_TCC_eq = 0.12581049903927163 m
R_target = 0.08896145701513261 m
```

Reference minimum actual-source UAV margin:

```text
-0.11386770161758925 m
```

Reference guardian source-1 / source-2-copy minimum margin:

```text
+9.201428508021081e-11 m
```

The negative actual-source margin is a numerical physical-postcheck failure. It is not an exact U4 safety certificate or anti-certificate.

## 9. Reproducibility criterion

Within the reference environment, the two supplied Attempt-2A runs are bit-for-bit identical for all persisted final-state arrays and exactly identical for complete summaries/event histories after excluding only timing fields.

The approved numerical reproducibility tolerance is `atol=rtol=1e-10`; the supplied reference runs achieved maximum final-state difference `0.0`.

## 10. What not to change during reproduction

Do not change:

- starts/goals;
- `K`, `dt`, or speed limits;
- `max_inner_iterations=100`;
- IPOPT Hessian option;
- local/tcc/physical thresholds;
- activity-aware diagnostic rule;
- no-retry policy.

Changing any of those creates a successor experiment and must be reported as such.
