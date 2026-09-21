# Attempt 3 — independent audit of the exact first-block negative result

**Date:** 18 September 2026  
**Scope:** independent mathematical verification of the terminal Assumption-3 counterexample. No simulation or solver rerun.

## Audit design

The primary audit reconstructs all compatible binary64 values for the two logged affine workspace rows and evaluates the derivative exactly over their Cartesian product. The independent audit deliberately uses a different route: it constructs exact IEEE-754 round-to-nearest rounding cells for the logged row values, translates those cells by the workspace constant 3, and propagates exact rational lower/upper bounds directly. It does not import the primary audit code and does not enumerate candidate coordinates.

## Independent results

For both official repetitions, the independent rounding-cell audit obtains

\[
\frac{558383}{1125899906842624}
\le 8p_{2,y}^{1}-2p_{2,y}^{2}+12
\le
\frac{558393}{1125899906842624},
\]

with strictly positive lower bound. It independently obtains strict upper bounds

\[
g_{2,0}^{\mathrm{spd}}\le -0.5624812534790724\ldots<0,
\qquad
 g_{2,1}^{\mathrm{spd}}\le -0.5623312813180935\ldots<0,
\]

and verifies strict workspace inactivity for the chosen coordinate.

Thus all exact local constraints that can contribute to the \(p_{2,y}^{1}\) normal component are inactive, the exact normal component is zero, and the exact first-block gradient component is strictly positive. Exact stationarity is impossible.

## Logical audit

The conclusion does not require recovery of a unique hidden binary64 point. The rounding-cell enclosure covers every real/binary64 coordinate consistent with the stored affine residual, including tie endpoints conservatively. Therefore uncertainty caused by the event log not serializing the entire first-block vector cannot rescue stationarity.

The exact nonincrease result is compatible with this conclusion: Assumption 3 is conjunctive, so exact descent does not compensate for exact stationarity failure.

One failed first-block update is sufficient because the source assumption is required at each first-block call. No asymptotic or later-iterate behavior can turn the historical executed sequence into an exact-Assumption-3 sequence retroactively.

## Verdict

```text
PRIMARY_EXACT_AUDIT                 = PASS
INDEPENDENT_ROUNDING_CELL_AUDIT    = PASS
ASSUMPTION3_STATIONARITY_AT_R1T1A2 = FAIL
ASSUMPTION3_NONINCREASE_AT_R1T1A2  = PASS
HISTORICAL_ATTEMPT3_EXACT_ORACLE   = FAIL
```

**Independent verdict: ACCEPT THE NEGATIVE RESULT.** No mathematical deal-breaker was found. The historical Attempt-3 execution must remain `SUNSUN_ALGORITHMICALLY_CERTIFIED = false` under the frozen exact-source meaning.
