# Model 0-D — Final numerical campaign report

> **Naming update — 17 September 2026.** Attempt 2 is the current name of the historical Attempt 2A; the next planned attempt is Attempt 3. [Naming and evidence-preservation map](provenance/ATTEMPT_NAMING_17_SEP_2026.md). Dated campaign conclusions and historical identifiers retain their original scope.


**Closed:** 13 September 2026.  
**Researcher / final scientific authority:** Ismaël Assoumane Idi.  
**Production:** DAILY WORKER; subsequent scoped review and this final synthesis: INDEPENDENT AUDITOR.  
**Repository / branch:** `ismo-idi/CCBO_Model1` / `Model-0_24-Aug-2026`.  
**Pre-archive checkpoint:** `bd4b7f19d687cf78976d3c99501ca1a75c4c91ce`.  
**Disposition:** researcher accepted the audit feedback, stopped the numerical campaign and authorized this final report and archival publication. No additional simulations or worker correction round were requested or performed.

## 1. Final conclusion

The campaign produced **reproducible negative experimental evidence**, not successful numerical validation of the selected solver. Two attempts were each repeated in the same recorded environment. Attempt 1 stopped on the original finite multiplier-sign diagnostic. Attempt 2, using a disclosed successor diagnostic, reached the inner-iteration cap while trajectory-copy disagreement and actual-source safety-clearance violation remained.

Neither attempt completed the first outer iteration. No obstacle experiment was executed. No converged, globally optimal, source-oracle-certified or physical-safety-certified solution was obtained. This does not establish that Sun–Sun Algorithm 2, frozen TCC, or the physical Model 0-D formulation is invalid. It establishes the observed limitations of this particular finite implementation, protocol, scenario and execution budget.

The strongest demonstrated lesson is that **guardian-local safety against a copied trajectory does not establish safety of the actual source trajectories when copy agreement has not been achieved**. Physical postchecking therefore remains essential.

## 2. Scientific and experimental scope

The approved formal model and selected solver are described in the [v1.4 synthesis](../model-0D_pdf/Old/CCBO_Model0_Authoritative_Deterministic_Baseline_Formulation_v1_4.pdf), [Decision 14: TCC](../decisions/14_TCC_formulation.md), [Decision 15: Sun–Sun Algorithm-2 specification](../decisions/15_Sun-Sun_TCC_algorithm.md), and the [final Sunday study](../decisions/work_06_SEP_2026.txt). Formal Gates 3 and 4 were already complete. These experiments do not change the approved mathematics.

The [approved numerical protocol](MODEL0D_NUMERICAL_PROTOCOL_AND_READINESS_V1_0_11_SEP_2026.md), especially §§3–10, supplies the experimental values and acceptance rules. The [pre-Step-3 freeze record](STEP2_RESEARCHER_APPROVED_PRE_STEP3_FREEZE_12_SEP_2026.md) preserves researcher approval and reported component verification before the baseline runs.

| Item | Executed baseline |
|---|---|
| UAVs / spatial dimension / obstacles | 2 / 2 / 0 |
| Free samples per UAV / sampling period | K = 8 / 0.5 s; horizon 4 s |
| Starts | UAV 1: (−2, 0) m; UAV 2: (0, −2) m |
| Goals | UAV 1: (2, 0) m; UAV 2: (0, 2) m |
| Workspace / auxiliary compactification box | [−3, 3]² m / [−3.5, 3.5]² m |
| UAV radii / maximum speeds | 0.1 m each / 1.5 m/s each |
| Pair clearance | 0.4 m = 0.1 + 0.1 + 0.2 m safety buffer |
| Physical objective weights | Terminal tracking 20; squared-step regularization 1, for each UAV |
| Initialization | Stationary source trajectories with exact initial copy agreement |
| TCC localization | Guardian({1,2}) = 1; UAV 1 holds its source and a source-2 copy; one copy-equality edge |
| First outer penalties | β¹ = 2; ρ¹ = 4 = 2β¹ |
| Finite caps | 100 inner iterations; 20 outer iterations; 600 s wall-clock cap; no in-run retry |
| Inner stopping thresholds at r = 1 | R₁ ≤ 10⁻⁴; R₂ ≤ 10⁻⁴; R₃ ≤ 10⁻⁶ |
| Direct TCC / target acceptance | 10⁻⁶ m each |

