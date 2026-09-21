# Model 0-D — Numerical Protocol and Implementation-Readiness Package v1.0

**Date:** Friday, 11 September 2026  
**Role:** DAILY WORKER  
**Researcher / final scientific decision-maker:** Ismaël Assoumane Idi  
**Project:** Constrained Consensus-Based Optimization for Decentralized Path Planning in UAV Swarms  
**Repository:** `ismo-idi/CCBO_Model1`  
**Scientific branch:** `Model-0_24-Aug-2026`  
**Live branch HEAD inspected:** `d0ce5a5609672f813f3c2f8e936b3e06dd4ff7b2`  
**HEAD message:** `Freeze Model 0-D post-audit state and execution plan`  
**Status:** **APPROVED NUMERICAL PROTOCOL — researcher approval on 11 September 2026; implementation/results remain unaudited and unapproved until the final independent audit and explicit researcher approval**  
**GitHub traceability status:** at protocol approval, no GitHub write had been performed. The researcher explicitly authorized the initial `model0d_alg2_numerics/` traceability commit on 11 September 2026 at 10:15:20Z. Committing this package records traceability only; it does not independently audit or finally approve future implementation/results.

**Approval / traceability record:** the researcher approved the complete protocol at 2026-09-11T10:13:24Z and authorized the initial repository traceability commit at 2026-09-11T10:15:20Z. Section 17 is retained as the historical pre-approval decision request that was answered affirmatively. Before this commit, the live branch was rechecked at `fbb66c38104eac59579a644d00fbd4e41751bdcd` (`Publish approved 11–15 September Markdown timetable and current handoff`). The earlier `d0ce...` line above records the checkpoint inspected during protocol preparation, not the pre-commit branch head.

---

## 0. Scope and repository checkpoint

This package freezes the proposed **bounded numerical experiment wrapper** for the already-approved Model 0-D / TCC / Sun--Sun Algorithm-2 mathematics. It does not reopen Gate 3, Gate 4, algorithm selection, the approved v1.4 synthesis, or the timetable.

Read-only inspection confirms:

- Gate 3 and formal Gate 4 are complete in the current continuation state.
- The approved v1.4 PDF and exact LaTeX are present under `Model-0D_PDF/`.
- Decision 15 is the normative solver specification.
- The current branch contains **no current Sun--Sun implementation outside `old-main/`**. Python material found under `old-main/` is historical and is not reused as current scientific authority or silently treated as the selected implementation.
- The current timetable requires protocol approval before experimental outcome inspection, a 2-UAV/0-obstacle baseline first, the Saturday-noon contingency checkpoint, at most one predefined obstacle scenario before optional extras, and a hard numerical cutoff Saturday at 17:00.

### Governing source locations

- `MODEL0D_APPROVED_TIMETABLE_11-15_SEP_2026.md`, especially **Starting state and priorities**, **Approved session table**, **Decisive contingency and protected time**, and **Execution, evidence and approval rules**.
- `MODEL0D_CONTINUATION_BACKUP_PROMPT.md`, §§0--3 and current-state summary.
- `decisions/06_frozen_deterministic_model0d_physical_problem.md`, §§2--7 and frozen physical constraints.
- `decisions/10_solver_analytic_representation_model0d.md`, exact segment-distance solver representation.
- `decisions/12_constraint_qualification_study_model0d.md`, active smoothness / degeneracy and MFCQ boundary.
- `decisions/13_kkt_study_model0d.md`, local KKT convention and multiplier families.
- `decisions/14_TCC_formulation.md`, exact TCC architecture and exactness/rank results.
- `decisions/15_Sun-Sun_TCC_algorithm.md`, especially §§3--5, 7--20, 22--25, 27--31.
- `decisions/work_06_SEP_2026.txt`, especially Q2/Q3/Q7--Q9 and U3/U4.
- Sun & Sun, *Computational Optimization and Applications* 84 (2023), checked PDF viewer pp. 9--18 as pinned by Decision 15.

---

