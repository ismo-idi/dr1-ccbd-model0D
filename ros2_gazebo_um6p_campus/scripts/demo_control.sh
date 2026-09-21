#!/usr/bin/env bash
# Only controls the separately named demonstration world; no arbitrary world name.
set -eo pipefail
source /opt/ros/jazzy/setup.bash
export GZ_PARTITION="${GZ_PARTITION:-campus_demo}"
case "${1:-}" in start|resume) REQUEST='pause: false' ;; pause) REQUEST='pause: true' ;;
  *) echo 'Usage: demo_control.sh start|pause|resume' >&2; exit 2 ;; esac
gz service -s /world/um6p_demo/control --reqtype gz.msgs.WorldControl \
  --reptype gz.msgs.Boolean --timeout 5000 --req "$REQUEST"
