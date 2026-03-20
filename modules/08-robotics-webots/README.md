---
tags:
  - curriculum
  - module
  - robotics-webots
status: stable
format: module-hub
difficulty: intermediate
---

# Robotics with Webots

## Status

- Concepts, cheat sheet, Python core, Webots scaffold, case studies, and exercises are present.
- The concept sequence now follows a numbered robotics reading path from motion fundamentals through SLAM and simulation workflow.
- The Python core and Webots scaffold support reproducible local experiments and scripted demos.

## Overview

This module covers mobile-robotics foundations and the Webots simulation
workflow: differential-drive kinematics, odometry, sensing, filtering,
occupancy-grid mapping, localization, planning, trajectory following, SLAM, and
controller structure. The emphasis is on building a coherent autonomy stack
from motion models to simulation-ready control loops.

## Recommended learning path

1. Start with kinematics, odometry, and sensing so the robot motion and measurement assumptions are explicit.
2. Learn mapping and localization before planning, because the planner depends on state and environment estimates.
3. Move into path planning and trajectory tracking once the state-estimation layer is clear.
4. Finish with SLAM and the Webots workflow so the full simulation stack fits together cleanly.

## Prerequisites

- Python 3.10+
- Basic linear algebra
- Webots installed locally if you want to run the simulator-backed scaffold

## Quickstart

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python3 -m pip install -r modules/08-robotics-webots/03-implementations/python/requirements.txt`
- `python3 -m pytest -q modules/08-robotics-webots/03-implementations/python/tests`
- `bash modules/08-robotics-webots/03-implementations/webots-suite/scripts/verify_no_webots.sh`

## Concepts (reading order)

- [01 Differential Drive Kinematics](01-concepts/01-differential-drive-kinematics.md)
- [02 Odometry and Dead Reckoning](01-concepts/02-odometry-and-dead-reckoning.md)
- [03 Sensors, Noise, and Filters](01-concepts/03-sensors-noise-and-filters.md)
- [04 Occupancy Grids and Mapping](01-concepts/04-occupancy-grids-and-mapping.md)
- [05 Localization Intuition: UKF and Particle Filters](01-concepts/05-localization-intuition-ukf-and-particle-filters.md)
- [06 Path Planning: A* and Dijkstra](01-concepts/06-path-planning-a-star-and-dijkstra.md)
- [07 Trajectory Generation and Controllers](01-concepts/07-trajectory-generation-and-controllers.md)
- [08 SLAM Overview and Tradeoffs](01-concepts/08-slam-overview-and-tradeoffs.md)
- [09 Webots Workflow and Controller Structure](01-concepts/09-webots-workflow-and-controller-structure.md)

## Concept-to-implementation bridge

- Read `01` through `03` before using the kinematics, odometry, and filter utilities in the Python core.
- Read `04` and `05` before working on mapping or localization extensions.
- Read `06` and `07` before running the planning and control demos.
- Read `08` and `09` before wiring more advanced state estimation into the Webots scaffold.

## Cheat sheet

- [Robotics Cheat Sheet](02-cheatsheets/robotics-cheatsheet.md)

## Case studies

- [Warehouse Navigation](04-case-studies/warehouse-navigation.md)
- [Indoor Mapping](04-case-studies/indoor-mapping.md)
- [Multi-Robot Coordination](04-case-studies/multi-robot-coordination.md)

## Implementations

- [Python robotics core](03-implementations/python/README.md)
- [Webots suite scaffold](03-implementations/webots-suite/README.md)

## Mini-project

- [Robotics Mini-Project](05-exercises/robotics-mini-project.md)
