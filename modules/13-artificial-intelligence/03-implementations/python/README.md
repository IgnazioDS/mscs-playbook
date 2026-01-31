# Python Implementations

Offline AI toolkit covering search, games, CSPs, Bayes nets, and MDP planning.

## Status
- Docs: complete
- Toolkit: complete
- Mini-project: complete

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/13-artificial-intelligence/03-implementations/python/requirements.txt
python3 -m pytest -q modules/13-artificial-intelligence/03-implementations/python/tests
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py route-plan --seed 42
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py schedule --seed 42
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py diagnose --seed 42
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py evaluate --seed 42
```

## API index
- `ai.search` (problems, bfs, dfs, ucs, astar, ida_star)
- `ai.games` (tictactoe, minimax, alphabeta)
- `ai.csp` (csp, heuristics, ac3, backtracking)
- `ai.probability` (bayes_net, inference)
- `ai.mdp` (mdp, value_iteration, policy_eval)
- `ai.mini_project` (route_planning, scheduling, diagnosis, evaluation, reporting)
- `ai13.mini_project` (cli)

## Determinism and limitations
- Toy problems with small state spaces and fixed seeds.
- Exact enumeration for Bayes nets does not scale to large networks.
- Discrete MDPs only; no continuous control or model learning.
- No external solvers or probabilistic graphical model learning.

## Usage snippets

### A* on a grid
```python
from src.ai.search.astar import astar
from src.ai.search.problems import Problem

class Grid(Problem):
    def __init__(self):
        self.grid = ["...", ".#.", "..."]
    def start_state(self):
        return (0, 0)
    def is_goal(self, state):
        return state == (2, 2)
    def neighbors(self, state):
        for dy, dx in [(1,0),(-1,0),(0,1),(0,-1)]:
            ny, nx = state[0]+dy, state[1]+dx
            if 0 <= ny < 3 and 0 <= nx < 3 and self.grid[ny][nx] != "#":
                yield (ny, nx), 1
    def heuristic(self, state):
        return abs(state[0]-2) + abs(state[1]-2)

path, cost, _ = astar(Grid())
```

### Minimax vs alpha-beta
```python
from src.ai.games.tictactoe import GameState
from src.ai.games.minimax import minimax
from src.ai.games.alphabeta import alphabeta

state = GameState(board=("X","X"," ","O","O"," "," "," "," "), player="X")
move_min, _ = minimax(state)
move_ab, _ = alphabeta(state)
```

### CSP solve
```python
from src.ai.csp.csp import CSP
from src.ai.csp.backtracking import backtracking_search

def different(a, aval, b, bval):
    return aval != bval

variables = ["A", "B"]
domains = {"A": [1, 2], "B": [1, 2]}
neighbors = {"A": ["B"], "B": ["A"]}
solution = backtracking_search(CSP(variables, domains, neighbors, different))
```

### Bayes net query
```python
from src.ai.probability.bayes_net import BayesNet, BayesNode
from src.ai.probability.inference import query

net = BayesNet()
net.add_node(BayesNode("C", [], {(): 0.5}))
net.add_node(BayesNode("R", ["C"], {(True,): 0.8, (False,): 0.2}))
result = query(net, "R", {"C": True})
```

### Value iteration
```python
from src.ai.mdp.mdp import MDP
from src.ai.mdp.value_iteration import value_iteration

mdp = MDP(states=["s0"], actions={"s0": ["a"]}, transitions={("s0","a","s0"): 1.0}, rewards={("s0","a","s0"): 1.0})
V, policy = value_iteration(mdp)
```

## Mini-project CLI
Run from the repo root:
```bash
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py route-plan --seed 42
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py schedule --seed 42
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py diagnose --seed 42
python3 modules/13-artificial-intelligence/03-implementations/python/src/ai13/mini_project/cli.py evaluate --seed 42
```
