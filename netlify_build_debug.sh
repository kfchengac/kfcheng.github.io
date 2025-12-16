#!/usr/bin/env bash
set -euo pipefail
# Root-level shim so Netlify UI/build can find the script even if base dir changes.
if [ -f "scripts/netlify_build_debug.sh" ]; then
  exec bash scripts/netlify_build_debug.sh
fi

echo "scripts/netlify_build_debug.sh not found relative to $(pwd)" >&2
exit 1
