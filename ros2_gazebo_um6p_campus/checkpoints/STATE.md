# Validated delivery checkpoint — 20 September 2026

## Authorization and scope
User authorized this complete delivery update in ros2_gazebo_um6p_campus on GitHub branch Model-0_24-Aug-2026, including both original MP4 recordings. Latest continuation asks to finish from checkpoint. No further approval is needed for that publication. Do not alter scientific files, other branches, host installations or drivers. No TCC/Sun–Sun/solver/controller work is authorized by this update.

## Completed
- Approved campus / demo/demo_1_no_obstacle / demo/demo_2_static_sphere / common organization; five installable packages and unchanged root demo commands.
- Separate route ownership and shared core; all 67 campus files byte-identical; executed coordinates/phases/status identical to prior validated demos.
- README, scenario instructions, architecture, troubleshooting, notices, media provenance and current evidence updated.
- Original user MP4s copied unchanged; actual Gazebo screenshots stored with each scenario.
- Build/install, installed asset checks, math/QML checks, both GUI demos, strict pause/resume, clearance, ROS exchange, renderer poses and clean exits PASS.
- ROS cross-talk repair PASS with Demo 2 verified alongside a separate paused Demo 1. Malformed commands now explain correct usage.
- Fresh directory with spaces: all five packages built; parked campus and both demos PASS; GUI/clean tick identity PASS.
- Tutorial 01: 37 pages; Tutorial 02: 39 pages. Compiled from exact source and every rendered page inspected. Final PDF QA hashes are in evidence/PDF_QA_CURRENT.json.

## Files and reproduction
Source, evidence and media are under this folder. Named PDFs and exact source are in tutorial/. Root README contains setup, build, each separate Terminal A launch / Terminal B start, and shutdown commands. Maintained files are hashed in SHA256SUMS. Publication excludes build/install/log/.runtime and document intermediates. These directories may exist in the working copy and are disposable after stopping owned processes.

Historical checkpoints/evidence retain dated results and original path strings. They are not current launch instructions. Current results: evidence/VERIFICATION_CURRENT.md and each scenario's evidence/. Host dependencies: Ubuntu 24.04.5 amd64, Jazzy, Gazebo 8.15.0, ros_gz 1.0.24, Iris Xe/Mesa; no upgrades performed. Original video full decoding remains NOT VERIFIED because the local H.264 decoder was absent; byte integrity and MP4 headers passed.

## Publication boundary and exact next action
Starting commit: 3e8f51848bd6057005a782b31da2a25c9c7ca268. Starting root tree: 1edd9accffd746c855436f945f97a47899309942. At this source snapshot, validation is complete and publication is authorized. The final commit cannot contain its own hash; a separate adjacent publication receipt records the verified commit/ref after upload. Check that receipt and the remote branch before resuming publication to avoid duplicate commits.

Next action at snapshot: finish source/archive integrity review, publish only this subtree with a non-forced branch update after rechecking HEAD, verify every published file hash and all unchanged external repository entries, then give the user commit/archive links. Upload progress is stored outside this folder in campus_publication_progress.json; completed receipt will be campus_publication_receipt_2026-09-20.json. The dated September 14/19 archives are preserved. Do not repeat passing simulations unless source changes justify it.

## Process state and approvals
All task-owned Gazebo/ROS verification processes shut down. No simulation is intentionally left running. Build/render helpers have completed. No host changes or additional approvals are pending. Publication is the remaining authorized action at this checkpoint snapshot.
