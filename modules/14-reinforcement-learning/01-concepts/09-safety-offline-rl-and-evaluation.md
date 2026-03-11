# Safety, Offline RL, and Evaluation

## Overview
Safety and evaluation in RL ensure policies behave reliably, especially when
trained offline or deployed in high-stakes environments.

## Why it matters
Unsafe exploration and distribution shift can cause costly failures.

## Key ideas
- Offline RL learns from logged data without exploration
- Distribution shift leads to extrapolation errors
- Safety constraints limit risky actions
- Evaluation needs multiple seeds and robustness tests

## Practical workflow
- Validate data quality and coverage for offline RL
- Use conservative or constraint-based methods
- Evaluate with held-out trajectories and stress tests
- Monitor deployment with rollback plans

## Failure modes
- Out-of-distribution actions with high Q-values
- Unsafe policies from biased logs
- Overfitting to benchmark environments
- Misleading metrics from single seeds

## Checklist
- Track policy performance under perturbations
- Use conservative Q-learning variants for offline settings
- Evaluate with multiple seeds and confidence intervals
- Establish safety constraints and monitoring

## References
- Offline RL survey — https://arxiv.org/abs/2005.01643
- Safe RL overview — https://arxiv.org/abs/1908.00685
