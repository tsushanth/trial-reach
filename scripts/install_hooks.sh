#!/bin/sh
# Point this clone at the committed hooks. Uses a per-repo core.hooksPath, which overrides any global hooks path,
# so the pre-push hook here calls the machine-wide one itself when present.
set -e
cd "$(dirname "$0")/.."
git config core.hooksPath .githooks
echo "guard hooks active (pre-commit, pre-push)"
