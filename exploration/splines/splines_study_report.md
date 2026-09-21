# Surface-Level Study: Spline / Function Trajectory Representation for Model 0-D

> **Status update — 17 September 2026.** The researcher reports supervisor approval of the spline idea, particularly the degree-1 continuous piecewise-linear interpretation already used by Model 0-D (Model 0 — Deterministic). Higher-order representations remain future work; no new implementation, smoothness guarantee or solver selection follows. This approval clarification comes from the researcher, not an explicit spline statement in the meeting report. See the [current research positioning](../../harmonization/final-pre-report-drafting_2026-09-20/CURRENT_RESEARCH_STATE_20_SEP_2026.md).


**Project:** Constraint Consensus-Based Dynamics for Decentralized Path Planning in UAV Swarms  
**Purpose:** short exploratory note for the supervisor meeting of **Tuesday, 15 September 2026**  
**Status:** exploratory only - **no change to the approved Model 0-D baseline is authorized or implied**  
**Scope:** give a rigorous recipe for a later study; no proof, implementation, superiority claim, or solver re-selection.

## 1. Why this note exists

During the 20 July 2026 supervision meeting, Pr. Habbal asked for a surface-level study of an alternative trajectory representation. Instead of storing a trajectory only through finitely many sampled positions, one may represent position as a continuous-time function

\[
p_i(t)=\sum_{\ell=0}^{L} b_i^{\ell}\,\psi_\ell(t),
\]

where \(\psi_\ell\) are chosen basis functions and the vector coefficients \(b_i^{\ell}\in\mathbb R^q\) become optimization parameters. Splines, polynomials, and approximation in Sobolev spaces were explicitly mentioned as directions to investigate.

The goal here is **not** to claim that such a representation is better than Model 0-D. The goal is only to state how it could be introduced, what mathematical tools would become relevant, and which parts of the present analysis would have to be redone.

## 2. Important observation: Model 0-D is already very close to this idea

The current approved Model 0-D uses sampled positions

\[
x_i=(p_i^0,\ldots,p_i^K),\qquad p_i^0=\widehat p_i(t_0),
\]

with only \((p_i^1,\ldots,p_i^K)\) free. Between samples, the physical trajectory is reconstructed by

\[
p_i(t)=(1-\lambda(t))p_i^k+\lambda(t)p_i^{k+1},
\qquad t\in[t_k,t_{k+1}].
\]

Therefore Model 0-D **already has a continuous-time trajectory determined by finitely many parameters**. Mathematically, this reconstruction can be viewed as a **degree-1 (linear) spline** on the planning grid.

Its present regularity is deliberately limited: the trajectory is continuous, but velocity may jump at the knots. Model 0-D therefore makes no global \(C^1\), \(C^2\), acceleration, curvature, or jerk claim.

So the natural research progression is not

> discrete trajectories \(\rightarrow\) continuous trajectories,

but rather

\[
\boxed{\text{piecewise-linear continuous reconstruction}}
\quad\longrightarrow\quad
\boxed{\text{higher-order finite-dimensional continuous representation}}.
\]

## 3. Minimal candidate formulation

A clean first candidate is a B-spline representation

\[
p_i(t;c_i)=\sum_{\ell=0}^{n_c-1} c_{i\ell}\mathcal{B}_{\ell,r}(t),
\]

where:

- \(r\) is the spline degree;
- \(\mathcal{B}_{\ell,r}\) are B-spline basis functions associated with a chosen knot vector;
- \(c_{i\ell}\in\mathbb R^q\) are control coefficients / control points;
- the stacked coefficient vector \(c_i\) becomes the finite-dimensional trajectory decision variable.

This is still a finite-dimensional optimization problem. We are **not** proposing an infinite-dimensional optimization problem at this stage.

A global or piecewise-polynomial representation is another valid option, but B-splines are the most natural first object to study because they combine a polynomial representation with local support and explicit derivative structure.

### First comparison rule

For a scientifically clean future comparison, the **first spline variant should change only the trajectory parameterization**. The workspace, obstacle model, safety radii, horizon, initial data, communication/TCC architecture, and preferably the current objective should initially remain unchanged. Otherwise we would not know whether an observed difference comes from splines or from another model change.

### Assumptions to freeze before any proof

For the first rigorous variant, a minimal assumption set should be explicit: fixed horizon \([t_0,t_K]\); fixed degree and knot vector (do not optimize knot times initially); the same basis/knot vector for all TCC copies of one source trajectory; a clamped/end-point-compatible construction so the known initial position can be fixed by construction; sufficient spline degree for whichever derivatives are constrained; bounded coefficient domain or another route to compactness; and **continuous-time** workspace/speed/safety constraints rather than knot-only checks. These are proposed study assumptions, not yet approved Model 0-D assumptions.

## 4. How the current Model 0-D ingredients could map to coefficients

