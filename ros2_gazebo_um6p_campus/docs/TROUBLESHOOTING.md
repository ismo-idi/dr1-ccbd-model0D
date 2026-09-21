# Launch and verification troubleshooting

## Build succeeds but Gazebo does not open
A build creates installed files; it does not launch a scene. In Terminal A run exactly `bash scripts/launch_demo.sh 1 gui` (or `2 gui`). The earlier malformed `guibash scripts/demo_control.sh start` joins two separate commands and is invalid. This string was also found in the working README; it has been removed. Invalid arguments now print usage and the two-terminal instructions.

## Start service times out
Wait for the scene to load in Terminal A. Keep it running and issue `bash scripts/demo_control.sh start` in Terminal B from the same root. Run one manual demo at a time. Both use partition `campus_demo` unless you explicitly set the same override in both terminals. Check Terminal A errors first; repeated start requests cannot launch a missing server.

## Automated verifier closes the window
This is intentional cleanup after completion or failure. Use launch_demo.sh for manual viewing and recording. The verifier is a test, not a presentation launcher.

## Historical pause assertion failure
The original verifier separated Gazebo partitions but subscribed to shared ROS domain-85 topics. User run `local-demo-2-20260919-230628` recorded a Demo-1 wave=1 state during a Demo-2 test. This directly establishes cross-talk; it does not establish a movement/clearance failure. The updated verifier assigns unique Gazebo partition and ROS topic/node namespace per test. It also requires a fresh paused sample at or beyond the latest observed tick and still checks exact pose/time equality throughout the pause. Received states are now saved for diagnosis. Current tests are listed in the verification record; original FAIL evidence remains historical.

## Assets missing or edited scene unchanged
Run build.sh again. Runtime resolves installed files, not source files directly. Do not mix an install folder from an older archive with new source. Build/install/log are local generated products.

## Blank GUI or ROS transport failure
Run inside the configured desktop session. Retain the launch log and check the installed version/graphics inventory. Do not change drivers, disable access controls or install a second ROS distribution to guess at a solution. Hardware GUI rendering was tested; other display arrangements require local verification.
