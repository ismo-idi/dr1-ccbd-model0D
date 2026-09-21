# Verification record - 14 September 2026

Scope: environment loading, installed asset resolution, paused ROS/Gazebo integration, actual GUI rendering and source portability. No physical simulation time was advanced. No numerical or flight experiment was performed.

| Check | Status | Actual evidence |
|---|---|---|
| Existing dependencies / setup plan | PASS | setup-plan.txt: no missing packages, no changes |
| Two ament packages build/install | PASS | build.log |
| World + seven model SDF validation | PASS | assets.json; standalone validator with SDF_PATH |
| Local meshes, valid vertices/indices | PASS | 25 meshes, 25,540 triangles; assets.json |
| Exactly uav_1 and uav_2, intended xyz/yaw | PASS | gui/results.json, clean-reproduction/local-headless/results.json; final Gazebo scene service responses |
| Real ROS/Gazebo integration | PASS | two unique strings crossed Gazebo transport -> ros_gz -> ROS subscriber; this is message exchange, not only discovery |
| No unintended ROS nodes | PASS | only campus_evidence_bridge and temporary campus_verifier discovered in isolated test domain |
| Paused and zero time / iterations | PASS | every received final-test stats sample paused=true, iterations=0, sim_time=0, stepping=false |
| Headless close and reopen | PASS | two original headless launches; two final clean-copy launches |
| Actual default GUI rendering | PASS | gui screenshot PNG after explicit saved-camera reset; visibly checked lattice, tower, buildings, both UAVs and shadows |
| Final GUI clean shutdown/relaunch | PASS | gui/launch-1.log and launch-2.log report both children finished cleanly |
| No missing required rendered resources | PASS | final GUI logs: no missing material/model/URI or Gazebo error |
| Clean build with spaces in directory | PASS | clean-reproduction/; new source/build/install, same existing OS/dependencies |
| Deterministic asset regeneration / approved appearance preservation | PASS | deterministic-generation.json and feedback-change-scope.json |
| Final LaTeX PDF and every-page visual inspection | PASS | PDF_QA.md; 34 pages, imported maintained listings |
| GUI camera/screenshot Python diagnostic | FAIL, corrected | Python request failure/false reply; final installed-config camera reset and PNG capture use successful bounded Gazebo CLI services |
| Original terminal Git clone | FAIL (alternative used) | sandbox DNS failure; outside sandbox private authentication unavailable; pinned connector snapshot retrieved instead |
| Initial standalone SDF check | FAIL, corrected | GZ_SIM_RESOURCE_PATH alone insufficient for standalone checker; SDF_PATH fixed it |
| Initial GUI material/shutdown diagnostic | FAIL, corrected | gui-initial-diagnostic/: missing MTL warnings and duplicate interrupt child exit; early wrapper PASS was incomplete and is superseded |
| Fresh OS provisioning / missing-package install | NOT VERIFIED | existing dependencies already available; no installation transaction needed |
| Docker / dev-container | NOT VERIFIED / not selected | executables/socket absent; no image/digest claimed |
| Final overview camera rendering | NOT VERIFIED as final config | saved view supplied; initial overview screenshot exists before final material cleanup |
| Interactive VS Code UI | NOT VERIFIED | included tasks call the commands that passed |
| Older user-reported 8.11.0 / 1.0.22 pair | NOT VERIFIED | current execution measured 8.15.0 / 1.0.24 |
| EGL or software-only rendering | NOT VERIFIED | actual hardware GUI rendering used |
| Dynamics, sensors, flight, controls, safety certification | OUT OF SCOPE | static rendering placeholders; no Physics system, controllers or numerical code |

The harness checks child-process logs as well as the launch parent's exit code. Initial GUI results.json said PASS because the early harness checked only the parent; the Gazebo child error in that attempt is explicitly classified FAIL here. The final harness prevents that false-positive condition.

Qt file-dialog binding warnings remain in the final logs. They did not prevent scene rendering, screenshot output or clean exits. Gazebo built-in generic world-control/system services exist even with the supplied restricted plugin set; no motion or control bridge is launched, and no such service was used to advance time.

No runtime assets require an external download. Runtime checks require local socket/interface access; the sandbox's transport denial was resolved through authorized execution outside the sandbox, without altering host security or graphics settings.

Future local user check: `bash scripts/setup_native.sh --plan`, `bash scripts/build.sh`, `bash scripts/verify.sh headless`, then `bash scripts/verify.sh gui`. Inspect its actual screenshot and results. Run one test/launcher at a time. Do not step physics to obtain clock/sensor data.

Final feedback changes: U/6 +12 degrees, M/P -12 degrees; building translated +12m Y, providing 13.8m clear facade gap; UAV/pad centers moved to x +/-3.6, y -8.2. Forecourt reserve 18x18m is a geometric staging area only. `feedback-change-scope.json` confirms all other description meshes are byte-identical. Final runtime/clean-copy evidence supersedes earlier poses and screenshots.