| Model 0-D ingredient | First spline recipe | Status |
|---|---|---|
| Fixed initial position | Enforce \(p_i(t_0)=\widehat p_i(t_0)\) **by parameterization/elimination if possible**, rather than adding a redundant optimization equality. | Feasible in principle; exact construction depends on basis/knot choice. |
| Terminal goal term | Replace \(p_i^K\) by \(p_i(t_K;c_i)\). | Direct. |
| Current squared-step regularizer | Keep the current evaluation grid and use \(\sum_k\|p_i(t_{k+1};c_i)-p_i(t_k;c_i)\|^2\) for the first comparison. | Preserves objective meaning. |
| Alternative smoothness cost | Later study \(\int\|p_i^{(m)}(t)\|^2dt\) (acceleration, jerk, snap, etc.). | **A model change**, not assumed here. |
| Convex workspace \(W\) | For B-splines, forcing relevant control points into convex \(W\) gives a sufficient all-time containment condition by the convex-hull property. | Useful but potentially conservative. |
| Speed bound | Differentiate the spline. Bounds can be imposed directly on \(\dot p_i(t)\), or sufficient bounds can be derived from derivative control points. | Requires a new exact/sufficient formulation. |
| Obstacle safety | Must hold for the entire spline, not only at knots/control points. | Requires renewed continuous-time safety analysis. |
| UAV-UAV safety | The relative trajectory \(p_i-p_j\) is again a spline when the same basis is used. Continuous-time separation still needs a certificate. | Requires renewed safety analysis. |
| TCC copies | Copy coefficient vectors instead of sampled free trajectories; impose same-source coefficient agreement. | Structurally plausible if all copies use the same linearly independent basis/knot vector. |
| Sun-Sun solver mapping | Same broad finite-dimensional distributed architecture may remain possible. | **All source assumptions and local-set properties must be re-audited.** |

### Crucial safety warning

The present Model 0-D has a major advantage: for every linear segment, exact obstacle and UAV-UAV closest approach has an explicit one-dimensional segment formula. That exact safety analysis does **not** transfer automatically to higher-order splines.

For a spline span, later possibilities include:

1. exact or certified minimization of distance over each polynomial span;
2. conservative convex-hull separation certificates;
3. subdivision / Bernstein or B-spline bounds;
4. sampling only when accompanied by a mathematically justified error bound.

Plain sampling without a certificate would not preserve the present Model 0-D continuous-time safety semantics.

## 5. Main spline facts that would support a later rigorous study

For a standard B-spline basis, the following are the first properties worth proving/using precisely later:

1. **Finite basis representation.** The curve is linear in its coefficients \(c_{i\ell}\).
2. **Local support.** Changing one coefficient affects only a limited set of knot spans.
3. **Non-negativity and partition of unity.** These properties lead to the convex-hull interpretation.
4. **Convex-hull property.** Each spline span lies in the convex hull of its active control points.
5. **Derivative closure.** Derivatives of a B-spline curve can again be represented by lower-degree B-splines whose coefficients are linear combinations of the original coefficients.
6. **Knot regularity.** For degree \(r\), a knot of multiplicity \(m\) gives the standard continuity level \(C^{r-m}\) under the usual B-spline construction. In particular, a cubic spline with simple interior knots is normally \(C^2\).
7. **Approximation theory.** As the spline space is refined, standard spline approximation results give convergence/error estimates under suitable regularity assumptions. Sobolev-norm estimates are the relevant bridge to Pr. Habbal's Sobolev-space remark.

These are **tools for the future study**, not new Model 0-D theorems claimed here.

## 6. Which current Model 0-D theorems would need to be revisited?

The current Model 0-D has already established nonemptiness/existence, objective convexity properties, nonuniqueness in general, parametric stability results, regularity facts for exact segment-distance constraints, CQ/KKT results, TCC exactness, and the Sun-Sun mapping. A spline parameterization changes the mathematical representation on which several of these results depend.

A later spline variant should therefore re-check at least the following.

| Later theorem/check | Likely starting idea |
|---|---|
| **Nonemptiness** | B-splines contain constant trajectories: set all control points to the safe initial position. This suggests that the existing hover construction may survive if the spline constraints are defined compatibly. |
| **Compactness + existence** | Keep a finite coefficient vector, impose a bounded/compact coefficient domain or derive boundedness from the workspace, ensure all trajectory constraints define a closed feasible set, then reuse a Weierstrass-type argument. |
| **Objective convexity** | If the current quadratic objective is evaluated through a trajectory that depends linearly on coefficients, it remains a quadratic function of the coefficients; strict-convexity conditions must nevertheless be recomputed because the parameterization may have null directions or different anchoring. |
| **Safety regularity** | Replace line-segment distance value functions by spline-span distance value functions; continuity/differentiability must be analyzed again. |
| **CQ/KKT** | Recompute gradients/Jacobians of the new constraint functions and re-check LICQ/MFCQ conditions. |
| **TCC exactness** | With a common linearly independent basis, equality of coefficient vectors implies equality of represented source trajectories; the exact copy-space reformulation can then be reconstructed in coefficient coordinates. |
| **Sun-Sun assumptions** | Re-check compact local sets, smooth/nonsmooth structure, equality dimensions, and the exact source assumptions. No convergence theorem should be carried over automatically. |

