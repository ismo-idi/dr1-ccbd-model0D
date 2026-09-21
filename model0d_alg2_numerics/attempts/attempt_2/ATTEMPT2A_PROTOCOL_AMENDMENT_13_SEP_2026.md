# Model 0-D Algorithm-2 Baseline — Attempt 2A Diagnostic Amendment

**Date:** 13 September 2026  
**Role:** DAILY WORKER  
**Researcher authorization:** explicit authorization to run Attempt 2A on 13 September 2026 after review of Step-3 failure.  
**Repository branch checkpoint:** `Model-0_24-Aug-2026` at `bd4b7f19d687cf78976d3c99501ca1a75c4c91ce` (read-only checkpoint; this Attempt-2A work is uncommitted).  
**Purpose:** isolate one post-failure diagnostic correction while keeping the original crossing scenario and every frozen numerical setting unchanged.

## 1. What is changed

Attempt 1 stopped because IPOPT returned a tiny negative multiplier on a workspace inequality that was strongly inactive. The canonical row at failure was

```text
a1:W:k8:dim1:upper
raw backend multiplier = -9.56248038286337e-08
canonical constraint value g = -2.9999999927837857
```

The original finite diagnostic applied the multiplier sign test to all smooth inequalities using the backend multiplier directly. Attempt 2A makes the multiplier diagnostic activity-aware using KKT complementarity.

For every local inequality row `ell` in family `F`, retain the raw backend multiplier `mu_backend[ell]` verbatim in evidence. Define the already-frozen family-aware strict-inactivity buffer

\[
\tau_{\mathrm{inactive},F}=100\,\tau_F.
\]

The diagnostic multiplier is

\[
\mu_{\ell}^{\mathrm{diag}}=
\begin{cases}
0, & g_\ell(z)<-\tau_{\mathrm{inactive},F},\\
\mu_{\ell}^{\mathrm{backend}}, & \text{otherwise}.
\end{cases}
\]

The zero is justified only for the **finite KKT diagnostic**: exact KKT complementarity requires a strictly inactive inequality to have multiplier zero. This correction is not fed back into IPOPT and does not modify the NLP or the Sun--Sun primal/dual updates.

Active and near-active rows retain the raw backend multiplier and remain subject to the unchanged nonnegativity threshold.

## 2. What is not changed

Attempt 2A deliberately leaves unchanged:

- the physical Model 0-D mathematics;
- TCC architecture and guardian assignment;
- original crossing starts/goals;
- `N=2`, `q=2`, `K=8`, `dt=0.5`;
- workspace and A1 boxes;
- objective weights and physical clearances;
- Algorithm-2 beta/lambda/rho rules;
- all stopping schedules and finite caps;
- CasADi/IPOPT backend options, including limited-memory Hessian;
- every numerical threshold;
- no-retry policy;
- U3/U4 qualifications;
- physical and TCC acceptance predicates.

In particular, **no tolerance was loosened after observing Attempt 1**. The existing values `inactive_factor=100`, `tau_W=1e-8`, `dual_normalized=1e-8`, `complementarity=1e-6`, and `stationarity_normalized=1e-6` are unchanged.

## 3. Test obligation before execution

Before Attempt 2A is executed, the complete existing component suite plus new targeted tests must pass. New tests must establish that:

1. a strongly inactive workspace row with a negative raw backend multiplier is zeroed only in the diagnostic multiplier while the raw multiplier is preserved;
2. an active workspace row with the same negative multiplier is **not** zeroed and still fails the dual-sign diagnostic;
3. no frozen threshold is modified.

## 4. Interpretation boundary

A successful Attempt 2A would show only that the bounded numerical baseline can proceed under this researcher-authorized finite diagnostic amendment. It would not prove exact source-oracle compliance, exact physical safety certification, global optimality, U3, or U4.

A failed Attempt 2A must be reported as failure without further silent retuning.
