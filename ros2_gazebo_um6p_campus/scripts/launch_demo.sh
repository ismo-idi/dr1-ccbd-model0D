#!/usr/bin/env bash
set -eo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
usage() {
  echo 'Usage: bash scripts/launch_demo.sh 1|2 [gui|headless]' >&2
  echo 'Terminal A: bash scripts/launch_demo.sh 1 gui  (or 2 gui)' >&2
  echo 'Wait for Gazebo. Terminal B: bash scripts/demo_control.sh start' >&2
  echo 'Enter each command separately; do not join the two terminal commands.' >&2
}
if [[ $# -lt 1 || $# -gt 2 || ! "$1" =~ ^[12]$ ]]; then usage; exit 2; fi
WAVE="$1"
case "${2:-gui}" in gui) GUI=true ;; headless) GUI=false ;; *) usage; exit 2 ;; esac
[[ -f "$ROOT/install/setup.bash" ]] || { echo 'Build first: bash scripts/build.sh' >&2; exit 2; }
source /opt/ros/jazzy/setup.bash
source "$ROOT/install/setup.bash"
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-85}"
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export GZ_PARTITION="${GZ_PARTITION:-campus_demo}"
export ROS_LOG_DIR="$ROOT/log/demo"
export GZ_HOMEDIR="$ROOT/.runtime/gz-demo"
mkdir -p "$ROS_LOG_DIR" "$GZ_HOMEDIR"
echo "Kinematic wave $WAVE starts PAUSED. Use demo_control.sh start in another terminal."
exec ros2 launch "um6p_demo_$WAVE" demo.launch.py gui:="$GUI"
