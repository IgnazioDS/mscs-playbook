#!/usr/bin/env bash
set -euo pipefail

# Run the compose stack and exit when the client finishes.
cd "$(dirname "$0")/.."

docker compose up --build --abort-on-container-exit --exit-code-from client
