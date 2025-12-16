#!/usr/bin/env bash
# Helper script to run `netlify dev` and then run smoke tests once the local server is available.
# Requires: netlify CLI installed (`npm i -g netlify-cli`) and Python requirements installed.

set -euo pipefail

PORT=${PORT:-8888}
SERVER_URL=${SERVER_URL:-http://127.0.0.1:${PORT}}

if ! command -v netlify >/dev/null 2>&1; then
  echo "netlify CLI not found. Install it with: npm i -g netlify-cli"
  exit 2
fi

echo "Syncing static files..."
python3 scripts/sync_static.py

echo "Starting netlify dev on port ${PORT} (in background)..."
# Start netlify dev; it will serve functions and static. We background it so we can run tests.
nohup netlify dev --port=${PORT} > /tmp/netlify_dev.log 2>&1 &
NETLIFY_PID=$!
echo "netlify dev pid=${NETLIFY_PID}, logs: /tmp/netlify_dev.log"

echo "Waiting for server to be ready at ${SERVER_URL}/health"
for i in $(seq 1 30); do
  if curl -sSf ${SERVER_URL}/health >/dev/null 2>&1; then
    echo "Server ready"
    break
  fi
  echo "Waiting... (${i})"
  sleep 1
done

echo "Running smoke tests against ${SERVER_URL}"
SERVER_URL=${SERVER_URL} python3 scripts/smoke_test.py

echo "Smoke tests passed; tailing netlify dev log (press Ctrl-C to stop)"
tail -f /tmp/netlify_dev.log
