#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python3 -m pip install -r modules/08-robotics-webots/03-implementations/python/requirements.txt
python3 -m pip install -r modules/08-robotics-webots/03-implementations/webots-suite/controller/requirements.txt
