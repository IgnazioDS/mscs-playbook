# Network Flow Basics

## Key Ideas

- A flow network models how a conserved quantity moves through directed edges with capacities.
- Residual graphs encode what additional flow can be pushed or canceled, which makes them the working state of max-flow algorithms.
- The max-flow problem is not only about routing; it is a reduction framework for cuts, bipartite matching, scheduling, and resource allocation.
- The max-flow min-cut theorem explains why a locally updated augmenting-path process can certify a globally optimal answer.
- Correct flow implementations depend on capacity constraints, skew symmetry in residual updates, and careful path reconstruction.

## 1. What It Is

A **flow network** is a directed graph with:

- a **source** `s`,
- a **sink** `t`,
- and a nonnegative capacity `c(u, v)` on each directed edge.

A **flow** assigns a value `f(u, v)` to each edge such that:

- `0 <= f(u, v) <= c(u, v)` for every edge,
- and for every vertex other than `s` and `t`, incoming flow equals outgoing flow.

The goal of **maximum flow** is to maximize the total amount sent from `s` to `t`.

This model matters because many problems become easier once rewritten as flow: transportation, bandwidth allocation, bipartite matching, feasible circulation, and cut-based partitioning.

## 2. Residual Graphs and Optimality

### 2.1 Residual capacity

If an edge currently carries flow `f(u, v)`, then the additional forward flow still possible is:

```text
c_f(u, v) = c(u, v) - f(u, v)
```

There is also a backward residual edge with capacity `f(u, v)`, which means we can cancel previously sent flow if that helps produce a better solution.

### 2.2 Augmenting paths

An **augmenting path** is a path from `s` to `t` in the residual graph whose every edge has positive residual capacity. Sending the bottleneck amount along that path strictly increases the total flow.

### 2.3 Max-flow min-cut theorem

An `s-t` **cut** partitions the vertices into `S` and `T` with `s in S` and `t in T`. Its capacity is the total capacity of edges from `S` to `T`.

The max-flow min-cut theorem states:

```text
maximum flow value = minimum cut capacity
```

This theorem is why finding a cut with capacity equal to the current flow certifies optimality.

## 3. Algorithms and Complexity

### 3.1 Ford-Fulkerson and Edmonds-Karp

The Ford-Fulkerson method repeatedly finds augmenting paths. Its runtime depends on how those paths are chosen.

**Edmonds-Karp** chooses shortest augmenting paths in number of edges using BFS.

- Time: `O(VE^2)` worst case.
- Space: `O(V + E)` beyond the stored residual graph.

### 3.2 Why the residual graph is the real state

A common misunderstanding is to view the current flow assignment as the complete state. In practice, the residual graph is what determines what can happen next. Every update changes both forward and backward residual capacities.

## 4. Worked Example

Consider the network:

```text
s -> a capacity 3
s -> b capacity 2
a -> b capacity 1
a -> t capacity 2
b -> t capacity 3
```

Start with zero flow on every edge.

### 4.1 First augmenting path

Choose path:

```text
s -> a -> t
```

Bottleneck:

```text
min(3, 2) = 2
```

Send `2` units.

Current flow value: `2`.

Residual capacities now include:

```text
s -> a: 1
 a -> s: 2
 a -> t: 0
 t -> a: 2
```

### 4.2 Second augmenting path

Choose path:

```text
s -> b -> t
```

Bottleneck:

```text
min(2, 3) = 2
```

Send `2` units.

Current flow value: `4`.

Residual capacities now include:

```text
s -> b: 0
b -> s: 2
b -> t: 1
t -> b: 2
```

### 4.3 Third augmenting path

Choose path:

```text
s -> a -> b -> t
```

Residual capacities along the path are:

```text
s -> a: 1
a -> b: 1
b -> t: 1
```

Bottleneck = `1`, so send `1` more unit.

Current flow value: `5`.

### 4.4 Certify optimality with a cut

Now both outgoing edges from `s` are saturated:

```text
s -> a carries 3 of 3
s -> b carries 2 of 2
```

Consider cut `S = {s}` and `T = {a, b, t}`. Its capacity is:

```text
c(s, a) + c(s, b) = 3 + 2 = 5
```

The flow value is also `5`, so by max-flow min-cut, the flow is optimal.

Verification: the traced augmentations produce total flow `5`, and the cut of capacity `5` certifies that no larger flow exists.

## 5. Pseudocode Pattern

```text
procedure edmonds_karp(residual_graph, source, sink):
    max_flow = 0

    while true:
        parent = bfs_augmenting_path(residual_graph, source, sink)
        if sink not reachable from source using parent:
            return max_flow

        bottleneck = inf
        v = sink
        while v != source:
            u = parent[v]
            bottleneck = min(bottleneck, residual_capacity(u, v))
            v = u

        v = sink
        while v != source:
            u = parent[v]
            decrease_residual_capacity(u, v, bottleneck)
            increase_residual_capacity(v, u, bottleneck)
            v = u

        max_flow = max_flow + bottleneck
```

Time: `O(VE^2)` worst case. Space: `O(V + E)` beyond the residual graph representation.

Many later problems, including bipartite matching, can be modeled by building an appropriate flow network and running this pattern.

## 6. Common Mistakes

1. **Backward-edge omission.** Updating only forward capacities after augmentation destroys the residual representation and can prevent valid rerouting; always add or increase the reverse residual edge.
2. **Flow-conservation drift.** Changing edge values without checking intermediate vertices conserve flow leads to invalid states; enforce conservation at every augmentation.
3. **Capacity-confusion bugs.** Mixing original capacities with residual capacities causes impossible path choices or incorrect bottlenecks; store and update residual state explicitly.
4. **Optimality-without-cut.** Stopping after a few augmentations without proving no augmenting path remains provides no correctness guarantee; certify maximality through the residual graph or an equal-capacity cut.
5. **Problem-model mismatch.** Forcing arbitrary constraints into a flow model without checking whether conservation and capacities represent the real system leads to incorrect reductions; define the reduction semantics before coding.

## 7. Practical Checklist

- [ ] Define source, sink, and edge capacities explicitly.
- [ ] Build and inspect the residual graph after each augmentation when debugging.
- [ ] Update both forward and backward residual edges on every path.
- [ ] Compute the bottleneck as the minimum residual capacity on the chosen path.
- [ ] Certify the final answer by showing no augmenting path remains or by identifying a cut with equal capacity.
- [ ] Consider a flow reduction when the problem involves assignment, routing, or cut-style separation.

## 8. References

- Ford, L. R., and D. R. Fulkerson. 1956. *Maximal Flow Through a Network*. *Canadian Journal of Mathematics* 8. <https://doi.org/10.4153/CJM-1956-045-5>
- Edmonds, Jack, and Richard M. Karp. 1972. *Theoretical Improvements in Algorithmic Efficiency for Network Flow Problems*. *Journal of the ACM* 19 (2). <https://doi.org/10.1145/321694.321699>
- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Kleinberg, Jon, and Eva Tardos. 2005. *Algorithm Design*. Pearson. <https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003815>
- Ahuja, Ravindra K., Thomas L. Magnanti, and James B. Orlin. 1993. *Network Flows*. Pearson. <https://www.pearson.com/en-us/subject-catalog/p/network-flows/P200000003554>
- MIT OpenCourseWare. 2012. *Advanced Algorithms*. <https://ocw.mit.edu/courses/6-854j-advanced-algorithms-fall-2005/>
