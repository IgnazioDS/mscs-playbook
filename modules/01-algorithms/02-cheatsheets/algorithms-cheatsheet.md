
# Algorithms Cheat Sheet

## Complexity Quick-Reference

### Core graph and optimization algorithms

| Problem | Algorithm | Time | Space | Key condition |
|---|---|---:|---:|---|
| Reachability / traversal | BFS | `O(V + E)` | `O(V)` | graph stored as adjacency list |
| Reachability / traversal | DFS | `O(V + E)` | `O(V)` | recursion depth may matter |
| Unweighted shortest path | BFS | `O(V + E)` | `O(V)` | all edges effectively equal weight |
| Weighted shortest path | Dijkstra | `O((V + E) log V)` | `O(V)` | all edge weights nonnegative |
| Shortest path with negative edges | Bellman-Ford | `O(VE)` | `O(V)` | handles negative edges; detects negative cycles |
| Minimum spanning tree | Kruskal | `O(E log E)` | `O(V)` | undirected weighted graph |
| Minimum spanning tree | Prim | `O((V + E) log V)` | `O(V)` | undirected weighted graph |
| DAG ordering | Topological sort | `O(V + E)` | `O(V)` | graph must be acyclic |
| Range sum with updates | Segment tree | `O(log n)` | `O(n)` | point updates + interval queries |
| Maximum flow | Edmonds-Karp | `O(VE^2)` | `O(V + E)` | directed capacitated graph |
| Vertex cover approximation | edge-pair 2-approx | polynomial | `O(V + E)` typical | minimization guarantee factor `2` |

### Core dynamic programming patterns

| Pattern | Typical state shape | Time template | Space template | Notes |
|---|---|---:|---:|---|
| 1D sequence DP | `dp[i]` | `states × transitions` | `O(n)` or `O(1)` compressed | Fibonacci, simple recurrences |
| 2D prefix / sequence DP | `dp[i][j]` | often `O(nm)` | `O(nm)` or row-compressed | LCS, edit distance |
| Knapsack-style DP | `dp[i][w]` or `dp[w]` | often `O(nW)` | `O(nW)` or `O(W)` | watch iteration order |
| DAG DP | value per vertex | `O(V + E)` after topological order | `O(V)` | depends on DAG ordering |
| Reconstruction-enabled DP | value + parent/choice | base DP cost + pointer storage | higher than value-only DP | needed for actual solution output |

### Core asymptotic classes

| Class | Typical pattern |
|---|---|
| `O(1)` | direct table lookup, array index access |
| `O(log n)` | heap operation, balanced BST query, binary search |
| `O(n)` | single scan, one-pass DP |
| `O(n log n)` | sort + scan, heap-based graph algorithms |
| `O(n^2)` | pairwise DP, dense graph processing |
| `O(V + E)` | graph traversal on adjacency lists |
| `O(VE)` | repeated edge relaxation |

## Decision Tree

### Which algorithmic pattern should you try?

```text
Need an optimal answer over overlapping subproblems?
├─ Can the problem be described by a reusable state and recurrence?   → Dynamic programming
└─ No repeated subproblem structure?                                  → Try greedy, graph search, or divide-and-conquer

Need to make one local decision at a time?
├─ Can you prove the local choice is always safe?                     → Greedy algorithm
└─ No proof or easy counterexample appears?                           → Do not trust greedy; consider DP or search

Need shortest paths?
├─ Graph unweighted or all edges same cost?                           → BFS
├─ Graph weighted and all weights nonnegative?                        → Dijkstra
└─ Graph may contain negative edges?                                  → Bellman-Ford

Need to connect all vertices at minimum total edge weight?
└─ Undirected weighted graph?                                         → MST (Kruskal or Prim)

Need repeated merge/find connectivity queries?
└─ Components merge over time?                                        → Union-Find

Need repeated interval / subarray queries with updates?
├─ Point updates + range queries?                                     → Segment tree
└─ Static query-only setting?                                         → consider prefix sums / sparse table / offline preprocessing

Need a near-optimal solution because exact optimization is too slow?
└─ NP-hard optimization problem with provable bound needed?           → Approximation algorithm
```

## Compact Glossary