This is a **single-process numerical implementation of the two localized UAV blocks**. The blocks are solved sequentially; see each attempt's `src/sunsun_algorithm2.py`, lines 408–409. It is not a deployed peer-to-peer system, communication benchmark, parallel speedup experiment, hardware test or real-flight demonstration. Historical discussion of distributed algorithm architecture must not be presented as experimentally measured distributed execution.

The recorded environment is Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, Matplotlib 3.10.8 and CasADi 3.7.2 with its IPOPT backend. IPOPT used the frozen limited-memory Hessian setting. Single-thread environment settings and `PYTHONHASHSEED=0` were recorded. Exact backend options and all thresholds remain in each attempt's `configs/baseline_2uav_0obs.json`; the run records include configuration and implementation hashes. The recorded environment is not a promise of bitwise identity on other platforms.

## 3. Chronology and schedule deviation

1. The numerical protocol was researcher-approved on 11 September. Step-2 component work and pre-run traceability were recorded on 12 September. The worker recorded 53 passing component tests in the pre-Step-3 freeze; this final audit did not independently rerun that suite.
2. Attempt 1, recorded in the Step-3 package dated 12 September, began **after the planned Saturday 17:00 cutoff**. The researcher explicitly acknowledged responsibility for the delay and directed that it not be attributed to the worker. This report records that deviation neutrally; it does not backdate execution or pretend the timetable was met.
3. The worker's amendment and report record researcher authorization of Attempt 2 on 13 September after review of Attempt 1. Its tests were reported as 56 passed before the new runs. This is a disclosed post-result change, not an unchanged-protocol repetition of Attempt 1.
4. The researcher stopped the campaign on 13 September, accepted the independent audit feedback and authorized archival closure. Proposed successor experiments in the historical worker report were **not executed**. No further numerical execution is authorized by this archive.

The final report does not assign precise execution start times unsupported by the evidence. Dates, the acknowledged late start, stored timing fields and historical approval records are preserved at their actual evidentiary level.

## 4. Attempt 1 — original diagnostic rejection

See [Attempt 1](attempts/attempt_1/ATTEMPT_README.md) and the unchanged [Step-3 worker report](attempts/attempt_1/STEP3_BASELINE_2UAV_0OBS_REPORT_12_SEP_2026.md), especially its executive findings and §§8–12.

Both recorded baseline runs stopped with `LOCAL_ORACLE_ABORT`, primary cause `FIRST_BLOCK_ORACLE_FAILED`, at attempted `(r,t) = (1,17)`. The persisted last complete state is `(1,16)`; it must not be confused with the rejected candidate.

At the rejected UAV-1 candidate, row 30 (`a1:W:k8:dim1:upper`) had canonical constraint value −2.9999999927837857 and raw backend multiplier −9.56248038286337 × 10⁻⁸. The normalized dual-sign residual was 9.56248038286337 × 10⁻⁸, exceeding the frozen 10⁻⁸ limit. That is a real failure of the original acceptance rule. The row was strongly inactive; the worker reported that the other required local diagnostics passed and the backend returned `Solved_To_Acceptable_Level`.

The last complete state had a positive ordinary-floating-point source safety margin, but substantial TCC disagreement. It was not an accepted outer solution, successful baseline or certified safe output. The rejection appropriately prevented obstacle expansion.

## 5. Attempt 2 — amended finite diagnostic, inner-cap failure

See [Attempt 2](attempts/attempt_2/ATTEMPT_README.md), the unchanged [diagnostic amendment](attempts/attempt_2/ATTEMPT2A_PROTOCOL_AMENDMENT_13_SEP_2026.md), and the [worker report](attempts/attempt_2/ATTEMPT2A_BASELINE_REPORT_13_SEP_2026.md), §§3–12.

The amendment constructs a diagnostic multiplier of zero for every inequality whose recomputed value satisfies `g < −100 × tau_family`, using the already frozen inactivity factor and family tolerances. Raw backend multipliers remain logged. Active and near-active rows retain their raw multiplier, and stationarity is recomputed using the resulting diagnostic vector. Only `src/diagnostics.py` changed among solver source files; test fixtures and focused tests were updated. The physical scenario, model, backend options, numerical thresholds and Sun–Sun update formulas were unchanged.

The change is motivated by KKT complementarity, but **changes the acceptance diagnostic and hence permitted execution**. It does not establish an exact KKT multiplier or exact source normal-cone oracle. “The amendment removed the original rejection” is supported; the historical phrase “false rejection” must not erase the original protocol failure.

