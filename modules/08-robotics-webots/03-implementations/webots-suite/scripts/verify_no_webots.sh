#!/usr/bin/env bash
set -euo pipefail

source .venv/bin/activate
python -m pytest -q modules/08-robotics-webots/03-implementations/python/tests
python modules/08-robotics-webots/03-implementations/webots-suite/controller/controller.py --mode headless --demo odometry
python modules/08-robotics-webots/03-implementations/webots-suite/controller/controller.py --mode headless --demo mapping
python modules/08-robotics-webots/03-implementations/webots-suite/controller/controller.py --mode headless --demo planning
