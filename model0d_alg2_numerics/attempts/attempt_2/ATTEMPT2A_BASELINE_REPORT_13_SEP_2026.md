# Model 0-D — Sun–Sun Algorithm-2 Baseline Attempt 2A Report

**Date:** 13 September 2026  
**Role:** DAILY WORKER  
**Researcher / final scientific decision-maker:** Ismaël Assoumane Idi  
**Project:** Constrained Consensus-Based Optimization for Decentralized Path Planning in UAV Swarms  
**Scenario:** original approved crossing geometry, `N=2`, `0` obstacles  
**Attempt:** **2A — activity-aware finite multiplier diagnostic only**  
**Repository branch checkpoint:** `Model-0_24-Aug-2026`  
**Live branch HEAD rechecked before Attempt 2A:** `bd4b7f19d687cf78976d3c99501ca1a75c4c91ce`  
**GitHub write status:** **no Attempt-2A commit or push performed**  
**Final Attempt-2A verdict:** **FAILS THE FROZEN BASELINE RELIABILITY GATE; the Attempt-1 oracle-noise blocker is removed, but the inner solver reaches its 100-iteration cap before TCC convergence and the last complete source trajectories are not physically safe.**

---

## 1. Executive result

Attempt 2A successfully isolated and corrected the specific diagnostic issue that stopped Attempt 1. At the exact Attempt-1 failure location `(r,t)=(1,17)`, IPOPT again returned the same raw negative workspace multiplier

\[
-9.56248038286337\times 10^{-8},
\]

on the same strongly inactive row with

\[
g=-2.9999999927837857.
\]

Under the researcher-authorized activity-aware diagnostic, that raw multiplier was preserved in the evidence but the finite **diagnostic multiplier** was set to zero because the constraint is far inside the feasible region. The UAV-1 local oracle therefore passed at `t=17`:

\[
R_{\mathrm{dual},1}^{\mathrm{norm}}=0,
\qquad
R_{\mathrm{comp},1}=0,
\qquad
R_{\mathrm{stat},1}^{\mathrm{norm}}
=3.952334901899828\times10^{-7}<10^{-6}.
\]

The run then continued through all 100 permitted inner iterations. No local oracle failure occurred.

However, the frozen inner stopping test was still not met at `t=100`:

\[
\boxed{R_1=1.343852896082126\times10^{-2}>10^{-4}},
\]

\[
\boxed{R_2=1.0401237528903013\times10^{-15}<10^{-4}},
\]

\[
\boxed{R_3=2.248160621244216\times10^{-4}>10^{-6}}.
\]

Therefore the execution stop mechanism was

```text
MAX_INNER_ITERATIONS
```

at `(r,t)=(1,100)`.

The common final postcheck also found:

- TCC not accepted;
- an ordinary-floating-point physical UAV–UAV safety violation on the **actual source trajectories**.

Under the frozen failure-precedence rule, the deterministic primary cause is therefore

```text
PHYSICAL_VIOLATION_DETECTED
```

although the loop itself stopped because the 100-inner-iteration cap was exhausted.

Accordingly,

\[
\boxed{\texttt{BASELINE_NUMERICALLY_RELIABLE_FOR_EXPANSION}=\mathrm{FALSE}.}
\]

No obstacle scenario was executed.

---

## 2. Why Attempt 2A was authorized

Attempt 1 did not stop because of collision, NaN/Inf, TCC algebra corruption, or a nonsmooth blocking row. It stopped at `t=17` because the finite dual-sign diagnostic rejected a tiny negative IPOPT multiplier on a workspace row that was strongly inactive.

The researcher reviewed the failure on 13 September 2026 and explicitly authorized **Attempt 2A** with the original crossing geometry unchanged and only a principled correction of that multiplier diagnostic.

The exact amendment is separately frozen in:

```text
ATTEMPT2A_PROTOCOL_AMENDMENT_13_SEP_2026.md
```

---

## 3. Exact diagnostic amendment

For a canonical inequality row \(g_\ell(z)\le0\) belonging to family \(\mathcal F\), the existing approved family tolerance \(\tau_{\mathcal F}\) and already-frozen `inactive_factor=100` define