## 7. Sobolev-space direction: what it would mean here

The supervisor's Sobolev-space remark can be interpreted as a **later functional-analytic viewpoint**, not as something required for the present Model 0-D implementation.

Instead of beginning directly with coefficients, one could first regard a trajectory as a function

\[
p_i\in H^s([t_0,t_K];\mathbb R^q)
\]

for an appropriate regularity index \(s\), and then approximate that function in a finite-dimensional spline space \(S_h\subset H^s\) (or a compatible lower-order Sobolev space). Standard spline/finite-element approximation theory then asks how the best spline approximation error decreases as the knot spacing \(h\) is refined, under regularity assumptions on the target trajectory.

For this DR, that direction would mainly be useful later to answer questions such as:

- what functional regularity is physically meaningful for a UAV trajectory;
- which derivative norms should be controlled;
- whether spline spaces approximate the desired trajectory class as resolution increases;
- how discretization error could interact with continuous-time safety.

No Sobolev theorem is needed to justify the current short exploratory note.

## 8. Short feasibility verdict

**Feasible as a research direction:** yes. A spline trajectory remains finitely parameterized and fits naturally into optimization; B-splines also provide useful smoothness, local support, derivative, and convex-hull structure.

**Ready to replace Model 0-D:** no conclusion. The current piecewise-linear model has already-proved exact segment safety and a completed mathematical/TCC analysis. A higher-order representation would require renewed safety, existence/regularity, CQ/KKT, and solver-assumption work.

**Recommended next step after the September meeting:** if Pr. Habbal wants this direction pursued, define one tightly controlled exploratory variant (probably a clamped cubic B-spline with the same horizon and physical data), keep the current objective initially, derive the new continuous-time safety formulation, and only then compare it numerically and mathematically with the approved piecewise-linear baseline.

This is a **recipe for a future study**, not a superiority claim.

## 9. References for later reading

### Start here - spline theory

1. **M. S. Floater, _An Introduction to Spline Theory_** (University of Oslo lecture notes).  
   PDF: <https://www.uio.no/studier/emner/matnat/math/MAT4170/v25/undervisningsmateriale/spline_notes.pdf>  
   Use for: basis functions, B-splines, knot vectors, interpolation/approximation.

2. **SciPy `BSpline` documentation.**  
   <https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.BSpline.html>  
   Use for: concise definition, basis representation, partition of unity, derivatives, and a direct implementation reference.

3. **MIT Robotic Manipulation - Motion Planning, B-spline trajectory parameterization.**  
   <https://manipulation.mit.edu/trajectories.html>  
   Use for: optimization interpretation, derivative control points, non-negativity/local support, and convex-hull reasoning.

### UAV / trajectory-planning bridge

4. **V. Usenko, L. von Stumberg, A. Pangercic, D. Cremers, "Real-Time Trajectory Replanning for MAVs using Uniform B-splines and a 3D Circular Buffer," 2017.**  
   arXiv: <https://arxiv.org/abs/1703.01416>  
   PDF: <https://arxiv.org/pdf/1703.01416.pdf>  
   Use for: a concrete MAV example where B-spline control points are optimized and derivatives/smoothness are handled analytically. This is an application source, not a proof source for our Model 0-D model.

5. **C. Richter, A. Bry, N. Roy, "Polynomial Trajectory Planning for Aggressive Quadrotor Flight in Dense Indoor Environments," ISRR 2013 / Springer 2016.**  
   Author PDF: <https://groups.csail.mit.edu/rrg/papers/Richter_ISRR13.pdf>  
   DOI: <https://doi.org/10.1007/978-3-319-28872-7_37>  
   Use for: comparison with piecewise polynomial trajectory parameterizations and smooth quadrotor trajectories.

### Sobolev / approximation direction - later, not urgent

6. **Y. Bazilevs, L. Beirao da Veiga, J. A. Cottrell, T. J. R. Hughes, G. Sangalli, "Isogeometric Analysis: Approximation, Stability and Error Estimates for h-Refined Meshes," 2006.**  
   DOI: <https://doi.org/10.1142/S0218202506001455>  
   Use for: rigorous B-spline/NURBS approximation estimates in Sobolev-type norms. This is mathematically deeper than needed for the September 15 discussion.

### Internal project anchors

- `DR_Update_July20_Meeting_Report.pdf`, Section 3.5 - supervisor request for the continuous-function / spline / Sobolev direction.
- [Approved Model 0-D v1.7](../../model-0D_pdf/Model0_Authoritative_Deterministic_Baseline_Formulation_v1_7.pdf), especially Sections 3.4, 4, 5, 6, 7, and 8, is the current approved baseline for comparison. The approved v1.7 integration revision does not change the spline model.

---

**Research discipline:** Do not rewrite the approved Model 0-D PDF or change the frozen model from this note alone. Any spline variant should become a separate, explicitly approved future modeling decision after its safety and theorem consequences are understood.
