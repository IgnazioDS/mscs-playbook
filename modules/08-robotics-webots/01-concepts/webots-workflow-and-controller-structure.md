# Webots Workflow and Controller Structure

## Overview
Webots uses a world file, robot model, and controller code that runs each
simulation step with sensor inputs and actuator outputs.

## Why it matters
A consistent controller structure prevents bugs and enables reproducible
experiments.

## Key ideas
- Simulation step loop with fixed dt
- Read sensors, compute control, set actuators
- Log outputs for debugging

## Practical workflow
- Create world and robot model
- Implement controller loop in Python
- Use supervisor tools for debugging

## Failure modes
- Inconsistent dt across controllers
- Uninitialized sensors or actuators
- Overly complex controller loops

## Checklist
- Fixed timestep and consistent units
- Sensors enabled with correct sampling
- Logging for pose and control signals

## References
- Webots User Guide — https://cyberbotics.com/doc/guide/
- Webots Python API — https://cyberbotics.com/doc/reference/python-api
