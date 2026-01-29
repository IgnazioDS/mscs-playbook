# Mini-project: RL Toolkit

## Goals
- Compare tabular control algorithms on a small gridworld
- Contrast bandit exploration strategies
- Demonstrate reward shaping effects with deterministic runs

## Commands and expected outputs

### Gridworld control
```bash
python modules/14-reinforcement-learning/03-implementations/python/src/rl/mini_project/cli.py gridworld-control --seed 42
```
Expected output (short):
```
task: gridworld-control
algo: q_learning
final_avg_return: ...
success_rate: ...
```

### Bandit comparison
```bash
python modules/14-reinforcement-learning/03-implementations/python/src/rl/mini_project/cli.py bandit-compare --seed 42
```
Expected output (short):
```
task: bandit-compare
probs: [0.2, 0.8, 0.5]
...
```

### Reward shaping
```bash
python modules/14-reinforcement-learning/03-implementations/python/src/rl/mini_project/cli.py reward-shaping --seed 42
```
Expected output (short):
```
task: reward-shaping
baseline_final_avg_return: ...
shaped_final_avg_return: ...
```

### Evaluation
```bash
python modules/14-reinforcement-learning/03-implementations/python/src/rl/mini_project/cli.py evaluate
```
Expected output (short):
```
task: evaluate
scenarios: 3
passed: 3
failed: 0
```

## How to extend to production
- Use richer environments and simulators for gridworld control
- Add contextual bandits or non-stationary reward models
- Integrate safe RL constraints and offline evaluation

## Pitfalls
- Misconfigured rewards or exploration schedules
- Off-by-one errors in episode handling
- Overfitting to small deterministic environments
