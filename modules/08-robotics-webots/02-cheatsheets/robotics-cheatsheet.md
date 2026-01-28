# Robotics Cheat Sheet

## Kinematics and odometry (compact)
- Differential drive:
  - v = r/2 * (ω_r + ω_l)
  - ω = r/L * (ω_r - ω_l)
- Pose update:
  - x_{t+1} = x_t + v * cos(θ) * dt
  - y_{t+1} = y_t + v * sin(θ) * dt
  - θ_{t+1} = θ_t + ω * dt

## Coordinate frames
- World frame: global map
- Robot frame: base_link
- Sensor frame: per sensor, with known transform
- Keep transforms explicit and documented

## Mapping/localization/planning checklist
- Calibrate sensors and noise
- Verify odometry drift rate
- Validate map resolution and bounds
- Use admissible heuristic for A*

## Tuning knobs
- dt (simulation step size)
- noise parameters (sensor + motion)
- inflation radius (planner)
- controller gains (PID)

## Debugging commands + what to log
- Log: pose, wheel speeds, sensor readings, control outputs
- Plot: tracking error, path length, collision count
- Snapshot: map state and localization error