- **State** — minimal information needed to define a DP subproblem.
- **Recurrence** — formula expressing one state in terms of smaller states.
- **Memoization** — top-down recursion with caching.
- **Tabulation** — bottom-up DP evaluation order.
- **Greedy-choice property** — existence of an optimal solution that begins with the greedy choice.
- **Exchange argument** — proof that swaps a greedy choice into an optimal solution without harm.
- **Stays-ahead argument** — proof that greedy is never behind a competitor under the relevant progress measure.
- **Relaxation** — shortest-path update that improves a tentative distance.
- **Cut property** — MST principle that identifies safe edges.
- **Union-Find** — data structure for repeated set representative and merge operations.
- **Amortised complexity** — average cost per operation over a whole sequence.
- **Approximation ratio** — worst-case bound relative to the optimal solution.
- **Feasible solution** — solution satisfying all constraints.
- **Topological order** — linear order of DAG vertices respecting edge directions.
- **Adjacency list** — graph representation storing neighbors per vertex.
- **Adjacency matrix** — `V x V` edge-presence representation.
- **Search tree** — tree of recursive or branching choices explored by an exact search method.
- **Reduction** — polynomial-time transformation that transfers solvability or hardness between problems.
- **Residual graph** — graph of remaining augmenting capacity in a flow network.

## Key Formulas / Index Formulas

### Dynamic programming

```text
time ≈ number of states × transitions per state
```

Fibonacci example:

```text
F(0) = 0
F(1) = 1
F(n) = F(n - 1) + F(n - 2)
```

### Shortest paths and MST

```text
if dist[u] + w(u, v) < dist[v]:
    dist[v] = dist[u] + w(u, v)
```

### Approximation ratios

For minimization:

```text
cost(alg) <= r * OPT
```

For maximization:

```text
value(alg) >= OPT / r
```

### Union-Find intuition

```text
find(x)   -- representative lookup
union(x,y) -- merge sets
```

With path compression + union by rank/size:

```text
amortised cost = O(alpha(n))
```

### Hardness transfer pattern

```text
if A reduces to B in polynomial time and A is hard,
then B is at least as hard as A
```

## Debugging / Diagnosis

| Symptom | Likely cause |
|---|---|
| DP is still exponential | recursion written without memoization, or state space recomputed under different aliases |
| DP table contains impossible values or zeros in the wrong places | base cases wrong or evaluation order violates dependencies |
| Greedy algorithm works on samples but fails on a small custom case | local rule lacks proof; wrong greedy key or missing feasibility check |
| BFS returns the wrong “shortest” path cost | graph has weighted edges and BFS is counting edges, not total weight |
| Dijkstra returns inconsistent distances | negative edge present or stale-priority handling is wrong |
| MST includes a cycle | Union-Find or cycle check is broken |
| Segment tree query fails near boundaries | interval convention mixed (inclusive vs half-open) |
| Approximation analysis sounds persuasive but has no inequality chain | heuristic presented as approximation without a proof |
| Backtracking blows up immediately | pruning is weak or the search tree was underestimated |
| Hardness claim sounds hand-wavy | reduction direction or decision formulation is missing |

## When NOT to Use

| Tool / Pattern | Avoid when |
|---|---|
| Dynamic programming | the problem has no reusable state structure or subproblems do not overlap |
| Top-down DP | recursion depth may exceed safe stack limits and a clean bottom-up order exists |
| Bottom-up DP | only a tiny reachable fraction of the state space matters and memoization is much simpler |
| Greedy algorithm | you cannot prove the local choice is safe or easy counterexamples appear |
| BFS | edge weights are unequal |
| Dijkstra | any negative edge may appear |
| Topological sort | the graph may contain cycles |
| Kruskal / Prim for MST | the graph problem is directed without a redefined objective |
| Union-Find | you need deletions, splits, or general ordered queries |
| Segment tree | there are no updates and a simpler static structure suffices |
| Approximation algorithm | exact polynomial-time solution already exists and quality loss is unnecessary |
| Backtracking | the problem has overlapping subproblems that a DP can exploit |
| NP-hardness rhetoric | you have not yet checked for special-case structure or approximation |

## References

- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Kleinberg, Jon, and Eva Tardos. 2021. *Algorithm Design*. Pearson. <https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003259/9780137546350>
- Tarjan, Robert E. 1975. Efficiency of a Good But Not Linear Set Union Algorithm. *Journal of the ACM* 22(2): 215–225. <https://doi.org/10.1145/321879.321884>
- Williamson, David P., and David B. Shmoys. 2011. *The Design of Approximation Algorithms*. Cambridge University Press. <https://www.designofapproxalgs.com/>
- Pat Morin. 2013. *Open Data Structures*. AU Press. <https://opendatastructures.org/>
- Erickson, Jeff. 2019. *Algorithms*. <https://jeffe.cs.illinois.edu/teaching/algorithms/>
- Garey, Michael R., and David S. Johnson. 1979. *Computers and Intractability*. W. H. Freeman. <https://archive.org/details/computersintract0000gare>
