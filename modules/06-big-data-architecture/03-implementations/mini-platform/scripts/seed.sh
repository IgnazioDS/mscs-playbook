#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://localhost:8000/ingest}"
ENV_FILE="${ENV_FILE:-}"
INGEST_API_KEY="${INGEST_API_KEY:-}"

if [[ -z "$INGEST_API_KEY" && -n "$ENV_FILE" && -f "$ENV_FILE" ]]; then
  INGEST_API_KEY="$(grep '^INGEST_API_KEY=' "$ENV_FILE" | tail -n 1 | cut -d= -f2- || true)"
fi

INGEST_API_KEY="${INGEST_API_KEY:-local-demo-ingest-key}"

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
    -H "X-API-Key: $INGEST_API_KEY" \
    -d "$payload" >/dev/null
  echo "sent event $i"
  sleep 0.2
done
