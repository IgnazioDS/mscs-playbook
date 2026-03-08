# Algorithms

## Status
- Concepts, cheat sheet, case study, and mini-project are present.
- Python reference implementations and tests are complete and runnable.

## Overview
This module now focuses on the core algorithms path: correctness, recursion, divide and conquer, sorting and selection, greedy methods, dynamic programming, graph algorithms, range-query structures, flow, string algorithms, matching, randomized methods, approximation, and hardness.

## How to use this module
- Read concepts in order, then scan the cheat sheet.
- Study implementations in `03-implementations/python/src/`.
- Run tests to validate understanding and changes.
- Treat cryptography and quantum computing as follow-on modules rather than prerequisites for the core sequence.

## Quickstart
From the repo root:
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python3 -m pip install -r modules/01-algorithms/03-implementations/python/requirements.txt`
- `python3 -m pytest -q modules/01-algorithms/03-implementations/python/tests`

## Concepts
- [Loop Invariants and Algorithm Correctness](01-concepts/01-loop-invariants-and-algorithm-correctness.md)
- [Recursion and Backtracking](01-concepts/02-recursion-and-backtracking.md)
- [Divide and Conquer](01-concepts/03-divide-and-conquer.md)
- [Sorting and Selection](01-concepts/04-sorting-and-selection.md)
- [Greedy Correctness](01-concepts/05-greedy-correctness.md)
- [DP Fundamentals](01-concepts/06-dp-fundamentals.md)
- [DP State Design Patterns](01-concepts/07-dp-state-design-patterns.md)
- [Data Structures Intro](01-concepts/08-data-structures-intro.md)
- [Graph Algorithms Toolkit](01-concepts/09-graph-algorithms-toolkit.md)
- [Bellman-Ford and Floyd-Warshall](01-concepts/10-bellman-ford-and-floyd-warshall.md)
- [Advanced Data Structures Intro](01-concepts/11-advanced-data-structures-intro.md)
- [Range Query Techniques](01-concepts/12-range-query-techniques.md)
- [Network Flow Basics](01-concepts/13-network-flow-basics.md)
- [Approximation Intro](01-concepts/14-approximation-intro.md)
- [Reductions and Hardness Basics](01-concepts/15-reductions-and-hardness-basics.md)

## Related Follow-On Modules
- [Cryptography and Number Theory](../16-cryptography-and-number-theory/README.md)
- [Quantum Computing](../17-quantum-computing/README.md)

## Cheat sheet
- [Algorithms Cheat Sheet](02-cheatsheets/algorithms-cheatsheet.md)

## Case study
- [Real-World Algorithm Selection](04-case-studies/real-world-algorithm-selection.md)

## Mini-project
- [Algorithms Toolkit CLI](05-exercises/mini-project-algorithms-toolkit.md)

## Tests
From the repo root:
`pytest -q modules/01-algorithms/03-implementations/python/tests`

## Code Walkthroughs and Audit
- [Code Audit Report](06-notes/code-audit.md)
- [Worked Examples](06-notes/worked-examples.md)

## Learning Outcomes
- Identify appropriate algorithm families for real problems.
- Implement core algorithms and data structures with tests.
- Analyze time and space tradeoffs, including hardness-driven design choices.
