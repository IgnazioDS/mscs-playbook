# Sensors, Noise, and Filters

## Overview
Robotic sensors are noisy and biased. Filters reduce noise and stabilize
estimates for control and mapping.

## Why it matters
Unfiltered sensor noise leads to unstable control and poor localization.

## Key ideas
- Gaussian noise and bias
- Low-pass filters and moving averages
- Kalman filter intuition (prediction + correction)

## Practical workflow
- Characterize sensor noise distribution
- Apply simple filter for smoothing
- Fuse multiple sensors if available

## Failure modes
- Over-smoothing causing lag
- Ignoring bias or drift
- Misaligned sensor frames

## Checklist
- Log raw vs filtered signals
- Tune filter parameters with data
- Validate units and coordinate frames

## References
- Probabilistic Robotics (Thrun et al.) — https://mitpress.mit.edu/9780262201629/
- Webots Sensors Guide — https://cyberbotics.com/doc/guide/sensors
