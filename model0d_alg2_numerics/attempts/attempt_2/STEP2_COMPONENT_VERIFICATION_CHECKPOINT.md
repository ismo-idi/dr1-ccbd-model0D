# Model 0-D Algorithm-2 numerics — Step 2 component-verification checkpoint

**Date:** Friday, 11 September 2026  
**Role:** DAILY WORKER  
**Researcher / final scientific decision-maker:** Ismaël Assoumane Idi  
**Repository / branch:** `ismo-idi/CCBO_Model1` / `Model-0_24-Aug-2026`  
**Repository traceability baseline / current remote HEAD:** `de49211ddd924e4751b7303ec3f1f2949b16bb23`  
**Protocol:** researcher-approved `MODEL0D_NUMERICAL_PROTOCOL_AND_READINESS_V1_0_11_SEP_2026.md`  
**Status:** **STEP 2 LOCALLY PASSED — IMPLEMENTATION READY FOR THE FIRST BOUNDED BASELINE EXPERIMENT, SUBJECT TO RESEARCHER DIRECTION**  
**Git status:** local working package only; no Step-2 commit or push performed. A future commit requires fresh explicit researcher authorization.

---

## 1. Scope and stopping boundary

Step 2 performs the approved **pre-baseline component verification** only. It does not inspect a complete Model-0D Algorithm-2 baseline outcome.

The `runs/` directory remains empty. No invocation of the real `run_experiment.py` baseline execution path was performed. The only use of the real baseline numerical data beyond static assembly was the protocol-required **one first-block solve per UAV from the accepted stationary/hover initialization**, used solely to verify the local CasADi/IPOPT backend, multiplier interface, finite oracle diagnostics, and hover treatment. Those local solves were not interpreted as a planning result.

No numerical protocol threshold, scenario datum, Algorithm-2 parameter, backend option, iteration cap, stopping rule, TCC architecture, or physical model choice was retuned during Step 2.

---

## 2. Authoritative implementation formulas checked

The verified implementation preserves the selected split and updates:

\[
S_{1\leftarrow 2}z_1-u_e=0,
\qquad
S_{2\leftarrow 2}z_2-u_e=0,
\]

\[
B^\top B=2I_Q,
\qquad Q=qK=16,
\]

\[
\rho^r=2\beta^r,
\]

\[
u_e^{r,t}
=
\operatorname{Proj}_{\mathcal B_K}
\left(
\frac{\psi_{e,1}^{r,t}+\psi_{e,2}^{r,t}}{2}
\right),
\]

\[
\xi^{r,t}
=-
\frac{\lambda^r+y^{r,t-1}+\rho^r(AZ^{r,t}+BU^{r,t})}
{\beta^r+\rho^r},
\]

\[
y^{r,t}
=y^{r,t-1}
+\rho^r(AZ^{r,t}+BU^{r,t}+\xi^{r,t}),
\]

and the exact floating-point integrity identity monitored after the update,

\[
\lambda^r+\beta^r\xi^{r,t}+y^{r,t}=0
\]

up to the researcher-approved finite integrity tolerance.

The direct residual implementation remains

\[
R_1^{r,t}
=
\left\|
\rho^r A^\top
\bigl[B(U^{r,t-1}-U^{r,t})+\xi^{r,t-1}-\xi^{r,t}\bigr]
\right\|,
\]

\[
R_2^{r,t}
=
\left\|
\rho^r B^\top(\xi^{r,t-1}-\xi^{r,t})
\right\|,
\]

\[
R_3^{r,t}
=
\|AZ^{r,t}+BU^{r,t}+\xi^{r,t}\|.
\]

The peer-to-peer reductions are independently cross-checked against the matrix forms before any complete inner snapshot is accepted.

---

## 3. Required protocol checks and evidence

