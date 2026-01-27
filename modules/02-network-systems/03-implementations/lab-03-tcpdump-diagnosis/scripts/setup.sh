#!/usr/bin/env bash
set -euo pipefail

# Pull images ahead of time for a faster run.
cd "$(dirname "$0")/.."

docker compose pull
