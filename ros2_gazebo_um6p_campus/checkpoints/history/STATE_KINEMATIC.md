# Current checkpoint — 20 September 2026 documentation follow-up

User approved the proposed new architecture but explicitly withholds commit/publication go. Do not reorganize files yet: this turn only clarifies manual Demo2 launch and updates README. Future presentation media is still awaited; the new terminal-error screenshot is diagnostic evidence only.

README now provides explicit Terminal A/Terminal B instructions for both demos, including `bash scripts/launch_demo.sh 2 gui` then `bash scripts/demo_control.sh start`, owner-terminal shutdown and separation from automated verification. Existing successful build can be reused. No runtime code, routes, installed package files, or architecture changed; no simulation executed or commit made.

New unresolved issue: user screenshot reports the automated verifier's midflight pause equality assertion (Wave2 GUI and also a Wave1 headless attempt). Exact cause is not yet diagnosed. Preserve and inspect local failing run logs/trace before proposing a fix. Incident: evidence/kinematic/user-reported-verifier-2026-09-20.md and .png. Prior successful test evidence remains historical. Before any later publication, resolve this issue and reverify affected behavior.

Exact next action: user can launch Demo2 manually with the README commands. Then, on requested follow-up, diagnose the verifier failure. Reorganization and publication await explicit user go; retain the accepted architecture from conversation. No task-owned processes started this turn.

The September19 ZIP and campus_kinematic_handoff.json are preserved as historical delivered artifacts and do not contain this README follow-up. The live folder checksum manifest is refreshed for this documentation revision. Regenerate the delivery archive after the later authorized changes and their validation. Previous completed handoff is preserved in STATE_HANDOFF_2026-09-19.md.