# 1. Readiness assessment

## 1.1 Current implementation state

**Verdict:** implementation must start from a new, minimal current solver path. No current selected-algorithm implementation exists on the scientific branch outside the historical `old-main/` subtree.

This is not a blocker. Decision 15 is sufficiently explicit to assemble the smallest complete N=2 implementation without reopening mathematics.

## 1.2 Verified local execution environment

Readiness commands executed before outcome inspection:

```text
Python      3.13.5
NumPy       2.3.5
SciPy       1.17.0
Matplotlib  3.10.8
CasADi      3.7.2
CasADi IPOPT plugin: available
```

`cyipopt` is not installed, but is not required because CasADi's IPOPT plugin is available.

A separate analytic backend sign sanity check was executed only to validate multiplier convention, not as a Model-0D experiment:

\[
\min_x (x-2)^2\quad\text{s.t.}\quad x\le1.
\]

With the constraint supplied to CasADi/IPOPT as an upper bound, the returned `lam_g` is positive and satisfies the KKT stationarity balance. Therefore the implementation will use

\[
\boxed{\mu=\texttt{lam\_g}\ge0}
\]

for explicit local inequalities written as \(g(z)\le0\) and supplied with `ubg=0`. This mapping will also be unit-tested inside the implementation package before the baseline is inspected.

## 1.3 Readiness verdict

\[
\boxed{\text{READY TO IMPLEMENT ON RESEARCHER APPROVAL OF THIS PROTOCOL}}
\]

The main unresolved scientific limitations are deliberately **not** treated as blockers for an uncertified numerical campaign:

- **U3:** the CPLD route to the actual Algorithm-2 dual sequence remains conditional.
- **Finite oracle:** passing finite local KKT/feasibility diagnostics does not prove the exact Sun--Sun normal-cone first-block oracle.
- **U4:** exact physical sign-certification technology remains unselected. Ordinary double-precision margins may be reported only as numerical diagnostics, never as `MODEL0D_SAFETY_CERTIFIED`.

---

# 2. Frozen campaign boundary

The numerical campaign is deliberately small:

1. implement and component-test the exact selected Algorithm-2/TCC path;
2. execute and repeat the **2-UAV / 0-obstacle baseline**;
3. at Saturday noon, classify the baseline as numerically reliable for expansion or not;
4. only if it passes, execute **one predefined 1-obstacle scenario**;
5. no more-UAV scaling, parameter sweep, Algorithm-3 campaign, ALADIN comparison, spline implementation, or outcome-driven threshold retuning.

No threshold, backend option, scenario datum, cap or stopping rule below may be changed after baseline outcomes are inspected without an explicit protocol revision approved by the researcher and recorded as such.

---

# 3. Frozen baseline scenario proposed for approval

## 3.1 Physical instance

The baseline is a deliberately small but nontrivial crossing-traffic problem.

| Quantity | Frozen proposed value |
|---|---|
| UAV count | \(N=2\) |
| dimension | \(q=2\) |
| horizon intervals | \(K=8\) |
| step | \(\Delta t=0.5\,\mathrm{s}\) |
| horizon | \(4\,\mathrm{s}\) |
| workspace | \(\mathcal W=[-3,3]\times[-3,3]\,\mathrm m\) |
| UAV radii | \(r_1=r_2=0.10\,\mathrm m\) |
| inter-UAV margin | \(\delta_{12}^{\mathrm{uav}}=0.20\,\mathrm m\) |
| required center clearance | \(\rho_{12}^{\mathrm{uav}}=0.40\,\mathrm m\) |
| max speeds | \(v_1^{\max}=v_2^{\max}=1.5\,\mathrm{m/s}\) |
| starts | \(p_1^0=(-2,0)\), \(p_2^0=(0,-2)\) m |
| goals | \(g_1=(2,0)\), \(g_2=(0,2)\) m |
| objective weights | \(\alpha_1=\alpha_2=20\), \(\beta_1=\beta_2=1\) |
| obstacle registry | \(\mathcal O=\varnothing\) |