\[
\tau_{\mathrm{inactive},\mathcal F}=100\tau_{\mathcal F}.
\]

Attempt 2A uses

\[
\boxed{
\mu_\ell^{\mathrm{diag}}=
\begin{cases}
0, & g_\ell(z)<-\tau_{\mathrm{inactive},\mathcal F},\\
\mu_\ell^{\mathrm{backend}}, & \text{otherwise}.
\end{cases}}
\]

This is a **finite KKT diagnostic convention only**. KKT complementarity requires the multiplier of a strictly inactive inequality to be zero. IPOPT's raw multiplier remains logged unchanged.

The amendment does **not** modify:

- the local NLP supplied to IPOPT;
- any primal trajectory;
- any Sun–Sun update;
- the TCC matrices;
- any physical constraint;
- any accepted threshold;
- the backend options;
- the no-retry policy.

Active and near-active inequalities retain their raw backend multiplier and are still subject to the same nonnegativity test.

### 3.1 Attempt-1 failure row replay

At `t=17`, Attempt 2A reproduced the same raw data:

```text
row       = 30
label     = a1:W:k8:dim1:upper
raw mu    = -9.56248038286337e-08
g          = -2.9999999927837857
```

Since

\[
g<-100\tau_W=-10^{-6},
\]

the diagnostic multiplier is set to zero. The event log records both the raw value and the reason for the diagnostic zeroing.

Thus the correction demonstrably removed the exact Attempt-1 blocker without loosening `dual_normalized=1e-8`.

---

## 4. Frozen quantities deliberately unchanged

Attempt 2A uses the exact original baseline configuration file:

```text
configs/baseline_2uav_0obs.json
SHA-256 a9120c15840c8ec1605f8ce5d21d946ac1734672bde044ea1e9bacbc55750784
```

The physical instance remains:

\[
N=2,\quad q=2,\quad K=8,\quad \Delta t=0.5\ \mathrm{s},
\]

\[
p_1^0=(-2,0),\quad p_2^0=(0,-2),
\]

\[
g_1=(2,0),\quad g_2=(0,2),
\]

with zero obstacles and required UAV center clearance

\[
\rho_{12}^{\mathrm{uav}}=0.4\ \mathrm m.
\]

The same Algorithm-2 and IPOPT values remain frozen, including

\[
\beta^1=2,\qquad \rho^1=4,
\]

`max_inner_iterations=100`, limited-memory IPOPT Hessian, and all original tolerances.

---

## 5. Code-level change and verification before execution

The executable change is confined to `src/diagnostics.py`, with the necessary diagnostic dataclass fixture synchronization in `tests/test_control_flow.py` and three new focused tests in

```text
tests/test_activity_aware_multiplier_diagnostic.py
```

The source change is reviewable in

```text
verification_attempt2a/ATTEMPT1_TO_ATTEMPT2A_SRC.diff
verification_attempt2a/ATTEMPT1_TO_ATTEMPT2A_TESTS.diff
```

Before running Attempt 2A, the complete test suite passed:

```text
56 passed in 5.99 s
```

The three added tests specifically establish that:

1. a strongly inactive workspace row with a negative raw multiplier is zeroed **only in the diagnostic copy**, while the raw multiplier is preserved;
2. an active workspace row with the same negative multiplier is **not** zeroed and still fails the frozen dual-sign test;
3. no frozen numerical threshold was changed.

### 5.1 Executed environment

```text
Python      3.13.5
NumPy       2.3.5
SciPy       1.17.0
Matplotlib  3.10.8
CasADi      3.7.2
```

Deterministic process variables:

```text
PYTHONHASHSEED=0
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
```

The actual Attempt-2A `src/diagnostics.py` SHA-256 recorded by each run is

```text
4bcef4c418c46d6938f4e50b4c1ec0b39811e821f3d017a7f657837e7945e84a
```

All other solver source hashes remain those from the Step-2/Attempt-1 package.

---

## 6. Executed commands

Each experimental run was launched in a separate Python process with the same frozen environment.

