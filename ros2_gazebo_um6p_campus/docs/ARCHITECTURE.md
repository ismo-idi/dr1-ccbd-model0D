# Delivery architecture

The root is one colcon workspace with five installed packages. `scripts/build.sh` explicitly searches only the four source roots below; it does not depend on the current working directory.

- `campus_environment/src/um6p_campus_description`: local static assets and paused world.
- `campus_environment/src/um6p_campus_bringup`: installed paused launch, bridge and camera configuration.
- `common/src/um6p_demo_core`: shared motion system, Qt/QML clearance panel, bridge and generic launch.
- `demo/demo_1_no_obstacle/src/um6p_demo_1`: Demo 1 route input, generated SDF and launch.
- `demo/demo_2_static_sphere/src/um6p_demo_2`: Demo 2 route input, generated SDF and launch.

Each demo depends on the shared core; the core depends on the campus packages. The core never imports a sibling source directory at runtime. Launch resolves installed package shares and library prefixes. The demo world refers to campus models through the resource path supplied from the installed description package. Shared GUI/bridge configuration is installed once.

Each scenario maintains `config/routes.txt`: exactly two lines, one per UAV, containing x y z triplets in waypoint order. `common/scripts/generate_demo_worlds.py` embeds these routes in the respective SDF worlds. Rebuild after generation. The core reads the embedded routes; it contains no duplicated scenario waypoint table. Safety bounds and deterministic priority/yield rules are shared in Motion.hh. Scenario tests record expected takeoff/completion/yield ticks independently.

Root scripts provide the stable user interface. `setup_demo.sh`, `setup_native.sh`, `launch_paused.sh`, `build_tutorial.sh` and `build_kinematic_tutorial.sh` remain compatibility commands. New instructions use `setup.sh`, `launch_environment.sh` and `build_tutorials.sh`.

Media belongs to its scenario. User videos are preserved byte-for-byte; screenshots are actual Gazebo output. Historical diagnostics retain their original results and paths as historical text. Current evidence is explicitly dated. No build/install/log/cache directories enter the publication or archive.
