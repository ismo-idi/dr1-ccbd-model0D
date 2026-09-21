#!/usr/bin/env bash
set -eo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/jazzy/setup.bash
source "$ROOT/install/setup.bash"
python3 "$ROOT/campus_environment/tests/verify_assets.py"
case "${1:-headless}" in
  headless) timeout --signal=INT --kill-after=15s 120s python3 "$ROOT/campus_environment/tests/verify_runtime.py" --output evidence/local-headless ;;
  gui) timeout --signal=INT --kill-after=15s 120s python3 "$ROOT/campus_environment/tests/verify_runtime.py" --gui --output evidence/local-gui ;;
  assets) ;;
  *) echo 'Usage: verify.sh [assets|headless|gui]' >&2; exit 2 ;;
esac
