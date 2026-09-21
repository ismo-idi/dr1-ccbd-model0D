# Model 0-D — Step 3 Numerical Baseline Report: 2 UAVs, 0 Obstacles

**Date:** 12 September 2026  
**Role:** DAILY WORKER  
**Researcher / final scientific decision-maker:** Ismaël Assoumane Idi  
**Project:** Constrained Consensus-Based Optimization for Decentralized Path Planning in UAV Swarms  
**Repository / branch:** `ismo-idi/CCBO_Model1` / `Model-0_24-Aug-2026`  
**Pre-Step-3 traceability commit:** `bd4b7f19d687cf78976d3c99501ca1a75c4c91ce`  
**Protocol:** `MODEL0D_NUMERICAL_PROTOCOL_AND_READINESS_V1_0_11_SEP_2026.md`, researcher-approved 11 September 2026  
**Step-2 status:** researcher-approved; 53/53 component tests passed; Step-2 manifest reverified before Step 3  
**Step-3 status:** **EXECUTED — BASELINE REPRODUCIBLY FAILED THE FROZEN FINITE FIRST-BLOCK ORACLE ACCEPTANCE CONTRACT**  
**Commit status of this Step-3 work:** **NOT COMMITTED**; the established commit cadence requires separate researcher authorization.

---

## 1. Executive conclusion

The complete approved `2-UAV / 0-obstacle` Sun--Sun Algorithm-2 baseline was executed twice in two fresh Python processes under the frozen configuration and deterministic environment. Both runs produced the same numerical trajectory of complete iterates and terminated at exactly the same point:

```text
termination_reason = LOCAL_ORACLE_ABORT
primary_cause      = FIRST_BLOCK_ORACLE_FAILED
failure location   = outer r=1, attempted inner t=17
last complete      = outer r=1, inner t=16
```

The failure is **reproducible**. Every persisted final-state array from the two runs is bit-for-bit identical; the maximum cross-run absolute difference is exactly `0.0`. Event logs and summaries are also exactly equal after excluding wall-clock/backend timing fields.

The blocking condition is specific: UAV 1's finite multiplier-sign diagnostic failed at attempted inner iteration `t=17`:

\[
R_{\mathrm{dual},1}^{\mathrm{norm}}
=
9.56248038286337\times10^{-8}
>
10^{-8}.
\]

Thus the violation is about `9.56248` times the frozen dual-sign threshold. The other UAV-1 finite oracle checks at that candidate passed:

\[
R_{\mathrm{comp},1}=3.148423710168679\times10^{-7}<10^{-6},
\]

\[
R_{\mathrm{stat},1}^{\mathrm{norm}}
=1.1976452902038308\times10^{-7}<10^{-6},
\]

and

\[
R_{\mathrm{desc},1}=0.
\]

All family-specific finite feasibility violations were zero, there were no near-active segment rows and no nonsmooth blocking rows. IPOPT reported `Solved_To_Acceptable_Level` for UAV 1 at the rejected candidate. UAV 2 independently passed all frozen oracle diagnostics at the same phase.

Under the approved **no-retry** policy, the common barrier correctly aborted the run. No threshold was retuned, no failed candidate was silently accepted, and no obstacle experiment was started.

Therefore:

\[
\boxed{
\text{BASELINE\_NUMERICALLY\_RELIABLE\_FOR\_EXPANSION}=\text{FALSE}
}
\]

and the predefined obstacle scenario is **not authorized by the baseline gate**.

---

## 2. Schedule deviation — explicitly authorized and attributed

The approved timetable originally imposed a Saturday 12 September 2026 numerical cutoff at 17:00. Step 3 began after that cutoff.

Before execution, the researcher explicitly authorized overriding the cutoff and explicitly requested that the schedule deviation be recorded as a **"procrastination issue" from the researcher**, not as a DAILY WORKER scheduling mistake. This report records that attribution exactly as requested. The cutoff override changed only the timing authority; it did not authorize changes to the frozen protocol, model, thresholds, backend, or campaign scope.

---

## 3. Frozen baseline instance

No scenario datum was changed after outcome inspection.

\[
N=2,\qquad q=2,\qquad K=8,\qquad \Delta t=0.5\ \mathrm{s}.
\]

Workspace:

\[
\mathcal W=[-3,3]\times[-3,3]\ \mathrm m.
\]

Starts and goals:

\[
p_1^0=(-2,0),\qquad g_1=(2,0),
\]

