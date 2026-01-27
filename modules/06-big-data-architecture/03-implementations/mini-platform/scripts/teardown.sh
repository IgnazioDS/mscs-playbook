#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml}"

docker compose -f "$COMPOSE_FILE" down -v