| Approved pre-baseline requirement | Step-2 evidence | Result |
|---|---|---|
| Exact dimensions \(Q=16,d_1=32,d_2=16,M_{eq}=1,m=32\) | `test_structure.py` | PASS |
| Selector extraction / fixed-prefix reconstruction | `test_structure.py::test_fixed_prefix_selector_and_architecture_legality` | PASS |
| One objective per source; no foreign-copy objective duplication | `test_local_nlp_contract.py::test_objective_is_source_counted_once_and_foreign_copy_does_not_duplicate_it` | PASS |
| Guardian-localized all-pairs physical coupling exactly once | constraint-count and metadata tests | PASS |
| \(\mathcal W\subset\operatorname{int}\mathcal B\) | frozen-config validator + structure test | PASS |
| Communication/equality/reduction edge legality | exact frozen-config validator + structure test | PASS |
| Exact stationary TCC lift / local-domain feasibility | `test_stationary_exact_lift_is_feasible_for_both_local_domains_and_a1` | PASS |
| \(B^\top B=2I\) and exact split elimination | `test_tcc_split.py` | PASS |
| Exact guarded segment geometry | dense sampling, bounded scalar minimization, symbolic/numeric and obstacle/UAV wrapper tests | PASS |
| Backend multiplier sign | scalar analytic KKT test | PASS |
| Backend multiplier row order | distinct two-row analytic KKT test (expected multipliers 2 and 4) | PASS |
| Missing multiplier mapping | explicit `MULTIPLIER_DIAGNOSTIC_UNAVAILABLE`; no reconstruction | PASS |
| Independent constraint-value recomputation | NumPy family recomputation cross-checked against CasADi solver graph | PASS |
| Local Jacobian / \(\nabla\phi\) assembly | central finite-difference component check at a non-switching point | PASS |
| Hover-initialized local first-block backend interface | one component solve per UAV; details in `verification/hover_first_block_component.json` | PASS |
| \(R_1\) aggregation | P2P vs independent matrix form | PASS |
| \(R_2\) symmetric half accounting | P2P vs independent matrix form | PASS |
| \(R_3\) full half-row norm | direct independent recomputation | PASS |
| Slack/dual identity | pure update unit test + integrity predicate | PASS |
| First penalty rule with \(\xi^0=0\) | pure outer-update unit test | PASS |
| Lambda safeguard projection | pure outer-update unit test | PASS |
| Acceptance barrier before A5 | synthetic control-flow test; A5 is forbidden if either local oracle fails | PASS |
| Success on final permitted inner iteration != cap exhaustion | synthetic control-flow test | PASS |
| Inner cap / outer cap finalization | synthetic control-flow tests | PASS |
| Timeout at outer and inner boundaries | synthetic control-flow tests | PASS |
| Backend-construction failure | explicit `SOLVER_BACKEND_FAILURE` finalization | PASS |
| Initialization integrity failure | explicit common finalization | PASS |
| Update NaN/Inf failure | explicit `NUMERICAL_NAN_INF`; partial candidate not accepted | PASS |
| Residual cross-check failure | explicit `ALGEBRAIC_INTEGRITY_FAILED` before snapshot acceptance | PASS |
| Postcheck evaluator exception/incompleteness | `POSTCHECK_EVALUATION_FAILED`, not relabeled as physical violation | PASS |
| Two-consecutive-outer-pass finite-stop rule | synthetic control-flow test | PASS |
| Empty obstacle family | expected count 0, violation 0, categorical N/A margin | PASS |
| Physical postcheck uses source trajectories, not guardian foreign copy | dedicated source-semantics test | PASS |
| Non-finite JSON evidence | categorical markers; no JSON NaN/Inf tokens | PASS |
| Frozen protocol/config values | exact scenario/backend/algorithm/threshold locks; drift tests | PASS |
| Deterministic process environment | entrypoint guard for the four approved environment variables | PASS |
| Reproducible code evidence | source-file SHA-256 manifest support and environment record | PASS at component level; two-process baseline comparison remains Step 3 |

---

## 4. Complete test result

Final clean component suite:

```text
53 passed in 2.51 s
```

JUnit evidence: `verification/pytest_results.xml`.  
Test inventory: `verification/test_inventory.txt`.  
Compilation check: `verification/compileall.txt`, exit code 0.  
Coverage run: **93% aggregate statement coverage over `src/`**, with 53/53 tests passing; exact report is `verification/coverage_stdout.txt`.

Coverage is supporting engineering evidence, not a scientific correctness certificate.

---

## 5. Hover-initialization backend component result

This is deliberately **not a full baseline run**. It is the required first-block/backend readiness check from the exact stationary TCC lift with \(\rho=4\), \(\xi=0\), and \(y=0\).

### UAV 1 local block

- IPOPT status: `Solve_Succeeded`
- iterations: 102
- finite output: yes
- multiplier mapping available: yes
- independent constraint-value cross-check: pass
- cross-check absolute mismatch: approximately \(8.88\times10^{-16}\)
- normalized multiplier-sign violation: approximately \(7.08\times10^{-10}\)
- complementarity residual: approximately \(3.21\times10^{-9}\)
- normalized smooth-stationarity residual: approximately \(1.46\times10^{-9}\)
- local nonincrease residual: \(0\)
- nonsmooth blocking rows at returned candidate: none
- finite oracle execution criterion: **PASS**

### UAV 2 local block

- IPOPT status: `Solve_Succeeded`
- iterations: 17
- finite output: yes
- multiplier mapping available: yes
- independent constraint-value cross-check: exact to reported floating precision
- normalized multiplier-sign violation: approximately \(1.60\times10^{-11}\)
- complementarity residual: approximately \(1.14\times10^{-9}\)
- normalized smooth-stationarity residual: approximately \(1.68\times10^{-11}\)
- local nonincrease residual: \(0\)
- nonsmooth blocking rows at returned candidate: none
- finite oracle execution criterion: **PASS**

These numbers establish only that the first-block backend interface can leave the hover initialization and return candidates satisfying the frozen finite execution diagnostics in this component check. They do **not** establish the exact Sun--Sun Assumption-3 normal-cone oracle.

