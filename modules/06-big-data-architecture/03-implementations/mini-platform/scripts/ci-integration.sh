#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-modules/06-big-data-architecture/03-implementations/mini-platform/.env.local.example}"

compose() {
  docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" "$@"
}

cleanup() {
  local exit_code=$?
  if [[ $exit_code -ne 0 ]]; then
    compose logs --no-color || true
  fi
  compose down -v --remove-orphans || true
  exit $exit_code
}

trap cleanup EXIT

retry() {
  local attempts="$1"
  shift

  local attempt=1
  while true; do
    if "$@"; then
      return 0
    fi
    if [[ $attempt -ge $attempts ]]; then
      return 1
    fi
    attempt=$((attempt + 1))
    sleep 5
  done
}

wait_for_exact_value() {
  local label="$1"
  local command="$2"
  local expected="$3"
  local retries=30

  for _i in $(seq 1 $retries); do
    value="$(eval "$command" | tr -d '[:space:]' || true)"
    if [[ "$value" == "$expected" ]]; then
      echo "$label: $value"
      return 0
    fi
    sleep 2
  done

  echo "timeout waiting for $label to become $expected"
  return 1
}

for image in \
  python:3.11-slim \
  postgres:15 \
  clickhouse/clickhouse-server:24.1 \
  minio/minio:RELEASE.2024-01-16T16-07-38Z \
  redpandadata/redpanda:v25.3.6
do
  retry 3 docker pull "$image"
done

compose config -q
compose build --pull
compose up -d

ENV_FILE="$ENV_FILE" bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/wait-for.sh "$COMPOSE_FILE"

API_KEY="$(grep '^INGEST_API_KEY=' "$ENV_FILE" | tail -n 1 | cut -d= -f2-)"
response="$(curl -fsS -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"schema_version":1,"event_type":"order_created","event_time":"2026-01-27T12:00:00Z","order_id":"O-ci","amount":42,"currency":"USD","customer_id":"C-ci"}')"
event_id="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["event_id"])' <<<"$response")"

wait_for_exact_value \
  "schema_migrations" \
  "compose exec -T postgres psql -U \${POSTGRES_USER:-bd06} -d \${POSTGRES_DB:-bd06} -t -A -c \"select count(*) from schema_migrations;\"" \
  "3"

wait_for_exact_value \
  "clickhouse.schema_migrations" \
  "compose exec -T clickhouse clickhouse-client --query \"select count() from analytics.schema_migrations;\"" \
  "2"

wait_for_exact_value \
  "ingest_log" \
  "compose exec -T postgres psql -U \${POSTGRES_USER:-bd06} -d \${POSTGRES_DB:-bd06} -t -A -c \"select count(*) from ingest_log where event_id = '$event_id';\"" \
  "1"

wait_for_exact_value \
  "event_processing.status" \
  "compose exec -T postgres psql -U \${POSTGRES_USER:-bd06} -d \${POSTGRES_DB:-bd06} -t -A -c \"select status from event_processing where event_id = '$event_id';\"" \
  "completed"

wait_for_exact_value \
  "processed_events" \
  "compose exec -T postgres psql -U \${POSTGRES_USER:-bd06} -d \${POSTGRES_DB:-bd06} -t -A -c \"select count(*) from processed_events where event_id = '$event_id';\"" \
  "1"

wait_for_exact_value \
  "clickhouse.events" \
  "compose exec -T clickhouse clickhouse-client --query \"select count() from analytics.events where event_id = '$event_id';\"" \
  "1"

wait_for_exact_value \
  "clickhouse.schema_version" \
  "compose exec -T clickhouse clickhouse-client --query \"select schema_version from analytics.events where event_id = '$event_id' limit 1;\"" \
  "1"

wait_for_exact_value \
  "in_progress_count" \
  "compose exec -T postgres psql -U \${POSTGRES_USER:-bd06} -d \${POSTGRES_DB:-bd06} -t -A -c \"select count(*) from event_processing where status in ('claimed','storage_written','analytics_written');\"" \
  "0"

replay_response="$(curl -fsS -X POST http://localhost:8000/ops/replays \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d "{\"selector_type\":\"event_id\",\"event_id\":\"$event_id\"}")"
replay_job_id="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["replay_job_id"])' <<<"$replay_response")"

wait_for_exact_value \
  "replay_job.status" \
  "compose exec -T postgres psql -U \${POSTGRES_USER:-bd06} -d \${POSTGRES_DB:-bd06} -t -A -c \"select status from replay_jobs where replay_job_id = '$replay_job_id';\"" \
  "completed"

wait_for_exact_value \
  "replay_job_event.status" \
  "compose exec -T postgres psql -U \${POSTGRES_USER:-bd06} -d \${POSTGRES_DB:-bd06} -t -A -c \"select status from replay_job_events where replay_job_id = '$replay_job_id' and event_id = '$event_id';\"" \
  "skipped"

wait_for_exact_value \
  "clickhouse.events.after_replay" \
  "compose exec -T clickhouse clickhouse-client --query \"select count() from analytics.events where event_id = '$event_id';\"" \
  "1"

curl -fsS http://localhost:8000/ops/telemetry -H "X-API-Key: $API_KEY" >/dev/null
