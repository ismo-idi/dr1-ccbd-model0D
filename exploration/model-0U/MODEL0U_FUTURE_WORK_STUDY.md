# Model 0-U — Short Future-Work Study for Dynamic and Uncertain Environments

**Project:** Constraint Consensus-Based Dynamics for Decentralized Path Planning in UAV Swarms  
**Baseline:** Model 0-D — Deterministic  
**Date:** 19 September 2026  
**Status:** Future-work study only — no integration into Model 0-D is authorized or implied  
**Purpose:** Define a short, rigorous roadmap for a later dynamic/uncertainty extension of Model 0-D.

---

## 1. Purpose and scope

Model 0-D deliberately freezes a deterministic planning problem before introducing dynamic environments and uncertainty. In particular, the current model uses static workspace/obstacle data, prescribed communication structures, exact deterministic physical safety constraints, Trajectory-Copy Consensus (TCC), and the selected Sun--Sun Algorithm-2 route.

The original Directed Research nevertheless requires a later extension toward:

- dynamic and time-varying constraints;
- uncertainty in sensing and communication;
- probabilistic or robust safety;
- analysis of how uncertainty propagates through decentralized coordination.

This short note records how that later extension, called **Model 0-U**, could be approached.

It is intentionally a roadmap, not a frozen formulation, theorem, implementation, or numerical campaign. Its content may change as the researcher's understanding improves and according to future supervisor or jury feedback.

---

## 2. Starting point inherited from Model 0-D

Model 0-U should extend the approved Model 0-D rather than replace its structure without justification.

Several Model 0-D simplifications were deliberately chosen so that they could be revisited later:

- the workspace is static;
- obstacle centers are static and exactly known;
- the initial UAV positions are treated as measured/estimated deterministic data;
- communication and collision-information edge sets are prescribed exogenously;
- the historical graph notation already reserves \(\rho(e,t_k)\) for edge presence and \(\zeta(e,t_k)\) for communication latency;
- distance/state-dependent communication, packet loss, delay dynamics, and stochastic communication are excluded from Model 0-D;
- hard physical UAV--UAV safety remains an all-pairs physical requirement and is not identified with communication availability;
- TCC and the current Sun--Sun implementation use a fixed reliable communication abstraction and therefore do not automatically provide guarantees under stale information, packet loss, delay, asynchronous communication, or changing graphs.

The dynamic/uncertain extension must preserve these distinctions unless a new modeling decision explicitly changes them.

---

## 3. Proposed Model 0-U study

### 3.1 Dynamic environment and receding-horizon planning

First reintroduce time dependence into the physical environment.

Possible extensions include

\[
\mathcal W \rightarrow \mathcal W(t),
\qquad
c_o \rightarrow c_o(t),
\qquad
C_i(t_0) \rightarrow C_i(t),
\]

and, where appropriate,

\[
h_{ij}(x_i,x_j)
\rightarrow
h_{ij}(x_i,x_j;t).
\]

Moving obstacles require a new continuous/inter-sample safety model; the static Model 0-D closest-distance formulas must not simply be reused without proving that they remain valid.

Because the environment evolves while the UAVs execute their trajectories, the natural first framework to investigate is **receding-horizon / Model Predictive Control (MPC)**:

1. estimate the current state/environment;
2. predict over a finite horizon;
3. solve the constrained multi-UAV planning problem;
4. execute only the first portion of the solution;
5. update the information and solve again.

This creates the dynamic layer of Model 0-U before stochastic uncertainty is added.

---

### 3.2 Sensing and localization uncertainty

Sensing uncertainty should be treated separately from communication uncertainty.

A first study should identify which quantities are actually uncertain, for example:

- UAV localization / estimated positions;
- estimates of neighboring UAV states;
- obstacle position or motion estimates;
- environmental measurements;
- disturbances or prediction errors, if later required.

Introduce an uncertainty variable, for example \(\xi^{\mathrm{sens}}\), only after its physical meaning is defined.

The study must then decide whether the uncertainty will be represented using:

- bounded uncertainty sets;
- stochastic random variables;
- empirical/data-driven models;
- or another justified representation.

No probability distribution should be invented merely to obtain a chance constraint.

---

### 3.3 Communication uncertainty and time-varying graphs

The communication layer should then extend the prescribed Model 0-D graph structure.

Possible future effects include:

- time-varying link availability;
- distance/state-dependent communication;
- packet loss;
- communication delay;
- stale neighbor information;
- temporary graph disconnections.

The already reserved notation

\[
\rho(e,t_k)
\]

may be used for communication-edge availability, while

\[
\zeta(e,t_k)
\]

may be developed for communication latency/delay.

The future communication graph may therefore become a time-dependent or random object such as

\[
G^{\mathrm{comm}}(t,\xi^{\mathrm{comm}}).
\]

A crucial Model 0-D principle must initially be retained:

\[
\boxed{
\text{physical safety}
\neq
\text{collision-information availability}
\neq
\text{communication availability}.
}
\]

