# Reproducibility contract

Primary deployment: existing native Ubuntu 24.04 amd64, ROS 2 Jazzy + official Harmonic vendor packages. No container image was built; base-image digest is not applicable. Docker and Podman were absent, and replacing the existing stack was unnecessary.

## Levels of reproducibility

1. Source/assets: deterministic Python standard-library generator; all generated OBJ/MTL/SDF assets included and hashed. No installation or rendering is needed to inspect them. Runtime resolves installed package paths with ament, never this session's absolute path.
2. Build: five ament_cmake packages installed using colcon, with dependency manifests. No symlink install is used. A fresh source copy with spaces in its path is checked separately.
3. Runtime: installed native packages are reused. Exact observed direct pins are in `references/observed-direct-package-pins.txt`. `evidence/installed-packages.tsv` records the complete host package inventory. The inventories are observations, not a complete immutable binary lock.
4. OS/graphics: kernel, GPU, Mesa, compiler and ROS vendor libraries influence behavior. Screenshot pixel equality is not promised. The user's earlier version observations are recorded separately and are not represented as tested versions.

For a disposable fresh Ubuntu target with the official ROS apt source configured, the direct pin file can be supplied to apt (`xargs -r sudo apt-get install -- < references/observed-direct-package-pins.txt`). This is optional and was NOT executed. Review the apt transaction before accepting it. Exact package availability may disappear; do not silently replace unavailable pins. Full permanent recovery would additionally require retaining verified dependency .deb files, repository metadata and a full OS image. None is claimed here.

The maintained `scripts/setup.sh` defaults to a read-only plan and preserves already installed packages. Its explicit install mode installs missing named packages from configured mutable repositories. This is a practical compatible setup, not a bitwise lock. A ROS apt setup release and HTTPS repository metadata are also mutable unless separately archived.

## Downloads and runtime

Installation-time downloads: Ubuntu/ROS packages, optional TeX packages. Runtime: local OBJ, MTL, SDF and configs only. No Fuel model lookup is required. Gazebo and ROS need local IPC/network sockets for discovery and messages; 'no runtime downloads' does not mean no networking system calls.

## Recovery

Extract source archive into a new directory. Verify checksums. Recheck `/opt/ros/jazzy`, `gz sim --versions`, graphics, disk, and dependencies. Build, then run bounded headless verification before the GUI. Do not copy old install/build directories between paths. Consult `checkpoints/STATE.md` before resuming authoring. Do not delete or overwrite another task's sources or ROS installation.
