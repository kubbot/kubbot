#!/usr/bin/env bash
# Retain the old entry point without overwriting the hand-maintained README.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/render-workflow.py" "$@"
