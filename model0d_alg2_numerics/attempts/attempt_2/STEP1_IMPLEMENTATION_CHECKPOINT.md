# Model 0-D Algorithm-2 Numerics — Step-1 Implementation Checkpoint

**Date:** 11 September 2026  
**Role:** DAILY WORKER  
**Repository branch:** `Model-0_24-Aug-2026`  
**Repository traceability baseline:** `de49211ddd924e4751b7303ec3f1f2949b16bb23`  
**Status:** LOCAL / UNCOMMITTED / UNAUDITED  
**Researcher authorization:** Step 1 implementation authorized; any commit requires a new explicit researcher go-ahead.

## Scope completed

Implemented the smallest approved current numerical path for the frozen N=2 baseline:

- approved baseline and predefined-obstacle configuration files;
- exact guarded segment-distance value functions from Decision 10;
- frozen N=2 TCC selectors, split matrices, A1 projection and stationary exact-TCC initialization;
- two UAV-local CasADi/IPOPT first-block NLPs with source objective counted once;
- guardian-owned all-pairs UAV safety rows localized only at UAV 1;
- source-owned workspace/speed/obstacle rows and A1 foreign-copy rows;
- finite local-oracle diagnostic machinery with family-aware feasibility thresholds and degenerate-row omission boundary;
- exact A5 auxiliary update, slack update, dual update, R1/R2/R3 and Algorithm-2 outer updates;
- common failure/finalization/status framework preserving U3/U4 claim boundaries;
- reproducible execution/logging entry point;
- component-test suite prepared for the next mandatory stage.

## Implementation authority

The implementation follows the researcher-approved numerical protocol and the current scientific authorities, especially Decision 15 Sections 3–20 and 22–25, Decision 10's exact guarded segment-distance representation, and the frozen physical Model 0-D constraints.

## Checks actually performed in Step 1

1. Runtime environment rechecked: Python 3.13.5; NumPy 2.3.5; SciPy 1.17.0; Matplotlib 3.10.8; CasADi 3.7.2; IPOPT plugin available.
2. `python3 -m compileall -q src run_experiment.py tests` — PASS.
3. `pytest --collect-only -q` — PASS; 8 component tests collected. **Tests were not executed yet.**
4. Non-experimental build smoke — PASS: configuration loaded; TCC and both local NLP solver objects assembled; expected dimensions printed; no local NLP or Model-0D baseline solve executed.
5. Live GitHub branch rechecked after local work: still `de49211ddd924e4751b7303ec3f1f2949b16bb23`.

## Deliberately not performed

- no baseline experimental run;
- no experimental outcome inspection;
- no executed component-verification suite (Step 2);
- no obstacle scenario run;
- no threshold retuning;
- no GitHub write/commit/push after the initial traceability commit;
- no claim of exact source-oracle compliance, U3 closure, U4 certification, or final numerical validation.

## Next mandatory gate

Execute the complete pre-baseline component-verification suite. A blocker in structure, geometry, multiplier mapping, residual algebra or failure/finalization handling must be corrected before the first baseline outcome is interpreted.
