# Bellman-Ford and Floyd-Warshall

## Key Ideas

- Bellman-Ford solves the single-source shortest-path problem even when negative edge weights are present, provided no reachable negative cycle makes the answer undefined.
- Floyd-Warshall computes all-pairs shortest paths by dynamic programming over allowed intermediate vertices.
- Edge relaxation is the central primitive in Bellman-Ford, and repeated relaxation works because shortest paths use at most `V - 1` edges when no negative cycle is involved.
- Floyd-Warshall trades higher `Theta(V^3)` worst-case time for conceptual simplicity and dense-graph convenience.
- Negative-cycle detection is not optional; without it, a reported distance can be mathematically meaningless.

## 1. What It Is

Shortest-path problems ask for minimum-weight paths in a weighted graph. Dijkstra's algorithm is efficient when all edge weights are nonnegative, but negative edges require different reasoning.

Bellman-Ford and Floyd-Warshall cover two important settings:

- **Bellman-Ford**: shortest paths from one source to all vertices.
- **Floyd-Warshall**: shortest paths between every ordered pair of vertices.

These algorithms matter because real optimization models can include credits, penalties, or transformed costs that make edge weights negative.

## 2. Bellman-Ford

### 2.1 Core idea

A path with no repeated vertices uses at most `V - 1` edges. Therefore, if we relax every edge `V - 1` times, the true shortest paths will have had enough opportunities to propagate.

An edge `(u, v)` with weight `w(u, v)` is **relaxed** by testing whether:

```text
dist[u] + w(u, v) < dist[v]
```

If so, update `dist[v]`.

### 2.2 Complexity

Bellman-Ford performs `V - 1` rounds over all `E` edges.

- Time: `Theta(VE)` worst case.
- Space: `Theta(V)` for distances and predecessors, beyond the graph representation.

### 2.3 Negative cycles

After the main `V - 1` rounds, one more pass detects reachable negative cycles. If any edge can still relax, no finite shortest-path solution exists for vertices reachable from that cycle.

## 3. Floyd-Warshall

### 3.1 Dynamic-programming view

Let `dist_k[i][j]` be the shortest path from `i` to `j` using only intermediate vertices from the set `{1, ..., k}`. Then:

```text
dist_k[i][j] = min(dist_(k-1)[i][j], dist_(k-1)[i][k] + dist_(k-1)[k][j])
```

This recurrence yields a triple loop over `k`, `i`, and `j`.

### 3.2 Complexity

- Time: `Theta(V^3)` worst case.
- Space: `Theta(V^2)` for the distance matrix, or `Theta(V^2)` with in-place updates.

### 3.3 When it is useful

Floyd-Warshall is especially attractive for dense graphs, transitive-closure-style reasoning, and settings where all-pairs answers are needed repeatedly after one preprocessing pass.

## 4. Worked Example

Run Bellman-Ford from source `s` on the graph with edges:

```text
s -> a weight 4
s -> b weight 5
a -> b weight -2
a -> c weight 4
b -> c weight 3
```

Initialize:

```text
dist[s] = 0
dist[a] = inf
dist[b] = inf
dist[c] = inf
```

### 4.1 First relaxation round

Relax `s -> a`:

```text
dist[a] = min(inf, 0 + 4) = 4
```

Relax `s -> b`:

```text
dist[b] = min(inf, 0 + 5) = 5
```

Relax `a -> b`:

```text
dist[b] = min(5, 4 + (-2)) = 2
```

Relax `a -> c`:

```text
dist[c] = min(inf, 4 + 4) = 8
```

Relax `b -> c`:

```text
dist[c] = min(8, 2 + 3) = 5
```

State after round 1:

```text
dist = {s: 0, a: 4, b: 2, c: 5}
```

### 4.2 Second relaxation round

Relaxing every edge again produces no improvement:

```text
s -> a gives 4
a -> b gives 2
a -> c gives 8
b -> c gives 5
```

So the distances remain unchanged.

### 4.3 Interpretation

The shortest path to `b` is `s -> a -> b` with weight `4 + (-2) = 2`.
The shortest path to `c` is `s -> a -> b -> c` with weight `4 + (-2) + 3 = 5`.

Verification: after one additional pass, no edge relaxes further, so there is no reachable negative cycle and the distances `{a: 4, b: 2, c: 5}` are correct.

## 5. Pseudocode Patterns

```text
procedure bellman_ford(vertices, edges, source):
    for v in vertices:
        dist[v] = inf
        parent[v] = null
    dist[source] = 0

    for round = 1 to length(vertices) - 1:
        changed = false
        for (u, v, w) in edges:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = true
        if not changed:
            break

    for (u, v, w) in edges:
        if dist[u] != inf and dist[u] + w < dist[v]:
            return negative_cycle

    return dist, parent
```

Time: `Theta(VE)` worst case. Space: `Theta(V)` auxiliary beyond the edge list.

```text
procedure floyd_warshall(dist):
    n = number_of_vertices(dist)
    for k = 0 to n - 1:
        for i = 0 to n - 1:
            for j = 0 to n - 1:
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist
```

Time: `Theta(V^3)` worst case. Space: `Theta(V^2)`.

## 6. Common Mistakes

1. **Negative-cycle omission.** Returning Bellman-Ford distances without the final detection pass can report finite answers when no finite optimum exists; always test for one more relaxation.
2. **Dijkstra substitution.** Using Dijkstra on graphs with negative edges can produce incorrect paths even if the graph has no negative cycle; choose Bellman-Ford when negative edges are possible.
3. **Infinity-arithmetic bugs.** Adding weights to an `inf` sentinel without guarding reachability can overflow or corrupt the comparison; check `dist[u] != inf` before relaxing.
4. **All-pairs overkill.** Running Floyd-Warshall when only one source matters wastes time on sparse graphs; match the algorithm to the query pattern.
5. **Path-reconstruction neglect.** Computing only distances when the application needs actual routes forces a second design later; store predecessors or next-hop information when required.

## 7. Practical Checklist

- [ ] Decide whether the task is single-source or all-pairs shortest paths.
- [ ] Check whether negative edge weights are possible before choosing the algorithm.
- [ ] Guard all relaxations against unreachable source vertices.
- [ ] Add negative-cycle detection for Bellman-Ford and diagonal checks for Floyd-Warshall.
- [ ] Store predecessor information if the application needs the path, not just the distance.
- [ ] Prefer adjacency matrices for Floyd-Warshall only when the graph is dense enough to justify them.

## 8. References

- Bellman, Richard. 1958. *On a Routing Problem*. *Quarterly of Applied Mathematics* 16 (1). <https://doi.org/10.1090/qam/102435>
- Ford, L. R. 1956. *Network Flow Theory*. RAND Corporation. <https://www.rand.org/pubs/papers/P923.html>
- Floyd, Robert W. 1962. *Algorithm 97: Shortest Path*. *Communications of the ACM* 5 (6). <https://cacm.acm.org/research/algorithm-97-shortest-path/>
- Warshall, Stephen. 1962. *A Theorem on Boolean Matrices*. *Journal of the ACM* 9 (1). <https://doi.org/10.1145/321105.321107>
- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Kleinberg, Jon, and Eva Tardos. 2005. *Algorithm Design*. Pearson. <https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003815>
