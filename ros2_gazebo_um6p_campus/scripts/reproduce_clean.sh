#!/usr/bin/env bash
# Fresh build and bounded tests. Never overwrite a previous destination.
set -eo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:?Pass a new target directory (spaces supported)}"
[[ ! -e "$TARGET" ]] || { echo 'Target already exists; choose a fresh directory.' >&2; exit 2; }
TARGET="$(realpath -m -- "$TARGET")"
case "$TARGET/" in "$ROOT/"*) echo 'Target must be outside source folder.' >&2; exit 2 ;; esac
mkdir -p "$TARGET"
for item in campus_environment common demo scripts references docs .vscode .gitignore; do
  cp -a -- "$ROOT/$item" "$TARGET/"
done
mkdir -p "$TARGET/evidence"
bash "$TARGET/scripts/build.sh" > "$TARGET/evidence/build.log" 2>&1
bash "$TARGET/scripts/verify_unit.sh" > "$TARGET/evidence/unit.log" 2>&1
bash "$TARGET/scripts/verify.sh" headless > "$TARGET/evidence/verification.log" 2>&1
for wave in 1 2; do
  bash "$TARGET/scripts/verify_demo.sh" "$wave" headless "$TARGET/evidence/wave$wave" > "$TARGET/evidence/wave$wave.log" 2>&1
done
printf 'Fresh build, paused campus and both kinematic demos PASS: %s\n' "$TARGET"