At `(1,17)`, the same raw row-30 multiplier and constraint value recurred. Its diagnostic multiplier became zero and the revised finite check passed. All 100 accepted inner iterations then passed the amended local diagnostics. However, the inner stopping conditions were still unmet at iteration 100. The execution mechanism was `MAX_INNER_ITERATIONS`; the final postcheck added `TCC_NOT_ACCEPTED` and `PHYSICAL_VIOLATION_DETECTED`. Under the protocol's failure priority, `PHYSICAL_VIOLATION_DETECTED` is the primary cause. These labels describe different aspects of the same failed run and are not contradictory.

## 6. Consolidated final-state results

Each column below describes the **last complete stored state**, not a converged solution. Both attempts were run twice; the two recorded runs within each attempt agree after excluding timing fields.

| Quantity | Attempt 1 | Attempt 2 |
|---|---:|---:|
| Last complete outer / inner indices | 1 / 16 | 1 / 100 |
| Completed outer iterations | 0 | 0 |
| R₁ | 0.37669732341234324 | 0.01343852896082126 |
| R₂ | 1.5328517645723046 × 10⁻¹⁵ | 1.0401237528903013 × 10⁻¹⁵ |
| R₃ | 0.01745669812479472 | 0.0002248160621244216 |
| Direct copy disagreement, stacked edge norm (m) | 0.3029946622823656 | 0.12581049903927163 |
| Target residual norm (m) | 0.21424958036318856 | 0.08896145701513261 |
| Physical objective F | 4.324447512461001 | 3.9962839227687965 |
| Minimum source-source center distance (m) | 0.500849953505317 | 0.2861322983824108 |
| Minimum source-source safety margin (m) | +0.100849953505317 | **−0.11386770161758925** |
| Minimum workspace margin (m) | +1.024844720443907 | +1.023424852321479 |
| Minimum step-length margin (m) | +1.0491674196089207 × 10⁻¹⁰ | +0.21869369907162417 |
| Algebraic identity residual | 8.268646384127626 × 10⁻¹⁷ | 2.5443010932208815 × 10⁻¹⁷ |
| Absolute error in ρ = 2β | 0 | 0 |
| TCC accepted | No | No |
| Physical postcheck numerical pass | Yes, last complete state only | No |
| Baseline reliable for expansion | No | No |
| Safety / algorithmic certification | Neither available | Neither available |

The step-length margin is `vmax × dt − segment_length`, in metres; it is not a speed margin expressed in m/s. The direct copy residual is a stacked trajectory-vector norm; it is not the mismatch at every individual sample.

At Attempt 2's cap, R₁ is about **134.39 times** its threshold and R₃ about **224.82 times** its threshold. The decrease from their initial values is observed finite behavior, not a convergence-rate result. Increasing the cap might or might not yield acceptance; that experiment was not performed. Neither attempt exercised an accepted outer update sequence, so adaptive outer progression is not experimentally validated here.

## 7. Safety interpretation: clearance violation, not demonstrated body overlap

For Attempt 2, the closest source-source approach is on interval `k = 4`, at interval fraction approximately 0.05377602986432309. The center distance is 0.2861322983824108 m. Relative to the required 0.4 m clearance, the safety margin is −0.11386770161758925 m: a substantial numerical violation of the approved safety requirement.

The physical radii sum to 0.2 m, however. The minimum body-separation margin of the modeled disks is therefore **+0.08613229838241077 m**. Do not describe the result as demonstrated body collision. These are planned trajectories, not executed UAV motion. Crossings of path curves in a static plot alone also do not establish simultaneous collision; the reported distances use the shared time parameter.

The guardian's source-1 versus copied-source-2 minimum distance is about 0.4000000000920143 m, with a numerical margin of +9.20 × 10⁻¹¹ m. The corresponding actual-source trajectories violate clearance because copy consistency is incomplete. The tiny guardian margin is ordinary floating-point evidence, not exact positivity certification. U4 remains unresolved.

## 8. Audit and reproducibility evidence

The independent auditor reviewed the principal update/control flow, local NLP, geometry, TCC assembly, finite diagnostics and source amendment; inspected the reports, protocol and GitHub freeze records; and visually checked the main Attempt-2A trajectory and residual plots. The scope was intentionally bounded to preserve time and credits.

Direct saved-evidence checks established:

