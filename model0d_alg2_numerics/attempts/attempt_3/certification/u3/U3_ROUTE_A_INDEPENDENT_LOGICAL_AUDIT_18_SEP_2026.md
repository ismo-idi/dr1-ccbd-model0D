# U3 Route A — independent logical audit

**Date:** 18 September 2026  
**Scope:** audit the U3-A proof and its Attempt-3-specific premises.  
**No simulation or solver execution was performed.**

## Audit questions and verdicts

### 1. Does the proof control the actual Algorithm-2 equality multiplier `y`, or only replacement multipliers?

**PASS.** The contradiction proof keeps the actual `y^{r_j}` from Sun–Sun condition (13) throughout. Local inequality multipliers are introduced only to represent exact normal-cone elements under MFCQ. No replacement equality multiplier is substituted for `y`.

### 2. Is the MFCQ abnormal-multiplier contradiction valid?

**PASS.** MFCQ supplies a direction `d` satisfying the equality tangent condition `Ed=0` and strict decrease of every active inequality. Any normalized abnormal relation

`E^T ybar + sum mu_bar_i grad g_i = 0`, `mu_bar_i >= 0`,

dotted with `d`, forces every `mu_bar_i=0`; equality full-row-rank then forces `ybar=0`. This contradicts unit normalization. Hence the actual primal-dual multiplier sequence is bounded.

### 3. Is equality full-row-rank merely assumed numerically?

**PASS — exact.** The frozen TCC theorem already proves it generally. The saved-evidence audit independently reconstructs the present `N=2, Q=16` integer matrices and obtains exact rank `32/32`; it also verifies `B^T B = 2 I_16` exactly with symbolic arithmetic.

### 4. Does the saved Attempt-3 exact lift satisfy MFCQ?

**PASS — exact for the saved candidate lift.** U4-E1 proves strictly positive exact physical workspace, speed and UAV–UAV margins; there are no obstacles. Exact A1/auxiliary-box margins are also positive. Therefore the complete active inequality set at the exact TCC lift is empty. With the equality Jacobian full row rank, MFCQ holds trivially.

### 5. Are nonsmooth active safety constraints a hidden problem?

**PASS / not applicable.** There are no active physical safety inequalities at the exact lift, so the active-safety `C^1` requirement is vacuous. Inactive degenerate rows do not enter the local active system.

### 6. Does the proof infer asymptotic boundedness merely from the ten finite outer iterations?

**PASS — no such inference is made.** The observed `beta = [2,4,4,...,4]`, finite `y`, and small slack are retained as descriptive consistency evidence only. The proof uses MFCQ plus the actual approximate-stationarity sequence.

### 7. Is there a circular assumption that the unknown Algorithm-2 limit equals the saved finite Attempt-3 state?

**NO hidden circularity, but an explicit scope condition remains.** The general U3-A theorem applies to any feasible smooth primal limit satisfying MFCQ. Separately, the exact lift of the saved Attempt-3 source trajectory is proved to satisfy MFCQ. The report does **not** claim that ten finite outer iterations prove an infinite exact-source sequence converges to this lift. It states the correct conditional implication: *if this exact lift is the selected primal limit, then the matching `y` limit is automatic.*

### 8. Does U3 closure also close the practical first-block oracle gap?

**NO.** This is correctly kept separate. The current practical finite IPOPT diagnostics still do not prove the exact normal-cone stationarity oracle required by Sun–Sun Assumption 3. Therefore `SUNSUN_ALGORITHMICALLY_CERTIFIED` remains false.

## Final independent verdict

The Route-A theorem is mathematically sound within its explicitly stated assumptions and closes the prior **actual-dual-sequence identification** gap. The Attempt-3 exact lift satisfies the MFCQ premise exactly. It is therefore defensible to freeze

```text
U3 = RESOLVED_BY_ROUTE_A_MFCQ_ACTUAL_SEQUENCE
```

with the two non-negotiable qualifications:

1. no universal MFCQ claim is made for all Model-0D feasible points; and
2. U3 closure is not equivalent to finite first-block oracle certification.

**Audit verdict: ACCEPT U3 ROUTE A FREEZE; NO DEAL-BREAKER FOUND.**
