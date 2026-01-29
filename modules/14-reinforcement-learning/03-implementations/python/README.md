# Python Implementations

Offline RL toolkit covering tabular DP, MC, TD, bandits, function approximation,
and evaluation utilities.

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r modules/14-reinforcement-learning/03-implementations/python/requirements.txt
python -m pytest -q modules/14-reinforcement-learning/03-implementations/python/tests
```

## Usage snippets

### Value iteration on gridworld
```python
from src.rl.envs.gridworld import Gridworld
from src.rl.dp.value_iteration import value_iteration

env = Gridworld(width=3, height=3, terminal_states={(2, 2): 0.0}, step_cost=-1.0, start_state=(0, 0))
V, policy = value_iteration(env, gamma=1.0)
```

### Q-learning training loop
```python
from src.rl.envs.gridworld import Gridworld
from src.rl.td.q_learning import q_learning

env = Gridworld(width=3, height=3, terminal_states={(2, 2): 0.0}, step_cost=-1.0, start_state=(0, 0))
Q = q_learning(env, episodes=200, alpha=0.5, gamma=1.0, epsilon=0.1, seed=0)
```

### Bandit comparison
```python
from src.rl.envs.bandit import BernoulliBandit
from src.rl.bandits.epsilon_greedy import run_epsilon_greedy

bandit = BernoulliBandit([0.2, 0.8], seed=0)
result = run_epsilon_greedy(bandit, steps=200, epsilon=0.1, seed=0)
```

### Linear value approximation
```python
from src.rl.envs.chain import ChainEnv
from src.rl.fa.features import chain_features
from src.rl.fa.linear_value import td0_linear

env = ChainEnv(length=5, start=2, reward_right=1.0)
w = td0_linear(env, lambda s: chain_features(s, env.length), alpha=0.1, gamma=1.0, episodes=50, seed=0)
```

## Reproducibility
- Deterministic environments and seeded RNGs.
- Fixed seeds in tests for stable learning curves.

## Mini-project CLI
Run from the repo root:
```bash
python modules/14-reinforcement-learning/03-implementations/python/src/rl/mini_project/cli.py gridworld-control --seed 42
python modules/14-reinforcement-learning/03-implementations/python/src/rl/mini_project/cli.py bandit-compare --seed 42
python modules/14-reinforcement-learning/03-implementations/python/src/rl/mini_project/cli.py reward-shaping --seed 42
python modules/14-reinforcement-learning/03-implementations/python/src/rl/mini_project/cli.py evaluate
```

Example outputs (short):
```
task: gridworld-control
final_avg_return: -15.000
success_rate: 1.000
```
```
task: bandit-compare
epsilon_greedy: total_reward=..., regret=..., best_pick_rate=...
```
```
task: reward-shaping
baseline_final_avg_return: ...
shaped_final_avg_return: ...
```
