# Advanced Data Structures Intro

## Key Ideas

- Advanced data structures improve asymptotic performance by storing extra structure that makes expensive queries or updates cheap later.
- The right data structure is defined by the operation mix: query-heavy, update-heavy, merge-heavy, and ordered-access workloads need different designs.
- Amortised bounds such as `O(alpha(n))` for Union-Find are sequence guarantees, not per-operation worst-case guarantees.
- Range-query structures such as segment trees trade additional memory and implementation complexity for `O(log n)` updates and queries.
- Structural invariants are the source of performance: if the invariant is broken, the advertised complexity and correctness both fail.

## 1. What It Is

Advanced data structures are data structures that support operations more efficiently than basic arrays, linked lists, or hash tables when the workload includes nontrivial queries, dynamic updates, merges, or ordering constraints.

The main idea is to spend extra memory, preprocessing, or bookkeeping so that repeated operations become fast. Instead of recomputing answers from scratch, the structure maintains information incrementally.

Typical examples include:

- **Union-Find** for maintaining disjoint sets under repeated merges,
- **Segment trees** for range queries and point updates,
- **Balanced binary search trees** for ordered lookup and predecessor/successor queries,
- **Heaps** for repeated minimum or maximum extraction.

### 1.1 Core Definitions

- A **data structure** is a representation of data together with a supported set of operations and their complexity bounds.
- A **query** asks for information without changing the represented data, such as a range sum or the minimum element.
- An **update** changes the represented data, such as modifying an array entry or merging two sets.
- An **amortised bound** is a guarantee on the average cost per operation over a sequence of operations.
- An **invariant** is a property that must remain true after every operation for the data structure to stay correct.

### 1.2 Why This Matters

Many algorithms are fast only because they rely on the right supporting structure. Kruskal’s minimum spanning tree algorithm is efficient because Union-Find answers connectivity questions quickly. Online range-sum and range-minimum tasks become practical because segment trees avoid rescanning the whole array after every update.

Without the right structure, an algorithm that should run in near-linear or `O(n log n)` time can easily degrade to quadratic time. In practice, data structure choice often determines whether a solution scales at all.

## 2. Choosing by Operation Pattern

An advanced data structure should be chosen based on the dominant operations.

### 2.1 Merge and Connectivity Workloads

If the problem repeatedly asks whether two elements belong to the same connected component and occasionally merges components, **Union-Find** is the right default.

Supported operations:

- `find(x)` — return the representative of the set containing `x`
- `union(x, y)` — merge the sets containing `x` and `y`

With **path compression** and **union by rank/size**, a sequence of operations runs in amortised `O(alpha(n))` time per operation, where `alpha` is the inverse Ackermann function.

### 2.2 Range Query and Point Update Workloads

If the problem asks repeated questions over intervals such as sums, minima, maxima, or gcd over subarrays while also allowing updates, **segment trees** are a standard choice.

Typical operations:

- build from an array,
- query an interval `[l, r]`,
- update one position.

A segment tree supports point updates and range queries in `O(log n)` worst-case time, with `O(n)` space.

For a more focused comparison of prefix sums, sparse tables, and segment trees, see [Range Query Techniques](12-range-query-techniques.md).

### 2.3 Ordered Search Workloads

If the problem requires ordered iteration, predecessor/successor queries, or range search over keys, a **balanced BST** is appropriate.

Compared with hash tables:

- balanced BSTs support ordering-based queries,
- hash tables generally provide faster expected point lookup but no intrinsic order.

### 2.4 Repeated Extremum Extraction

If the dominant task is repeatedly retrieving and removing the minimum or maximum element, use a **heap**.

Typical bounds for a binary heap:

- insert: `O(log n)` worst case
- extract-min / extract-max: `O(log n)` worst case
- peek-min / peek-max: `O(1)` worst case

## 3. Union-Find and Segment Trees at a Glance

### 3.1 Union-Find

Union-Find represents a partition of elements into disjoint sets. Each set has a representative. The implementation usually stores a forest of parent pointers.

Two heuristics are essential:

- **Union by rank or size** keeps trees shallow by attaching the smaller or lower-rank tree below the larger one.
- **Path compression** flattens the tree during `find`, making future operations faster.

These heuristics do not merely optimize constants; they are what give Union-Find its near-constant amortised performance.

### 3.2 Segment Tree

A segment tree stores aggregate information for intervals of an array. Each internal node represents a segment, and its value is computed by combining the values of its children.

For a range-sum segment tree:

- leaves store single array elements,
- each internal node stores the sum of its interval.

This lets the structure answer interval queries without scanning every element.

**Why this matters:** the tree is useful only because the merge operation is well-defined and associative enough for the chosen query type. Sum, min, max, and gcd work well; more complex operations may need richer node state.

## 4. Worked Example

Consider the following workload on elements `{0, 1, 2, 3, 4}` using Union-Find:

