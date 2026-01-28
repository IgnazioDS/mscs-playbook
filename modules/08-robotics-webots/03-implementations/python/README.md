# Robotics Core (Python)

Pure-Python robotics core for kinematics, odometry, mapping, planning, and control.

## Quickstart
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/08-robotics-webots/03-implementations/python/requirements.txt`
- `python -m pytest -q modules/08-robotics-webots/03-implementations/python/tests`

## API index
- `Pose2D`, `normalize_angle`, `transform_point` — `src/robotics/math2d.py`
- `forward_kinematics`, `integrate_pose` — `src/robotics/kinematics.py`
- `DifferentialDriveOdometry` — `src/robotics/odometry.py`
- `moving_average`, `alpha_beta_filter` — `src/robotics/filters.py`
- `OccupancyGrid` — `src/robotics/mapping/occupancy_grid.py`
- `astar` — `src/robotics/planning/grid_astar.py`
- `PurePursuitController` — `src/robotics/control/pure_pursuit.py`

## Modules
- `math2d`: 2D pose math, transforms, angle normalization
- `kinematics`: differential drive kinematics and pose integration
- `odometry`: incremental wheel-based pose updates
- `filters`: moving average and alpha-beta filter
- `mapping/occupancy_grid`: log-odds grid mapping
- `planning/grid_astar`: grid-based A* planner
- `control/pure_pursuit`: simple path tracking controller

## Webots integration (later)
These modules will be wired into Webots controllers in a later branch.
The controller loop will call kinematics/odometry each timestep, update maps,
run A*, and compute control commands.

## Determinism
- All tests use fixed inputs and should be stable across runs.
