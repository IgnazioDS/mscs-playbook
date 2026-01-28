#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate
python modules/08-robotics-webots/03-implementations/webots-suite/controller/controller.py --mode headless --demo mapping