Logical command for run 1:

```bash
PYTHONHASHSEED=0 \
OMP_NUM_THREADS=1 \
OPENBLAS_NUM_THREADS=1 \
MKL_NUM_THREADS=1 \
python run_experiment.py \
  --config configs/baseline_2uav_0obs.json \
  --output runs/attempt2a_run1
```

Run 2 used the identical command with output directory `runs/attempt2a_run2`.

No retry was performed within either run.

---

# 7. Numerical results

## 7.1 Termination

Both independent runs returned:

```text
termination_reason = MAX_INNER_ITERATIONS
primary_cause      = PHYSICAL_VIOLATION_DETECTED
all_causes         = [
  MAX_INNER_ITERATIONS,
  TCC_NOT_ACCEPTED,
  PHYSICAL_VIOLATION_DETECTED
]
last complete      = (r,t) = (1,100)
```

The two wall-clock times were about 32 s and are not deterministic acceptance quantities.

## 7.2 Local finite-oracle diagnostics

Every one of the 100 accepted inner iterations passed both local finite-oracle checks.

Across the whole run, UAV 1 had

\[
\max_t R_{\mathrm{dual},1}^{\mathrm{norm}}=0,
\]

\[
\max_t R_{\mathrm{comp},1}=1.0000031292354875\times10^{-11},
\]

\[
\max_t R_{\mathrm{stat},1}^{\mathrm{norm}}
=3.952334901899828\times10^{-7}<10^{-6},
\]

and zero descent violation. UAV 2 likewise passed throughout, with maximum normalized stationarity residual about

\[
7.842267230241798\times10^{-9}.
\]

At the last complete iterate, the only nonzero UAV-1 diagnostic multipliers correspond to the two near-active guardian UAV-safety rows `k3` and `k4`; the strongly inactive rows are diagnostic-zeroed while their raw backend multipliers remain in the log.

This finite diagnostic pass still does **not** establish the exact Sun–Sun first-block normal-cone oracle.

## 7.3 Inner residuals

At `t=1`:

\[
R_1=14.95635361042984,
\qquad
R_3=1.0370365353139532.
\]

At `t=17`:

\[
R_1=0.3475876944914568,
\qquad
R_3=0.01387458747976318.
\]

At `t=100`:

\[
\boxed{R_1=0.01343852896082126},
\]

\[
\boxed{R_2=1.0401237528903013\times10^{-15}},
\]

\[
\boxed{R_3=0.0002248160621244216}.
\]

The required `r=1` thresholds are

\[
\epsilon_1^1=\epsilon_2^1=10^{-4},
\qquad
\epsilon_3^1=10^{-6}.
\]

Thus, at the cap,

\[
R_1/\epsilon_1^1\approx134.39,
\qquad
R_3/\epsilon_3^1\approx224.82.
\]

The tail of `R1` is decreasing, and `R3` is also much smaller than initially, but the protocol does not permit extrapolating this trend into a convergence claim. The only admissible conclusion is that **100 inner iterations were insufficient under this configuration**.

## 7.4 TCC status

At the last complete state:

\[
\boxed{R_{\mathrm{TCC,eq}}=0.12581049903927163\ \mathrm m},
\]

\[
\boxed{R_{\mathrm{target}}=0.08896145701513261\ \mathrm m}.
\]

Both are far above the frozen `1e-6 m` acceptance levels.

Therefore

```text
TCC_CONSISTENT = false
```

and no exact-lift interpretation is available at this finite state.

## 7.5 Objective behavior

At the last complete state,

\[
F=3.9962839227687965,
\]

with

\[
f_1=1.9972397385660279,
\qquad
f_2=1.9990441842027686.
\]

Terminal goal errors are small:

\[
\|p_1^K-g_1\|=0.02345173333151424\ \mathrm m,
\]

\[
\|p_2^K-g_2\|=0.026570298695394772\ \mathrm m.
\]

These values are descriptive only. The run did not satisfy the distributed stopping conditions, and no global-optimality claim is made.

---

# 8. Physical postcheck and why it failed

