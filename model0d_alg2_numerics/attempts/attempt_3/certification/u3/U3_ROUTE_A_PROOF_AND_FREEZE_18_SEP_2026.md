# Model 0-D — U3 Route A proof and freeze record

**Date:** 18 September 2026  
**Research:** Constraint Consensus-Based Dynamics for Decentralized Path Planning in UAV Swarms  
**Researcher / scientific authority:** Ismaël Assoumane Idi  
**Role:** DAILY WORKER  
**Route selected by researcher:** **U3 Route A — actual Algorithm-2 multiplier boundedness via MFCQ / actual approximate-KKT sequence**  
**Execution boundary:** **NO Attempt-3 rerun, no solver execution, no retuning.** This record is a theorem/proof and saved-evidence post-analysis only.  
**Attempt-3 evidence:** the two official saved repetitions already produced under Checkpoint C and the subsequent U4-E1/U4-E2 post-certification package.  

---

## 1. What U3 was

For the Sun–Sun two-level method, the original split problem is

\[
\min_{Z\in X,\ U\in\bar X} F(Z)
\qquad\text{s.t.}\qquad AZ+BU=0.
\]

The source Algorithm 2 introduces the outer slack \(\xi\), and the terminated inner ADMM outer iterate satisfies the approximate stationarity relations

\[
d_1^r\in \nabla F(Z^r)+A^\top y^r+N_X(Z^r),
\]

\[
d_2^r\in B^\top y^r+N_{\bar X}(U^r),
\]

\[
0=\lambda^r+\beta^r\xi^r+y^r,
\]

\[
d_3^r=AZ^r+BU^r+\xi^r,
\]

with source tolerances tending to zero in the exact outer-sequence analysis.

Sun–Sun Theorem 2 requires that, along a primal subsequence

\[
(Z^{r_j},U^{r_j},\xi^{r_j})\to(Z^\star,U^\star,\xi^\star),
\]

the **actual** dual sequence \(y^{r_j}\) have a matching limit point \(y^\star\). The previous Model-0D record established MFCQ/CPLD transfer at smooth exact TCC lifts but deliberately did **not** prove that a generic CPLD multiplier theorem controlled the **particular Algorithm-2 sequence \(y^r\)**. That sequence-identification gap was U3.

The purpose of Route A is to close that exact gap by proving boundedness of the actual Algorithm-2 multiplier sequence under MFCQ, rather than by invoking existence of unrelated replacement multipliers.

---

## 2. Source and project facts used

### 2.1 Sun–Sun source facts

Kaizhao Sun and X. Andy Sun, *A two-level distributed algorithm for nonconvex constrained optimization*, Computational Optimization and Applications 84 (2023), 609–649, DOI 10.1007/s10589-022-00433-4.

Relevant source facts:

1. Stationarity of the original split problem is condition (7).
2. Approximate stationarity of an outer iterate is condition (13).
3. Theorem 2 states that if the actual \(y^r\) has a limit point along a primal-convergent subsequence, then the corresponding limit satisfies the original stationarity condition.
4. Immediately after Theorem 2 the authors note that a bounded dual subsequence is sufficient and mention CPLD as a smooth-NLP route.

Publisher: <https://link.springer.com/article/10.1007/s10589-022-00433-4>

### 2.2 Standard AKKT/MFCQ fact used as external corroboration

A standard sequential optimality result states that, for an approximate-KKT sequence converging to a point satisfying MFCQ, the associated multiplier sequence is uniformly bounded and has limit points. One explicit reference is Theorem 3.8(2) in the regularized-SQP analysis used in the research review:

<https://optimization-online.org/wp-content/uploads/2013/10/4102.pdf>

The proof below is nevertheless given directly, specialized to the present TCC split, so the project does not rely on a black-box theorem invocation.

### 2.3 Frozen project facts

The proof also uses already-established project results:

- `decisions/14_TCC_formulation.md`, Theorem T13: the exact TCC tree-equality Jacobian has full row rank.
- `decisions/work_06_SEP_2026.txt`, §9.5: at a corresponding smooth exact lift, physical MFCQ is equivalent to split-TCC MFCQ, assuming inactive A1 boxes and the frozen equality tree.
- Model-0D CQ study: MFCQ is a candidate-point property, not a universal property of every feasible Model-0D point.
- U4-E1 exact certification: the saved Attempt-3 physical source trajectory has strictly positive exact workspace, speed, and UAV–UAV safety margins; the obstacle family is empty.

