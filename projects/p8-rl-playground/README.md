---
summary: Portfolio project for deterministic reinforcement-learning experiments spanning bandits, TD control, and reward shaping.
tags:
  - project
  - portfolio
  - reinforcement-learning
status: stable
format: project-brief
difficulty: advanced
---

# p8-rl-playground

## Purpose
Create a deterministic RL playground baseline for bandits, TD control, and reward-shaping comparisons.

## Scope
- Execute RL mini-project scenarios using fixed seeds.
- Validate scenario outputs and regression checks.
- Provide a baseline for future environment/model expansion.

## Modules Used
- [Reinforcement Learning](../../modules/14-reinforcement-learning/README.md)
- [Autonomous Systems](../../modules/05-autonomous-systems/README.md)
- [Artificial Intelligence](../../modules/13-artificial-intelligence/README.md)

## How to Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/14-reinforcement-learning/03-implementations/python/requirements.txt
python3 modules/14-reinforcement-learning/03-implementations/python/src/rl/mini_project/cli.py gridworld-control --seed 42 --episodes 200
python3 modules/14-reinforcement-learning/03-implementations/python/src/rl/mini_project/cli.py bandit-compare --seed 42 --steps 500
python3 modules/14-reinforcement-learning/03-implementations/python/src/rl/mini_project/cli.py evaluate --seed 42
```

## How to Test
```bash
python3 -m pytest -q modules/14-reinforcement-learning/03-implementations/python/tests
```

## Expected Output
- Scenario commands print deterministic performance summaries.
- Evaluate command returns a passing deterministic check report.
- RL module tests pass.
