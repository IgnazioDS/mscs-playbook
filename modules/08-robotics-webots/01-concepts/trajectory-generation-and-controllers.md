# Trajectory Generation and Controllers

## Overview
Trajectory generation computes feasible paths over time, while controllers
track those trajectories with feedback.

## Why it matters
Poor trajectories or unstable controllers cause unsafe behavior and drift.

## Key ideas
- Trajectory = position + velocity + time
- Controllers: PID, pure pursuit, MPC
- Constraints on velocity and curvature

## Practical workflow
- Define waypoints and constraints
- Generate time-parameterized trajectory
- Apply controller and log tracking error

## Failure modes
- Overshoot due to high gains
- Trajectories violating dynamics
- Control instability in sharp turns

## Checklist
- Validate trajectories against constraints
- Tune gains with step responses
- Log tracking error and control outputs

## References
- Mobile Robot Control — https://www.coursera.org/learn/mobile-robot
- Webots Controllers — https://cyberbotics.com/doc/guide/controller-programming
