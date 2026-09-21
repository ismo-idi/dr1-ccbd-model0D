# Attempt 1 — original finite diagnostic

**Primary runs:** `runs/baseline_run1/`, `runs/baseline_run2/`.  
**Recorded date:** 12 September 2026; execution began after the planned 17:00 cutoff.  
**Outcome:** local-oracle abort at attempted `(r,t)=(1,17)`; last complete state `(1,16)`. Baseline expansion gate failed.

Read the [canonical final campaign report](../../FINAL_SIMULATION_CAMPAIGN_REPORT_13_SEP_2026.md) for the audited interpretation. The [original Step-3 report](STEP3_BASELINE_2UAV_0OBS_REPORT_12_SEP_2026.md) is preserved unchanged, alongside the [machine summary](STEP3_MACHINE_SUMMARY.json), [configuration](configs/baseline_2uav_0obs.json), original source/tests, plots and verification evidence.

This folder preserves the original source version with raw backend multiplier sign checks on smooth rows. Do not replace its diagnostic implementation with Attempt 2A's version. Original preparation/status files are historical; the final campaign is now closed and archived.

Large summaries are stored as `.json.gz`. Follow the root [reproducibility guide](../../REPRODUCIBILITY.md) to verify or restore original bytes before running historical verification scripts. No new run is authorized by this archive.
