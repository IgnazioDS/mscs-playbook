# RL Problem Formalism (MDP)

## Overview
Reinforcement learning formalizes decision-making with Markov decision processes
(MDPs) and rewards.

## Why it matters
A clear MDP definition is essential for choosing algorithms and ensuring correct
training signals.

## Key ideas
- MDPs define states, actions, transitions, rewards, and discount factor
- Policies map states to action distributions
- Value functions estimate expected returns
- Optimality depends on the reward structure

## Practical workflow
- Define state and action representations
- Specify transition dynamics or simulators
- Choose reward design and discount factor
- Validate the Markov property assumptions

## Failure modes
- Poor state representation breaks Markov property
- Rewards misaligned with task objectives
- Non-stationary dynamics causing instability
- Sparse rewards slowing learning

## Checklist
- Document S, A, R, P, and gamma explicitly
- Validate rewards against desired behavior
- Test with simple baseline policies
- Monitor returns and episode length

## References
- Sutton & Barto, Reinforcement Learning: An Introduction
- MDP overview — https://web.stanford.edu/class/cs234/lecture1.pdf
