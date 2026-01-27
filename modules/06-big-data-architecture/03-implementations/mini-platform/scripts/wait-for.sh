#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${1:-modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml}"

wait_for_cmd() {
  local name="$1"
  local cmd="$2"
  local retries=30

  for i in $(seq 1 $retries); do
    if eval "$cmd" >/dev/null 2>&1; then
      echo "ready: $name"
      return 0
    fi
    sleep 2
  done

  echo "timeout waiting for $name"
  return 1
}

wait_for_cmd "redpanda" "docker compose -f $COMPOSE_FILE exec -T redpanda rpk cluster health"
wait_for_cmd "postgres" "docker compose -f $COMPOSE_FILE exec -T postgres pg_isready -U ${POSTGRES_USER:-bd06}"
wait_for_cmd "minio" "curl -fsS http://localhost:9000/minio/health/ready"
wait_for_cmd "clickhouse" "curl -fsS http://localhost:8123/ping"
wait_for_cmd "ingest-api" "curl -fsS http://localhost:8000/health"
