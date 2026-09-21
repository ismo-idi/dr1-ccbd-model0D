# Official sources checked 14 September 2026

- ROS/Gazebo compatibility and vendor-package installation: https://gazebosim.org/docs/harmonic/ros_installation/
- ROS Jazzy Ubuntu apt installation: https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
- Supported targets and Jazzy support through May 2029: https://www.ros.org/reps/rep-2000.html
- Gazebo Harmonic support/release information: https://gazebosim.org/docs/harmonic/releases/
- ROS bridge: https://docs.ros.org/en/jazzy/p/ros_gz_bridge/ (web access returned a bot challenge; installed official package headers, YAML launch configuration and Python bindings were inspected instead).
- ros_gz upstream: https://github.com/gazebosim/ros_gz/tree/jazzy
- World files: https://gazebosim.org/docs/harmonic/sdf_worlds/
- Installed authoritative command help: `gz sim --help` distinguishes default paused from `-r`; `gz sdf --help` provides validation.
- Installed `gz.transport13.Node` Python bindings and gz-msgs10 proto definitions inspected for read-only scene requests, statistics, screenshot and StringMsg exchange.

These web pages and apt repositories can change. The chosen pair is supported; it is not claimed to be the newest pair. Installed binary versions are recorded separately. Source inspection did not execute scientific algorithms.
- Official ROS Jazzy apt documentation source inspected after web bot challenge: https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Installation/Ubuntu-Install-Debs.rst and https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Installation/_Apt-Repositories.rst

## September 20 recheck
Official Gazebo pairing table still lists Jazzy/Harmonic as recommended: https://gazebosim.org/docs/harmonic/ros_installation/. Newer ROS/Gazebo releases also exist; this delivery does not claim newest. ROS Jazzy installation and ros_gz_bridge documentation endpoints returned a bot challenge again; existing official-source references and installed source remain applicable. No dependency installation or upgrade was needed.