No claim below upgrades these facts beyond their proven scope.

---

# 3. Route-A theorem: actual Algorithm-2 dual boundedness under MFCQ

## Theorem U3-A1 — actual-sequence multiplier boundedness

Let

\[
w:=(Z,U),\qquad E:=[A\ B],
\]

and write a finite local smooth representation of all inequalities defining \(X\times\bar X\) near a feasible candidate \(w^\star\) as

\[
g_\ell(w)\le 0,\qquad \ell=1,\dots,m_g.
\]

Assume:

**A1. Smooth feasible limit.** There is a subsequence of exact-source Algorithm-2 outer iterates, indexed by \(r_j\), such that

\[
w^{r_j}\to w^\star,
\]

where \(w^\star\) is feasible for the original split equality

\[
Ew^\star=0,
\]

and all active inequalities are \(C^1\) in a neighborhood of \(w^\star\).

**A2. MFCQ at the selected limit.** The equality Jacobian \(E\) has full row rank and there exists a direction \(d\) such that

\[
Ed=0,
\]

and

\[
\nabla g_\ell(w^\star)^\top d<0
\qquad \forall\ell\in\mathcal A(w^\star),
\]

where \(\mathcal A(w^\star)=\{\ell:g_\ell(w^\star)=0\}\).

**A3. Actual source approximate stationarity.** Along the same subsequence the actual Algorithm-2 dual variables \(y^{r_j}\) and the exact source normal terms satisfy the source approximate-stationarity relations with errors tending to zero. Equivalently, using the local multiplier representation of the normal cones valid under MFCQ, there exist inequality multipliers \(\mu^{r_j}\ge0\), supported on the active inequalities at \(w^{r_j}\), such that

\[
\nabla \Phi(w^{r_j})
+E^\top y^{r_j}
+G(w^{r_j})^\top\mu^{r_j}
=e^{r_j},
\]

with

\[
e^{r_j}\to0.
\]

Here \(\nabla\Phi(w)=(\nabla F(Z),0)\), and \(G\) stacks the inequality gradients.

Then the **actual** multiplier sequence

\[
\{(y^{r_j},\mu^{r_j})\}
\]

is bounded. Consequently, \(\{y^{r_j}\}\) is bounded and there exists a further subsequence \(r_{j_\ell}\) and a finite vector \(y^\star\) such that

\[
y^{r_{j_\ell}}\to y^\star
\]

while

\[
w^{r_{j_\ell}}\to w^\star.
\]

Therefore the matching-dual-limit hypothesis required in Sun–Sun Theorem 2 is automatically satisfied at any limit point fulfilling A1–A3.

---

## Proof

### Step 1 — MFCQ remains valid locally on sufficiently close feasible iterates

If an inequality is inactive at the limit,

\[
g_\ell(w^\star)<0,
\]

continuity implies that it remains inactive for all sufficiently large \(j\). Hence, eventually,

\[
\mathcal A(w^{r_j})\subseteq\mathcal A(w^\star).
\]

For every \(\ell\in\mathcal A(w^\star)\), continuity of \(\nabla g_\ell\) and the strict inequality

\[
\nabla g_\ell(w^\star)^\top d<0
\]

imply

\[
\nabla g_\ell(w^{r_j})^\top d<0
\]

for all sufficiently large \(j\). Since \(E\) is constant and \(Ed=0\), the same direction is an MFCQ direction for every sufficiently close feasible iterate. Thus the normal terms in the exact source inclusion admit the standard active-gradient representation with nonnegative coefficients. Importantly, this introduces only inequality multipliers representing the exact normal term; it does **not** replace or redefine the Algorithm-2 equality multiplier \(y^{r_j}\).

### Step 2 — suppose the actual multiplier sequence is unbounded

Assume, for contradiction, that

\[
\|(y^{r_j},\mu^{r_j})\|\to\infty
\]

