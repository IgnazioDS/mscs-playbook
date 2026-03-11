# Value Function Approximation

## Overview
Function approximation generalizes value estimates across large or continuous
state spaces using parametric models.

## Why it matters
Most real-world RL tasks require approximation to scale beyond tabular methods.

## Key ideas
- Linear function approximation is stable and interpretable
- Nonlinear approximators (NNs) enable richer policies
- Bootstrapping can diverge with approximation
- Target networks and replay reduce instability

## Practical workflow
- Choose features or representation learning strategy
- Use stable optimizers and small learning rates
- Monitor value estimates and gradient norms
- Evaluate generalization on unseen states

## Failure modes
- Divergence due to off-policy learning
- Overfitting to narrow state distributions
- Unstable training with large step sizes
- Poor feature scaling or normalization

## Checklist
- Validate with small-scale tabular baselines
- Use fixed seeds and logging for reproducibility
- Track loss curves and value ranges
- Add regularization and early stopping

## References
- Sutton & Barto Chapter on Function Approximation
- DQN — https://www.nature.com/articles/nature14236
