# Matching Basics

## Key Ideas

- A matching is a set of edges with no shared endpoints, so feasibility depends on vertex conflicts rather than path length or cut capacity.
- Maximal and maximum matchings are different objects; a maximal matching cannot be extended locally, while a maximum matching has the largest possible cardinality.
- Augmenting paths are the central correctness tool because flipping matched and unmatched edges along such a path always increases the matching size by exactly one.
- Bipartite matching connects directly to flow, assignment, and scheduling problems, which is why it appears across systems and optimization work.
- The right algorithm depends on graph class: simple augmenting-path methods are easy to reason about, while Hopcroft-Karp improves worst-case time on large bipartite graphs.

## 1. What It Is

In graph theory, a **matching** is a set of edges such that no two chosen edges share a vertex. Matching problems ask for a large or optimal conflict-free pairing between two sets of objects, such as workers and tasks, students and projects, or requests and servers.

### 1.1 Core Definitions

- A **matching** is a set of pairwise nonincident edges.
- A **matched vertex** is a vertex incident to an edge in the matching.
- An **unmatched vertex** is a vertex not incident to any matching edge.
- A **maximal matching** cannot be extended by adding one more edge.
- A **maximum matching** has largest possible cardinality among all matchings.
- A **perfect matching** matches every vertex in the graph.
- An **augmenting path** is a path that starts and ends at unmatched vertices and alternates between unmatched and matched edges.

### 1.2 Why This Matters

Matching models discrete resource allocation with exclusivity constraints. The same abstraction appears in job assignment, ad serving, switch scheduling, ride matching, and compiler register allocation variants. Understanding why augmenting paths work provides a reusable pattern for more advanced combinatorial optimization.

## 2. Bipartite Matching and Flow

### 2.1 Bipartite Graphs

A **bipartite graph** splits vertices into two disjoint sets `L` and `R`, and every edge goes from `L` to `R`. This structure is common when each side represents a different kind of object, such as applicants on one side and positions on the other.

### 2.2 Flow Reduction

Maximum bipartite matching can be reduced to maximum flow:

1. connect a source to every vertex in `L` with capacity `1`,
2. direct every bipartite edge from `L` to `R` with capacity `1`,
3. connect every vertex in `R` to a sink with capacity `1`.

An integral max flow in this network corresponds to a matching.

### 2.3 Augmenting-Path Principle

If an augmenting path exists, flipping the matched and unmatched status of every edge on that path increases the matching size by exactly `1`.

If no augmenting path exists, the current matching is maximum. This is the core theorem behind augmenting-path algorithms.

## 3. Algorithmic Patterns

### 3.1 Simple DFS/BFS Augmentation

For bipartite graphs, one straightforward method repeatedly searches for an augmenting path and flips it.

- Time: `O(VE)` worst case for a repeated DFS-based implementation.
- Space: `O(V)` auxiliary space beyond the graph and matching state.

This is often enough for moderate-size inputs or instructional implementations.

### 3.2 Hopcroft-Karp

Hopcroft-Karp finds many shortest augmenting paths in parallel layers before flipping them.

- Time: `O(E sqrt(V))` worst case on bipartite graphs.
- Space: `O(V)` auxiliary space beyond the graph and matching state.

It is the standard asymptotically faster algorithm for large unweighted bipartite matching.

## 4. Worked Example

Consider bipartite graph:

```text
L = {u1, u2, u3}
R = {v1, v2, v3}
Edges = {(u1, v1), (u1, v2), (u2, v2), (u2, v3), (u3, v2)}
```

Start with empty matching:

```text
M = {}
```

### 4.1 First Augmentation

Choose path:

```text
u1 - v1
```

This is an augmenting path because both endpoints are unmatched. Flip its edge into the matching:

```text
M = {(u1, v1)}
```

### 4.2 Second Augmentation

Choose path:

```text
u2 - v2
```

Again both endpoints are unmatched, so add it:

```text
M = {(u1, v1), (u2, v2)}
```

### 4.3 Third Augmenting Path

Vertex `u3` is unmatched, but its only neighbor `v2` is already matched to `u2`. Search for an alternating path:

```text
u3 - v2 - u2 - v3
```

Interpretation:

- `(u3, v2)` is currently unmatched,
- `(u2, v2)` is currently matched,
- `(u2, v3)` is currently unmatched.

Flip every edge on this path:

- add `(u3, v2)`,
- remove `(u2, v2)`,
- add `(u2, v3)`.

The new matching is:

```text
M = {(u1, v1), (u3, v2), (u2, v3)}
```

Now every vertex in `L` is matched, so the matching has size `3`.

Verification: the final matching uses three edges with no shared endpoints, and because `|L| = 3`, no larger bipartite matching is possible, so the matching is maximum.

## 5. Pseudocode Pattern

```text
procedure augmenting_path_bipartite_matching(graph, left_vertices):
    match_right = map_with_default(nil)

    for u in left_vertices:
        visited = empty_set()
        try_augment(u, graph, match_right, visited)

    return match_right
```

Time: `O(VE)` worst case for a DFS-based augmenting-path implementation on a bipartite graph. Space: `O(V)` auxiliary space beyond the graph and matching representation.

## 6. Common Mistakes

1. **Maximal-versus-maximum confusion.** Stopping at a matching that cannot be extended by one obvious edge does not prove optimality; use augmenting-path reasoning or a proven algorithm.
2. **Alternation loss.** Calling an arbitrary path an augmenting path without checking the matched-unmatched alternation pattern breaks the augmentation theorem; verify the path structure before flipping edges.
3. **Flow-reduction mismatch.** Omitting capacity `1` constraints in the flow reduction can allow one vertex to be matched multiple times; preserve matching semantics exactly in the network model.
4. **Graph-class overgeneralization.** Applying a bipartite-specific algorithm to a general graph without checking assumptions ignores odd-cycle complications; choose the algorithm for the graph class you actually have.
5. **Unverified optimality claims.** Reporting a large matching without proving that no augmenting path remains turns the result into a heuristic claim rather than a correct maximum-matching result.

## 7. Practical Checklist

- [ ] Distinguish clearly whether the target is any matching, a maximal matching, a maximum matching, or a perfect matching.
- [ ] Check whether the graph is bipartite before choosing a bipartite-specific algorithm.
- [ ] Use augmenting paths as the main debugging and correctness lens.
- [ ] Encode capacity `1` constraints explicitly if you reduce the problem to max flow.
- [ ] Verify that the final matching has no shared endpoints and no remaining augmenting path.
- [ ] Upgrade to Hopcroft-Karp when worst-case performance on large bipartite graphs matters.

## 8. References

- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Kleinberg, Jon, and Eva Tardos. 2005. *Algorithm Design*. Pearson.
- Lovasz, Laszlo, and Michael D. Plummer. 2009. *Matching Theory*. American Mathematical Society.
- Hopcroft, John E., and Richard M. Karp. 1973. An `n^{5/2}` Algorithm for Maximum Matchings in Bipartite Graphs. *SIAM Journal on Computing* 2(4): 225-231. <https://doi.org/10.1137/0202019>
- Goemans, Michel. 2023. *Bipartite Matching* lecture notes. Massachusetts Institute of Technology.
- Cornell University. 2021. *CS 6820 Lectures*. <https://www.cs.cornell.edu/courses/cs6820/2021fa/lectures.html>
