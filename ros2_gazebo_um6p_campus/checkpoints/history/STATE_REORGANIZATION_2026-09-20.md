# Current checkpoint — 20 September 2026 authorized delivery update

Latest user explicitly authorizes reorganization, adding both supplied recordings, README simplification and committing the complete delivery to GitHub. Earlier publication holds are superseded. No mathematical changes or new scenario behavior requested.

Starting remote branch: Model-0_24-Aug-2026, commit 3e8f51848bd6057005a782b31da2a25c9c7ca268. Recheck before publication. Preserve all unrelated scientific files. Backup: ../delivery_reorganization_backup/before-2026-09-20.tar.gz.

Completed: read checkpoints and current scripts; inspected original user failure logs. Demo 2 run local-demo-2-20260919-230628 contains wave=1 telemetry in near_obstacle_state, proving cross-talk: ROS domain 85 is shared with manual runs although Gazebo partitions differ. Manual malformed command also silently exits (concatenated guibash). Record these findings, isolate verifier ROS topics/nodes and test.

Next: reorganize into campus_environment, demo/demo_1_no_obstacle, demo/demo_2_static_sphere and common; preserve approved scene and tick-level motion. Add recordings, update scripts/docs/tutorials, rebuild and test including clean copy, render and inspect every tutorial page, refresh checksums/archive, then commit/publish only this delivery subtree and verify remote result.

Pending: all actions in preceding paragraph. No task-owned processes running. No host installation changes required. No commit created yet. User videos remain untouched at their supplied paths.

## Reorganization milestone
Five-package build PASS; Demo 1 GUI PASS; Demo 2 GUI PASS while a separate paused manual Demo 1 ran on the same ROS domain. Cross-talk regression PASS. All tick-level executed trajectories match earlier approved GUI traces; campus package bytes unchanged. Both videos copied unchanged. README and structure updated. New source paths installed and resolved. Both task-owned scenes shut down with exit 0.

Next: unit checks, paused campus GUI, complete clean rebuild in a path with spaces, tutorial compilation/page QA, artifact/remote review, then authorized commit/publication. No commit yet.

## Final verification / latest user continuation
Latest user asks to continue from checkpoint and finish; prior commit authorization remains effective. Verified saved GUI and clean result files exist and all four demo results are PASS. Parked campus GUI/clean checks and math/QML checks PASS. Both PDFs compiled; every rendered page inspected, with final wording corrections being applied. Videos uploaded as unattached GitHub blobs only; no commit/ref update yet. Upload journal: ../campus_publication_progress.json. No simulation processes remain from these checks.

Exact next action: finish PDF wording recompile/changed-page inspection; finalize evidence, checksums and ZIP; upload remaining changed blobs, construct only the delivery subtree, recheck branch HEAD, commit and update ref without force, then verify all remote file hashes and unchanged research entries.
