# Differential Drive Kinematics

## Overview
Differential-drive robots use two independently driven wheels to move and turn.
The kinematics relate wheel velocities to linear and angular motion.

## Why it matters
Most mobile robots in simulation and education are differential drive. Correct
kinematics are the basis for control, odometry, and planning.

## Key ideas
- Linear velocity v and angular velocity ω derived from wheel speeds
- Track width and wheel radius determine motion
- Small integration errors accumulate over time

## Practical workflow
- Define wheel radius r and axle length L
- Convert wheel speeds to v, ω
- Integrate pose (x, y, θ) over dt

## Failure modes
- Wrong units (rad/s vs rpm)
- Incorrect axle length
- Large dt causing drift

## Checklist
- Verify units and dimensions
- Test with straight and in-place rotation
- Compare to Webots ground truth

## References
- Probabilistic Robotics (Thrun et al.) — https://mitpress.mit.edu/9780262201629/
- Differential Drive Kinematics — https://www.cs.cmu.edu/~16311/s07/labs/NXJ/Advanced%20Lab%203.html