Loss of a communication edge must not silently remove a physical UAV--UAV safety requirement.

Because TCC currently relies on connected copy structures and exchange of same-source trajectory information, the validity of TCC under changing, delayed, or unreliable communication must be studied again rather than assumed.

---

### 3.4 Chance constraints and robust safety

After the sources of uncertainty are defined, physical safety may be reformulated probabilistically.

A generic pairwise form is

\[
\boxed{
\mathbb P\!\left(
h_{ij}(x_i,x_j;t,\xi)\le 0
\right)
\ge 1-\varepsilon_{ij},
}
\]

where \(\xi\) represents the relevant uncertainty and \(\varepsilon_{ij}\) is an admissible risk level.

Before using such a constraint, Model 0-U must define:

- the uncertainty/random variables;
- the probability space or data model;
- the safety event;
- the meaning and justification of \(\varepsilon\);
- whether risk is individual or joint across UAV pairs;
- whether the guarantee applies at one instant, at sampled times, or over the complete planning horizon.

Robust counterparts may also be investigated when bounded uncertainty is more appropriate than a stochastic model.

The present deterministic margins

\[
\delta_i^{\mathrm{obs}},
\qquad
\delta_{ij}^{\mathrm{uav}}
\]

must also be reconsidered. Fixed margins may remain valid, while conservative or uncertainty-dependent tightening may be studied as a separate modeling decision. Such tightening must not be introduced silently.

---

### 3.5 Propagation of uncertainty through TCC and decentralized coordination

The central Model 0-U question is not only how to add noise to the physical model, but how uncertainty propagates through the whole decentralized planning chain:

\[
\boxed{
\text{uncertain observations / communication}
\rightarrow
\text{local information}
\rightarrow
\text{graph and TCC exchanges}
\rightarrow
\text{distributed optimization}
\rightarrow
\text{planned trajectories}
\rightarrow
\text{physical safety and feasibility}.
}
\]

Relevant questions include:

- How does sensing error modify the physical constraints seen by each UAV?
- How do delay, link loss, or stale copies affect TCC disagreement?
- Under what graph/connectivity assumptions can coordination still be maintained?
- How are deterministic safety margins affected?
- Can uncertainty cause infeasibility, oscillation, deadlock, or slower recovery?
- Which deterministic conclusions from Model 0-D remain valid and which must be weakened or replaced?

This is the point where sensing uncertainty, communication uncertainty, chance constraints, and consensus dynamics meet.

---

### 3.6 Mathematical re-audit

Model 0-U must not automatically inherit every deterministic Model 0-D theorem.

Once one precise uncertainty/dynamic model is selected, re-check only the mathematical results affected by the extension, including as necessary:

- continuous-time/inter-sample safety;
- nonemptiness and existence;
- stability and dependence on problem data;
- regularity of the new constraint functions;
- LICQ/MFCQ and KKT applicability;
- TCC equivalence under the new communication model;
- assumptions required by the selected distributed solver;
- interpretation of safety and convergence guarantees.

The objective is not to reproduce the complete Model 0-D analysis unnecessarily, but to identify exactly which conclusions survive and which ones change.

---

### 3.7 Minimal future numerical study

The first numerical Model 0-U study should remain small and interpretable.

A possible progression is:

1. deterministic Model 0-D reference case;
2. known moving obstacle;
3. sensing/localization uncertainty only;
4. communication uncertainty only;
5. combined sensing + communication uncertainty;
6. later, larger/swarm-scalability scenarios if justified.

Start with \(N=2\) before increasing the swarm size.

Possible observations include:

- minimum physical safety margin;
- chance/constraint violations;
- feasibility and solver status;
- TCC disagreement;
- communication loss/delay effects;
- deadlock and oscillation;
- recovery behavior;
- computational cost.

Monte Carlo experiments may estimate empirical violation frequencies, but empirical frequencies alone must not be presented as a proof of the probability guarantee required by a chance constraint.

---

## 4. Main research discipline

Model 0-U should initially remain a controlled extension of Model 0-D.

In particular:

- do not invent uncertainty distributions;
- do not conflate communication and physical-safety graphs;
- do not assume the present TCC fixed-graph results hold under packet loss or delay;
- do not reuse static-obstacle continuous-safety formulas for moving obstacles without a new derivation;
- do not claim probabilistic guarantees solely from Monte Carlo simulation;
- do not silently reinterpret the deterministic safety margins;
- do not transfer Model 0-D convergence, CQ, KKT, or solver conclusions without checking the assumptions affected by the new model.

---

## 5. Short future-work roadmap

The intended research progression is therefore

\[
\boxed{
\begin{aligned}
\text{Model 0-D deterministic baseline}
&\longrightarrow
\text{dynamic constraints + MPC}\\
&\longrightarrow
\text{sensing uncertainty}\\
&\longrightarrow
\text{communication uncertainty / }G(t)\\
&\longrightarrow
\text{chance or robust safety}\\
&\longrightarrow
\text{uncertainty propagation through TCC}\\
&\longrightarrow
\text{targeted mathematical re-audit}\\
&\longrightarrow
\text{small uncertainty-aware numerical study}.
\end{aligned}
}
\]

