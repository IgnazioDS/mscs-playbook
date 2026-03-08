

# Graph Algorithms Toolkit

## Key Ideas

- Graph algorithms are defined as much by graph properties as by algorithm logic: edge weights, directionality, cycles, and connectivity determine which methods are valid.
- Breadth-first search solves shortest-path problems only when every edge has equal weight, while Dijkstra’s algorithm requires all edge weights to be nonnegative.
- Depth-first search is a traversal framework rather than a single-purpose algorithm; its entry and exit structure supports cycle detection, topological sorting, and connected-component analysis.
- Minimum spanning tree algorithms such as Kruskal’s rely on a cut property and a supporting data structure such as Union-Find to remain efficient.
- Choosing the wrong graph representation or the wrong algorithmic precondition can produce results that are not just slow, but incorrect.

## 1. What It Is

Graph algorithms solve problems on structures made of **vertices** and **edges**. They are used to model networks, dependencies, state transitions, routes, workflows, and relationships between entities.

A graph may be:

- **directed** or **undirected**,
- **weighted** or **unweighted**,
- **cyclic** or **acyclic**,
- **connected** or split into multiple components.

The algorithm you should use depends heavily on these properties. A method that is optimal for one graph type may be invalid for another.

### 1.1 Core Definitions

- A **graph** is a pair `G = (V, E)` where `V` is a set of vertices and `E` is a set of edges.
- A **directed graph** has ordered edges `(u, v)`.
- An **undirected graph** has unordered edges `{u, v}`.
- A **path** is a sequence of vertices connected by edges.
- A **cycle** is a path that starts and ends at the same vertex.
- A **connected component** is a maximal set of vertices connected by paths in an undirected graph.
- A **shortest path** is a path of minimum total cost from a source to a target.
- A **minimum spanning tree (MST)** is a minimum-weight set of edges that connects all vertices in a connected undirected weighted graph without cycles.

### 1.2 Why This Matters

Many systems problems reduce naturally to graphs. Package managers depend on directed acyclic dependency graphs. Network routing uses shortest-path methods. Task scheduling often relies on topological order. Cluster connectivity and image segmentation often use connected components or spanning trees.

Graph algorithms are especially sensitive to preconditions. Using BFS on weighted edges, Dijkstra on negative edges, or topological sort on a cyclic graph produces incorrect answers even if the code runs without crashing.

## 2. Core Traversal Algorithms

### 2.1 Breadth-First Search (BFS)

BFS explores vertices in increasing order of distance from a source in an **unweighted** graph, or equivalently in a graph where every edge has the same cost.

Core properties:

- uses a queue,
- explores one distance layer at a time,
- computes shortest-path distances in number of edges.

For an adjacency-list representation, BFS runs in `O(V + E)` time in all cases because each vertex is enqueued at most once and each edge is inspected at most once.

**Use BFS when:** you need reachability or shortest paths in an unweighted graph.

### 2.2 Depth-First Search (DFS)

DFS explores one branch as deeply as possible before backtracking.

Core properties:

- uses recursion or an explicit stack,
- reveals tree, back, forward, or cross-edge structure,
- supports cycle detection and topological reasoning.

DFS also runs in `O(V + E)` time in all cases with adjacency lists.

**Use DFS when:** you need reachability, connected components, cycle detection, or a traversal order that captures dependency structure.

### 2.3 Topological Sorting

A topological order is a linear ordering of the vertices of a **directed acyclic graph (DAG)** such that every directed edge `(u, v)` places `u` before `v`.

This exists if and only if the directed graph is acyclic.

A DFS-based approach obtains a topological order by pushing vertices after exploring all outgoing edges, then reversing that finishing order.

**Use it when:** tasks have dependencies and no cycles are allowed.

## 3. Shortest Paths and Minimum Spanning Trees

### 3.1 Dijkstra’s Algorithm

