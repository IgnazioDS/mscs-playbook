# 08-robotics-webots

## Status
- Docs: complete
- Implementations: planned

## Overview
This module introduces mobile robotics fundamentals and the Webots simulation
workflow, focusing on kinematics, localization, mapping, planning, and control.

## Prerequisites
- Python 3.10+
- Basic linear algebra
- Webots (optional, for later branches)

## Quickstart
- Read the concepts in order
- Use the cheat sheet during implementation
- Future: venv + tests will be added in implementation branches

## Concepts
- [Differential Drive Kinematics](01-concepts/differential-drive-kinematics.md)
- [Odometry and Dead Reckoning](01-concepts/odometry-and-dead-reckoning.md)
- [Sensors, Noise, and Filters](01-concepts/sensors-noise-and-filters.md)
- [Occupancy Grids and Mapping](01-concepts/occupancy-grids-and-mapping.md)
- [Localization Intuition: UKF and Particle Filters](01-concepts/localization-intuition-ukf-particle.md)
- [Trajectory Generation and Controllers](01-concepts/trajectory-generation-and-controllers.md)
- [Path Planning: A* and Dijkstra](01-concepts/path-planning-a-star-dijkstra.md)
- [SLAM Overview and Tradeoffs](01-concepts/slam-overview-and-tradeoffs.md)
- [Webots Workflow and Controller Structure](01-concepts/webots-workflow-and-controller-structure.md)

## Cheat sheet
- [Robotics Cheat Sheet](02-cheatsheets/robotics-cheatsheet.md)

## Case studies
- [Warehouse Navigation](04-case-studies/warehouse-navigation.md)
- [Indoor Mapping](04-case-studies/indoor-mapping.md)
- [Multi-Robot Coordination](04-case-studies/multi-robot-coordination.md)

## Implementations
- [Python Webots suite](03-implementations/python/README.md)

## Webots suite
- [Webots scenarios and controllers](03-implementations/webots/README.md)