along a further subsequence, relabeled \(j\).

Define

\[
\theta_j:=\|(y^{r_j},\mu^{r_j})\|>0,
\]

and normalized multipliers

\[
\widehat y^j:=\frac{y^{r_j}}{\theta_j},
\qquad
\widehat\mu^j:=\frac{\mu^{r_j}}{\theta_j}.
\]

They satisfy

\[
\|(\widehat y^j,\widehat\mu^j)\|=1.
\]

By finite-dimensional compactness of the unit sphere, pass to a further subsequence such that

\[
(\widehat y^j,\widehat\mu^j)
\to
(\bar y,\bar\mu),
\]

with

\[
\|(\bar y,\bar\mu)\|=1
\]

and

\[
\bar\mu\ge0.
\]

Because inequalities inactive at \(w^\star\) are eventually inactive at \(w^{r_j}\), their normal-cone multipliers are eventually zero. Hence \(\bar\mu\) is supported only on \(\mathcal A(w^\star)\).

### Step 3 — normalize the actual approximate-stationarity equation

Divide

\[
\nabla \Phi(w^{r_j})
+E^\top y^{r_j}
+G(w^{r_j})^\top\mu^{r_j}
=e^{r_j}
\]

by \(\theta_j\). Since \(w^{r_j}\to w^\star\), \(\nabla\Phi(w^{r_j})\) is bounded. Also \(e^{r_j}\to0\). Therefore

\[
\frac{\nabla\Phi(w^{r_j})}{\theta_j}\to0,
\qquad
\frac{e^{r_j}}{\theta_j}\to0.
\]

Passing to the limit yields the abnormal multiplier relation

\[
\boxed{
E^\top\bar y
+
\sum_{\ell\in\mathcal A(w^\star)}
\bar\mu_\ell\nabla g_\ell(w^\star)
=0,
\qquad
\bar\mu_\ell\ge0.
}
\]

### Step 4 — MFCQ excludes every nonzero abnormal multiplier

Take the inner product with the MFCQ direction \(d\). Since \(Ed=0\),

\[
\bar y^\top Ed=0.
\]

Thus

\[
0
=
\sum_{\ell\in\mathcal A(w^\star)}
\bar\mu_\ell
\nabla g_\ell(w^\star)^\top d.
\]

Every term has

\[
\bar\mu_\ell\ge0,
\qquad
\nabla g_\ell(w^\star)^\top d<0.
\]

Hence the only way their sum can equal zero is

\[
\bar\mu=0.
\]

The abnormal relation reduces to

\[
E^\top\bar y=0.
\]

Because \(E\) has full row rank, \(E^\top\) is injective, so

\[
\bar y=0.
\]

Therefore

\[
(\bar y,\bar\mu)=0,
\]

contradicting

\[
\|(\bar y,\bar\mu)\|=1.
\]

The assumption of unboundedness is false. Therefore

\[
\boxed{
\{(y^{r_j},\mu^{r_j})\}\text{ is bounded.}
}
\]

In particular \(\{y^{r_j}\}\) is bounded. By Bolzano–Weierstrass it has a convergent further subsequence, and this subsequence is automatically a subsequence of the already primal-convergent sequence. Therefore the primal and actual Algorithm-2 dual variables converge along the same index set. This is exactly the missing sequence-identification step in U3. \(\square\)

---

# 4. Stronger Attempt-3 specialization

The saved Attempt-3 trajectory has an especially simple regularity structure after U4 resolution.

## 4.1 Exact strict physical inequalities

The U4-E1 exact-rational certifier proves for both official repetitions:

- exact workspace minimum margin:

\[
1.0229604892253025\ldots>0;
\]

- exact minimum squared speed margin:

\[
0.2756924228770560\ldots>0;
\]

- exact minimum UAV–UAV squared clearance margin:

\[
4.3946965024440438902\ldots\times10^{-7}>0;
\]

- obstacle family: empty.

Therefore **every physical optimization inequality is strictly inactive** at the saved physical source trajectory.

## 4.2 Exact TCC lift and artificial boxes

Take the unique exact-consensus TCC lift of those physical source trajectories: each foreign source-2 copy is set exactly equal to source 2, and the corresponding edge auxiliary is set to that same source trajectory.

