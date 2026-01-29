# Monte Carlo Methods

## Overview
Monte Carlo methods estimate value functions from sampled episodes without a
model of the environment.

## Why it matters
MC methods are simple baselines for episodic tasks and support off-policy
learning.

## Key ideas
- Returns are computed from complete episodes
- First-visit and every-visit variants
- On-policy MC control uses epsilon-greedy policies
- Off-policy MC uses importance sampling

## Practical workflow
- Generate episodes with a behavior policy
- Compute returns for visited states
- Update value estimates with averages
- Add epsilon-greedy improvement for control

## Failure modes
- High variance due to long episodes
- Inefficiency for continuing tasks
- Poor exploration leads to biased estimates
- Importance sampling instability

## Checklist
- Use enough episodes for stable estimates
- Track variance and confidence intervals
- Compare on-policy vs off-policy performance
- Ensure episode termination conditions are correct

## References
- Sutton & Barto Chapter on MC
- MC control — https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf
