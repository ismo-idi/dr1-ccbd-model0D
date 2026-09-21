# UM6P campus and two UAV demonstrations

This delivery contains a paused campus environment and two **deterministic kinematic demonstrations**. Exactly two UAVs take off together, travel, yield at a predicted crossing conflict and land on opposite pads. Demo 2 adds one stationary red sphere. These are geometric demonstrations: no rotor dynamics, flight controller, TCC, consensus or optimization solver runs.

## 1. Prepare the folder once

Open a Bash terminal **in this folder**, the one containing this README and `scripts/`. If needed, enter it using your own path (keep quotation marks around paths with spaces):

```bash
cd "/your/path/ros2_gazebo_um6p_campus"
```

Check dependencies without installing anything:

```bash
bash scripts/setup.sh --plan
```

Then build the five packages:

```bash
bash scripts/build.sh
```

Expected result: `Summary: 5 packages finished`. Build once after extracting this delivery, and again after source changes. You do not need to rebuild merely to switch demos. If packages are missing, review the plan and the native installation instructions in Tutorial 01. `bash scripts/setup.sh --install-missing` explicitly opts into installing missing packages; it is not part of normal launching.

## 2. Open Demo 1 — no obstacle

**Terminal A**, in this folder: copy only this command and press Enter.

```bash
bash scripts/launch_demo.sh 1 gui
```

**Wait until the Gazebo window shows the campus and both UAVs.** The scene starts paused. Keep Terminal A open; it owns Gazebo.

**Terminal B**, opened in the same folder: copy only this command and press Enter.

```bash
bash scripts/demo_control.sh start
```

Expected reply: `data: true`. After a three-second simulation-time preparation interval, both UAVs take off. UAV 2 yields once, then resumes and lands. The mission finishes at approximately 51.92 simulation seconds.

## 3. Open Demo 2 — static red sphere

First stop Demo 1: press **Ctrl+C once in Terminal A** and wait for the shell prompt to return. Run only one manual demo at a time.

**Terminal A**, in this folder:

```bash
bash scripts/launch_demo.sh 2 gui
```

**Wait until Gazebo shows both UAVs and the red sphere.** Keep Terminal A open.

**Terminal B**, in the same folder:

```bash
bash scripts/demo_control.sh start
```

Expected reply: `data: true`. Both UAVs take off, pass close to opposite sides of the static sphere, yield at the later crossing and land. The mission finishes at approximately 54.22 simulation seconds.

**The only change between launch commands is `1` versus `2`.** The start command is identical. It starts the already opened scene; it does not open Gazebo.

## 4. Pause, continue, stop or replay

To pause either demo, in Terminal B:

```bash
bash scripts/demo_control.sh pause
```

To continue, in Terminal B:

```bash
bash scripts/demo_control.sh resume
```

To stop, press **Ctrl+C once in Terminal A**, then wait. To replay, launch the desired demo again in Terminal A and start it from Terminal B. Relaunch is the supported reset. Ctrl+C in Terminal B after a completed control request does not stop Gazebo.

Do not paste Terminal A and Terminal B commands together. For example, `gui` followed immediately by `bash` makes an invalid command. The launcher now explains such errors. Always retain `scripts/` in the script path.

If `start` says `Service call timed out`, check Terminal A: the scene must already be running, with the same Gazebo partition in both terminals. A successful build alone does not open Gazebo. If the GUI fails, retain Terminal A's error rather than repeatedly sending start requests. See [troubleshooting](docs/TROUBLESHOOTING.md).

## 5. Open only the parked campus

From this folder, with other campus launches stopped:

```bash
bash scripts/launch_environment.sh gui
```

This separate world contains exactly two static placeholders. Leave it paused; do not press Play or send demo controls. `bash scripts/launch_environment.sh gui overview` selects the second saved camera. Stop with Ctrl+C in its owning terminal.

## 6. What the counters mean

The top-right panel shows live center distances and the corresponding minimum. Green means at least 0.80 m margin above the minimum; orange means nonnegative margin below 0.80 m; red means the minimum is violated; gray means stale telemetry. Pair minimum: **3.20 m**. Sphere-center minimum: **4.20 m**, including the UAV bounding radius and required surface gap. Exactly two fixed-size vehicles are supported. The displays are not real-flight or Model 0-D safety certification.

