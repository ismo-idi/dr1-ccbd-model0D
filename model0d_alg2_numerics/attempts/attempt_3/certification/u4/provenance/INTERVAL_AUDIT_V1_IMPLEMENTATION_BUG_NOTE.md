# U4-E2 interval-audit implementation correction note

During pre-report cross-comparison of U4-E1 and the first U4-E2 implementation, the interval enclosure did not contain the independently computed exact-rational squared margin. The discrepancy was traced to Decimal unary negation in `neg()`: unary `-Decimal` was executed under the process default Decimal context (precision 28) before the directed-rounding operation, so an input endpoint was rounded prematurely.

This was an implementation defect in the *audit code*, not a simulation or trajectory result. The initial U4-E2 output is therefore invalid and is not used for any scientific conclusion. It is preserved for provenance only.

Correction: replace unary negation with `Decimal.copy_negate()`, which changes the sign without context rounding. The corrected U4-E2 script is separately hashed before re-execution. No Attempt-3 solver/simulation is rerun, and U4-E1 exact-rational inputs/results are unchanged.