This sequence is provisional. Individual layers may later be combined, reordered, or simplified according to mathematical insight, numerical evidence, and feedback from the supervisor or jury.

---

## 6. Initial references and project anchors

### Internal Model 0-D anchors

- [Repository state and branch map](../../README.md)
- [Model 0-D continuation/handoff record](../../MODEL0D_CONTINUATION_BACKUP_PROMPT.md)
- [Decision 01 — Communication Graph and Physical Collision Structure](../../decisions/01_graph_and_collision_structure.md)
- [Decision 03 — Inter-Sample UAV--UAV Collision Safety](../../decisions/03_intersample_uav_uav_collision_safety.md)
- [Decision 04 — Inter-Sample UAV--Obstacle Collision Safety](../../decisions/04_intersample_uav_obstacle_safety.md)
- [Decision 06 — Frozen Deterministic Model 0-D Physical Optimization Problem](../../decisions/06_frozen_deterministic_model0d_physical_problem.md)
- [Decision 09 — Well-Posedness and Dependence on Deterministic Problem Data](../../decisions/09_well_posedness_and_problem_data_dependence_model0d.md)
- [Decision 14 — Trajectory-Copy Consensus (TCC)](../../decisions/14_TCC_formulation.md)
- [Decision 15 — Sun--Sun Algorithm-2 Solver Specification](../../decisions/15_Sun-Sun_TCC_algorithm.md)
- [Final Sunday scientific study](../../decisions/work_06_SEP_2026.txt)
- [Current approved Model 0-D v1.7 PDF](../../model-0D_pdf/Model0_Authoritative_Deterministic_Baseline_Formulation_v1_7.pdf)

### Directed Research / literature starting points

1. **Directed Research Guidelines, Section 6.5 — Dynamic and Uncertain Environments.**  
   Project authority: DR_Guidelines_REFS.pdf.

2. L. Blackmore, M. Ono, and B. C. Williams,  
   **"Chance-Constrained Optimal Path Planning With Obstacles,"**  
   *IEEE Transactions on Robotics*, 27(6):1080--1094, 2011.  
   DOI: https://doi.org/10.1109/TRO.2011.2161160

3. M. Ono and B. C. Williams,  
   **"Decentralized Chance-Constrained Finite-Horizon Optimal Control for Multi-Agent Systems,"**  
   *IEEE Conference on Decision and Control*, pp. 138--145, 2010.  
   DOI: https://doi.org/10.1109/CDC.2010.5718144

4. X. Li, X. Yi, and L. Xie,  
   **"Distributed Online Optimization for Multi-Agent Networks With Coupled Inequality Constraints,"**  
   *IEEE Transactions on Automatic Control*, 66(8):3575--3591, 2021.  
   DOI: https://doi.org/10.1109/TAC.2020.3021011

5. L. Dai, Q. Cao, Y. Xia, and Y. Gao,  
   **"Distributed MPC for Formation of Multi-Agent Systems with Collision Avoidance and Obstacle Avoidance,"**  
   *Journal of the Franklin Institute*, 354(4):2068--2085, 2017.  
   DOI: https://doi.org/10.1016/j.jfranklin.2016.12.021

6. R. Olfati-Saber and R. M. Murray,  
   **"Consensus Problems in Networks of Agents with Switching Topology and Time-Delays,"**  
   *IEEE Transactions on Automatic Control*, 49(9):1520--1533, 2004.  
   DOI: https://doi.org/10.1109/TAC.2004.834113

7. S. S. Mansouri et al.,  
   **"A Unified NMPC Scheme for MAVs Navigation With 3D Collision Avoidance Under Position Uncertainty,"**  
   *IEEE Robotics and Automation Letters*, 5(4):5740--5747, 2020.  
   DOI: https://doi.org/10.1109/LRA.2020.3010485

8. A. Papadimitriou, H. Jafari, S. S. Mansouri, and G. Nikolakopoulos,  
   **"Multi-Stage NMPC for a MAV based Collision Free Navigation Under Varying Communication Delays,"**  
   *Journal of Intelligent & Robotic Systems*, 107:33, 2023.  
   DOI: https://doi.org/10.1007/s10846-023-01818-1

9. A. Ben-Tal, L. El Ghaoui, and A. Nemirovski,  
   **Robust Optimization**, Princeton University Press, 2009.  
   DOI: https://doi.org/10.1515/9781400831050

10. A. Shapiro, D. Dentcheva, and A. Ruszczyński,  
    **Lectures on Stochastic Programming: Modeling and Theory**, SIAM, 2009.  
    DOI: https://doi.org/10.1137/1.9780898718751

---

**Research discipline:** This note defines a future study only. It does not modify the approved Model 0-D physical model, TCC architecture, Sun--Sun solver selection, or current deterministic claims.
