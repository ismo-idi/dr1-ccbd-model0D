# Final source handoff — 19 September 2026

The paused campus and both authorized deterministic kinematic demonstrations are implemented, built and verified to the recorded scope. The latest user changes are included: simultaneous takeoff, one continuous yield with prompt predictive release, farther opposite-side landing pads, sphere farther from takeoff, tighter bypass, live colored counters, and removal of the counter footer. No simulator or ROS launch is intended to remain running.

## Completed

- [x] Original campus package files preserved byte-for-byte; no mathematical documents, archived campaign, presentation or timetable altered.
- [x] Paused baseline published first: GitHub commit3e8f51848bd6057005a782b31da2a25c9c7ca268, parent62bf3304431a9a458a8d2b4d2b6042fc4ceb5b96.
- [x] Current repository context harmonized to Model0-D v1.6 and Attempt3 closure, without executing any scientific campaign.
- [x] Three packages build/install on Ubuntu24.04.5 amd64 / Jazzy / Gazebo Sim8.15.0 / ros_gz1.0.24 / Qt5 / IrisXe Mesa.
- [x] Final GUI waves PASS, complete51.92s and54.22s; pair minima3.53160945558m and3.53026645591m; sphere minimum4.36664631039m.
- [x] One continuous yield of4.26s/4.86s, no rejected step, simultaneous ascent, exact final poses, pause/resume, actual ROS message exchange, dynamic render poses and clean exit.
- [x] Clean source build in a directory with spaces; both headless waves PASS and tick-by-tick deterministic identity against GUI runs.
- [x] Original paused mode loaded twice, remained at zero simulation time, exchanged ROS bridge messages and shut down cleanly.
- [x] Native clearance panel tested in actual Gazebo;20 isolated QML cases check green/orange/red/stale states without an unsafe simulation.
- [x] New32-page LaTeX tutorial compiled and every final page visually inspected; original34-page tutorial retained unchanged.
- [x] Source, dependency records, actual PNG evidence and trace logs preserved. Checksum manifest covers the finalized archive payload.

## Recovery paths

Source: src/um6p_campus_demo plus original description/bringup packages.
Guide: tutorial_kinematics/tutorial.pdf and tutorial.tex, chapters.tex, results.tex, listings.tex, assets/.
Current results: evidence/kinematic/VERIFICATION.md and final-results.json.
Final screenshots: evidence/kinematic/delivery-wave1-gui/hud.png; delivery-wave2-gui/obstacle.png and hud.png.
Versions: references/demo-installed-versions.tsv; historical and mutable-source limitations are explicit in the guide.
Source hashes: SHA256SUMS; previous manifest preserved as references/paused-baseline-SHA256SUMS.
Historical paused checkpoint: checkpoints/STATE_PAUSED_BASELINE.md.
Archive: ros2_gazebo_um6p_campus_2026-09-19.zip beside this folder. Its checksum and extraction verification are recorded beside the archive after packaging; see campus_kinematic_handoff.json.

## Exact next action

Review README, the new guide and the final actual screenshots. For manual recording, run setup_demo.sh --plan, build.sh if using an extracted copy, launch_demo.sh 1 gui, then demo_control.sh start in a second terminal. Ctrl+C in the launch terminal stops it; close before Wave2. On resume, read this file first, verify SHA256SUMS and existing evidence, preserve intervening edits, then continue only the requested follow-up. Do not redo authoring or reinstall a working stack.

The source delivery is complete. This kinematic update has not been committed or published remotely. The original baseline publication is verified separately. A new remote update requires the user's final instruction/review. No background automation or automatic credit-reset continuation is promised.

## Limits / pending local steps

The user records their own video. VS Code UI interaction, desktop recording, fresh-OS apt provisioning, older patch versions, Docker, software-only Gazebo rendering and in-place world reset are not verified. Hardware GUI and native terminal workflows are verified on this execution host. Kinematics use known deterministic waypoints and a static sphere; no dynamics, sensing noise, control, TCC, Sun-Sun or solver is implemented. More UAVs or arbitrary layouts require separate validation. No consequential host installation, driver/security change or paid service is pending.
