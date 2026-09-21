#!/usr/bin/env bash
set -eo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/jazzy/setup.bash
source "$ROOT/install/setup.bash"
WAVE="${1:?Usage: verify_demo.sh 1|2 [gui|headless] [new-output-folder]}"
EXTRA=(); case "${2:-headless}" in gui) EXTRA=(--gui) ;; headless) ;; *) exit 2 ;; esac
OUTPUT="${3:-$ROOT/evidence/local-demo-$WAVE-$(date +%Y%m%d-%H%M%S)}"
timeout --signal=INT --kill-after=20s 150s python3 "$ROOT/common/tests/verify_demo.py" "$WAVE" \
  "${EXTRA[@]}" --output "$OUTPUT"
