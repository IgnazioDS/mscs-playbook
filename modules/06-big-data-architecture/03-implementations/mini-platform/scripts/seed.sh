#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://localhost:8000/ingest}"
ENV_FILE="${ENV_FILE:-}"
INGEST_API_KEYS="${INGEST_API_KEYS:-}"
INGEST_KEY_ID="${INGEST_KEY_ID:-}"
INGEST_API_KEY="${INGEST_API_KEY:-}"

if [[ -z "$INGEST_API_KEYS" && -n "$ENV_FILE" && -f "$ENV_FILE" ]]; then
  INGEST_API_KEYS="$(grep '^INGEST_API_KEYS=' "$ENV_FILE" | tail -n 1 | cut -d= -f2- || true)"
fi

if [[ -n "$INGEST_API_KEYS" ]]; then
  INGEST_KEY_ID="${INGEST_KEY_ID:-$(echo "$INGEST_API_KEYS" | cut -d, -f1 | cut -d: -f1)}"
  INGEST_API_KEY="${INGEST_API_KEY:-$(echo "$INGEST_API_KEYS" | cut -d, -f1 | cut -d: -f2-)}"
fi

INGEST_KEY_ID="${INGEST_KEY_ID:-local-ingest}"
INGEST_API_KEY="${INGEST_API_KEY:-local-demo-ingest-key}"

for i in $(seq 1 5); do
  payload=$(printf '%s' "{\"schema_version\":1,\"event_type\":\"order_created\",\"event_time\":\"2026-01-27T12:00:0${i}Z\",\"order_id\":\"O-${i}\",\"amount\":$((i * 10)),\"currency\":\"USD\",\"customer_id\":\"C-${i}\"}")

  curl -fsS -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -H "X-API-Key-Id: $INGEST_KEY_ID" \
    -H "X-API-Key: $INGEST_API_KEY" \
    -d "$payload" >/dev/null
  echo "sent event $i"
  sleep 0.2
done
