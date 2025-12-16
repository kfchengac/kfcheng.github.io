#!/usr/bin/env bash
set -euo pipefail

if [ -z "${REDIS_URL:-}" ]; then
  echo "Please set REDIS_URL environment variable (e.g. redis://localhost:6379/0)"
  exit 2
fi

python3 -m pip install -r requirements.txt
echo "Starting rq worker connected to $REDIS_URL"
rq --url $REDIS_URL worker default
