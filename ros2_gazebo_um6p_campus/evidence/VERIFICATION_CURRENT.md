# Current verification — 20 September 2026

## PASS

- Native build/install of all five reorganized packages; source-tree absolute paths are not needed by launch.
- Installed campus model/world validation: 7 static models, exactly two UAVs, 25,540 mesh triangles, all required OBJ/MTL assets local.
- Parked campus GUI: two launches, zero simulation time/iterations and no stepping, scene service exchange, exact Gazebo-to-ROS informational message, actual rendering and clean child exits. See campus_environment/evidence/gui/.
- Both demo GUI checks: entity count/poses, simultaneous takeoff, continuous yield, interval clearances, freeze/resume, ROS telemetry/clock, actual renderer poses, landings and clean shutdown. Each demo owns its evidence.
- Cross-talk regression: Demo 2 passes while a separate paused manual Demo 1 is alive on ROS domain 85; test ROS topics and nodes are uniquely namespaced.
- Reorganization preservation: 67 campus package files byte-identical; every executed pose/phase/status through 2,597 / 2,712 ticks matches the earlier approved trajectories.
- Fresh directory with spaces: five-package rebuild, math/QML tests, two paused campus launches and both headless demos. GUI and clean traces match tick for tick.
- Determinism scope (clarified 20 September 2026): the recorded trajectory is a deterministic function of the simulation tick, and every common tick agrees exactly between the GUI and clean-directory runs. The tick at which the pause request lands is **not** deterministic, so the mid-flight snapshots in the two `result.json` files are sampled one tick apart; the completed states are identical.
- Four malformed-launch cases now return clear Terminal A/Terminal B instructions. Twenty actual QML color/stale cases pass with synthetic data; no unsafe flight was used to show red.
- Both user MP4 files copied byte-for-byte, SHA-256 recorded; MP4 container headers describe 1920x1080 videos of 32.134 s and 33.767 s.

## Historical FAIL, repaired

The user's original verifier shared ROS topics with manual launches. The saved Demo-2 failure includes a wave=1 state, directly demonstrating contamination. The new unique ROS topic/node namespace supplements Gazebo isolation. A fresh paused-state barrier is checked without relaxing exact pose/time equality. Earlier failure logs are retained as failures under evidence/historical/kinematic/.

The working README also contained concatenated launch/start text (`guibash`). Correct separate commands now appear in README, both scenario READMEs and Tutorial 02. The launcher rejects malformed input with an explanation.

## NOT VERIFIED / scope limits

Fresh OS provisioning, Docker/dev-container, software-only/EGL Gazebo rendering, older user-reported package revisions and interactive VS Code task UI. Full decoding/playback of user MP4s was not performed: local GStreamer lacks the required H.264 High Profile decoder; no host codec was installed. The originals and checksums are preserved.

Physical dynamics, aerodynamic fidelity, controllers, sensors, arbitrary obstacle planning, more than two vehicles, TCC/Sun–Sun and numerical campaign replication are outside these kinematic tests. No mathematical baseline was changed.

## Reproduction and evidence

Follow README commands from the delivery root. GUI/hardware tests ran on the configured local Ubuntu 24.04.5 amd64 / Jazzy / Gazebo 8.15.0 / ros_gz 1.0.24 / Iris Xe system, not an inferred cloud environment. Reproduction reuses those installed dependencies. Exact current source hashes are in SHA256SUMS; historical evidence is explicitly separated. PDF compilation and page inspection are recorded in PDF_QA_CURRENT.json. Publication verification is a separate receipt after the commit becomes known.