\[
p_2^0=(0,-2),\qquad g_2=(0,2).
\]

UAV radii and safety margin:

\[
r_1=r_2=0.10\ \mathrm m,
\qquad
\delta_{12}^{\mathrm{uav}}=0.20\ \mathrm m,
\]

so the required center clearance is

\[
\rho_{12}^{\mathrm{uav}}=0.40\ \mathrm m.
\]

Maximum speed:

\[
v_1^{\max}=v_2^{\max}=1.5\ \mathrm{m/s}.
\]

Objective weights:

\[
\alpha_1=\alpha_2=20,
\qquad
\beta_1=\beta_2=1.
\]

Obstacle registry:

\[
\mathcal O=\varnothing.
\]

The obstacle family is therefore verified empty, not missing: expected obstacle cardinality is zero, aggregate obstacle violation is zero, and the minimum obstacle margin is `NOT_APPLICABLE_EMPTY_FAMILY`.

---

## 4. Frozen TCC architecture

Guardian assignment:

\[
\gamma(\{1,2\})=1.
\]

The unique TCC equality copies source 2 between UAV 1 and UAV 2. With

\[
Q=qK=16,
\]

the local blocks are

\[
z_1=\operatorname{col}(x_{1,\mathrm{free}},\widetilde x_{1\leftarrow2})\in\mathbb R^{32},
\]

\[
z_2=x_{2,\mathrm{free}}\in\mathbb R^{16}.
\]

There is one vector equality edge, hence

\[
M_{\mathrm{eq}}=1,
\qquad
\dim U=16,
\qquad
\dim\xi=\dim y=\dim\lambda=32.
\]

The split equalities are

\[
S_{1\leftarrow2}z_1-u_e=0,
\qquad
S_{2\leftarrow2}z_2-u_e=0.
\]

A1 uses

\[
\mathcal B=[-3.5,3.5]^2,
\]

only for the foreign source-2 copy and edge auxiliary, as frozen.

---

## 5. Frozen Algorithm-2 settings

The run used the researcher-approved values without modification:

\[
\beta^0=1,
\qquad
\vartheta=2,
\qquad
\beta^1=2,
\qquad
\omega=0.5,
\]

\[
\lambda^1=0,
\qquad
-100\mathbf1\le\lambda^r\le100\mathbf1,
\]

and at every outer iteration

\[
\boxed{\rho^r=2\beta^r}.
\]

Inner stopping schedules:

\[
\epsilon_1^r=\frac{10^{-4}}{r},
\qquad
\epsilon_2^r=\frac{10^{-4}}{r},
\qquad
\epsilon_3^r=\frac{10^{-6}}{r}.
\]

Finite caps:

```text
max_outer_iterations = 20
max_inner_iterations = 100
wall_clock_cap_per_run = 600 s
IPOPT max_iter = 500 per local solve
retry_count = 0
```

The local NLP backend was the frozen `CasADi 3.7.2 + IPOPT` configuration. No backend option was changed between the two runs.

---

## 6. Exact implementation identity used for the experiment

The Step-3 run used the exact Step-2 verified implementation. The persisted run environment records these SHA-256 identities:

```text
config baseline_2uav_0obs.json
  a9120c15840c8ec1605f8ce5d21d946ac1734672bde044ea1e9bacbc55750784

run_experiment.py
  555881830578179db1c3b8e48a309a5e4276004595c7732d59fec065cc552823
src/config.py
  3d035be4ac0ca7e82e1a7063193ae12274bad957ce5d751fa21b3684910145ae
src/diagnostics.py
  af629c69912fec45a15e9e8c73562cfbb5565db9692d2ad2de6baaced160db84
src/geometry.py
  bbcee181c372d462e2b56dcbe4bee831a2f13fe9f97298eb6747c719e5ba47a8
src/io_utils.py
  c448d2108f0b846c9c2897a8a20a3cac7c702547d08812fb0299fbaa8b778239
src/local_nlp.py
  789bc9da93e593d9ff62ab874fe20e50188b2800d3fab6815badb0275adee504
src/sunsun_algorithm2.py
  dfdc931ae1e1ce17d37e8e7b886cb313047c30cfab405ba4a3be253b61719024
src/tcc.py
  852af3aea5228a9efba8d87a8ba66d4856b4755a0f840d11defa4e71f834658f
```

No core implementation file was altered between run 1 and run 2.

---

## 7. Environment

Both runs used the deterministic process settings

```text
PYTHONHASHSEED=0
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
```

with

