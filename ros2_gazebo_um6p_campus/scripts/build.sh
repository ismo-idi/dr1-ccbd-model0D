#!/usr/bin/env bash
set -eo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/jazzy/setup.bash
cd "$ROOT"
colcon --log-base "$ROOT/log" build --base-paths "$ROOT/campus_environment/src" "$ROOT/common/src" \
    "$ROOT/demo/demo_1_no_obstacle/src" "$ROOT/demo/demo_2_static_sphere/src" \
  --build-base "$ROOT/build" --install-base "$ROOT/install" \
  --event-handlers console_direct+
