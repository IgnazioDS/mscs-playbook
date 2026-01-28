# SLAM Overview and Tradeoffs

## Overview
SLAM (Simultaneous Localization and Mapping) estimates both the robot pose and
map of the environment at the same time.

## Why it matters
Without SLAM, robots cannot reliably operate in unknown environments.

## Key ideas
- Joint estimation of pose and map
- Loop closure reduces drift
- Tradeoff between accuracy and compute

## Practical workflow
- Choose SLAM approach (EKF, particle, graph-based)
- Configure sensor models and constraints
- Validate with loop closure scenarios

## Failure modes
- Drift without loop closure
- Data association errors
- Excessive compute latency

## Checklist
- Monitor drift and loop closure events
- Log map quality metrics
- Validate against ground truth

## References
- Probabilistic Robotics (Thrun et al.) — https://mitpress.mit.edu/9780262201629/
- Graph SLAM Tutorial — https://www.cs.cmu.edu/~kaess/pub/Kaess11icra.pdf