The corresponding straight goal-directed paths intersect, so the baseline exercises the all-pairs physical coupling even though there are no obstacles. The accepted initialization remains the exact stationary lift

\[
p_i^k=p_i^0,\qquad k=1,\ldots,K.
\]

The initial pair clearance is strict. The initial exact segment rows are degenerate because of the stationary lift; that fact is handled by the frozen degeneracy policy in §7 below and is not hidden.

## 3.2 TCC architecture

Use the fixed connected communication graph

\[
G_0^{\mathrm{comm}}=(\{1,2\},\{\{1,2\}\}).
\]

Choose the endpoint-valid guardian

\[
\boxed{\gamma(\{1,2\})=1.}
\]

Then

\[
V_1^{\mathrm{copy}}=\{1\},\qquad
V_2^{\mathrm{copy}}=\{1,2\},
\]

with the single source-2 equality tree edge

\[
E_2^{\mathrm{eq}}=\{\{1,2\}\}.
\]

This is relay-free and satisfies the frozen N=2 guardian-load rule. Define

\[
Q=qK=16,
\qquad M_{\mathrm{eq}}=1,
\qquad m=2QM_{\mathrm{eq}}=32.
\]

The local blocks are

\[
z_1=\operatorname{col}(x_{1,\mathrm{free}},\widetilde x_{1\leftarrow2})\in\mathbb R^{32},
\qquad
z_2=x_{2,\mathrm{free}}\in\mathbb R^{16}.
\]

The unique vector TCC equality concerns source 2 only. Its split auxiliary is \(u_e\in\mathbb R^{16}\). The reduction tree \(T^{\mathrm{redux}}\) is the same one-edge communication tree.

## 3.3 A1 box

Use

\[
\boxed{\mathcal B=[-3.5,3.5]^2\ \mathrm m},
\qquad
\mathcal B_K=\mathcal B^K.
\]

Thus

\[
\mathcal W\subset\operatorname{int}\mathcal B.
\]

A1 is applied only to the foreign source-2 copy held by UAV 1 and to the edge auxiliary through \(\bar X\). No additional A1 box is applied to physical source trajectories, and no A1 bound is added to \(\xi\), \(y\), or the outer multiplier beyond Algorithm 2's native safeguard.

---

# 4. Predefined obstacle scenario — frozen now, executed only after the baseline gate

If and only if the Saturday-noon baseline gate passes, use exactly the same physical/TCC/algorithm configuration and add one static circular obstacle:

\[
\boxed{c_1^{\mathrm{obs}}=(1,0)\,\mathrm m,\qquad R_1=0.35\,\mathrm m.}
\]

For both UAVs set

\[
\delta_i^{\mathrm{obs}}=0.10\,\mathrm m,
\]

hence the required obstacle-center clearance is

\[
\rho_{i1}^{\mathrm{obs}}=R_1+r_i+\delta_i^{\mathrm{obs}}=0.55\,\mathrm m.
\]

No other datum or threshold changes. This scenario is selected **before** any baseline result is inspected.

---

# 5. Backend and deterministic execution settings

## 5.1 First-block NLP backend

Selected proposed backend:

\[
\boxed{\text{CasADi 3.7.2 + IPOPT}}
\]

Reasons: installed and callable in the current environment; supports nonlinear constrained local blocks; exposes constraint multipliers; and permits independent residual recomputation from the returned primal/multiplier data.

Proposed frozen IPOPT options:

```text
ipopt.tol                 = 1e-9
ipopt.constr_viol_tol     = 1e-9
ipopt.dual_inf_tol        = 1e-8
ipopt.compl_inf_tol       = 1e-8
ipopt.max_iter            = 500
ipopt.acceptable_iter     = 0
ipopt.hessian_approximation = limited-memory
ipopt.bound_relax_factor  = 0
ipopt.print_level         = 0
print_time                = false
```

There is **no retry policy**. A failed local solve or failed independent oracle diagnostic terminates the run through the common finalization path.

