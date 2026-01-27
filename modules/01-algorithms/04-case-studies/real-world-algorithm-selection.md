# Real-World Algorithm Selection

## Scenario 1: Route planning for navigation

**Choice:** Dijkstra (or A* if heuristics are available).

**Why:** Road networks are weighted graphs with nonnegative edge costs. Dijkstra
is correct and efficient with a heap; A* improves speed with good heuristics.

**Tradeoffs:**

- Time: O((V + E) log V) for Dijkstra
- Memory: stores distances and predecessors
- Correctness: exact shortest path with nonnegative weights
- Approximation: A* trades worst-case guarantees for faster typical cases

## Scenario 2: Scheduling jobs on a single machine

**Choice:** Greedy interval scheduling (earliest finish time).

**Why:** The greedy choice yields an optimal maximum set of non-overlapping
intervals with a clean proof by exchange.

**Tradeoffs:**

- Time: O(n log n) due to sorting
- Memory: O(1) beyond storage of intervals
- Correctness: exact optimal solution
- Approximation: not needed for this variant

## Scenario 3: Large-scale similarity search pre-processing

**Choice:** Approximate clustering and indexing (e.g., locality-sensitive hashing
with a greedy candidate selection step).

**Why:** Exact nearest neighbors are costly at scale; approximation reduces
query time with acceptable quality loss for retrieval pipelines.

**Tradeoffs:**

- Time: faster queries with preprocessing cost
- Memory: additional index structures
- Correctness: approximate neighbors, not exact
- Approximation: controlled by hash family and parameters
