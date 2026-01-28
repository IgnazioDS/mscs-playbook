# Localization Intuition: UKF and Particle Filters

## Overview
Localization estimates robot pose by combining motion models with sensor
measurements. UKF and particle filters are common nonlinear methods.

## Why it matters
Accurate localization is required for mapping, planning, and control.

## Key ideas
- UKF: Gaussian belief with sigma points
- Particle filter: weighted samples of pose
- Measurement updates reduce uncertainty

## Practical workflow
- Define motion and sensor models
- Initialize belief distribution
- Apply predict/update cycle each timestep

## Failure modes
- Poor motion model causing divergence
- Particle depletion (too few particles)
- Overconfidence in noisy sensors

## Checklist
- Validate motion and sensor models
- Track uncertainty growth over time
- Monitor effective particle count

## References
- Probabilistic Robotics (Thrun et al.) — https://mitpress.mit.edu/9780262201629/
- UKF Tutorial — https://www.cse.sc.edu/~terejanu/files/tutorialUKF.pdf