## 7. Automated checks are separate from manual recording

For a presentation, use Sections 2 and 3. The verifier below owns a bounded test: it starts, pauses, checks, resumes and **closes its own scene automatically**, including after a failed assertion. Do not control that scene manually.

From this folder after building, run the checks sequentially:

```bash
bash scripts/verify.sh headless
bash scripts/verify_demo.sh 1 headless
bash scripts/verify_demo.sh 2 gui
```

Each demo test writes a new evidence directory and exits. The repaired verifier isolates Gazebo transport and ROS topics/nodes, preventing a manually opened demo from contaminating test telemetry. The original failed logs remain documented; see [verification](evidence/VERIFICATION_CURRENT.md).

A full clean rebuild and all headless checks, using a **new nonexistent destination outside this folder**, are available with:

```bash
bash scripts/reproduce_clean.sh "/new/path/campus clean copy"
```

This uses the existing system dependencies. It does not provision a new OS or container.

## 8. Files, recordings and tutorials

| Location | Contents |
|---|---|
| `campus_environment/` | Campus packages, generator, tests, scene design and screenshots |
| `demo/demo_1_no_obstacle/` | Demo 1 package, routes, evidence, screenshots and your original video |
| `demo/demo_2_static_sphere/` | Demo 2 package, routes, evidence, screenshots and your original video |
| `common/` | Shared motion, clearance panel, bridge and verification code |
| `tutorial/` | Two clearly named PDFs and their exact LaTeX sources |
| `scripts/` | Commands used in this README; compatibility aliases retained |
| `references/`, `evidence/`, `checkpoints/` | Provenance, versions, verification and recovery state |

Start with [Tutorial 01: campus setup and coding](tutorial/01_UM6P_Campus_Environment_Setup_and_Coding.pdf), then [Tutorial 02: kinematic demos](tutorial/02_Two_UAV_Kinematic_Demos_Coding_and_Verification.pdf). The [tutorial source index](tutorial/README.md) explains recompilation. See [architecture](docs/ARCHITECTURE.md), [recording guide](docs/RECORDING_GUIDE.md) and [notices](THIRD_PARTY_NOTICES.md).

VS Code: use File > Open Folder, select this delivery, then open two integrated terminals and follow the same instructions. Tasks are also supplied for build, campus, each demo and controls. The underlying commands were tested; the VS Code task UI itself was not tested.

## 9. Versions and scope

Tested native stack: Ubuntu 24.04.5 amd64, ROS 2 Jazzy, Gazebo Harmonic Sim 8.15.0, ros_gz 1.0.24, Intel Iris Xe/Mesa 25.2.8. No host upgrades or driver changes were made. Jazzy/Harmonic is a supported official pairing, not a claim to be the newest stack. Earlier user-reported patch versions, clean-OS provisioning, Docker and software-only rendering remain unverified. Package inventories and apt pins record observations; mutable repositories prevent a permanent binary lock.

The photo-inspired campus is not a surveyed digital twin or official logo asset. Coordinates are metres, right handed: +X across the courtyard, +Y toward the rear buildings, +Z up. Starts: blue `uav_1` at (-3.6,-8.2,0.12), yaw +0.3 rad; orange `uav_2` at (3.6,-8.2,0.12), yaw -0.3. Both demos land at the opposite x coordinates, y=-40, z=0.12. Sphere center is (0,-22,2.4), radius 2.4. Landmark blocks alternate ±12 degrees; the pergola/building gap is 13.8 m. Decorative choices do not alter the mathematical benchmark.

Current research context is the approved [Model 0-D v1.7](../model-0D_pdf/Model0_Authoritative_Deterministic_Baseline_Formulation_v1_7.pdf). The tutorials and earlier publication records retain their dated v1.6 context; the deterministic mathematics is unchanged. The separate numerical campaign is not replayed. [Publication context](PUBLICATION_CONTEXT.md) identifies the scientific baseline and earlier campus commit.

`build/`, `install/`, `log/` and `.runtime/` contain disposable local products. Stop owned processes before removing only those directories inside this workspace. Keep source, media, evidence and checkpoints. For recovery, read [STATE.md](checkpoints/STATE.md) first. `sha256sum --check SHA256SUMS` verifies the delivered files before intentional edits.
