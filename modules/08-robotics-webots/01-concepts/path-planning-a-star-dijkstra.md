# Path Planning: A* and Dijkstra

## Overview
Graph-based planning methods compute shortest paths on discretized maps.
Dijkstra is optimal but uninformed; A* uses heuristics for speed.

## Why it matters
Planning efficiency and optimality determine navigation performance.

## Key ideas
- Dijkstra: uniform-cost search
- A*: f = g + h with admissible heuristic
- Grid and graph representations

## Practical workflow
- Convert map to grid or graph
- Choose heuristic (Euclidean/Manhattan)
- Run planner and smooth path if needed

## Failure modes
- Heuristic too aggressive (inadmissible)
- Grid resolution too coarse
- Ignoring dynamic obstacles

## Checklist
- Validate heuristic admissibility
- Test on simple maps first
- Monitor path length vs compute time

## References
- A* Algorithm — https://theory.stanford.edu/~amitp/GameProgramming/
- Introduction to Algorithms (CLRS) — https://mitpress.mit.edu/9780262046305/