- All **76 Step-3** and **114 Attempt-2A** original manifest entries match their source packages. Recorded code and configuration hashes match the respective executable snapshots.
- Of 77 files shared between the packages, only `src/diagnostics.py` and `tests/test_control_flow.py` differ; Attempt 2 also adds focused tests and its new evidence. Earlier run data remain byte-identical.
- Saved NPZ arrays match the summary states; event files match the summary histories; repeated states, summaries and event histories agree after excluding `elapsed_s` and `backend_elapsed_s`.
- Auditor-written NumPy checks independently recover final objective, direct TCC/target residuals, R₃, algebraic identity and source/guardian closest-approach values. Direct evaluation of the closest relative vector corroborates the physical margin without importing the worker solver.
- The recorded multiplier sign/complementarity values and Attempt-2A inactivity mask agree with direct recomputation from raw/diagnostic multipliers.

The [saved auditor results](audit/independent_saved_evidence_checks.json) and [check script](audit/check_saved_evidence.py) are included. The script's paths were adapted for this archive; it does not call a solver. See [reproduction instructions](REPRODUCIBILITY.md) before using it.

Limits: no simulation was rerun during this audit or closure, and the component suites were not independently rerun. The supplied repeat evidence is verified, not a new auditor-generated repeat. Worker “independent verification” denotes a separate implementation path, not an independent reviewer. In `analysis/verify_attempt2a.py`, line 109, the inner R₁/R₂/R₃ values are read from the history; this auditor independently recovered final R₃ but did not reconstruct R₁/R₂ from preceding primal states. The package does not persist all intermediate primal states needed for an exhaustive per-iteration replay. Recorded P2P/matrix residual crosschecks and inspected update formulas provide scoped corroboration, not a proof of implementation correctness.

No major defect was identified that invalidates the two reported failure outcomes within this scope. The required interpretation refinements are incorporated in this final report; the historical worker reports remain unmodified evidence.

## 9. Presentation-ready lessons and permitted claims

1. **Implemented a bounded two-UAV test of the selected formulation.** Two attempts and same-environment repeats yielded traceable results; no successful baseline was obtained.
2. **Finite backend output needs explicit acceptance diagnostics.** A small negative multiplier on a strongly inactive row stopped the original protocol; a disclosed amended diagnostic allowed further progress.
3. **Local copied-trajectory feasibility is insufficient before TCC agreement.** The final Attempt-2A source clearance violation was caught by checking actual source trajectories.
4. **Numerical integrity is distinct from success.** `NUMERICALLY_VALID=true` means the state/evaluators were well formed under the implemented checks, not that the run converged, met TCC, satisfied safety or was certified.
5. **The campaign ends with known limits rather than an unsupported result.** More iterations, different geometry, obstacle cases and outer-loop progression remain untested hypotheses, not conclusions.

The [presentation assets guide](presentation_assets/README.md) supplies figures, captions, a compact comparison table and suggested answers. Its figures are unchanged copies of worker-generated assets; captions apply the audited interpretation. Do not claim obstacle performance, global optimality, deployed decentralization, a theoretical convergence rate, source-oracle certification, resolved U3/U4, or safety of executed flight.

## 10. Archive, closure and future use

The [archive README](README.md) explains the attempt folders and historical records. Each attempt retains its own code, settings, reports, verification evidence and run files. Attempt 2 was delivered as a cumulative package; its included `baseline_run1/2` and Step-3 material are historical duplicates of Attempt 1, not additional experiments. The campaign comprises **four experimental runs total: two per attempt**.

Large JSON/JSONL evidence is losslessly compressed. [Input provenance](provenance/INPUT_FILE_MAP.json) maps original paths and hashes to stored files, and the supplied helper verifies and restores original bytes for inspection or reproduction. Generated cache directories are omitted from the browsable attempt trees; their exact bytes remain encoded in provenance for original-manifest reconstruction. Existing pre-run protocol/freeze records remain identifiable; the root README and this report are the current closure narrative.

Archived proposals for Attempt 2A.1 or 2B are **not executed and not adopted by this closure**. The phrase “Model-1-like geometry” in the worker's proposals does not define or approve a new Model 1. Future work may refine the implementation under a separately reviewed protocol while preserving this immutable evidence.

The researcher is undertaking the spline study separately; no spline result is claimed in this numerical report. No further numerical run, model amendment, timetable revision, PDF rewrite or presentation generation was performed by this closure. The next task awaits the researcher's instruction concerning the meeting presentation.
