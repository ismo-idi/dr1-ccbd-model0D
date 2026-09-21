# Model 0-D — U4 Physical-Safety Certification Protocol

**Date:** 18 September 2026  
**Scope:** immutable saved Attempt-3 final source trajectories only; no solver or simulation rerun.  
**Researcher decision:** approve U4-E1 exact-rational certification, with an additional independent validated interval-arithmetic audit.

## U4-E1 — exact-rational primary certificate

- Saved NumPy binary64 trajectory coordinates are converted to the exact dyadic rational values represented by those binary64 numbers, using `float.as_integer_ratio()`/`fractions.Fraction` semantics.
- Deterministic model constants in the JSON configuration are interpreted from their exact decimal literals, not from binary64 approximations.
- Physical safety is recomputed only on actual source trajectories.
- Workspace, speed, initial admissibility, obstacle (if present), and all-pairs UAV segment predicates are checked.
- Segment minimum-distance regime decisions and squared-distance comparisons are exact rational comparisons.
- No safety tolerance is used.
- For UAV/obstacle segment safety, certification uses the exact signed squared margin `M - rho^2`; taking a square root is unnecessary for the sign decision.
- `MODEL0D_SAFETY_CERTIFIED = true` iff every required physical predicate is completely evaluated and all exact signed margins are nonnegative.

## U4-E2 — independent interval audit

- A separate implementation uses `decimal.Decimal` interval arithmetic with directed rounding (`ROUND_FLOOR`/`ROUND_CEILING`) at 100 decimal digits.
- Inputs use exact singleton decimal representations of the saved binary64 values and exact decimal model constants.
- Every arithmetic operation produces an outward enclosure; each segment regime must itself be certified by interval inequalities. If a regime cannot be proved, the audit is inconclusive rather than guessed.
- The audit passes only if the lower endpoint of every required signed-margin interval is nonnegative.
- U4-E2 is an additional audit; it does not replace U4-E1.

## Claim boundary

Certification applies to the saved deterministic Model 0-D planned trajectories as represented in the immutable Attempt-3 evidence. It does not certify unknown real-UAV tracking/localization error, disturbances, asynchronous communication, or a global convergence theorem.
