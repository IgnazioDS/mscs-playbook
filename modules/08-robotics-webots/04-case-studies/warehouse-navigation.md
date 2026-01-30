# Warehouse Navigation

TL;DR: Build a mobile robot navigation stack for warehouse picking, validate in Webots with realistic noise, and ship a safe, repeatable route execution pipeline.

## Overview
- Problem: robots must navigate dynamic aisles and reach pick locations safely.
- Why it matters: missed picks and collisions cause downtime and cost.
- Scope: indoor ground robot with differential drive and lidar.
- Stakeholders: robotics engineering, operations, safety.
- Out of scope: full fleet optimization or human-robot interaction.
- Deliverable: stable navigation stack with repeatable pick routes.
- Success: operators can configure goals without robotics support.
- Constraint: safety review required before any speed increase.

## Requirements and Constraints
### Functional
- Localize robot within a prebuilt map.
- Plan paths around static and dynamic obstacles.
- Execute routes and report arrival with pose confidence.
- Support manual override and emergency stop.

### Non-functional
- SLO: 98% route completion within time budget.
- Latency: control loop at 10 to 20 Hz.
- Cost: compute on embedded CPU without GPU.
- Safety: maintain minimum distance of 0.5 m from obstacles.
- Reliability: recover from brief sensor dropouts.

### Assumptions
- Warehouse layout changes weekly, not hourly.
- Lidar and wheel encoders are primary sensors.
- Floor is mostly planar with mild slopes near loading docks.
- Operators can mark temporary no-go zones during shifts.

## System Design
### Components
- Map server stores occupancy grid and metadata.
- Localization module (particle filter) estimates pose.
- Global planner generates path from start to goal.
- Local planner performs obstacle avoidance.
- Controller executes velocity commands.
- Safety monitor enforces speed and distance limits.

### Data Flow
1) Map server provides occupancy grid and frame transforms.
2) Localization fuses lidar and odometry to estimate pose.
3) Global planner computes route on costmap.
4) Local planner tracks route and avoids obstacles.
5) Controller sends velocity commands to the robot.

### Interfaces
- `POST /navigate` with goal pose and time budget.
- `GET /status` returns pose, confidence, and current state.
- `POST /stop` for emergency halt.

### Data Schemas
- `map_metadata`: map_id, resolution, origin, updated_at.
- `route_plan`: plan_id, path_points, expected_time.
- `run_log`: run_id, start_pose, end_pose, success, collisions.

## Data and Modeling Approach
- Mapping: static occupancy grid with periodic updates.
- Localization: particle filter with lidar scan matching.
- Planning: A* on global grid, DWA for local planning.
- Control: PID velocity control with speed caps.
- Sim-to-real: calibrate wheel radius, lidar noise, and friction.
- Webots validation: inject sensor noise and dynamic obstacles.

## Evaluation Plan
- Metrics: success rate, path length ratio, time-to-goal.
- Safety: minimum distance violations per run.
- Baselines: straight-line planner and no-dynamic-avoidance mode.
- Sim-to-real: compare Webots and real logs for pose drift.
- Acceptance gates:
  - Success rate >= 98% over 200 runs.
  - No collision in 500 runs; near-miss rate < 2%.
  - Median time-to-goal within 1.2x planned.

## Failure Modes and Mitigations
- Localization drift -> increase lidar update rate and resample.
- Dynamic obstacles -> add velocity scaling and local replanning.
- Map staleness -> schedule map refresh and diff updates.
- Controller oscillation -> tune PID and limit acceleration.
- Sim-to-real gap -> use domain randomization in Webots.

## Operational Runbook
### Logging
- Log pose, covariance, control commands, and planner states.
- Store run_id with map_id and parameter versions.

### Metrics
- Success rate, time-to-goal, collision count.
- Localization uncertainty and replanning frequency.

### Tracing
- Trace run_id from planning to control execution.

### Alerts
- Collision detected or minimum distance violation.
- Localization uncertainty > threshold for > 5 seconds.
- Planner failure or repeated replans.

### Rollback
- Keep last stable parameter set and map version.
- Revert to conservative speed profile if incidents rise.

### On-call Checklist
- Inspect map freshness and sensor calibration.
- Review recent runs for repeated failure locations.
- Validate Webots test suite before deploying changes.

## Security, Privacy, and Compliance
- Restrict navigation APIs to authenticated operators.
- Store logs without facility identifiers when shared externally.
- Maintain safety audit logs for incident reviews.

## Iteration Plan
- Add multi-floor map support and elevator integration.
- Use semantic costmaps for aisle priority.
- Integrate fleet-level coordination for shared corridors.
