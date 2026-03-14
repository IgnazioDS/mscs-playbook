#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml}"
ENV_FILE="${ENV_FILE:-}"

if [[ -n "$ENV_FILE" ]]; then
  docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" down -v
else
  docker compose -f "$COMPOSE_FILE" down -v
fi
