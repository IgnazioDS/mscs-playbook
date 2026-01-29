# Uninformed and Informed Search

## Overview
Search algorithms explore state spaces to find goal states using different
strategies and heuristics.

## Why it matters
Search is a core AI technique for planning, routing, and optimization problems.

## Key ideas
- BFS guarantees shortest path in unweighted graphs
- DFS is memory-efficient but may not find optimal paths
- UCS optimizes cost when step costs vary
- A* uses heuristics to reduce search effort

## Practical workflow
- Define state representation and successor function
- Choose algorithm based on optimality and resources
- Design admissible heuristics for A*
- Track explored states to avoid cycles

## Failure modes
- State explosion for large branching factors
- Non-admissible heuristics break optimality
- Memory blowups in BFS/UCS
- Incorrect goal tests or transitions

## Checklist
- Estimate branching factor and depth
- Use closed sets for graph search
- Validate heuristics against known optimal costs
- Instrument expansions and frontier size

## References
- AIMA Chapter on Search
- A* original paper — https://doi.org/10.1109/TSSC.1968.300136
