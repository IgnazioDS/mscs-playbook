# Algorithms Cheat Sheet

## DP patterns and checklist

- Identify state, transitions, base cases, and goal state.
- Check optimal substructure and overlapping subproblems.
- Choose top-down memo or bottom-up table.
- Consider state compression if only previous layer is needed.
- Track choices if you need reconstruction.

## Greedy proof patterns

- Exchange argument: swap a non-greedy choice with greedy without harm.
- Stays-ahead: greedy partial solution is never worse than optimal.
- Cut property: local choice is safe for global optimality.

## Graph algorithm selection

| Goal | Use | Notes |
| --- | --- | --- |
| Reachability / components | BFS / DFS | O(V + E) |
| Unweighted shortest path | BFS | O(V + E) |
| Shortest path (nonnegative) | Dijkstra | O((V + E) log V) |
| Shortest path (negative edges) | Bellman-Ford | O(VE) |
| Minimum spanning tree | Kruskal / Prim | Kruskal uses union-find |
| DAG ordering | Topological sort | Detect cycles |

## Common time complexities

- O(1): hash lookup, array access
- O(log n): balanced BST, heap ops
- O(n): linear scan
- O(n log n): sorting, heap-based algorithms
- O(n^2): DP over pairs, dense graph ops

## When approximations are used

- Problem is NP-hard and exact solutions are too slow.
- Need bounded-quality answers quickly.
- Input size is large and near-optimal is acceptable.
