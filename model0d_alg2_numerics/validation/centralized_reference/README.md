# Centralized reference solve — external validation of the TCC reformulation

**Added by the independent pre-report audit, 20 September 2026. This is not part of the frozen three-attempt campaign and does not change any campaign result.**

## Why this exists

Every quantity the Attempt-3 campaign reports — `R1`, `R2`, `R3`, `R_TCC_eq`, `||xi||` — is internal to the Sun–Sun/TCC algorithm. None of them can distinguish *"solved the physical problem (P0)"* from *"converged to a stationary point of the feasibility-violation problem"*, an outcome Sun–Sun Theorem 1, case 2, explicitly permits. A direct centralized solve of (P0) is the only instrument external to the method, and it is what numerically corroborates Theorem T7 (exact feasible-set, value and optimizer-set preservation under the TCC copy-space reformulation).

## What it is not

It is **not** a competing algorithm. It needs a central coordinator, it does not scale, and it is precisely the architecture this research rejects. It plays the role an analytical solution plays for a partial-differential-equation solver: a validation oracle.

## Fidelity

- Physical data are read from the frozen Attempt-3 configuration, hash `faf2338e9e72b4de44864c0bb922102d3752fe647f684efad2c9226f11a0af6d`.
- The exact segment-safety constraints are imported from the frozen Attempt-3 `src/geometry.py`, so the centralized and distributed models evaluate the **same code path** for the only nonconvex constraint family.
- Backend: IPOPT (Interior Point OPTimizer) through CasADi, `ipopt.tol = 1e-10`, `bound_relax_factor = 0`.
- 20 starts: the constructive hover initialization plus 19 workspace-clipped Gaussian perturbations, seed 0.

## Result

```text
starts converged                          20 / 20
F*  (centralized)                         4.015742261564965
F   (Attempt-3 distributed)               4.0157423760136215
absolute objective gap                    1.1444865677390226e-07
relative objective gap                    2.85e-06 %
distinct global minimizers found          2   (separated by 0.9609 m in stacked l2 norm)
|x_TCC - nearest minimizer|_2             3.261077006949802e-05 m
max coordinate difference                 8.875261982552174e-06 m
min UAV clearance margin at that optimum  1.0649314763355733e-10 m   (constraint ACTIVE)
```

## Two consequences

1. **TCC exactness is numerically corroborated.** The distributed copy-space result and a direct centralized solve of (P0) agree to seven significant figures in objective and to 33 micrometres over the whole 32-coordinate trajectory.
2. **Non-uniqueness is exhibited on the actual baseline instance.** Two distinct trajectories attain `F*`, separated by almost a metre. This is a concrete numerical instance of the theorem proved in Decision Study 08: the objective is strictly convex (`alpha_i + beta_i > 0`, `beta_i > 0`), but the feasible set is nonconvex, so uniqueness fails. The two minimizers are the mirror pair of the symmetric crossing — UAV 1 yielding on one side or the other.

## Terminal-weight activity sweep

`weight_activity_sweep.py` answers one further question: is the inter-UAV clearance constraint active only because of the frozen weight `alpha = 20`? It is not.

```text
alpha      F*                 min UAV clearance margin (m)   active
  0.5      3.232602115                       1.095e-11        yes
  1.0      3.595555556                       4.543e-12        yes
  2.0      3.805996205                       4.398e-12        yes
  5.0      3.943255351                       4.433e-12        yes
 10.0      3.991167318                       5.366e-12        yes
 20.0      4.015742262                       1.061e-11        yes
 50.0      4.030702504                       3.116e-11        yes
```

The constraint is active at the centralized optimum across two orders of magnitude of `alpha`. Activity follows from the **symmetric crossing geometry** — both straight goal-directed paths pass through the origin — and not from the weight choice. This is the premise used in Decision 17, Section 10.4.

## Non-claims

Multistart IPOPT (Interior Point OPTimizer) on a nonconvex feasible set is **not** a proof of global optimality, and 20 starts is not exhaustive. This is numerical evidence on one instance. It certifies neither convergence of Algorithm 2, nor real-UAV safety, nor any property at `N > 2` or with a nonempty obstacle registry.

## Reproduce

```bash
python centralized_reference.py \
  --config ../../attempts/attempt_3/configs/baseline_2uav_0obs.json \
  --state  ../../attempts/attempt_3/runs/attempt3_run1/final_state.npz \
  --src    ../../attempts/attempt_3/src \
  --starts 20 --seed 0 --tol 1e-10 --output results.json
```

Requires NumPy and CasADi. Recorded environment is in `environment.json`; it differs from the frozen campaign environment, which is expected because this oracle is not part of the campaign.
