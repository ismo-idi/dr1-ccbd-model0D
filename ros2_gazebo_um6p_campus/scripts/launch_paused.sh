#!/usr/bin/env bash
# Compatibility alias; use launch_environment.sh in new instructions.
exec bash "$(dirname -- "${BASH_SOURCE[0]}")/launch_environment.sh" "$@"
