# Graph Algorithms Toolkit

## What it is
A practical toolkit of traversal and shortest-path algorithms for directed and
undirected graphs.

## Why it matters
Many systems problems reduce to graphs: routing, dependencies, networks, and
flows. Picking the right algorithm saves orders of magnitude in runtime.

## Core idea (intuition)
Represent relationships as vertices and edges, then use traversal or relaxation
strategies to explore structure and compute paths.

## Formal definition
Given a graph G = (V, E), algorithms operate on vertices and edges to compute
reachability, ordering, and shortest or minimum-cost structures.

## Patterns / common techniques
- BFS for unweighted shortest paths
- DFS for reachability, cycle detection, and topological ordering
- Dijkstra for nonnegative weights using relaxations
- Kruskal for MST using union-find

## Complexity notes
- BFS/DFS: O(V + E)
- Dijkstra with heap: O((V + E) log V)
- Kruskal: O(E log E)

## Pitfalls
- Using Dijkstra with negative edges
- Forgetting to detect cycles in DAG assumptions
- Misrepresenting graphs (directed vs undirected)

## References
- Cormen et al., Introduction to Algorithms (Graph chapters)
- Sedgewick, Algorithms (Graph section)
