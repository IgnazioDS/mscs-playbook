# Mini-project: AI Local Toolkit

## Goals
- Build deterministic CLI workflows for planning, scheduling, and diagnosis
- Demonstrate A* search, CSP solving, and Bayes net inference
- Provide reproducible evaluation checks for regression testing

## Commands and expected outputs

### Route planning
```bash
python modules/13-artificial-intelligence/03-implementations/python/src/ai/mini_project/cli.py route-plan --seed 42
```
Expected output (short):
```
task: route-plan
seed: 42
size: 10
density: 0.18
path_len: ...
cost: ...
```

### Scheduling
```bash
python modules/13-artificial-intelligence/03-implementations/python/src/ai/mini_project/cli.py schedule --seed 42
```
Expected output (short):
```
task: schedule
solved: true
assignments: ...
```

### Diagnosis
```bash
python modules/13-artificial-intelligence/03-implementations/python/src/ai/mini_project/cli.py diagnose --seed 42
```
Expected output (short):
```
task: diagnose
evidence: {'W': True}
query_results:
  P(Rain=1): 0.xxx
```

### Deterministic evaluation
```bash
python modules/13-artificial-intelligence/03-implementations/python/src/ai/mini_project/cli.py evaluate
```
Expected output (short):
```
task: evaluate
scenarios: 3
passed: 3
failed: 0
```

## How to extend to production
- Replace grid worlds with real road networks and costs
- Use OR-Tools for larger scheduling CSPs
- Expand Bayes nets to richer PGMs and data-driven CPTs

## Pitfalls
- Heuristic misuse breaks A* optimality
- Constraint modeling errors hide infeasibility
- Probability assumptions and CPT drift
