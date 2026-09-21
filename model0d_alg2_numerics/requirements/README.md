# Frozen dependency manifests

Added by the independent-audit correction of 20 September 2026 (audit finding **B6**). Before this, the executed environment of each attempt was *recorded* in `attempts/attempt_*/runs/*/environment.json` but nothing in the repository declared it in installable form, so a clean checkout could not stand the campaign environment up.

One manifest per attempt, because each attempt owns its own frozen snapshot and must never be reproduced against another attempt's stack:

| File | Attempt |
|---|---|
| `attempt_1.txt` | Attempt 1 |
| `attempt_2.txt` | Attempt 2 (historical raw identifiers `attempt2a_*`) |
| `attempt_3.txt` | Attempt 3 |

Each manifest is transcribed verbatim from that attempt's recorded `environment.json`; no version was inferred or updated.

**What the pins are for.** They are required to reproduce **bit-identical** numerical results. They are *not* required to run the component test suite: during the audit all three suites were re-run on a materially newer stack (Python 3.12.3, CasADi 3.8.1, NumPy 2.5.3, SciPy 1.18.1, Matplotlib 3.11.2) and passed in full — 53/53, 56/56 and 58/58. The suites are therefore not version-fragile.

**Determinism.** `run_experiment.py` refuses to start unless `PYTHONHASHSEED=0`, `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1` and `MKL_NUM_THREADS=1` are set. The manifests repeat this as a comment; the guard itself is in the entry point and is covered by `tests/test_run_entrypoint_guard.py`.

Re-running any attempt remains a **new execution** requiring explicit researcher authorization, as stated in `../REPRODUCIBILITY.md`.