---

## 6. Implementation defects/gaps discovered and corrected during Step 2

The following were corrected **before any complete baseline run**. None changes the approved numerical protocol or frozen mathematics.

1. **Test-launch import robustness.** Direct `pytest` initially did not place the package root on the import path in this environment. Added `pytest.ini` so both `pytest` and `python3 -m pytest` execute the same suite reliably.
2. **Incomplete protocol drift protection.** Step 1 validated only a subset of frozen settings. Step 2 now rejects silent changes to all approved model/scenario, TCC, Algorithm-2, backend and threshold values.
3. **Deterministic environment was recorded but not enforced.** `run_experiment.py` now refuses execution unless `PYTHONHASHSEED=0`, `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, and `MKL_NUM_THREADS=1` are active, before creating a run directory.
4. **Multiplier availability/order handling needed an explicit failure path.** Missing or mis-sized multiplier vectors now produce `MULTIPLIER_DIAGNOSTIC_UNAVAILABLE`; no multiplier is invented or reconstructed.
5. **Simultaneous failure causes were not fully preserved.** Local diagnostics now retain all applicable causes in protocol priority order rather than only one code.
6. **Constraint-value checks were tied to the solver graph.** Added independent NumPy recomputation of every local physical/A1 row and an algebraic cross-check against the CasADi representation using the already-approved integrity scale.
7. **Residual cross-checks were calculated but not enforced.** P2P \(R_1/R_2\) values are now required to agree with the independent matrix forms before the snapshot is accepted.
8. **Physical evaluator incompleteness could be conflated with physical violation.** Missing/non-finite/incomplete postchecks now yield `POSTCHECK_EVALUATION_FAILED`; a complete finite negative-margin result is the separate physical-violation case.
9. **`NUMERICALLY_VALID` completion logic was too weak.** It now requires finite state/integrity plus finite TCC evaluation and complete physical evaluator execution; it remains logically separate from TCC and physical pass/fail.
10. **Finalization logic was duplicated across exits.** All normal runtime exit branches now feed one common finalization helper (with a guarded backend-construction failure record before that helper can exist), and every finalization records the termination reason, all causes, primary cause, status fields and last complete snapshot identifier.
11. **Non-finite failure diagnostics could break strict JSON logging.** They are converted to explicit categorical strings rather than JSON NaN/Infinity tokens.
12. **Local backend reporting lacked elapsed time.** Local solve status, iteration count and elapsed time are now retained in oracle diagnostics.
13. **Objective reporting lacked the requested regularization decomposition.** The harness now records terminal tracking, goal error, squared-step sums and weighted step-regularization terms separately.
14. **Implementation hash evidence was absent from future run records.** `run_experiment.py` now records SHA-256 hashes of the executable and all source modules in the run environment record.

One verification-only test adjustment was also made: SciPy's bounded scalar minimizer does not necessarily evaluate the exact interval endpoints. The independent geometry test was corrected to compare against the minimum of the bounded-solver candidate **and both exact endpoints**. This changed only the test methodology, not any Model-0D geometry code or tolerance used by experiments.

---

## 7. Frozen configuration / protocol identity

The protocol copy included in this local package has Git blob identity

```text
38d0f0bb83cfa136ea614752d9aa2e67cb9fba0b
```

which matches the file committed at the repository traceability baseline. Its SHA-256 is

```text
5fe939984ece604c064ad21d748fb7ccbad08f2571d2decb3a072c5971c77262
```

The baseline and predefined obstacle JSON files were not retuned during Step 2.

---

## 8. Scientific claim boundary after Step 2

Step 2 supports the following engineering statement only:

\[
\boxed{
\text{the bounded N=2 implementation has passed the approved pre-baseline component gate.}
}
\]

It does **not** imply

\[
\texttt{SUNSUN\_ALGORITHMICALLY\_CERTIFIED},
\]

because finite KKT-balance diagnostics still do not construct a generally valid exact normal-cone witness.

It does **not** imply

\[
\texttt{MODEL0D\_SAFETY\_CERTIFIED},
\]

because U4 remains unselected. Ordinary floating-point source-trajectory margins will remain numerical diagnostics only.

U3 remains conditional. No global-optimality, theorem-applicability, or real-UAV execution claim is made.

---

## 9. Step-2 verdict and next bounded action

### Worker verdict

\[
\boxed{\text{STEP 2 COMPONENT GATE: PASS}}
\]

No blocking component defect remains from the approved Step-2 checklist.

### Next action, not yet executed

The next bounded task is **Step 3: execute the first approved 2-UAV / 0-obstacle baseline run**, then execute it again from a fresh Python process and apply the frozen reproducibility and numerical-reliability gate. No obstacle scenario is permitted until that baseline gate passes.

The current package remains **local, uncommitted, unaudited working evidence**. A GitHub commit requires a separate explicit researcher go-ahead.