Workspace and speed margins pass numerically:

\[
m_{W,\min}=1.023424852321479\ \mathrm m>0,
\]

\[
m_{\mathrm{spd},\min}=0.21869369907162417\ \mathrm m>0.
\]

The obstacle family is correctly verified empty.

However, the actual source trajectories violate UAV–UAV clearance. The required center distance is

\[
0.4\ \mathrm m.
\]

On physical interval `k=4`, at approximately

\[
\lambda=0.05377602986432309,
\]

the independently recomputed source-source distance is

\[
0.2861322983824108\ \mathrm m,
\]

so the ordinary numerical physical margin is

\[
\boxed{-0.11386770161758925\ \mathrm m}.
\]

Hence

```text
PHYSICAL_POSTCHECK_NUMERIC_PASS = false
MODEL0D_SAFETY_CERTIFIED        = false
```

The second status would remain unavailable even with positive ordinary margins because U4 is unresolved.

## 8.1 Why the local guardian constraint can pass while the actual sources collide

This is a crucial TCC point, not a contradiction.

UAV 1, as guardian, enforces pair safety locally against its **copy of source 2**. At the final state the independently recomputed minimum guardian distance is

\[
0.4000000000920143\ \mathrm m,
\]

with a tiny positive numerical margin

\[
9.201428508021081\times10^{-11}\ \mathrm m.
\]

So the guardian-localized pair constraint is numerically satisfied.

But TCC has not converged. The guardian's source-2 copy differs from the true UAV-2 source trajectory by

\[
R_{\mathrm{TCC,eq}}=0.12581049903927163\ \mathrm m
\]

in stacked norm. Near the physical closest-approach interval, the copy/source-2 mismatch is of order `0.1 m`, large enough to explain the difference between the guardian-safe geometry and the actual-source collision geometry.

Therefore this failure illustrates exactly why

\[
\boxed{\text{local guardian safety} + \text{nonzero TCC mismatch}\not\Rightarrow\text{actual-source safety}.}
\]

The TCC reformulation recovers physical exactness at exact copy agreement; Attempt 2A did not reach that state before its finite cap.

---

# 9. Numerical integrity

The final algebraic checks pass:

\[
R_{\mathrm{id}}
=2.5443010932208815\times10^{-17}
\le10^{-12},
\]

\[
R_{\rho\beta}=0.
\]

No NaN/Inf, missing multiplier mapping, residual crosscheck failure, or nonsmooth blocking row was reported.

`NUMERICALLY_VALID=true` in the implementation means the finite state and evaluators were numerically well-formed. It does **not** mean TCC consistency, physical safety, Algorithm-2 certification, or experiment success.

---

# 10. Reproducibility

A completely separate second process reproduced the first run.

After excluding only wall-clock timing fields (`elapsed_s`, `backend_elapsed_s`):

```text
termination reason                    exact equal
primary cause                         exact equal
all causes                            exact equal
sanitized summary                     exact equal
sanitized complete event history      exact equal
all saved final-state arrays          bit-for-bit exact equal
maximum final-state absolute diff     0.0
```

Therefore Attempt 2A passes the approved same-environment reproducibility requirement by a margin stronger than the required `1e-10` numerical tolerance.

The independent verifier does **not** import the solver implementation. It recomputed the objective, TCC residuals, algebraic identity, workspace/speed margins, actual-source UAV margin, and guardian-copy UAV margin directly from the persisted configuration and NPZ state. Every reported scalar crosscheck agreed within `1e-12` (maximum observed discrepancy was floating-point roundoff of about `5.55e-17`).

---

# 11. Comparison with Attempt 1

| Quantity | Attempt 1 | Attempt 2A |
|---|---:|---:|
| stop point | `r=1,t=17 attempted`; last complete `t=16` | `r=1,t=100` |
| local-oracle abort | yes | **no** |
| Attempt-1 row-30 diagnostic multiplier | raw negative caused abort | raw negative retained, diagnostic zero |
| \(R_1\) at last complete state | `0.3766973234` | **`0.0134385290`** |
| \(R_3\) at last complete state | `0.0174566981` | **`0.0002248161`** |
| \(R_{TCC,eq}\) | `0.3029946623 m` | **`0.1258104990 m`** |
| \(R_{target}\) | `0.2142495804 m` | **`0.0889614570 m`** |
| numerical actual-source UAV margin | `+0.1008499535 m` | **`-0.1138677016 m`** |
| baseline reliable for expansion | no | **no** |