Dijkstra’s algorithm computes shortest paths from a source in a graph whose edge weights are all **nonnegative**.

Core idea:

- maintain tentative distances,
- repeatedly extract the unsettled vertex with minimum tentative distance,
- relax its outgoing edges.

With a binary heap and adjacency lists, Dijkstra runs in `O((V + E) log V)` worst-case time.

**Use Dijkstra when:** edge weights are nonnegative and shortest weighted paths are needed.

### 3.2 Why Relaxation Matters

For an edge `(u, v)` with weight `w(u, v)`, relaxation tests whether the path through `u` improves the current best-known distance to `v`:

```text
if dist[u] + w(u, v) < dist[v]:
    dist[v] = dist[u] + w(u, v)
```

This is the central update rule in many shortest-path algorithms.

### 3.3 Kruskal’s Algorithm for MST

Kruskal’s algorithm builds a minimum spanning tree by processing edges in nondecreasing order of weight and adding an edge when it connects two different components.

Core idea:

- sort all edges by weight,
- scan from smallest to largest,
- use Union-Find to reject edges that would create a cycle.

With sorting plus near-constant amortised Union-Find operations, the total time is `O(E log E)` worst case.

**Use Kruskal when:** you need an MST in an undirected weighted graph, especially when the graph is sparse or edge-sorted processing is convenient.

## 4. Graph Representation and Complexity

### 4.1 Adjacency List vs Adjacency Matrix

The graph representation affects both runtime and memory.

| Representation | Space | Edge lookup | Iterate neighbors |
|---|---:|---:|---:|
| Adjacency list | `O(V + E)` | `O(deg(v))` typical | `Theta(deg(v))` |
| Adjacency matrix | `O(V^2)` | `O(1)` | `O(V)` |

Adjacency lists are usually preferred for sparse graphs and for traversal algorithms such as BFS and DFS.

Adjacency matrices are useful when:

- the graph is dense,
- constant-time edge existence checks dominate,
- or matrix-based algorithms are being applied.

### 4.2 Complexity Summary

| Algorithm | Problem type | Time | Space | Key precondition |
|---|---|---:|---:|---|
| BFS | unweighted shortest path / reachability | `O(V + E)` | `O(V)` | edges effectively unweighted |
| DFS | traversal / reachability / cycle structure | `O(V + E)` | `O(V)` | none beyond graph representation |
| Topological sort | DAG ordering | `O(V + E)` | `O(V)` | graph must be acyclic |
| Dijkstra | weighted shortest paths | `O((V + E) log V)` | `O(V)` | all weights nonnegative |
| Kruskal | MST | `O(E log E)` | `O(V)` | graph undirected for MST formulation |

## 5. Worked Example

Consider the directed graph with source `A` and weighted edges:

```text
A -> B (1)
A -> C (4)
B -> C (2)
B -> D (5)
C -> D (1)
```

We compute shortest-path distances from `A` using Dijkstra’s algorithm.

### 5.1 Initialization

Set:

```text
dist[A] = 0
dist[B] = inf
dist[C] = inf
dist[D] = inf
```

Unsettled set initially contains all vertices.

### 5.2 Step-by-Step Relaxation Trace

| Step | Extracted vertex | Distance | Relaxation updates |
|---|---|---:|---|
| 1 | `A` | 0 | `dist[B] = 1`, `dist[C] = 4` |
| 2 | `B` | 1 | `dist[C] = min(4, 1 + 2) = 3`, `dist[D] = 6` |
| 3 | `C` | 3 | `dist[D] = min(6, 3 + 1) = 4` |
| 4 | `D` | 4 | no outgoing improvement |

Final distances:

```text
dist[A] = 0
dist[B] = 1
dist[C] = 3
dist[D] = 4
```

### 5.3 Verify the Shortest Paths

- `A -> B` has cost `1`
- `A -> B -> C` has cost `1 + 2 = 3`, which beats direct edge `A -> C = 4`
- `A -> B -> C -> D` has cost `1 + 2 + 1 = 4`, which beats `A -> B -> D = 6`