```text
Python      3.13.5
NumPy       2.3.5
SciPy       1.17.0
Matplotlib  3.10.8
CasADi      3.7.2
Platform    Linux 6.18.35 x86_64, glibc 2.41
```

The two runs were launched in two distinct Python processes and in distinct output directories.

---

## 8. Procedure executed from A to Z

### 8.1 Pre-experiment freeze verification

Before the first Model-0D baseline outcome was generated:

1. the exact Step-2 package was copied into a fresh Step-3 working directory;
2. the Step-2 SHA-256 manifest was checked: `46/46` files matched, `0` errors;
3. the Step-3 local `runs/` directory was confirmed empty;
4. no protocol or source file was changed.

### 8.2 Run 1

Exact execution command:

```bash
export PYTHONHASHSEED=0
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
python3 run_experiment.py \
  --config configs/baseline_2uav_0obs.json \
  --output runs/baseline_run1
```

The harness performed, in order:

1. configuration freeze validation;
2. deterministic environment validation;
3. exact stationary TCC initialization;
4. Algorithm-2 outer/inner execution;
5. two local first-block solves at each inner step;
6. independent finite-oracle recomputation and all-agent acceptance barrier;
7. exact A5 edge update when both local solves passed;
8. exact slack update;
9. exact inner-dual update;
10. integrity checks;
11. independent \(R_1,R_2,R_3\) calculation and matrix-form cross-checks;
12. inner stopping test;
13. common finalization on the first blocking failure.

The run stopped at the local-oracle barrier before executing the A5/update phase for attempted `t=17`, so the saved result is the **last complete finite snapshot** at `r=1,t=16`.

### 8.3 Run 2

A second fresh Python process used the same command except

```text
--output runs/baseline_run2
```

No file or threshold was changed between runs.

### 8.4 Independent post-run verifier

After both runs had terminated, `analysis/verify_step3_baseline.py` independently recomputed key quantities using NumPy/Python only and deliberately did **not** import the solver implementation. It recomputed:

- source trajectories from persisted arrays;
- physical objective;
- terminal goal errors;
- direct TCC residual;
- split target residual;
- algebraic identity residual;
- workspace, speed and exact inter-segment UAV margins;
- run-to-run final-state equality;
- persisted report consistency.

All independently recomputed key values matched the persisted summary to absolute error at most `1e-12`.

---

## 9. Inner-loop behavior before failure

For outer iteration \(r=1\), the frozen stopping thresholds were

\[
\epsilon_1^1=10^{-4},
\qquad
\epsilon_2^1=10^{-4},
\qquad
\epsilon_3^1=10^{-6}.
\]

At the last complete iteration, \(t=16\),

\[
R_1=0.37669732341234324,
\]

\[
R_2=1.5328517645723046\times10^{-15},
\]

\[
R_3=0.01745669812479472.
\]

Thus \(R_2\) passed its threshold, while \(R_1\) and \(R_3\) remained far above their required stopping thresholds. The inner Algorithm-1 solve had **not** terminated successfully before the oracle failure.

The residual history nevertheless shows numerical reduction before the abort:

```text
R1: 14.9563536104  at t=1  -> 0.3766973234 at t=16
R3:  1.0370365353  at t=1  -> 0.0174566981 at t=16
```

This is descriptive behavior only. It is not evidence of convergence because execution stopped before the frozen stopping conditions were met.

---

## 10. Exact failure characterization at attempted t=17

At \((r,t)=(1,17)\), UAV 1's backend returned:

```text
backend_success    = true
backend_status     = Solved_To_Acceptable_Level
backend_iterations = 69
```

But backend success was not the acceptance criterion. Independent finite diagnostics gave:

| Diagnostic | Value | Frozen threshold | Pass? |
|---|---:|---:|---|
| family feasibility | all `0.0` violations | family-specific | yes |
| normalized dual-sign violation | `9.56248038286337e-08` | `1e-08` | **no** |
| complementarity | `3.148423710168679e-07` | `1e-06` | yes |
| normalized stationarity balance | `1.1976452902038308e-07` | `1e-06` | yes |
| descent violation | `0.0` | relative rule | yes |
| nonsmooth blocking rows | none | none permitted | yes |

The worst negative diagnostic multiplier was localized to canonical local row 30:

```text
family = W
label  = a1:W:k8:dim1:upper
mu     = -9.56248038286337e-08
g      = -2.9999999927837857
```