The independent U3 saved-evidence audit computes the minimum A1 / auxiliary-box margin exactly from the stored binary64 source-2 coordinates against the intended exact decimal box \([-3.5,3.5]^2\):

\[
\frac{6875075867184351}{4503599627370496}
=
1.5265735047585662\ldots>0.
\]

Hence all A1 and \(\bar X\) box inequalities are also strictly inactive at this exact lift.

Thus the complete active inequality set of the exact split-TCC lift is

\[
\boxed{\mathcal A(w^\star)=\varnothing.}
\]

The active-safety smoothness issue is therefore vacuous: no active exact safety constraint needs a classical derivative.

## 4.3 Exact equality rank

For the frozen \(N=2\), \(Q=16\) architecture, the independent audit constructs the exact integer/rational split matrices and verifies

\[
\operatorname{rank}[A\ B]=32,
\]

which equals the number of equality rows, and

\[
B^\top B=2I_{16}
\]

exactly.

Therefore classical MFCQ at this exact lift reduces to equality full-row-rank, and hence

\[
\boxed{
\text{MFCQ holds at the exact TCC lift of the U4-certified Attempt-3 physical trajectory.}
}
\]

This is stronger than a floating rank diagnostic: the audit uses exact symbolic integer matrices.

---

# 5. Stronger direct-dual corollary at the Attempt-3 exact lift

Because every inequality is strictly inactive at this exact lift, there is a neighborhood in which all inequality normal cones vanish. Therefore, if an exact-source Algorithm-2 outer subsequence converges to this exact lift, then for all sufficiently large indices the source relations (13a)–(13b) reduce to

\[
d_1^{r_j}
=
\nabla F(Z^{r_j})+A^\top y^{r_j},
\]

\[
d_2^{r_j}=B^\top y^{r_j}.
\]

Stack them:

\[
E^\top y^{r_j}
=
\begin{bmatrix}
 d_1^{r_j}-\nabla F(Z^{r_j})\\
 d_2^{r_j}
\end{bmatrix}
=:b_j.
\]

Since \(E\) has full row rank,

\[
EE^\top
\]

is invertible and

\[
\boxed{
y^{r_j}
=
(EE^\top)^{-1}E\,b_j.
}
\]

If the source errors tend to zero and \(Z^{r_j}\to Z^\star\), then

\[
b_j
\to
\begin{bmatrix}
-\nabla F(Z^\star)\\
0
\end{bmatrix}.
\]

Therefore the **actual** Algorithm-2 dual sequence itself converges:

\[
\boxed{
y^{r_j}\to
(EE^\top)^{-1}E
\begin{bmatrix}
-\nabla F(Z^\star)\\
0
\end{bmatrix}.
}
\]

This is stronger than merely proving that a bounded dual subsequence exists. No replacement equality multiplier is introduced.

The statement is conditional only in the standard theorem sense: it concerns an exact-source outer subsequence whose primal limit is this exact feasible lift. A finite ten-outer-iteration experimental run is not, by itself, a proof that an infinite source-algorithm sequence converges to that exact lift.

---

# 6. Saved Attempt-3 finite evidence — descriptive, not the proof

The independent saved-evidence audit, without rerunning the solver, verifies for both official repetitions:

\[
\beta^{10}=4,
\]

\[
\|\xi^{10}\|_2
=5.181917114188811\times10^{-7},
\]

\[
\|\lambda^{10}\|_2
=0.2678809665814552,
\]

\[
\|y^{10}\|_2
=0.26787941622148165,
\]

and

\[
\|\lambda^{10}+\beta^{10}\xi^{10}+y^{10}\|_2
\approx2.995\times10^{-22}.
\]

The observed finite outer penalty sequence is

\[
2,4,4,4,4,4,4,4,4,4.
\]

These values are useful consistency evidence only. They are **not** used to infer asymptotic boundedness. The U3 proof is the theorem in §3, with the exact-lift specialization in §§4–5.

Both official repetitions remain bit-for-bit identical in every final-state array.

---

# 7. U3 freeze decision

The previous route

