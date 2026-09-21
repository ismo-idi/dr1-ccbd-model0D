#!/usr/bin/env bash
# Inspect first. Only --install-missing invokes apt; installed packages are not upgraded.
set -eo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source /etc/os-release
[[ "$ID" == ubuntu && "$VERSION_ID" == 24.04 ]] || { echo 'Requires Ubuntu 24.04'; exit 2; }
[[ "$(dpkg --print-architecture)" == amd64 ]] || { echo 'This tested manifest targets amd64'; exit 2; }
MISSING=()
while IFS= read -r package; do
  [[ -z "$package" || "$package" == \#* ]] && continue
  if [[ "$(dpkg-query -W -f='${db:Status-Status}' "$package" 2>/dev/null || true)" != installed ]]; then MISSING+=("$package"); fi
done < "$ROOT/references/native-packages.txt"
if (( ${#MISSING[@]} == 0 )); then echo 'All required packages already installed; no changes.'; exit 0; fi
printf 'Missing: %s\n' "${MISSING[@]}"
case "${1:---plan}" in
 --plan) echo 'Configure the official ROS Jazzy apt repository if absent; then rerun with --install-missing.' ;;
 --install-missing) sudo apt-get update; sudo apt-get install --no-upgrade "${MISSING[@]}" ;;
 *) echo 'Usage: setup_native.sh [--plan|--install-missing]' >&2; exit 2 ;;
esac