The constraint itself was strongly inactive; the failure is specifically the frozen multiplier-sign diagnostic. No multiplier clipping or inactive-row deletion was introduced after seeing this outcome because the approved protocol did not authorize such a repair.

At the same attempted inner iteration, UAV 2 passed:

```text
backend_status          = Solve_Succeeded
backend_iterations      = 18
R_dual_normalized       = 1.0413166924835302e-10
R_comp                  = 4.73278620868634e-10
R_stat_normalized       = 2.33915771266219e-10
R_desc                  = 0.0
accepted                = true
```

The common phase barrier therefore correctly aborted all agents because **every** local candidate had to pass.

---

## 11. Last complete snapshot — diagnostics, not an accepted plan

The saved snapshot is at \((r,t)=(1,16)\). Because the inner loop had not terminated, this is **not** a completed outer output and must not be presented as the successful Model-0D plan.

### 11.1 Objective behavior

On that snapshot:

\[
f_1=1.9875776397515528,
\qquad
f_2=2.336869872709448,
\]

\[
\boxed{F=4.324447512461001.}
\]

Terminal goal errors are

\[
\|p_1^K-g_1\|=0.024844720443907065\ \mathrm m,
\]

\[
\|p_2^K-g_2\|=0.043226996229548176\ \mathrm m.
\]

These values show that the physical source blocks were already near their goals. They do **not** establish optimality or algorithm completion.

### 11.2 Numerical physical postcheck

The independent ordinary-floating-point source-trajectory margins are:

```text
workspace minimum margin = 1.024844720443907 m
speed minimum margin     = 1.0491674196089207e-10 m
obstacle family           = verified empty
UAV minimum margin        = 0.100849953505317 m
```

All expected evaluators completed and the protocol's numerical physical postcheck passes at this last complete snapshot. The speed margin is extremely close to zero but positive in ordinary floating point.

This does **not** imply exact physical safety certification because U4 remains unresolved:

\[
\boxed{
\texttt{PHYSICAL\_POSTCHECK\_NUMERIC\_PASS}
\neq
\texttt{MODEL0D\_SAFETY\_CERTIFIED}.
}
\]

### 11.3 TCC disagreement

At the same snapshot:

\[
\boxed{R_{\mathrm{TCC,eq}}=0.3029946622823656\ \mathrm m},
\]

\[
\boxed{R_{\mathrm{target}}=0.21424958036318856\ \mathrm m}.
\]

Both are vastly above the frozen `1e-6 m` finite TCC thresholds. Hence

```text
TCC_CONSISTENT = false
```

for the last complete snapshot.

### 11.4 Algebraic integrity

The exact update identities remained numerically intact:

\[
R_{\mathrm{id}}
=
8.268646384127626\times10^{-17},
\]

with limit `1e-12`, and

\[
R_{\rho\beta}=0.
\]

So the observed failure is not an algebraic-integrity failure.

---

## 12. Reproducibility result

The protocol required two fresh-process runs. Both runs produced the same:

- termination reason;
- primary and complete cause lists;
- failure location \((r,t)=(1,17)\);
- 16 complete inner iterations before failure;
- numerical diagnostics, except timing quantities;
- last complete state.

For every persisted final-state array

```text
z1, z2, u, xi, y, lambda_outer, beta, rho, outer_r, inner_t
```

run 1 and run 2 are **exactly equal**, with

\[
\boxed{\max |x^{(1)}-x^{(2)}|=0.0.}
\]

Therefore the protocol reproducibility requirement

\[
\max |x^{(1)}-x^{(2)}|\le10^{-10}
\]

is satisfied for the observed **failure outcome**.

This distinction matters: the failure is reproducible; the baseline is not thereby successful.

---

## 13. Status classification

For the persisted last complete snapshot:

```text
NUMERICALLY_VALID                 = true
TCC_CONSISTENT                    = false
PHYSICAL_POSTCHECK_NUMERIC_PASS   = true
MODEL0D_SAFETY_CERTIFIED          = false
SUNSUN_ALGORITHMICALLY_CERTIFIED  = false
FULLY_CERTIFIED_MODEL0D_RESULT    = false
U3                                 = CONDITIONAL
U4                                 = UNSELECTED
```

The **run itself** is classified as a failed baseline because the local first-block finite acceptance contract stopped execution before an outer output was completed.

Accordingly, the Saturday-routing predicate is false:

```text
BASELINE_NUMERICALLY_RELIABLE_FOR_EXPANSION = false
```

---

## 14. What the result supports

