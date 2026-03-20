---
summary: Portfolio project for validating robotics helpers and Webots-oriented verification workflows from the archive.
tags:
  - project
  - portfolio
  - robotics
status: stable
format: project-brief
difficulty: advanced
---

# p10-webots-robotics-suite

## Purpose
Deliver a robotics suite baseline for kinematics, filtering, planning, and Webots-oriented verification.

## Scope
- Validate non-Webots robotics functionality via Python tests.
- Run Webots-suite scaffold verification script.
- Keep baseline deterministic and runnable on local environments.

## Modules Used
- [Robotics with Webots](../../modules/08-robotics-webots/README.md)
- [Autonomous Systems](../../modules/05-autonomous-systems/README.md)

## How to Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/08-robotics-webots/03-implementations/python/requirements.txt
bash modules/08-robotics-webots/03-implementations/webots-suite/scripts/verify_no_webots.sh
```

## How to Test
```bash
python3 -m pytest -q modules/08-robotics-webots/03-implementations/python/tests
```

## Expected Output
- `verify_no_webots.sh` completes and validates scaffold assumptions.
- Robotics Python tests pass for odometry, kinematics, mapping, and planning helpers.
