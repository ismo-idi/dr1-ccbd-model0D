> **Post-execution status notice — 19 September 2026.** This dated naming record preserves the 17 September pre-Attempt-3 state. Attempt 3 was subsequently executed as the final presentation-stage numerical attempt and is now closed. Its current evidence and conclusion are in [Attempt 3](../attempts/attempt_3/ATTEMPT_README.md) and the [final three-attempt campaign report](../FINAL_SIMULATION_CAMPAIGN_REPORT_18_SEP_2026.md). The table below is retained as historical naming provenance; its “none executed/planned” cell is not current status.

# Attempt naming and evidence preservation — 17 September 2026

The researcher approved the following naming on 17 September. This changes navigation and current presentation labels, not experimental results.

| Current name | Former name | Current location | Evidence identity |
|---|---|---|---|
| Attempt 1 | Attempt 1 | [Attempt 1](../attempts/attempt_1/ATTEMPT_README.md) | Original baseline package and runs |
| Attempt 2 | Attempt 2A | [Attempt 2](../attempts/attempt_2/ATTEMPT_README.md) | The same 13 September successor package and two runs |
| Attempt 3 | None executed | No attempt directory or results yet | One final attempt planned after harmonization |

The former directory `attempts/attempt_2a/` is now `attempts/attempt_2/`. Internal original filenames such as `ATTEMPT2A_MACHINE_SUMMARY.json`, run identifiers `attempt2a_run1/2`, historical unexecuted proposals `Attempt 2A.1` and `2B`, original worker plots and JSON keys such as `attempt2a` retain their provenance spelling. They do not introduce extra attempts. Presentation-asset filenames now use `attempt2_`; the image bytes are unchanged and embedded old labels refer to this mapping.

Original input files, solver code, configuration, logs, summaries, tests and raw hashes are unchanged. Only the added navigation README inside the attempt folder is updated. `INPUT_FILE_MAP.json` changes storage locators, not original package identities or content hashes. `audit/check_saved_evidence.py` changes the two directory locators only; its checks and output keys are unchanged.

The original 13 September archive manifest is preserved as `ARCHIVE_SHA256_MANIFEST_13_SEP_2026.txt` in this directory; it describes the historical tree. The root `ARCHIVE_SHA256_MANIFEST.txt` describes the harmonized archive. Dated audit outputs remain historical evidence; the new verification record distinguishes checks repeated during this naming change.

Restoration and saved-evidence checks do not run the solver. No additional simulation or change to numerical acceptance criteria is authorized by this naming update.
