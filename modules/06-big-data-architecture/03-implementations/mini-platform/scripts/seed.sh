#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://localhost:8000/ingest}"

for i in $(seq 1 5); do
  payload=$(cat <<JSON
{
  "event_type": "order_created",
  "event_time": "2026-01-27T12:00:0${i}Z",
  "order_id": "O-${i}",
  "amount": $((i * 10)),
  "currency": "USD",
  "customer_id": "C-${i}"
}
JSON
)

  curl -fsS -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "$payload" >/dev/null
  echo "sent event $i"
  sleep 0.2
 done
