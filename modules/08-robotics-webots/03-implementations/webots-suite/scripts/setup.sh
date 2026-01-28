#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install -r modules/08-robotics-webots/03-implementations/python/requirements.txt
pip install -r modules/08-robotics-webots/03-implementations/webots-suite/controller/requirements.txt