## 5.2 Exact segment evaluator and nonsmooth hover treatment

The mathematical value function remains the exact guarded piecewise squared-distance representation from Decision 10. The code must branch on the exact mathematical degenerate condition \(s=0\); no \(s\le\varepsilon\) replacement is introduced into the physical model.

At a nonsmooth hover point, a backend branch derivative may be used internally as a numerical search device, but it is **never** treated as a mathematical smooth-oracle witness. Independent acceptance is governed by the returned candidate:

- if a required row is nondegenerate, use its justified ordinary derivative;
- if it is numerically degenerate but demonstrably strictly inactive under the frozen omission rule, keep the physical value check, set its diagnostic multiplier to zero and log the omission;
- otherwise terminate with `ORACLE_UNCERTIFIED_NONSMOOTH`.

The protocol diagnostic scale for identifying a **numerically near-degenerate** row is

\[
\boxed{\tau_s=10^{-12}\ \mathrm{m}^2.}
\]

This does not replace the exact mathematical condition \(s=0\); it only controls whether a finite smooth diagnostic is trusted.

---

# 6. Sun--Sun Algorithm-2 numerical settings

Freeze:

\[
\boxed{
\beta^0=1,
\qquad
\vartheta=2,
\qquad
\beta^1=2,
\qquad
\omega=0.5.
}
\]

Outer multiplier initialization and safeguard:

\[
\boxed{
\lambda^1=0,
\qquad
\underline\lambda=-100\mathbf 1,
\qquad
\overline\lambda=100\mathbf 1.
}
\]

At every outer iteration:

\[
\boxed{\rho^r=2\beta^r.}
\]

Source inner stopping schedules:

\[
\boxed{
\epsilon_1^r=\frac{10^{-4}}{r},
\qquad
\epsilon_2^r=\frac{10^{-4}}{r},
\qquad
\epsilon_3^r=\frac{10^{-6}}{r}.
}
\]

These are positive and converge to zero, as required by the source asymptotic parameter class. Their numerical values are experiment-wrapper choices, not claims that the published theorem applies to the finite implementation.

Finite caps:

```text
max_outer_iterations = 20
max_inner_iterations = 100
wall_clock_cap_per_run = 600 s
local_IPOPT_cap = 500 iterations per local solve
retry_count = 0
```

Success on the last permitted iteration is success; cap exhaustion means the corresponding explicit cap status.

---

# 7. Frozen finite-oracle diagnostics and thresholds

Every local candidate is independently checked after the backend returns. A solver `success=True` flag is insufficient.

## 7.1 Family-specific local feasibility thresholds

Canonical unscaled constraint functions are retained. Execution tolerances are family-specific:

\[
\boxed{
\begin{array}{ll}
\tau_W=10^{-8}\ \mathrm m, & \text{workspace rows},\\
\tau_{\mathrm{spd}}=10^{-8}\ \mathrm m^2, & \text{squared speed rows},\\
\tau_{\mathrm{obs}}=10^{-8}\ \mathrm m^2, & \text{squared obstacle rows},\\
\tau_{\mathrm{uav}}=10^{-8}\ \mathrm m^2, & \text{squared UAV--UAV rows},\\
\tau_{A1}=10^{-8}\ \mathrm m, & \text{foreign-copy box rows}.
\end{array}}
\]

These are **finite execution** thresholds. Passing them does not establish exact membership in \(X_a\).

A degenerate row may be omitted from the local smooth stationarity diagnostic only if its independently recomputed constraint value is strictly inactive by a **family-aware** buffer

\[
\boxed{\tau_{\mathrm{inactive},\mathcal F}=100\,\tau_{\mathcal F}}
\]

for its own constraint family. The row remains in the physical/constraint-value evaluation and its omission is logged.

Near-active classification likewise uses the family-aware buffer

\[
\boxed{\tau_{\mathrm{near},\mathcal F}=10\,\tau_{\mathcal F}.}
\]