Verification: the computed distances are `0, 1, 3, 4`, and each matches the minimum path cost from `A`. All weights are nonnegative, so Dijkstra’s precondition holds. Correct.

## 6. Pseudocode Patterns

### 6.1 BFS

```text
procedure bfs(G, source):
    for each vertex v in G:
        visited[v] = false
        dist[v] = inf
    visited[source] = true
    dist[source] = 0
    Q = empty_queue()
    enqueue(Q, source)
    while Q is not empty:
        u = dequeue(Q)
        for each v in adj[u]:
            if not visited[v]:
                visited[v] = true
                dist[v] = dist[u] + 1
                enqueue(Q, v)
    return dist
```

Time: `O(V + E)` in all cases with adjacency lists. Space: `O(V)`.

### 6.2 DFS

```text
procedure dfs(G, u):
    visited[u] = true
    for each v in adj[u]:
        if not visited[v]:
            dfs(G, v)
```

Time: `O(V + E)` in all cases with adjacency lists. Space: `O(V)` including recursion stack in the worst case.

### 6.3 Dijkstra

```text
procedure dijkstra(G, source):
    for each vertex v in G:
        dist[v] = inf
    dist[source] = 0
    H = min_heap()
    push(H, (0, source))
    while H is not empty:
        (du, u) = pop_min(H)
        if du != dist[u]:
            continue
        for each edge (u, v, w) outgoing from u:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                push(H, (dist[v], v))
    return dist
```

Time: `O((V + E) log V)` worst case with adjacency lists and a binary heap. Space: `O(V)` excluding graph storage.

## 7. Common Mistakes

1. **Weighted-BFS misuse.** Using BFS on a graph with unequal edge weights returns shortest paths in edge count, not minimum total weight.
2. **Negative-edge Dijkstra.** Running Dijkstra on graphs with negative edges breaks its correctness argument because the extracted minimum-distance vertex may later need improvement.
3. **DAG assumption without cycle check.** Applying topological ordering logic to a graph that may contain cycles produces invalid schedules or incomplete traversals.
4. **Directed-undirected mismatch.** Treating a directed graph as undirected, or the reverse, changes reachability and path structure and can completely alter the answer.
5. **Wrong MST problem type.** Asking for a minimum spanning tree on a directed graph without redefining the problem is incorrect; the standard MST formulation is for undirected graphs.

## 8. Practical Checklist

- [ ] Identify whether the graph is directed or undirected before choosing the algorithm.
- [ ] Check whether edges are unweighted, uniformly weighted, nonnegative weighted, or may include negative values.
- [ ] Choose adjacency lists for sparse traversal-heavy workloads unless dense-graph edge lookup dominates.
- [ ] Verify DAG assumptions explicitly before using topological-order reasoning.
- [ ] For Dijkstra, confirm that every edge weight is nonnegative.
- [ ] For Kruskal, ensure Union-Find is implemented correctly and edges are sorted by nondecreasing weight.
- [ ] Trace one small graph by hand before trusting the implementation on larger inputs.

## 9. References

- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Kleinberg, Jon, and Eva Tardos. 2021. *Algorithm Design*. Pearson. <https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003259/9780137546350>
- Erickson, Jeff. 2019. *Algorithms*. <https://jeffe.cs.illinois.edu/teaching/algorithms/>
- Sedgewick, Robert, and Kevin Wayne. 2011. *Algorithms* (4th ed.). Addison-Wesley. <https://algs4.cs.princeton.edu/home/>
- Mehlhorn, Kurt, and Peter Sanders. 2008. *Algorithms and Data Structures: The Basic Toolbox*. Springer. <https://doi.org/10.1007/978-3-540-77978-0>
- Pat Morin. 2013. *Open Data Structures*. AU Press. <https://opendatastructures.org/>
