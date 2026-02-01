#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml}"

printf "Starting mini platform...\n"
docker compose -f "$COMPOSE_FILE" up -d

bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/wait-for.sh "$COMPOSE_FILE"

printf "Seeding events...\n"
bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/seed.sh

wait_for_count() {
  local label="$1"
  local cmd="$2"
  local retries=10
  for i in $(seq 1 $retries); do
    count=$(eval "$cmd" 2>/dev/null | tr -d '[:space:]' || echo "")
    if [ -n "$count" ] && [ "$count" != "0" ]; then
      echo "$label: $count"
      return 0
    fi
    sleep 1
  done
  echo "$label: 0"
  return 0
}

printf "\nKafka topics:\n"
docker compose -f "$COMPOSE_FILE" exec -T redpanda rpk topic list || true

printf "\nPostgres ingest_log count:\n"
docker compose -f "$COMPOSE_FILE" exec -T postgres psql -U ${POSTGRES_USER:-bd06} -d ${POSTGRES_DB:-bd06} \
  -c "select count(*) from ingest_log;"

printf "\nPostgres processed_events count:\n"
wait_for_count "processed_events" \
  "docker compose -f $COMPOSE_FILE exec -T postgres psql -U ${POSTGRES_USER:-bd06} -d ${POSTGRES_DB:-bd06} -t -A -c \"select count(*) from processed_events;\""

printf "\nMinIO objects (raw):\n"
docker compose -f "$COMPOSE_FILE" exec -T minio sh -c "ls -1 /data | head -n 5"

printf "\nClickHouse analytics rows:\n"
docker compose -f "$COMPOSE_FILE" exec -T clickhouse clickhouse-client --multiquery --query "\
CREATE DATABASE IF NOT EXISTS analytics;\
CREATE TABLE IF NOT EXISTS analytics.events (\
  event_date Date,\
  event_time DateTime,\
  received_at DateTime,\
  event_id String,\
  event_type String,\
  payload String\
) ENGINE = MergeTree\
 PARTITION BY event_date\
 ORDER BY (event_date, event_type, event_id)\
;\
SELECT count(*) FROM analytics.events;"
wait_for_count "analytics.events" \
  "docker compose -f $COMPOSE_FILE exec -T clickhouse clickhouse-client --query \"select count(*) from analytics.events;\""
