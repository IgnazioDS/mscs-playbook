#!/usr/bin/env bash
set -euo pipefail

# Stop containers and remove the lab network.
cd "$(dirname "$0")/.."

docker compose down --remove-orphans
