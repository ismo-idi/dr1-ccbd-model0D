# Numerical campaign — presentation assets and speaking notes

> **Current closure — 19 September 2026.** The campaign now contains three attempts. Existing Attempt-1/2 figures remain historical diagnostic assets; current presentation claims must use the final three-attempt report and the Attempt-3 closure status below.

These assets support the presentation; they are not a finished deck.

## Suggested main slide message

**One controlled cap-only successor converted the frozen two-UAV zero-obstacle baseline from an incomplete inner solve into a reproducible finite Model-0D/TCC success; deterministic saved-plan safety is rigorously certified, while exact Sun–Sun Assumption-3 certification is explicitly rejected for the historical binary64 execution.**

## Attempt-3 headline facts

- sole scientific/executable change versus Attempt 2: `max_inner_iterations 100 -> 1000`;
- two official fresh-process repetitions;
- both terminate `FINITE_OUTER_STOP` at `(r,t)=(10,3)`;
- 853 complete inner iterations total; first outer solve required 211 inner iterations;
- direct TCC disagreement `7.850016699224997e-07 m < 1e-6 m`;
- target residual `5.550800040449635e-07 m < 1e-6 m`;
- exact-rational U4 physical-safety certificate passes and independent corrected interval audit confirms it;
- U3 is resolved by the actual-sequence MFCQ theorem;
- exact first-block stationarity fails at `(r,t,a)=(1,1,2)`, so `SUNSUN_ALGORITHMICALLY_CERTIFIED=false` and the full four-way certificate is false.

Use `attempt3_outer_progression.csv` and the final campaign report for current numerical values.

## Historical figures retained

### Attempt 2 — actual sources and guardian copy

`attempt2_source_and_copy_trajectories.png` remains a correct historical illustration of incomplete copy agreement and source-safety failure at Attempt 2. It must be labeled **Attempt 2**, not presented as the final trajectory.

### Attempt 2 — inner residuals

`attempt2_inner_residuals.png` remains correct for the old cap-100 run. It is useful to motivate the cap-isolation question, but it must now be followed by the Attempt-3 fact that the first outer solve required 211 inner iterations. This supports the scenario-specific conclusion that cap 100 was an active blocker; it does not prove asymptotic convergence in general.

### Attempt 1 — original finite diagnostic rejection

`attempt1_oracle_rejection_t17.png` remains a historical diagnostic figure. The later activity-aware diagnostic amendment is preserved separately and must not be described as unchanged-protocol replication.

## Disciplined answers to likely questions

- **Did the selected implementation produce a successful finite baseline?** Yes for Attempt 3 under the frozen finite wrapper: it reached the finite outer stop, passed finite TCC consistency and numerical-integrity criteria, and the saved deterministic source trajectory is exactly safety-certified.
- **Is that an exact Sun–Sun Algorithm-2 theorem-certified execution?** No. The terminal exact audit proves first-block Assumption-3 stationarity fails at the first accepted agent-2 update.
- **Does that invalidate TCC or the Sun–Sun paper?** No. It characterizes this historical finite binary64 realization. Exact TCC formulation results and the source theorem remain distinct from the implementation evidence.
- **Did the UAV bodies collide in Attempt 2?** The required 0.4 m center-clearance was violated, but the minimum center distance remained above the combined modeled radii 0.2 m; do not call that demonstrated body overlap.
- **Is Attempt 3 obstacle-validated?** No. Its obstacle registry is empty; the empty family passes vacuously.
- **Is this deployed distributed performance?** No. It is single-process orchestration of localized blocks, not a networked peer-to-peer benchmark or flight test.
- **What are the defensible final research gains?** Exact physical Model-0D semantics, exact TCC reformulation, a controlled three-attempt finite campaign, reproducible Attempt-3 finite success, exact deterministic safety certification, a resolved U3 theorem route, and an exact negative theorem-fidelity result for the finite first-block oracle.

No Attempt 4 or hidden post-result retuning belongs to this presentation-stage path.
