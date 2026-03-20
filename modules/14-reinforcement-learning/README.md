---
tags:
  - curriculum
  - module
  - reinforcement-learning
status: stable
format: module-hub
difficulty: advanced
---

# Reinforcement Learning

This module builds a reinforcement learning reading path from formal task definition to modern policy optimization and deployment-aware evaluation. It is organized around how practitioners usually learn the subject: first understand MDPs and Bellman reasoning, then master tabular prediction and control, then move into approximation, exploration design, and safety.

## Why This Module Matters

Reinforcement learning is the part of machine learning concerned with sequential decision-making under feedback and uncertainty. The same core ideas appear in robotics, recommender systems, game-playing agents, resource allocation, and control systems. A good curriculum must cover not only algorithms, but also task formalization, reward design, and the gap between benchmark success and deployable systems.

## Recommended Reading Path

1. [Reinforcement Learning Problem Formalism and Markov Decision Processes](01-concepts/01-rl-problem-formalism-mdp.md)
2. [Dynamic Programming for Policy Evaluation and Control](01-concepts/02-dynamic-programming-policy-evaluation-and-control.md)
3. [Monte Carlo Methods in Reinforcement Learning](01-concepts/03-monte-carlo-methods.md)
4. [Temporal-Difference Learning](01-concepts/04-temporal-difference-learning.md)
5. [Value Function Approximation](01-concepts/05-value-function-approximation.md)
6. [Policy Gradient and Actor-Critic Methods](01-concepts/06-policy-gradient-and-actor-critic.md)
7. [Exploration, Exploitation, and Bandits](01-concepts/07-exploration-exploitation-and-bandits.md)
8. [Reward Design and Shaping](01-concepts/08-reward-design-and-shaping.md)
9. [Safety, Offline Reinforcement Learning, and Evaluation](01-concepts/09-safety-offline-rl-and-evaluation.md)

## Module Map

- [Concepts](01-concepts/README.md): the main conceptual spine for the module
- [Cheatsheets](02-cheatsheets/README.md): compact formulas and terminology once the concepts are familiar
- [Python Implementations](03-implementations/python/README.md): reference code, environments, and tests
- [TypeScript Implementations](03-implementations/typescript/README.md): lighter implementation notes and extension points
- [Case Studies](04-case-studies/README.md): worked scenarios that connect algorithms to engineering tradeoffs
- [Exercises](05-exercises/README.md): prompts and mini-project material for deliberate practice
- [Notes](06-notes/README.md): extra reading and short supporting material

## Suggested Workflow

1. Read the first four concept pages until Bellman equations, returns, and TD errors are comfortable.
2. Use the Python implementation track to run tabular examples and inspect logged values.
3. Move to approximation and policy methods only after the tabular setting is clear.
4. End with reward design, offline RL, and safety so algorithm choice stays grounded in deployment constraints.

## Prerequisites

- probability and expectation
- linear algebra and basic optimization
- Python familiarity for the implementation track

## Case Studies and Exercises

- [Warehouse Picking with Q-Learning](04-case-studies/warehouse-picking-q-learning.md)
- [Portfolio Allocation with Policy Gradient](04-case-studies/portfolio-allocation-policy-gradient.md)
- [Safe Navigation with Constrained RL](04-case-studies/safe-navigation-constrained-rl.md)
- [RL Mini-Project](05-exercises/rl-mini-project.md)