A near-active row with \(s\le\tau_s\) is not treated as a smooth row. This avoids applying one dimensionally ambiguous threshold across heterogeneous constraint families.

## 7.2 Multiplier, complementarity, stationarity and descent diagnostics

Retain the Decision-15 raw quantities

\[
R_{\mathrm{dual},a}=\|[-\mu_a]_+\|_\infty,
\]

\[
R_{\mathrm{comp},a}=\|\mu_a\odot g_a(z_a)\|_\infty,
\]

\[
R_{\mathrm{stat},a}
=\|\nabla\phi_a+J_{a,\mathrm{diff}}^\top\mu_{a,\mathrm{diff}}\|_2,
\]

\[
R_{\mathrm{desc},a}
=[\phi_a(z_a^{\mathrm{new}})-\phi_a(z_a^{\mathrm{old}})]_+.
\]

Execution acceptance thresholds:

\[
\boxed{
\frac{R_{\mathrm{dual},a}}{\max(1,\|\mu_a\|_\infty)}\le10^{-8},
}
\]

\[
\boxed{R_{\mathrm{comp},a}\le10^{-6},}
\]

\[
\boxed{
\frac{R_{\mathrm{stat},a}}
{\max(1,\|\nabla\phi_a\|_2,\|J_{a,\mathrm{diff}}^\top\mu_{a,\mathrm{diff}}\|_2)}
\le10^{-6},
}
\]

and

\[
\boxed{
R_{\mathrm{desc},a}
\le
10^{-10}\max(1,|\phi_a^{\mathrm{old}}|,|\phi_a^{\mathrm{new}}|).
}
\]

Raw unnormalized values are always logged as well.

Passing these diagnostics is only a finite implementation-acceptance condition. It does not establish a genuine normal-cone witness \(e_Z\) and therefore does not make `SUNSUN_ALGORITHMICALLY_CERTIFIED` available.

---

# 8. Algebraic integrity, TCC and physical-output predicates

## 8.1 Algebraic integrity

After every inner update independently recompute

\[
R_{\mathrm{id}}^{r,t}
=\|\lambda^r+\beta^r\xi^{r,t}+y^{r,t}\|_2
\]

and

\[
R_{\rho\beta}^{r}=|\rho^r-2\beta^r|.
\]

Require

\[
\boxed{
R_{\mathrm{id}}^{r,t}
\le10^{-12}\max(1,\|\lambda^r\|_2,\|\beta^r\xi^{r,t}\|_2,\|y^{r,t}\|_2)
}
\]

and

\[
\boxed{
R_{\rho\beta}^{r}
\le10^{-12}\max(1,|\rho^r|,2|\beta^r|).
}
\]

Every required array and scalar must be finite. Failure is `ALGEBRAIC_INTEGRITY_FAILED` or `NUMERICAL_NAN_INF`.

## 8.2 TCC finite numerical acceptance

Directly compute

\[
R_{\mathrm{TCC,eq}}(Z)
=
\max_{i,\{a,b\}\in E_i^{\mathrm{eq}}}
\|S_{a\leftarrow i}z_a-S_{b\leftarrow i}z_b\|_2,
\]

and

\[
R_{\mathrm{target}}(Z,U)=\|AZ+BU\|_2.
\]

Freeze

\[
\boxed{
\tau_{\mathrm{eq}}=10^{-6}\ \mathrm m,
\qquad
\tau_{\mathrm{target}}=10^{-6}\ \mathrm m.
}
\]

For this experiment only,

`TCC_CONSISTENT_NUMERIC`

means both thresholds pass. It does **not** mean exact zero TCC residual.

## 8.3 Numerical physical post-check

Use actual source trajectories only. Independently evaluate the Decision-15 unsquared physical margins for every expected index.

For each nonempty family report

\[
R_{\mathcal F}=\max[-m_\ell]_+,
\qquad
m_{\mathcal F,\min}=\min m_\ell.
\]

