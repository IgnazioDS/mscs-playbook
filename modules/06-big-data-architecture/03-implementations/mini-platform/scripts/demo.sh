#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-}"

compose() {
  if [[ -n "$ENV_FILE" ]]; then
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" "$@"
  else
    docker compose -f "$COMPOSE_FILE" "$@"
  fi
}

printf "Starting mini platform...\n"
compose up -d

bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/wait-for.sh "$COMPOSE_FILE"

printf "Seeding events...\n"
bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/seed.sh

wait_for_count() {
  local label="$1"
  local cmd="$2"
  local retries=10
  for _i in $(seq 1 $retries); do
    count=$(eval "$cmd" 2>/dev/null | tr -d '[:space:]' || echo "")
    if [[ -n "$count" && "$count" != "0" ]]; then
      echo "$label: $count"
      return 0
    fi
    sleep 1
  done
  echo "$label: 0"
  return 0
}

printf "\nKafka topics:\n"
compose exec -T redpanda rpk topic list || true

printf "\nPostgres ingest_log count:\n"
compose exec -T postgres psql -U ${POSTGRES_USER:-bd06} -d ${POSTGRES_DB:-bd06} \
  -c "select count(*) from ingest_log;"

printf "\nPostgres event_processing status counts:\n"
compose exec -T postgres psql -U ${POSTGRES_USER:-bd06} -d ${POSTGRES_DB:-bd06} \
  -c "select status, count(*) from event_processing group by status order by status;"

printf "\nMinIO objects (raw):\n"
compose exec -T minio sh -c "find /data -type f | head -n 5"

printf "\nClickHouse analytics rows:\n"
wait_for_count "analytics.events" \
  "compose exec -T clickhouse clickhouse-client --query \"select count(*) from analytics.events;\""
