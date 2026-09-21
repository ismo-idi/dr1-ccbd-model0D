#!/usr/bin/env bash
# Geometry/math and actual QML tests without advancing Gazebo.
set -eo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/jazzy/setup.bash
source "$ROOT/install/setup.bash"
python3 "$ROOT/common/tests/check_cli.py"
"$ROOT/install/um6p_demo_core/lib/um6p_demo_core/motion_check" \
  "$ROOT/demo/demo_1_no_obstacle/src/um6p_demo_1/config/routes.txt" \
  "$ROOT/demo/demo_2_static_sphere/src/um6p_demo_2/config/routes.txt"
QT_QPA_PLATFORM=offscreen "$ROOT/install/um6p_demo_core/lib/um6p_demo_core/panel_check" \
  "$ROOT/install/um6p_demo_core/share/um6p_demo_core/config/ClearancePanel.qml"