Attempt 2A therefore validates the specific diagnosis of the Attempt-1 blocker: the tiny negative multiplier on a far-inactive workspace row was a finite diagnostic issue, not the main long-run convergence blocker.

But Attempt 2A also exposes the next blocker: **the frozen 100-iteration inner cap is reached while copy agreement and primal/slack residuals remain too large.** Because TCC is still incomplete, the actual sources can be unsafe even while the guardian's local source/copy constraint is satisfied.

---

# 12. What this experiment does and does not establish

## Established numerical facts

1. The activity-aware multiplier diagnostic removes the exact Attempt-1 false rejection while preserving raw backend evidence.
2. All 100 local first-block solutions pass the amended finite diagnostic.
3. Algorithm-2 residuals substantially decrease but do not meet the frozen inner stopping thresholds by iteration 100.
4. TCC agreement is not reached.
5. The last complete actual source trajectories violate the UAV–UAV clearance numerically.
6. The entire Attempt-2A result is exactly reproducible in the same recorded environment.

## Not established

- exact Sun–Sun first-block oracle compliance;
- `SUNSUN_ALGORITHMICALLY_CERTIFIED`;
- `MODEL0D_SAFETY_CERTIFIED`;
- exact safety under U4;
- convergence if the cap were increased;
- global optimality;
- success of the future order-preserving Model-1-like geometry;
- obstacle-scenario readiness.

U3 remains conditional and U4 remains unselected.

---

# 13. Rigorous next choices — not executed in Attempt 2A

No further parameter was changed after seeing Attempt-2A outcomes.

The evidence now supports two **separate** possible next experiments, each requiring researcher approval:

1. **Attempt 2A.1 — isolate the finite-cap question.** Keep the crossing geometry, activity-aware diagnostic, backend and all thresholds unchanged; change only `max_inner_iterations` under an explicitly approved successor protocol. This would test whether the observed decreasing residual sequence actually reaches the source tolerances rather than assuming it will.

2. **Attempt 2B — scaled order-preserving Model-1-like geometry.** Introduce the separately discussed scaled start/goal geometry while keeping the algorithmic framework fixed. This tests the researcher's intended order-preserving visual/physical scenario and must not be conflated with the cap investigation.

Running both changes simultaneously would make causal interpretation weaker and is not recommended for the immediate next experiment.

---

# 14. Traceability note

The live branch still points to

```text
bd4b7f19d687cf78976d3c99501ca1a75c4c91ce
```

and Attempt 2A has **not** been committed.

A repository inspection also confirms that, at this checkpoint, the root `model0d_alg2_numerics/src/` and `tests/` entries on GitHub are still empty scaffolding directories; the executable Step-2/Step-3 code used for Attempt 2A comes from the exact previously delivered local Step-3 package. Therefore **GitHub alone is not yet sufficient to reproduce the executable campaign**. The complete Attempt-2A package delivered with this report is the current reproducible code/evidence artifact. A future repository commit should be performed only after explicit researcher permission and should include the executable source/tests, not only traceability records.

This is a traceability limitation, not a scientific reinterpretation of the numerical result.

---

# 15. Final worker verdict

\[
\boxed{\text{ATTEMPT 2A: REPRODUCIBLE FAILURE AT THE INNER CAP}}
\]

The Attempt-1 multiplier-noise issue is successfully corrected. The current crossing baseline still does **not** qualify as reliable because the inner process has not converged within 100 iterations, TCC agreement remains incomplete, and the last complete actual source trajectories violate pairwise clearance numerically.

No obstacle expansion is justified from Attempt 2A.

This report is a DAILY WORKER result and remains subject to researcher challenge, independent audit, and explicit final researcher approval.
