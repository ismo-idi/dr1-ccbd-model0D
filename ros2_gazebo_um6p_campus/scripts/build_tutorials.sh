#!/usr/bin/env bash
set -eo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-all}"
case "$MODE" in all|campus|demos) ;; *) echo 'Usage: build_tutorials.sh [all|campus|demos]' >&2; exit 2 ;; esac
python3 "$ROOT/scripts/tutorial_listings.py"
python3 "$ROOT/scripts/kinematic_listings.py"
for kind in campus_environment kinematic_demos; do
  [[ "$MODE" != campus || "$kind" == campus_environment ]] || continue
  [[ "$MODE" != demos || "$kind" == kinematic_demos ]] || continue
  cd "$ROOT/tutorial/source/$kind"
  if command -v latexmk >/dev/null; then
    latexmk -pdf -interaction=nonstopmode -halt-on-error tutorial.tex
  elif command -v tectonic >/dev/null; then
    tectonic --keep-logs tutorial.tex
  else
    echo 'Install optional documentation tools or provide Tectonic on PATH.' >&2; exit 2
  fi
  if [[ "$kind" == campus_environment ]]; then
    NAME=01_UM6P_Campus_Environment_Setup_and_Coding.pdf
  else
    NAME=02_Two_UAV_Kinematic_Demos_Coding_and_Verification.pdf
  fi
  cp tutorial.pdf "$ROOT/tutorial/$NAME"
  pdfinfo "$ROOT/tutorial/$NAME"
done
