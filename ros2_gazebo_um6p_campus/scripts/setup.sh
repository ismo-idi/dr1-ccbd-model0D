#!/usr/bin/env bash
# One dependency plan for campus and both demos; installs only with explicit option.
exec bash "$(dirname -- "${BASH_SOURCE[0]}")/setup_demo.sh" "$@"
