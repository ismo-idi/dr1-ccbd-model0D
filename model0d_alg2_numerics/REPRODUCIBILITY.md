# Inspecting and reproducing the Model 0-D numerical campaign

> **Current closure — 19 September 2026.** Attempts 1–3 are complete. Attempt 2 is the current name of historical Attempt 2A. Historical attempt-specific instructions remain valid for the bytes and status they recorded; this document supplies the current cross-attempt navigation.

## Saved-evidence verification without simulations

Attempts 1 and 2 retain their archived evidence/restoration workflow. From `model0d_alg2_numerics/`, using Python 3 with its standard library:

```bash
python tools/restore_evidence.py --verify
```

This verifies the historical compressed evidence without launching the solver. The saved-state audit needs the uncompressed logs and original cache entries, which `--verify` does not restore. To repeat it, first copy the complete `model0d_alg2_numerics/` directory to a new disposable location, enter that copied directory, and use Python 3 with NumPy available:

```bash
python tools/restore_evidence.py --restore
python audit/check_saved_evidence.py
```

The first command reconstructs the archived files. The second verifies the original manifests and saved-state facts for Attempts 1–2; it writes `audit/independent_saved_evidence_checks.json` in that copy. Do not run this writing audit inside the preserved publication tree. Neither command runs the optimizer. Attempt-3 certification is separate, as described below.

Attempt 3 is stored under `attempts/attempt_3/`. Its committed evidence includes the exact source/config/test snapshot, pre-run verification, execution provenance, both `final_state.npz` files, compact summaries, U3/U4 certification records and the terminal exact first-block audit. The complete raw official `events.jsonl` and `summary.json` files are preserved in the immutable Checkpoint-C archive rather than duplicated in the Git repository; their SHA-256 identities and sizes are frozen in:

```text
attempts/attempt_3/RAW_EXECUTION_EVIDENCE_MANIFEST.json
```

The official final-state SHA-256 for both Attempt-3 repetitions is:

```text
d444e1d5df70c64639f5a3f0de1445bc82150ec9797a7b9533a76feebed58e46
```

## Attempt-3 post-certification checks

No solver is needed to inspect the post-certification logic. The exact first-block negative audit scripts live in `attempts/attempt_3/oracle_audit/`; U3 proof/audit is under `certification/u3/`; U4 exact-rational and interval scripts/results are under `certification/u4/`.

The U4 interval history intentionally preserves an invalid first implementation and its correction. The invalid result is evidence of QA detection and must not be substituted for the corrected audit.

For a U4 saved-plan replay, work in the disposable copy and create a fresh `review_outputs/` directory there. For run 1:

```bash
mkdir review_outputs
python attempts/attempt_3/certification/u4/scripts/u4_exact_rational_certifier.py --config attempts/attempt_3/runs/attempt3_run1/config.json --state attempts/attempt_3/runs/attempt3_run1/final_state.npz --output review_outputs/run1_exact.json
python attempts/attempt_3/certification/u4/scripts/u4_interval_auditor.py --config attempts/attempt_3/runs/attempt3_run1/config.json --state attempts/attempt_3/runs/attempt3_run1/final_state.npz --output review_outputs/run1_interval.json
```

Use `attempt3_run2` and new output names for run 2. These commands need NumPy but no NLP solver. Use the recorded per-run `config.json` when comparing certificate input hashes: the source configuration and serialized run configuration have different file bytes even where their model values agree. Absolute input-path strings in the exact certificate naturally differ across machines; compare the input hashes and mathematical results, not those path strings.

The original first-block oracle scripts reference their original absolute raw-run directory and need complete `events.jsonl` files. Those logs are not in this Git tree. Before replaying that audit, obtain the immutable Checkpoint-C package identified by `RAW_EXECUTION_EVIDENCE_MANIFEST.json`, verify the recorded file hashes, and adapt only the input/output paths in a disposable copy of the audit scripts. Do not silently change the preserved scripts or their mathematical logic. Reading the committed audit results is not the same as independently replaying them.

The current `ARCHIVE_SHA256_MANIFEST.txt` covers this repository subtree, excluding itself. It does not claim to contain the separately archived large Attempt-3 raw logs. The previous root manifest is preserved in `provenance/ARCHIVE_SHA256_MANIFEST_CAPTURED_20_SEP_2026.txt`; at capture it was stale for five documentation/metadata files and did not cover the Attempt-3 additions. This was an archive-maintenance defect, not evidence that the saved trajectories changed.

## Dependency manifests and the external validation oracle

**Added 20 September 2026 (independent-audit correction).**

Installable dependency manifests, one per attempt, are in [`requirements/`](requirements/). They are transcribed verbatim from each attempt's recorded `environment.json` and are required for **bit-identical** numerical reproduction. The component test suites are not version-fragile: during the audit all three were re-run on a materially newer stack and passed in full (53/53, 56/56, 58/58).

A **centralized reference solve** of the frozen physical problem (P0) is in [`validation/centralized_reference/`](validation/centralized_reference/), with its script, results, console, environment and SHA-256 manifest. It is an external validation oracle for the TCC copy-space reformulation, adopted by [Decision 18](../decisions/18_centralized_reference_validation.md). It is **not** part of the frozen three-attempt campaign, does not change any campaign result, and is not a competing algorithm. Reproducing it needs NumPy and CasADi; the backend is IPOPT (Interior Point OPTimizer).

## Experimental reproduction — new authorization required

The presentation-stage campaign is closed. Re-running any attempt is a new execution and requires explicit researcher authorization. If later authorized:

- Attempt 1 must use its own source/config snapshot and original diagnostic rule.
- Attempt 2 must use its own activity-aware diagnostic amendment and historical `attempt2a_*` raw identifiers.
- Attempt 3 must use its own `src/`, `configs/`, exact cap-1000 freeze and the environment/provenance recorded in its folder.

Do **not** merge source trees or silently retune thresholds, geometry, caps, backend/options or stopping criteria. A new scientific change creates a separately identified successor experiment; no Attempt 4 belongs to the current presentation-stage closure.

## Claim boundary

Reproducibility of the finite run does not imply a convergence theorem. Attempt 3 is reproducible and finite-TCC-consistent, and its immutable deterministic saved source trajectory is exactly safety-certified. The historical binary64 first-block sequence nevertheless fails original Sun–Sun Assumption 3 exactly at a proved accepted update, so exact Sun–Sun algorithmic/full certification remains false for this execution.
