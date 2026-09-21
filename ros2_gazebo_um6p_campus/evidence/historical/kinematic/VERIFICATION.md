> Follow-up, 20 September 2026: a user-reported local verifier pause-check assertion remains unresolved. See [incident record](user-reported-verifier-2026-09-20.md). The PASS results below describe the saved 19 September runs, not a verification of this later failure. Manual launch instructions have been clarified; no runtime code was changed in that follow-up.

# Kinematic demonstrations — final verification, 19 September 2026

Final evidence is `delivery-wave1-gui/`, `delivery-wave2-gui/`, `clean-wave1-final/` and `clean-wave2-final/`. Earlier `wave*`, `revised-*` and `final-wave1-gui` directories are development history and are superseded by the delivery runs. Their old route values must not be used as current results.

| Check | Result | Evidence and scope |
|---|---|---|
| Build/install all three packages | PASS | `build-tight-bypass.log`; native Jazzy/Harmonic/Qt5 |
| Fresh directory with spaces, new build/install | PASS | `clean-build-final.log`, `clean-source-identity.json` |
| Both actual Gazebo GUI waves | PASS | `delivery-wave*/result.json`, PNGs, launch logs and full ECM traces |
| Exactly two UAVs and expected static scenery | PASS | Scene service exchange, named entities and final dynamic rendering poses |
| Both take off simultaneously | PASS | Both first leave z=.12 at tick150, simulation time3.00s |
| One continuous yield and subsequent travel | PASS | Independent trace assertions; no rejected movement steps |
| Farther opposite-side landings | PASS | Both end at (+/-3.6,-40,.12), with sides swapped |
| Pair clearance on whole synchronized intervals | PASS | Independent closest-point computation from actual per-update ECM positions |
| Static sphere and close bypass | PASS | Sphere (0,-22,2.4), radius2.4; waypoint x=+/-4.3; full interval obstacle checks |
| Scenery and ground/pads | PASS | All23,432 scenery triangles considered; inflated flight region does not intersect relevant scenery AABBs; UAV vertex bounds, apron/pad geometry checked |
| Initial pause, midflight pause/resume | PASS | Zero initial time; paused time/positions unchanged while telemetry continues |
| ROS integration | PASS | Actual state and clock messages, validated distance fields; service control replies true |
| Motion path scope | PASS | Only `campus_demo_bridge` plus verifier in ROS graph; explicit system list has SceneBroadcaster and CampusKinematics, no Physics/controller/planner |
| Clean shutdown | PASS | All final launch owners exit0; relaunches start at initial state |
| Deterministic clean reproduction | PASS | `determinism-final.json`: GUI and clean traces identical through2597/2712 ticks |
| Live counter and color logic | PASS | Actual GUI PNGs: green/orange; `hud-unit.json`:20 synthetic actual-QML cases including red and stale gray |
| Original package preservation | PASS | `baseline-preservation.json`; original two packages unchanged byte-for-byte |
| Original paused-mode regression | PASS | Two bounded zero-time launches recorded separately; no demo motion plugin in original world |
| Tutorial | PASS | Exact source imports maintained implementation; final compiled PDF and every-page review |

## Observed final measurements

| Quantity | Wave1 | Wave2 |
|---|---:|---:|
| Completion simulation time |51.92s|54.22s|
| Minimum UAV center distance |3.53160945558m|3.53026645591m|
| Required UAV center distance |3.20m|3.20m|
| Minimum UAV-to-sphere center distance |N/A|4.36664631039m|
| Required sphere center distance |N/A|4.20m|
| Continuous yield duration |4.26s|4.86s|
| Rejected steps |0|0|

The 1.20m vehicle bound is conservative: actual maximum mesh radius is1.13626013947m around (0,0,.36) in each UAV frame. Required surface gaps are0.80m between bounds and0.60m from the bound to the sphere. The close bypass retains approximately0.16665m extra center-distance margin. These are position-level engineering checks, not physical flight validation, exact-rational certification, or certification of Model0-D's numerical campaign.

## Failures and corrections retained honestly

- `wave1-initial/`: FAIL because scene/info retained initial poses even after completed motion. The verifier now uses dynamic_pose/info for executed rendering poses.
- Earlier clean-copy Wave2 tests could not receive the Python scene service response. The final verifier uses bounded CLI scene exchange; both final clean runs pass. Earlier logs remain in the development clean folder, with a diagnostic summary copied here.
- Short-horizon release originally caused rapid stop/start alternation. The final motion uses a latched hold and full current-leg prediction for release, with one continuous yield asserted in both core and execution tests. Superseded GUI traces are retained.
- Initial GUI build did not automatically process .hh Qt meta-object headers. CMake policy CMP0100 NEW fixed it.
- The first standalone HUD test approach lacked Python QtQuick bindings. The final test is C++ using already installed Qt; a resource-style QML URL avoids a local component name shadowing the mock. No extra system package was installed. Its remaining implicit Connections deprecation warning is nonfatal.
- The first proposed fresh-copy directory name already belonged to the earlier paused baseline. Copying was refused; an unnecessary build of that old checkout's generated outputs completed. No source was overwritten. The final reproduction uses the distinct dated directory recorded in clean-source-identity.json. A missing optional root config directory was corrected before its first build; configuration belongs to installed packages.

## NOT VERIFIED / practical limits

Fresh-OS apt provisioning, exact older patch versions reported by the user, Docker/dev-container execution, software-only Gazebo rendering, VS Code UI interaction, desktop video recording, and in-place world reset are NOT VERIFIED. Tested hardware rendering uses Intel Iris Xe/Mesa on the current local host. The offscreen QML unit test is not a Gazebo software-rendering test.

No force integration, rotor dynamics, sensing uncertainty, communications delay, tracking error, acceleration/jerk feasibility, TCC, Sun-Sun, optimizer or autonomous controller is implemented. The two known waypoint layouts are supported; arbitrary obstacles or more than two UAVs require new design and validation. A sphere inflated around a landed UAV intersects ground conservatively; actual mesh height is used for ground contact checks.

## Commands and reproducibility

From the delivery root, on the compatible installed stack:

```bash
bash scripts/setup_demo.sh --plan
bash scripts/build.sh
bash scripts/verify_demo.sh 1 gui
bash scripts/verify_demo.sh 2 gui
```

Each verification command owns an isolated Gazebo partition, starts paused, explicitly runs only the authorized kinematic world, saves new evidence, and cleans up. It enforces150s wall time plus bounded shutdown. One run at a time. For manual inspection use launch_demo.sh and demo_control.sh as described in README and the guide; Ctrl+C stops the owning launch terminal.

The clean test copied only src, scripts, tests and references to a new folder whose name contains spaces, compared every copied file, built a new install, then ran both verification commands there in headless mode. It used the existing system packages, not a fresh OS or copied install/cache. Recorded patches in references/demo-installed-versions.tsv are evidence, not a permanent package lock. Source targets Ubuntu24.04 amd64, Jazzy, Gazebo Sim8/GUI8/plugin2 and Qt5. Apt repositories and documentation remain mutable.

Runtime model/material/mesh assets are local. Installation/documentation compilation may download dependencies. Original GitHub baseline commit3e8f51848bd6057005a782b31da2a25c9c7ca268 is verified separately; the new update is a local review delivery and has not been published.
