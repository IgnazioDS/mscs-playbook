# Occupancy Grids and Mapping

## Overview
Occupancy grids represent space as cells with probabilities of being occupied.
They are a simple and robust mapping approach.

## Why it matters
Grid maps are widely used in navigation and planning pipelines.

## Key ideas
- Discretize space into cells
- Update probabilities with sensor models
- Unknown vs free vs occupied

## Practical workflow
- Define grid resolution and bounds
- Ray-cast sensor updates into grid
- Apply Bayesian update per cell

## Failure modes
- Grid too coarse or too fine
- Sensor model mismatch
- Accumulated drift without localization

## Checklist
- Choose resolution based on robot size
- Validate updates with simple scenes
- Visualize maps regularly

## References
- Probabilistic Robotics (Thrun et al.) — https://mitpress.mit.edu/9780262201629/
- Occupancy Grid Mapping — https://www.cs.cmu.edu/~16311/s07/labs/NXJ/OccupancyGrid.pdf