The experiment supports the following claims:

1. the Step-2 implementation can execute the selected Algorithm-2 update chain for multiple complete inner iterations;
2. TCC residual and update/integrity diagnostics are produced reproducibly;
3. the no-retry local-oracle barrier is operational and reproducibly rejects a candidate that violates the frozen finite dual-sign threshold;
4. the failure is not due to NaN/Inf, missing multipliers, a nonsmooth blocking segment, physical-postcheck evaluator failure, algebraic identity failure, or nondeterminism between repeated runs;
5. the exact same failure is reproduced in a fresh process.

---

## 15. What the result does not support

It does **not** support claims that:

- the baseline converged;
- the inner loop met \(R_1,R_2,R_3\) stopping conditions;
- a complete Algorithm-2 outer result was produced;
- TCC agreement was achieved;
- the predefined obstacle case should be run;
- the exact Sun--Sun first-block assumption was certified;
- the project has exact physical-safety certification;
- U3 or U4 is resolved;
- the returned diagnostic snapshot is globally or locally optimal for the original problem;
- the failure proves Algorithm 2 is unsuitable in general.

---

## 16. Interpretation and next technical question

The baseline failed **because the project deliberately imposed a finite first-block acceptance contract stricter than “IPOPT returned success.”** That distinction worked exactly as intended.

At the rejected UAV-1 candidate, IPOPT's own status was only `Solved_To_Acceptable_Level`, and the independent multiplier-sign residual exceeded the frozen project threshold. This is a concrete numerical issue that now requires targeted investigation before obstacle expansion.

The correct next technical question is therefore not “how does the obstacle case perform?” It is:

> Can the selected finite first-block realization reliably satisfy the already-frozen oracle acceptance contract, or does the project need an explicitly reviewed protocol/backend/oracle-handling amendment?

No such amendment is made in this Step-3 report. In particular, this report does **not** authorize:

- loosening the `1e-8` dual threshold;
- clipping negative multipliers;
- silently zeroing multipliers of inactive ordinary smooth constraints;
- enabling retries;
- changing IPOPT options after seeing this run;
- switching to another algorithm/backend;
- continuing from the rejected candidate.

Those would be new choices requiring researcher review and, where appropriate, independent audit.

---

## 17. Plots

Supporting plots are stored under `plots/`:

- `step3_last_complete_source_trajectories.png` — physical source trajectories at the last complete snapshot;
- `step3_inner_residuals_run1.png` — \(R_1,R_2,R_3\) through accepted inner iterations;
- `step3_uav1_oracle_failure_t17.png` — UAV-1 finite oracle diagnostics including the rejected `t=17` point;
- `step3_uav1_oracle_diagnostics_run1.png` — accepted-iteration oracle history.

The plots supplement, but do not replace, raw JSON/JSONL/NPZ evidence.

---

## 18. Evidence inventory

### Raw run evidence

Each of `runs/baseline_run1/` and `runs/baseline_run2/` contains:

```text
config.json
environment.json
events.jsonl
final_state.npz
summary.json
```

### Independent verification

`verification_step3/` contains:

```text
baseline_run1_console.txt
baseline_run2_console.txt
independent_run1_verification.json
independent_run2_verification.json
independent_verifier_console.txt
reproducibility_comparison.json
log_reproducibility.json
failure_localization.json
inner_iteration_metrics_run1.csv
```

### Reproduction documentation

See:

`REPRODUCING_BASELINE_2UAV_0OBS.md`

for exact commands, prerequisites, expected failure signature and independent verification steps.

---

## 19. Final Step-3 verdict

\[
\boxed{
\begin{array}{l}
\text{Complete approved baseline executed twice: YES}\\
\text{Fresh-process reproducibility: PASS}\\
\text{Numerical/algebraic integrity of saved snapshot: PASS}\\
\text{Numerical physical postcheck of saved snapshot: PASS, U4-uncertified}\\
\text{Finite TCC consistency: FAIL}\\
\text{Finite first-block oracle acceptance: FAIL at }(r,t)=(1,17)\\
\text{Successful inner termination: NO}\\
\text{Successful outer termination: NO}\\
\text{Baseline reliable for obstacle expansion: NO}\\
\text{Obstacle scenario executed: NO}
\end{array}
}
\]

The rigorous outcome of Step 3 is therefore a **reproducible, well-characterized baseline failure**, not a successful numerical validation. That failure is itself valid experimental evidence and should be carried honestly into the next researcher/auditor decision.
