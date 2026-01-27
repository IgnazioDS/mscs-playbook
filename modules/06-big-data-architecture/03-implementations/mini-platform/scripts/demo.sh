#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml}"

printf "Starting mini platform...\n"
docker compose -f "$COMPOSE_FILE" up -d

bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/wait-for.sh "$COMPOSE_FILE"

printf "Seeding events...\n"
bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/seed.sh

sleep 3

printf "\nKafka topics:\n"
docker compose -f "$COMPOSE_FILE" exec -T redpanda rpk topic list || true

printf "\nPostgres ingest_log count:\n"
docker compose -f "$COMPOSE_FILE" exec -T postgres psql -U ${POSTGRES_USER:-bd06} -d ${POSTGRES_DB:-bd06} \
  -c "select count(*) from ingest_log;"

printf "\nPostgres processed_events count:\n"
docker compose -f "$COMPOSE_FILE" exec -T postgres psql -U ${POSTGRES_USER:-bd06} -d ${POSTGRES_DB:-bd06} \
  -c "select count(*) from processed_events;"

printf "\nMinIO objects (raw):\n"
docker compose -f "$COMPOSE_FILE" exec -T minio sh -c "find /data -type f | head -n 5"

printf "\nClickHouse analytics rows:\n"
docker compose -f "$COMPOSE_FILE" exec -T clickhouse clickhouse-client \
  --query "select count(*) from analytics.events;"
