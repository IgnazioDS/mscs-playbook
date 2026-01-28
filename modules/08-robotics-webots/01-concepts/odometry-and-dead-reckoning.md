# Odometry and Dead Reckoning

## Overview
Odometry estimates robot pose by integrating wheel encoder data over time.
Dead reckoning accumulates motion estimates without external corrections.

## Why it matters
Odometry is the baseline for localization and mapping, but errors grow quickly.

## Key ideas
- Pose update via integrated v and ω
- Systematic errors (wheel slip, calibration)
- Random errors (sensor noise)

## Practical workflow
- Compute wheel displacements per dt
- Update pose using differential drive model
- Compare against landmarks or ground truth

## Failure modes
- Drift from unmodeled slip
- Encoder overflow or quantization errors
- Using stale dt

## Checklist
- Validate with straight-line test
- Calibrate wheel radius and axle length
- Log encoder values and pose

## References
- Probabilistic Robotics (Thrun et al.) — https://mitpress.mit.edu/9780262201629/
- Webots Odometry Example — https://cyberbotics.com/doc/guide/odometry
