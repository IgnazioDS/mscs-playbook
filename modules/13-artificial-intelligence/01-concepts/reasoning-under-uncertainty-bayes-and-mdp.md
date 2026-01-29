# Reasoning Under Uncertainty: Bayes and MDP

## Overview
Uncertainty arises from noisy observations and stochastic dynamics; probabilistic
models and MDPs formalize decision-making under uncertainty.

## Why it matters
Many real systems require reasoning about probabilities and expected outcomes.

## Key ideas
- Bayes rule updates beliefs with new evidence
- MDPs model states, actions, transitions, and rewards
- Value functions guide optimal policies
- Bellman equations define recursive optimization

## Practical workflow
- Define random variables and prior distributions
- Update beliefs with Bayes rule and likelihoods
- Model decision problems as MDPs
- Solve with value iteration or policy iteration

## Failure modes
- Poor priors skew inference
- State spaces too large for exact MDP solutions
- Incorrect transition probabilities
- Ignoring uncertainty in observations

## Checklist
- Validate probabilistic assumptions with data
- Use approximate methods for large state spaces
- Track expected value and variance
- Monitor policy performance across scenarios

## References
- Bayes rule — https://en.wikipedia.org/wiki/Bayes%27_theorem
- MDP overview — https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/lecture-notes/mdps.pdf
