# Range Query Techniques

## Key Ideas

- Range-query problems ask for aggregate information over intervals, subarrays, or index ranges, often under repeated queries and updates.
- The right technique depends first on whether the data is static or dynamic, and second on whether updates are point updates or range updates.
- Prefix sums are the simplest static range-query structure because they trade `Theta(n)` preprocessing for `Theta(1)` worst-case query time.
- Segment trees generalize range querying to dynamic settings with `Theta(log n)` worst-case queries and updates.
- Sparse tables support idempotent static queries such as range minimum with `Theta(1)` worst-case query time after preprocessing.

## 1. What It Is

A **range query** asks for an aggregate over a contiguous interval such as:

- sum of `A[l:r]`,
- minimum on `A[l:r]`,
- maximum on `A[l:r]`,
- or gcd on `A[l:r]`.

The main design question is not the aggregation alone. It is the workload:

- Are there updates?
- If yes, how often?
- Is the aggregation associative?
- Is it idempotent, meaning `combine(x, x) = x`?

These properties determine which structure is appropriate.

## 2. Main Techniques

### 2.1 Prefix sums

For static range sums, define:

```text
prefix[i] = A[0] + A[1] + ... + A[i - 1]
```

Then:

```text
sum(l, r) = prefix[r + 1] - prefix[l]
```

This gives `Theta(1)` worst-case query time after `Theta(n)` preprocessing.

### 2.2 Segment trees

Segment trees support dynamic point updates and range queries by storing interval aggregates in a binary tree over the array.

Typical bounds:

- build: `Theta(n)` worst case
- query: `Theta(log n)` worst case
- point update: `Theta(log n)` worst case

### 2.3 Sparse tables

Sparse tables preprocess intervals of lengths `2^k` and are especially useful for static idempotent queries such as range minimum.

Typical bounds:

- build: `Theta(n log n)` worst case
- query: `Theta(1)` worst case for idempotent operations such as `min`
- updates: not supported efficiently in the standard static form

## 3. Technique Selection

### 3.1 Static versus dynamic

If the array never changes, simpler structures often beat dynamic ones.

- Static sum queries -> prefix sums
- Static min/max/gcd queries -> sparse table or offline preprocessing
- Dynamic queries with updates -> segment tree or Fenwick tree depending on the operation

### 3.2 Why the algebra matters

The aggregate operation must fit the structure.

- Prefix sums need invertibility for subtraction-based interval recovery.
- Segment trees need an associative combine operation.
- Sparse tables benefit from idempotence when overlapping blocks are used.

## 4. Worked Example

Use prefix sums on:

```text
A = [3, 1, 4, 1, 5]
```

### 4.1 Build the prefix array

Define `prefix[0] = 0`.

Then:

```text
prefix[1] = 3
prefix[2] = 4
prefix[3] = 8
prefix[4] = 9
prefix[5] = 14
```

So:

```text
prefix = [0, 3, 4, 8, 9, 14]
```

### 4.2 Answer a range-sum query

Query the sum from index `1` through `3`, meaning `1 + 4 + 1`.

Using prefix sums:

```text
sum(1, 3) = prefix[4] - prefix[1] = 9 - 3 = 6
```

### 4.3 Check directly

Direct computation gives:

```text
A[1] + A[2] + A[3] = 1 + 4 + 1 = 6
```

Verification: the prefix-sum answer `6` matches the direct interval sum.

## 5. Pseudocode Pattern

```text
procedure build_prefix_sums(A):
    n = length(A)
    prefix = array of size n + 1
    prefix[0] = 0
    for i = 0 to n - 1:
        prefix[i + 1] = prefix[i] + A[i]
    return prefix

procedure range_sum(prefix, left, right):
    return prefix[right + 1] - prefix[left]
```

Build time: `Theta(n)` worst case. Query time: `Theta(1)` worst case. Space: `Theta(n)`.

## 6. Common Mistakes

1. **Static-dynamic mismatch.** Using a static technique such as prefix sums when frequent updates occur makes each update too expensive; choose a dynamic structure when the workload changes the array.
2. **Interval-convention drift.** Mixing inclusive and half-open ranges causes off-by-one errors at query boundaries; fix one convention and use it everywhere.
3. **Operation-structure mismatch.** Applying prefix-sum intuition to operations that do not support subtraction-based recovery leads to wrong answers; match the algebra to the structure.
4. **Sparse-table overreach.** Using sparse tables in update-heavy settings ignores that the classic structure is static; rebuild cost can dominate.
5. **Segment-tree identity bugs.** Returning the wrong neutral element for a no-overlap branch corrupts the combined query result; choose the identity to match the aggregation.

## 7. Practical Checklist

- [ ] Decide whether the workload is static or dynamic before choosing a structure.
- [ ] State the aggregate operation explicitly.
- [ ] Fix the interval convention as inclusive or half-open.
- [ ] Use prefix sums for static range sums whenever subtraction is valid.
- [ ] Use segment trees when point updates and range queries both matter.
- [ ] Use sparse tables only for static queries with suitable aggregation behavior.

## 8. References

- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Sedgewick, Robert, and Kevin Wayne. 2011. *Algorithms* (4th ed.). Addison-Wesley. <https://algs4.cs.princeton.edu/home/>
- Morin, Pat. 2013. *Open Data Structures*. AU Press. <https://opendatastructures.org/>
- Mehlhorn, Kurt, and Peter Sanders. 2008. *Algorithms and Data Structures: The Basic Toolbox*. Springer. <https://doi.org/10.1007/978-3-540-77978-0>
- Black, Paul E. 2023. *Segment tree*. Dictionary of Algorithms and Data Structures, National Institute of Standards and Technology. <https://www.nist.gov/dads/HTML/segmentTree.html>
- Black, Paul E. 2022. *Fenwick tree*. Dictionary of Algorithms and Data Structures, National Institute of Standards and Technology. <https://www.nist.gov/dads/HTML/fenwickTree.html>
