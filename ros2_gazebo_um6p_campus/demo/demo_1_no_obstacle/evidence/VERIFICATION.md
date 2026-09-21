# Demo 1 verification — 20 September 2026

PASS: installed GUI launch, exactly two named UAVs with intended poses, initially paused at zero, simultaneous takeoff, one continuous yield, interval separation, live ROS state/clock exchange, midflight freeze and resume, both landings, executed/rendered pose agreement and clean shutdown. GUI result and full CSV trace: gui/. Fresh build/headless result: clean_reproduction/. Both runs have identical six-coordinate/phase/status records through all 2597 ticks ending at first COMPLETE.

Minimum pair distance: 3.531609455583 m (required 3.2 m). Minimum sphere distance: not applicable (required 4.2 m in Demo 2). Figures copied to ../media/screenshots are actual Gazebo output. User video provenance is separate.



NOT VERIFIED: rigid-body/aerodynamic flight dynamics, arbitrary obstacle layouts, additional UAVs, VS Code task UI, older package versions or clean-OS provisioning. These are deterministic position-level checks, not Model 0-D certification.