For the zero-obstacle baseline, verify the expected obstacle-row cardinality is zero, set its aggregate violation to \(0\), and set minimum margin to the categorical marker

`NOT_APPLICABLE_EMPTY_FAMILY`.

Define a strictly **numerical** physical-postcheck tolerance

\[
\boxed{\tau_{\mathrm{phys,num}}=10^{-7}\ \mathrm m.}
\]

A family passes the finite execution post-check when every computed unsquared margin is at least \(-\tau_{\mathrm{phys,num}}\) and all expected evaluations completed. This status is

`PHYSICAL_POSTCHECK_NUMERIC_PASS`,

not `MODEL0D_SAFETY_CERTIFIED`.

U4 remains unresolved, so the exact safety-certified status remains unavailable regardless of the ordinary floating-point margin values.

---

# 9. Inner and outer stopping / failure contract

## 9.1 Inner stop

Use the exact Decision-15 source quantities

\[
R_1^{r,t},\qquad R_2^{r,t},\qquad R_3^{r,t}
\]

with the mandated aggregation order. Stop the inner loop only when

\[
R_1^{r,t}\le\epsilon_1^r,
\qquad
R_2^{r,t}\le\epsilon_2^r,
\qquad
R_3^{r,t}\le\epsilon_3^r.
\]

All local candidates and update-integrity checks must already have passed.

## 9.2 Experimental outer stop

The published Algorithm 2 does not supply this project finite stop. Freeze the following wrapper predicate, evaluated only after a complete successful outer output:

\[
\boxed{
\begin{aligned}
\|\xi^r\|_2 &\le 10^{-6},\\
R_{\mathrm{TCC,eq}}(Z^r)&\le10^{-6}\ \mathrm m,\\
R_{\mathrm{target}}(Z^r,U^r)&\le10^{-6}\ \mathrm m,\\
\text{all numerical-integrity checks}&\text{ pass},\\
\text{all finite local-oracle diagnostics}&\text{ pass},\\
\text{numerical physical post-check}&\text{ passes}.
\end{aligned}}
\]

Require the predicate on **two consecutive complete outer iterates** before returning

`FINITE_OUTER_STOP`.

Objective decrease or goal error is logged but is **not** part of the stop predicate.

## 9.3 Failure precedence and common finalization

No endpoint proceeds after another local candidate fails. In the single-process harness, implement the same all-agent barriers logically.

Use deterministic primary-cause priority:

1. `INPUT_ADMISSIBILITY_FAILED`
2. `NUMERICAL_NAN_INF`
3. `LINEAR_ALGEBRA_FAILURE`
4. `SOLVER_BACKEND_FAILURE`
5. `MULTIPLIER_DIAGNOSTIC_UNAVAILABLE`
6. `ORACLE_UNCERTIFIED_NONSMOOTH`
7. `FIRST_BLOCK_ORACLE_FAILED`
8. `ALGEBRAIC_INTEGRITY_FAILED`
9. `POSTCHECK_EVALUATION_FAILED`
10. `PHYSICAL_VIOLATION_DETECTED`
11. `TCC_NOT_ACCEPTED`
12. `MAX_INNER_ITERATIONS`
13. `MAX_OUTER_ITERATIONS`
14. `TIMEOUT`

Preserve all simultaneous causes in the log even when one deterministic primary cause is selected.

Every exit uses the common finalization contract and returns the **last complete finite snapshot**. A partial failed candidate is diagnostic evidence only, never the accepted result.

---

# 10. Required pre-baseline component checks

These checks occur after implementation but **before baseline outcome inspection**. All must pass or the baseline run is not judged.

### Structure and dimensions

- exact expected dimensions \(d_1=32\), \(d_2=16\), \(Q=16\), \(M_{\mathrm{eq}}=1\), \(m=32\);
- selector extraction and fixed-prefix reconstruction;
- one physical objective term per source, no foreign-copy objective duplication;
- exactly one guardian-localized physical pair family;
- exact all-pairs count for N=2;
- \(\mathcal W\subset\operatorname{int}\mathcal B\);
- communication/equality/reduction-tree legality.