> split-TCC MFCQ \(\Rightarrow\) CPLD \(\Rightarrow\) somehow the actual Algorithm-2 \(y^r\) has a matching bounded subsequence

is no longer the active justification, because its last implication was not proved for the actual generated sequence.

The frozen Route-A result is now:

\[
\boxed{
\begin{gathered}
\text{smooth feasible split-TCC limit}
+\text{MFCQ}
+\text{actual source approximate stationarity}\
\Longrightarrow
\text{actual Algorithm-2 multiplier sequence is bounded along that primal subsequence}\
\Longrightarrow
\text{a matching }y\text{-limit subsequence exists.}
\end{gathered}}
\]

For the saved U4-certified Attempt-3 physical trajectory, its unique exact TCC lift satisfies the MFCQ premise exactly, in fact with **no active inequalities** and a full-row-rank split equality Jacobian.

Therefore the exact U3 logical gap concerning **actual dual-sequence identification** is closed by Route A.

### Frozen status

```text
U3_ROUTE_A_THEOREM                    = PROVED
U3_ACTUAL_y_SEQUENCE_IDENTIFICATION  = RESOLVED_UNDER_MFCQ
ATTEMPT3_EXACT_LIFT_MFCQ             = PASS
U3                                   = RESOLVED_BY_ROUTE_A_MFCQ_ACTUAL_SEQUENCE
```

### Scope guard

This status does **not** mean:

- global MFCQ holds at every Model-0D feasible point;
- the finite Attempt-3 output is itself an asymptotic limit point;
- the practical IPOPT first-block diagnostic has been proved equal to the exact Sun–Sun normal-cone oracle;
- Sun–Sun Algorithm 2 has a universal global convergence guarantee for every practical inexact implementation;
- global optimality has been proved.

The first-block exact-oracle issue remains a **separate algorithmic-certification gap**.

---

# 8. Consequence for the current Attempt-3 status

After U4 and U3 Route A:

```text
NUMERICALLY_VALID                     = true
TCC_CONSISTENT                        = true
PHYSICAL_POSTCHECK_NUMERIC_PASS       = true
MODEL0D_SAFETY_CERTIFIED              = true
U4                                    = RESOLVED (U4-E1 + independent U4-E2 audit)
U3                                    = RESOLVED_BY_ROUTE_A_MFCQ_ACTUAL_SEQUENCE
ATTEMPT3_EXACT_LIFT_MFCQ              = true

SUNSUN_ALGORITHMICALLY_CERTIFIED      = false
FULLY_CERTIFIED_MODEL0D_SUNSUN_RESULT = false
```

The two final `false` values remain because finite first-block diagnostics have not yet been upgraded to a theorem-faithful exact normal-cone/oracle certificate. U3 is no longer the reason for those two statuses.

---

# 9. Required documentation note for the future repository commit

The current original Model 0-D v1.5 PDF/TeX still records **U4 as unresolved/unselected**, because it predates the post-simulation U4-E1/U4-E2 work. The future final simulation commit must explicitly state this documentation lag:

> **Post-simulation note.** U4 has been resolved for the saved Attempt-3 deterministic trajectory by exact-rational physical safety certification, with an independent validated interval audit. The current Model 0-D v1.5 PDF/TeX predates this post-simulation resolution and still describes U4 as unresolved. Synchronizing the Model 0-D mathematical document with the approved U4 technology/result is future documentation work and is not silently backdated into the original v1.5 artifact.

Likewise, this U3 Route-A theorem is a post-simulation proof record and should be incorporated into a future synchronized Model-0D revision rather than silently rewriting historical documents.

---

# 10. Evidence files

- `u3_route_a/results/U3_ROUTE_A_SAVED_EVIDENCE_AUDIT_18_SEP_2026.json`
- `u3_route_a/scripts/u3_route_a_saved_evidence_audit.py`
- `results/attempt3_run1_u4_exact_rational.json`
- `results/attempt3_run2_u4_exact_rational.json`
- `results/attempt3_run1_u4_interval_audit.json`
- `results/attempt3_run2_u4_interval_audit.json`
- Checkpoint-C saved run states under the preserved Attempt-3 execution package.

No file in this U3 package invokes the solver or modifies the Attempt-3 trajectories.
