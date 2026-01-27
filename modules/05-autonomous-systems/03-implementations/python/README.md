# Autonomous Systems — Python Implementations

Minimal, deterministic reference implementations for Module 05.

## Setup
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/05-autonomous-systems/03-implementations/python/requirements.txt`

## Tests
- `python -m pytest -q modules/05-autonomous-systems/03-implementations/python/tests`

## Demo
- `python modules/05-autonomous-systems/03-implementations/python/src/demo.py`
- Expected output includes section headers for Example A/B and PASS/FAIL summaries.

## Structure
- `src/lti/`: discrete-time LTI simulation + ZOH discretization
- `src/ts/`: transition systems + BFS reachability
- `src/ta/`: simplified timed automaton + simulator
- `src/ltl/`: LTL AST + finite-trace checker
- `src/verify/`: bounded reachability + invariant checks
- `src/synthesis/`: toy safety policy selector
- `src/utils/`: small utilities
- `tests/`: deterministic unit tests

## Tiny examples

Discrete LTI simulation:
```python
import numpy as np
from src.lti.lti import simulate_discrete

A = np.array([[1.0]])
B = np.array([[1.0]])
x0 = np.array([0.0])
U = np.array([1.0, 1.0, 1.0])
X = simulate_discrete(A, B, x0, U)
print(X.squeeze())  # [0. 1. 2. 3.]
```

Timed automaton simulation:
```python
from src.ta.timed_automaton import TimedAutomaton, Edge
from src.ta.simulate import simulate_ta

ta = TimedAutomaton(
    locations={"safe", "unsafe"},
    initial_location="safe",
    clocks=["x"],
    invariants={"safe": [("x", "<=", 2.0)]},
    edges=[Edge("safe", "unsafe", guard=[("x", ">=", 2.0)], resets=[])],
)
trace = simulate_ta(ta, T=3.0, dt=1.0)
print(trace["locations"])
```

LTL finite-trace checking:
```python
from src.ltl.ast import AP, G, Not
from src.ltl.trace_check import check

trace = [
    {"ok"},
    {"ok"},
    {"ok"},
]
formula = G(Not(AP("bad")))
print(check(formula, trace))  # True
```
