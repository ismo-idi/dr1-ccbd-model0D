#!/usr/bin/env bash
# Additive dependency check; no installation without explicit --install-missing.
set -eo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:---plan}"
case "$MODE" in --plan|--install-missing) ;; *) echo 'Usage: setup_demo.sh [--plan|--install-missing]' >&2; exit 2 ;; esac
bash "$ROOT/scripts/setup_native.sh" "$MODE"
MISSING=()
while IFS= read -r package; do
  [[ -z "$package" || "$package" == \#* ]] && continue
  if [[ "$(dpkg-query -W -f='${db:Status-Status}' "$package" 2>/dev/null || true)" != installed ]]; then MISSING+=("$package"); fi
done < "$ROOT/references/demo-packages.txt"
if (( ${#MISSING[@]} == 0 )); then echo 'All demo packages installed; no changes.'; exit 0; fi
printf 'Missing demo package: %s\n' "${MISSING[@]}"
if [[ "$MODE" == --install-missing ]]; then
  sudo apt-get update
  sudo apt-get install --no-upgrade "${MISSING[@]}"
else
  echo 'Review these packages; --install-missing installs only missing dependencies.'
fi
