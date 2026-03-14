#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${1:-modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-}"

compose() {
  if [[ -n "$ENV_FILE" ]]; then
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" "$@"
  else
    docker compose -f "$COMPOSE_FILE" "$@"
  fi
}

wait_for_cmd() {
  local name="$1"
  local cmd="$2"
  local retries=30

  for _i in $(seq 1 $retries); do
    if eval "$cmd" >/dev/null 2>&1; then
      echo "ready: $name"
      return 0
    fi
    sleep 2
  done

  echo "timeout waiting for $name"
  return 1
}

wait_for_cmd "redpanda" "compose exec -T redpanda rpk cluster health"
wait_for_cmd "postgres" "compose exec -T postgres pg_isready -U ${POSTGRES_USER:-bd06}"
wait_for_cmd "minio" "compose exec -T minio mc ls /data"
wait_for_cmd "clickhouse" "compose exec -T clickhouse wget -q -O - http://localhost:8123/ping"
wait_for_cmd "ingest-api health" "python3 -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()\""
wait_for_cmd "ingest-api ready" "python3 -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000/ready').read()\""