### Exact split and linear algebra

Programmatically verify

\[
B^\top B=2I_{16},
\]

and exact elimination of the split auxiliary on synthetic vectors.

### Geometry

For obstacle and UAV-pair segment-distance evaluators, compare each guarded analytic regime against independent dense scalar sampling and direct clipped one-dimensional minimization for representative endpoint/interior/degenerate cases. This is a component test, not solver validation.

### Backend/multiplier mapping

Repeat the analytic scalar KKT sign test and verify constraint/multiplier row ordering. Abort implementation readiness if the mapping cannot be established.

### Residuals and control flow

Unit-test:

- \(R_1\): sum incident vectors before squaring;
- \(R_2\): symmetric half accounting / no double count;
- \(R_3\): complete half-row sum;
- identity residuals;
- acceptance/abort barrier;
- success exactly at a cap;
- every finalization path;
- empty obstacle family semantics;
- NaN/Inf injection and explicit failure classification.

---

# 11. Baseline reproducibility and Saturday-noon gate

Use fixed configuration file contents and fixed seed

```text
seed = 20260911
PYTHONHASHSEED = 0
OMP_NUM_THREADS = 1
OPENBLAS_NUM_THREADS = 1
MKL_NUM_THREADS = 1
```

for ordering/synthetic checks and deterministic single-thread numerical execution. The optimizer itself contains no intended randomness.

The baseline must be executed from **two fresh Python processes** with the same frozen configuration and environment.

Reproducibility comparison:

\[
\boxed{
\max |x^{(1)}-x^{(2)}|\le10^{-10}
}
\]

for final accepted source/free/copy/auxiliary/slack/dual arrays, with `rtol=1e-10`, and scalar diagnostic agreement to the same numerical scale. Raw logs are retained even if this comparison fails.

Define the Saturday routing status

`BASELINE_NUMERICALLY_RELIABLE_FOR_EXPANSION`

only if both repeats:

- finish with `FINITE_OUTER_STOP`, not a cap/failure;
- pass every mandatory component/integrity/finite-oracle diagnostic;
- satisfy the finite numerical TCC predicates;
- pass the numerical physical post-check on all expected source-trajectory families;
- contain no NaN/Inf or missing evaluator;
- satisfy the reproducibility comparison;
- produce complete logs/config/environment hashes.

This routing status is **not** `SUNSUN_ALGORITHMICALLY_CERTIFIED` and is **not** `MODEL0D_SAFETY_CERTIFIED`.

If any condition fails by Saturday noon, obstacle expansion is dropped. The Saturday afternoon task becomes failure reproduction, localization and characterization only.

---

# 12. Objective and interpretation reporting

For every complete outer output report separately:

- physical objective \(F\);
- each \(f_i\);
- terminal goal errors \(\|p_i^K-g_i\|\);
- total squared-step regularization per UAV;
- \(R_1,R_2,R_3\);
- \(\|\xi\|\), \(R_{\mathrm{TCC,eq}}\), \(R_{\mathrm{target}}\);
- local oracle diagnostics per UAV;
- raw physical minimum margins by family;
- \(R_{\mathrm{id}}\), \(R_{\rho\beta}\);
- \(\beta^r,\rho^r,\|\lambda^r\|,\|y^r\|\);
- local NLP status/iterations/time;
- run termination and certification-status fields.

Objective behavior is descriptive evidence. Because the feasible problem is nonconvex and Algorithm 2 is not a global-optimum method, the report must not interpret a low or decreasing objective as a global-optimality certificate.

---

# 13. Planned implementation/reproducibility artifacts after approval

The DAILY WORKER will maintain the researcher-authorized repository-root traceability package `model0d_alg2_numerics/` with a minimal structure equivalent to:

