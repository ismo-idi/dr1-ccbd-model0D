# Independent audit scope and archival verification

The researcher accepted the audit feedback on 13 September 2026 and authorized a final report and archival commit. The accepted verdict is **usable reproducible negative experimental evidence; no successful numerical validation**. The final report incorporates the wording and interpretation refinements; historical worker reports remain intact.

The auditor checked the supplied two packages against recorded manifests and code/configuration hashes, reviewed principal scientific implementation paths and the diagnostic amendment, inspected key plots, and independently recomputed saved-state facts without importing the solver. The exact results are in `independent_saved_evidence_checks.json`; `check_saved_evidence.py` is the repeatable saved-data check with archive-relative paths. It does not execute a numerical experiment.

This is not a new independent repeat of the simulations, an exhaustive proof of implementation correctness or an independent rerun of the worker's component tests. Reported 53/56-test passes remain worker evidence. Same-environment run equivalence was checked on supplied records. No claims about actual outer-loop convergence, real distributed execution or hardware safety follow.

For archival closure, original attempt files are copied without scientific edits. Large logs are losslessly compressed, with raw/stored hashes in provenance. The supplied restoration helper is checked in an isolated local copy, including reconstruction of encoded historical cache files needed by the original full-package manifests. The auditor check is rerun on that restored copy, without simulation. The two attempt code versions, all four distinct run records and historical duplicate evidence remain recoverable. New Markdown links, selected plot identities, comparison metrics and publication scope are checked.

The final root report and presentation captions govern present interpretation. Archive creation does not authorize future runs. Researcher responsibility for the acknowledged timetable deviation is preserved neutrally; splines and presentation generation are separate tasks.
