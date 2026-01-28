# Webots Suite (Scaffold)

## What this is
A lightweight scaffold that shows how the pure-Python robotics core plugs into
Webots controllers. It includes a controller skeleton and headless demo mode.

## What this is not
- A fully wired Webots simulation
- Production-ready robot models

## Prerequisites
- Webots installed locally (manual)
- Python venv from repo root

## Integration with the core
The controller imports from:
`modules/08-robotics-webots/03-implementations/python/src`
so you can reuse math, mapping, planning, and control logic.

## Demos
- Odometry demo: forward + rotate updates, prints pose trace
- Mapping demo: simulates lidar ray and updates occupancy grid
- Planning demo: runs A* on a grid and prints path length

## How to run (headless)
- `bash modules/08-robotics-webots/03-implementations/webots-suite/scripts/run_odometry_demo.sh`
- `bash modules/08-robotics-webots/03-implementations/webots-suite/scripts/run_mapping_demo.sh`
- `bash modules/08-robotics-webots/03-implementations/webots-suite/scripts/run_planning_demo.sh`
