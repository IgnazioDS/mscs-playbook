---
summary: Portfolio project that packages foundational and algorithms implementations into a deterministic CLI toolkit.
tags:
  - project
  - portfolio
  - algorithms
status: stable
format: project-brief
difficulty: intermediate
---

# p0-algorithms-toolkit

## Purpose
Build a deterministic algorithms toolkit that packages core routines (DP, graph, greedy, approximation) into reproducible CLI workflows.

## Scope
- Reuse and consolidate algorithms from foundational modules into one project-facing toolkit baseline.
- Provide deterministic CLI examples for common tasks (statistics sanity checks + algorithm execution).
- Define a stable output contract for future benchmarking and packaging work.

## Modules Used
- [Foundations](../../modules/00-foundations/README.md)
- [Algorithms](../../modules/01-algorithms/README.md)

## How to Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/00-foundations/03-implementations/python/requirements.txt
python3 -m pip install -r modules/01-algorithms/03-implementations/python/requirements.txt
python3 modules/00-foundations/03-implementations/python/src/foundations/mini_project/cli.py stats --nums "1 2 3 4 5"
python3 modules/01-algorithms/03-implementations/python/src/cli.py fibonacci '{"n": 10}'
```

## How to Test
```bash
python3 -m pytest -q modules/00-foundations/03-implementations/python/tests
python3 -m pytest -q modules/01-algorithms/03-implementations/python/tests
```

## Expected Output
- Foundations command prints a structured stats report (`mean`, `median`, `variance`).
- Algorithms command prints a deterministic numeric result (`55` for `fibonacci n=10`).
- Both test suites pass without failures.