1. `union(0, 1)`
2. `union(1, 2)`
3. `find(2)`
4. `union(3, 4)`
5. `find(4)`
6. `union(2, 4)`
7. `find(3)`

We track connected components rather than low-level parent arrays so the logic stays clear.

### 4.1 Step-by-Step Trace

Initial sets:

```text
{0} {1} {2} {3} {4}
```

After `union(0, 1)`:

```text
{0, 1} {2} {3} {4}
```

After `union(1, 2)`:

```text
{0, 1, 2} {3} {4}
```

Now `find(2)` returns the representative of the set containing `2`, which is the same set as `0` and `1`.

After `union(3, 4)`:

```text
{0, 1, 2} {3, 4}
```

Now `find(4)` returns the representative of the set containing `4`, which is the same set as `3`.

After `union(2, 4)`:

```text
{0, 1, 2, 3, 4}
```

Now every element is in one set, so `find(3)` must return the same representative as `find(0)`, `find(1)`, `find(2)`, and `find(4)`.

Verification: after the final union, all five elements belong to a single connected component. Therefore the final `find(3)` agrees with the representative of every other element. Correct.

## 5. Pseudocode Patterns

### 5.1 Union-Find

```text
procedure find(x):
    -- path compression
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]
```

Time: amortised `O(alpha(n))` per operation when used together with union by rank/size over a sequence of operations. Space: `O(n)`.

```text
procedure union(x, y):
    rx = find(x)
    ry = find(y)
    if rx == ry:
        return
    if rank[rx] < rank[ry]:
        parent[rx] = ry
    else if rank[rx] > rank[ry]:
        parent[ry] = rx
    else:
        parent[ry] = rx
        rank[rx] = rank[rx] + 1
```

Time: amortised `O(alpha(n))` per operation over a sequence of operations. Space: `O(n)`.

### 5.2 Segment Tree Query Pattern

```text
procedure range_query(node, seg_left, seg_right, q_left, q_right):
    if q_right < seg_left or seg_right < q_left:
        return identity_value
    if q_left <= seg_left and seg_right <= q_right:
        return tree[node]
    mid = (seg_left + seg_right) // 2
    left_ans = range_query(2 * node,
                           seg_left,
                           mid,
                           q_left,
                           q_right)
    right_ans = range_query(2 * node + 1,
                            mid + 1,
                            seg_right,
                            q_left,
                            q_right)
    return combine(left_ans, right_ans)
```

Time: `O(log n)` worst case for standard range queries on a segment tree. Space: `O(log n)` recursion depth, excluding the stored tree.

## 6. Common Mistakes

1. **Missing amortised qualifier.** Writing Union-Find as “`O(1)`” hides that the bound is amortised `O(alpha(n))` over a sequence, not constant worst-case per isolated operation.
2. **Dropped Union-Find heuristics.** Omitting path compression or union by rank/size keeps the structure correct but can make it much slower than the advertised near-constant behaviour.
3. **Segment tree indexing errors.** Mixing inclusive and half-open interval conventions causes off-by-one bugs that return wrong query results near boundaries.
4. **Wrong identity element.** Returning the wrong neutral element in a no-overlap segment-tree query, such as `0` for range minimum, corrupts the combined result.
5. **Hash-table substitution by habit.** Replacing a balanced BST with a hash table breaks ordered operations such as predecessor, successor, and range traversal even if point lookup still works.

## 7. Practical Checklist

- [ ] Identify the dominant operation pattern before choosing the structure: merge/find, range query/update, ordered search, or repeated min/max extraction.
- [ ] State whether each advertised bound is worst case, expected, or amortised.
- [ ] For Union-Find, verify that both path compression and union by rank/size are implemented.
- [ ] For segment trees, fix one interval convention and use it consistently in build, query, and update code.
- [ ] Check that the segment-tree identity element matches the aggregation operation.
- [ ] Use balanced BSTs only when ordered queries are required; otherwise consider a hash table or heap if they match the workload better.
- [ ] Trace at least one nontrivial example by hand before trusting the implementation.

## References

- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Tarjan, Robert E. 1975. Efficiency of a Good But Not Linear Set Union Algorithm. *Journal of the ACM* 22(2): 215–225. <https://doi.org/10.1145/321879.321884>
- Sedgewick, Robert, and Kevin Wayne. 2011. *Algorithms* (4th ed.). Addison-Wesley. <https://algs4.cs.princeton.edu/home/>
- Pat Morin. 2013. *Open Data Structures*. AU Press. <https://opendatastructures.org/>
- Mehlhorn, Kurt, and Peter Sanders. 2008. *Algorithms and Data Structures: The Basic Toolbox*. Springer. <https://doi.org/10.1007/978-3-540-77978-0>
- CP-Algorithms. *Disjoint Set Union* and *Segment Tree*. <https://cp-algorithms.com/>
