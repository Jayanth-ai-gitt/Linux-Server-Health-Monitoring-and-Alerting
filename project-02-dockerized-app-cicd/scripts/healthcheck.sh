#!/usr/bin/env bash
# Simple monitoring script: checks the /health endpoint and logs the result.
# Usage: ./scripts/healthcheck.sh [url]
# Exit code 0 = healthy, 1 = unhealthy (so cron / CI can react to it).

set -u

URL="${1:-http://localhost:5000/health}"
LOG_FILE="${LOG_FILE:-healthcheck.log}"

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }

# -s silent, -o discard body, -w print only HTTP status code, --max-time avoids hanging
STATUS=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "$URL" || true)

if [ "$STATUS" = "200" ]; then
  echo "$(timestamp) OK    $URL (HTTP $STATUS)" | tee -a "$LOG_FILE"
  exit 0
else
  echo "$(timestamp) FAIL  $URL (HTTP ${STATUS:-none})" | tee -a "$LOG_FILE"
  exit 1
fi
