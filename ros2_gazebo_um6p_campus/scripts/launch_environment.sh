#!/usr/bin/env bash
set -eo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/jazzy/setup.bash
source "$ROOT/install/setup.bash"
export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-84}"
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export GZ_PARTITION="${GZ_PARTITION:-ccbo_campus}"
export ROS_LOG_DIR="$ROOT/log/ros"
export GZ_HOMEDIR="$ROOT/.runtime/gz"
mkdir -p "$ROS_LOG_DIR" "$GZ_HOMEDIR"
# Only the documented GUI selector is accepted; arbitrary run arguments cannot leak in.
VIEW="${2:-courtyard}"
case "$VIEW" in courtyard|overview) ;; *) echo "View must be courtyard or overview" >&2; exit 2 ;; esac
case "${1:-gui}" in
  gui) exec ros2 launch um6p_campus_bringup campus.launch.py gui:=true view:="$VIEW" ;;
  headless) exec ros2 launch um6p_campus_bringup campus.launch.py gui:=false view:="$VIEW" ;;
  *) echo 'Usage: launch_paused.sh [gui|headless] [courtyard|overview]' >&2; exit 2 ;;
esac