```text
model0d_alg2_numerics/
  README.md
  environment.txt
  run_experiment.py
  src/
    geometry.py
    tcc.py
    local_nlp.py
    sunsun_algorithm2.py
    diagnostics.py
    io_utils.py
  configs/
    baseline_2uav_0obs.json
    obstacle_2uav_1obs.json
  tests/
    test_geometry.py
    test_tcc_split.py
    test_residuals.py
    test_backend_multiplier_sign.py
    test_failure_paths.py
  runs/
    <run-id>/config.json
    <run-id>/environment.txt
    <run-id>/events.jsonl
    <run-id>/outer.csv
    <run-id>/local_oracle.csv
    <run-id>/final_state.npz
    <run-id>/summary.json
  plots/
```

Exact filenames may be simplified during implementation, but the evidence content may not be weakened.

Planned reproducible command form:

```bash
python3 run_experiment.py --config configs/baseline_2uav_0obs.json --output runs/<run-id>
```

The final report will record exact file hashes and exact executed commands.

---

# 14. Required plots after execution

No plot is produced or inspected before protocol approval. After execution, the minimum evidence set is:

1. source trajectories in the workspace, with required UAV-clearance interpretation and obstacle geometry when applicable;
2. \(F\) and terminal goal errors versus outer iteration;
3. log-scale \(R_1,R_2,R_3,\|\xi\|,R_{\mathrm{TCC,eq}},R_{\mathrm{target}}\);
4. local finite-oracle diagnostics versus inner/outer iteration;
5. minimum numerical physical margins by nonempty family;
6. \(\beta^r\), \(\|\lambda^r\|\), \(\|y^r\|\) to expose penalty/dual behavior.

Plots supplement raw logs; they never replace raw numerical evidence.

---

# 15. Certification language frozen for the campaign

The campaign may report:

- `NUMERICALLY_VALID` only after the protocol's integrity/evaluator requirements pass;
- `TCC_CONSISTENT` only as a finite tolerance-qualified status with raw residuals retained;
- `PHYSICAL_POSTCHECK_NUMERIC_PASS` as an explicitly uncertified ordinary-floating-point result.

The campaign may **not** report:

- `MODEL0D_SAFETY_CERTIFIED` while U4 is unresolved;
- `SUNSUN_ALGORITHMICALLY_CERTIFIED` while the finite genuine-normal-witness contract remains unavailable;
- a “fully certified Model-0D Sun--Sun planning result”;
- global optimality;
- real-UAV execution certification.

Small \(R_1,R_2,R_3\), small TCC residuals or a backend success code do not change these restrictions.

---

# 16. Timetable binding

Friday 11 September, **15:00--17:00**: implement the smallest complete baseline solver, run component checks, and attempt the first baseline only if implementation readiness passes.

Saturday 12, morning: finish/debug/repeat the baseline and reach the **noon checkpoint**.

Saturday 12, afternoon: execute the one predefined obstacle scenario only if `BASELINE_NUMERICALLY_RELIABLE_FOR_EXPANSION` is true. Otherwise spend the period characterizing the baseline failure.

The complete numerical review package must reach the researcher **by the start of the Saturday 16:00--17:00 consolidation/audit block, preferably earlier**. Numerical execution stops at 17:00. Sunday/Monday are protected preparation time.

---

# 17. Exact decision requested

The researcher is asked to **approve, correct, or reject this protocol as the frozen finite experimental wrapper**, specifically:

- the two predefined scenarios and TCC architecture;
- CasADi/IPOPT backend and options;
- Algorithm-2 numerical parameters and finite caps;
- all finite diagnostic/TCC/physical thresholds;
- no-retry policy and failure precedence;
- the experimental outer-stop predicate;
- the reproducibility criterion and Saturday baseline routing predicate.

Upon approval, the DAILY WORKER will implement and component-test this exact protocol. **Experimental outcome inspection will begin only after that approval.**

Historical note: this pre-approval package itself did not request a GitHub commit. The researcher subsequently authorized the initial traceability commit on 11 September 2026; that authorization does not grant blanket commit permission for unrelated work and does not convert implementation/results into audited or finally approved deliverables.
