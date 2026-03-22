---
tags:
  - archive
  - 05-exercises
status: stable
---

# Mini Project: Algorithms Toolkit CLI

## Goal

Build and use a minimal CLI to run core algorithms from this module.

## What you will implement

- A small command router in `03-implementations/python/src/cli.py`.
- JSON-based inputs for algorithm parameters.

## How to run

From `modules/01-algorithms/03-implementations/python/`:

- `python3 -m src.cli fibonacci '{"n": 10}'`
- `python3 -m src.cli knapsack_01 '{"values": [6, 10, 12], "weights": [1, 2, 3], "capacity": 5}'`
- `python3 -m src.cli interval_scheduling '{"intervals": [[1, 3], [2, 4], [3, 5]]}'`
- `python3 -m src.cli dijkstra '{"graph": {"A": [["B", 1], ["C", 4]], "B": [["C", 2]]}, "start": "A"}'`
- `python3 -m src.cli vertex_cover '{"num_vertices": 4, "edges": [[0, 1], [1, 2], [2, 3]]}'`

## Stretch ideas

- Add output formatting as JSON.
- Add algorithm aliases and help output.
- Add a small dataset loader for graph examples.


## Related Concepts

- [Loop Invariants and Algorithm Correctness](../01-concepts/01-loop-invariants-and-algorithm-correctness.md)
- [Recursion and Backtracking](../01-concepts/02-recursion-and-backtracking.md)
- [Divide and Conquer](../01-concepts/03-divide-and-conquer.md)
