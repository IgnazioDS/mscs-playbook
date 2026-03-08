# Data Structures Intro

## Key Ideas

- Data structures organize information to improve algorithm efficiency; choosing the right structure affects speed and memory use.
- An array stores elements in contiguous memory and supports constant-time access by index, but insertions or deletions inside the array require shifting elements.
- A hash table uses a hash function to map keys to buckets and typically supports expected O(1) lookup, insertion, and deletion when collisions are controlled.
- Trees and graphs model hierarchical and network relationships, but their performance depends heavily on representation and structural invariants.
- Data-structure selection is really operation-cost selection, so complexity claims should always name the relevant case and workload.

## 1. What It Is

A **data structure** is an organization of information, usually in memory, designed to improve algorithm efficiency and support useful operations such as search, insertion, deletion, and traversal. Different structures optimize different operations, so data structure choice is part of algorithm design rather than a separate implementation detail.

This page introduces four foundational families:

- arrays for indexed storage,
- hash tables for key-value lookup,
- trees for ordered or hierarchical data, and
- graphs for relationship-rich data.

It also explains how to compare structures by the operations they need to support.

### 1.1 Core Definitions

- A **time complexity** bound describes how the number of primitive operations grows with input size `n`.
- A **space complexity** bound describes how memory usage grows with input size `n`.
- An **array** is a sequence of same-type elements stored in contiguous memory.
- A **hash table** is a dictionary-like structure that maps keys to positions using a hash function.
- A **binary search tree** is an ordered tree where each node separates smaller keys on the left from larger keys on the right.
- A **graph** is a set of vertices connected by edges.

### 1.2 Why This Matters

In real systems, performance failures often come from using the wrong structure for the dominant operation. A feature store optimized for lookup behaves differently from a scheduler optimized for ordered extraction, and a sparse graph requires different storage than a dense one. Data structure decisions affect latency, memory footprint, cache behavior, and scaling limits.

## 2. Operation-Cost Reasoning

Data-structure choice is justified by operation costs. Big-O notation gives an asymptotic upper bound on growth. Formally, `f(n) = O(g(n))` means there exist constants `c > 0` and `k` such that `0 <= f(n) <= c * g(n)` for all `n >= k`.

In practice, this lets us compare how algorithms scale without getting distracted by machine-specific constants.

### 2.1 Common Growth Classes

| Complexity | Meaning | Typical intuition |
|---|---|---|
| `O(1)` | Constant | Cost does not grow with input size |
| `O(log n)` | Logarithmic | Problem size shrinks by a constant factor each step |
| `O(n)` | Linear | Work grows proportionally with input size |
| `O(n log n)` | Linearithmic | Common in efficient comparison-based sorting |
| `O(n^2)` | Quadratic | Nested iteration over the input |

### 2.2 Why Case Labels Matter

Complexity claims are incomplete without a case label when behavior varies.

- **Worst-case O(...)** means the algorithm never exceeds that bound.
- **Average-case O(...)** describes typical behavior under an assumed input distribution.
- **Expected O(...)** includes randomness in the algorithm or hashing model.
- **Amortised O(...)** averages the cost of expensive occasional operations across a sequence.

For example:

- Hash table lookup is typically **expected O(1)**, not unconditional O(1).
- Binary search tree search is **O(n) worst case** in an unbalanced tree.
- Balanced search tree operations are **O(log n) worst case**.

## 3. Arrays, Hash Tables, Trees, and Graphs

### 3.1 Arrays

An array stores elements in contiguous memory. This makes indexed access efficient because the address of `A[i]` can be computed directly.

Typical properties:

- Access by index: `O(1)`
- Sequential search: `O(n)` worst case
- Insert at end of a fixed-size array: not supported without free capacity
- Insert inside array: `O(n)` worst case due to shifting
- Delete inside array: `O(n)` worst case due to shifting
- Space: `O(n)`

**Why this matters:** Arrays are excellent when reads by position dominate. They are poor when frequent mid-array insertions or deletions dominate.

### 3.2 Hash Tables

A hash table maps a key to a bucket using a hash function. If the function distributes keys well and the load factor stays controlled, lookup, insertion, and deletion are typically expected `O(1)`.

Typical properties:

- Lookup: expected `O(1)`
- Insert: expected `O(1)`
- Delete: expected `O(1)`
- Worst-case operations: `O(n)` if many keys collide
- Space: `O(n)` plus bucket overhead

Hash tables do not preserve sorted order. They are optimized for direct access by key, not range queries or ordered traversal.

**Why this matters:** A hash table is often the right default when key-based lookup dominates. It is the wrong choice when you need sorted iteration, predecessor/successor queries, or stable ordering semantics.

### 3.3 Trees

A binary tree has at most two children per node. A binary search tree (BST) adds an ordering invariant:

- keys in the left subtree are smaller than the node key,
- keys in the right subtree are larger than the node key.

For a general unbalanced BST:

- Search: `O(n)` worst case
- Insert: `O(n)` worst case
- Delete: `O(n)` worst case

For a balanced BST:

- Search: `O(log n)` worst case
- Insert: `O(log n)` worst case
- Delete: `O(log n)` worst case

**Why this matters:** Trees support ordered data efficiently. Unlike hash tables, they can answer range queries and support in-order traversal. But unless balance is maintained, performance can collapse to linear time.

### 3.4 Graphs

A graph consists of vertices and edges. Two common representations are adjacency matrices and adjacency lists.

#### Adjacency Matrix

An adjacency matrix stores a boolean-like table `a[i][j]` indicating whether edge `(i, j)` exists.

- `has_edge(i, j)`: `O(1)`
- `add_edge(i, j)`: `O(1)`
- `remove_edge(i, j)`: `O(1)`
- Enumerate neighbors of `i`: `O(n)`
- Space: `O(n^2)`

This representation is appropriate for dense graphs or workloads dominated by edge existence checks.

#### Adjacency List

An adjacency list stores, for each vertex `i`, the list of outgoing neighbors.

- `add_edge(i, j)`: `O(1)` amortised if append is efficient
- `has_edge(i, j)`: `O(deg(i))`
- `remove_edge(i, j)`: `O(deg(i))`
- Enumerate neighbors of `i`: `Theta(deg(i))`
- Space: `O(n + m)` where `m` is the number of edges

This representation is usually preferable for sparse graphs.

**Why this matters:** Choosing the wrong graph representation can waste substantial memory or make the dominant operation asymptotically slower.

## 4. Comparison Table

| Structure | Access / Search | Insert | Delete | Space | Best use |
|---|---|---|---|---|---|
| Array | `O(1)` indexed access, `O(n)` worst-case search | `O(n)` worst case inside array | `O(n)` worst case inside array | `O(n)` | Fast indexed reads |
| Hash table | Expected `O(1)` lookup | Expected `O(1)` | Expected `O(1)` | `O(n)` | Key-based lookup |
| Balanced BST | `O(log n)` worst case | `O(log n)` worst case | `O(log n)` worst case | `O(n)` | Ordered lookup and range queries |
| Adjacency matrix | `O(1)` edge check | `O(1)` edge add | `O(1)` edge delete | `O(n^2)` | Dense graphs |
| Adjacency list | `O(deg(v))` edge check | `O(1)` amortised edge add | `O(deg(v))` edge delete | `O(n + m)` | Sparse graphs |

## 5. Worked Example

Consider searching for `7` in the sorted array:

```text
A = [1, 3, 5, 7, 9, 11]
```

We compare sequential search and binary search.

### 5.1 Sequential Search Trace

Sequential search examines elements left to right.

| Step | Index | Value | Action |
|---|---:|---:|---|
| 1 | 0 | 1 | `1 != 7`, continue |
| 2 | 1 | 3 | `3 != 7`, continue |
| 3 | 2 | 5 | `5 != 7`, continue |
| 4 | 3 | 7 | Found target |

Sequential search runs in `O(n)` worst case because it may examine every element.

### 5.2 Binary Search Trace

Binary search assumes the array is sorted and halves the search interval each step.

**Worked example:**
Search for `7` in `A = [1, 3, 5, 7, 9, 11]`.

| Step | lo | hi | mid | A[mid] | Action |
|------|----|----|-----|--------|--------|
| 1 | 0 | 5 | 2 | 5 | `5 < 7`, set `lo = 3` |
| 2 | 3 | 5 | 4 | 9 | `9 > 7`, set `hi = 3` |
| 3 | 3 | 3 | 3 | 7 | Found at index 3 |

Binary search runs in `O(log n)` worst case on a sorted array with constant-time indexing.

Verification: both traces find the target value `7` at index `3`, and the binary-search trace reaches the answer in three comparisons on this input.

### 5.3 Pseudocode

```text
procedure binary_search(array, target):
    lo = 0
    hi = length(array) - 1
    while lo <= hi:
        mid = floor((lo + hi) / 2)
        if array[mid] == target:
            return mid
        else if array[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

Time: `Theta(log n)` worst case on a sorted random-access array. Space: `Theta(1)` auxiliary space in the iterative form.

## 6. Common Mistakes

1. **Assuming expected means guaranteed.** Treating hash table lookup as guaranteed `O(1)` ignores collision behavior and worst-case degradation; write **expected O(1)** unless the structure provides stronger guarantees.
2. **Using arrays for mutation-heavy workloads.** Choosing arrays when the dominant operations are repeated insertions or deletions inside the sequence introduces unnecessary `O(n)` shifts.
3. **Ignoring tree balance.** Claiming `O(log n)` for a plain binary search tree is incorrect unless the tree is balanced or randomized in a way that justifies the bound.
4. **Choosing adjacency matrices for sparse graphs.** A sparse graph stored as an `n x n` matrix wastes `O(n^2)` space when an adjacency list would use `O(n + m)`.
5. **Stating complexity without the case.** Writing “hash lookup is O(1)” or “tree search is O(log n)” without saying expected, worst case, or amortised hides important performance assumptions.

## 7. Practical Checklist

- [ ] Identify the dominant operations before choosing a data structure.
- [ ] Use arrays when constant-time indexed access is more important than insertion or deletion cost.
- [ ] Use hash tables when direct key lookup dominates and sorted order is not required.
- [ ] Use balanced trees when you need ordered traversal, range queries, or predecessor/successor operations.
- [ ] Choose adjacency lists for sparse graphs and adjacency matrices for dense graphs or constant-time edge checks.
- [ ] State every nontrivial complexity claim with its case: worst case, expected, or amortised.
- [ ] Include at least one concrete trace when explaining a search or traversal algorithm.

## 8. References

- Black, Paul E. 2024. *Data structure*. Dictionary of Algorithms and Data Structures, National Institute of Standards and Technology. <https://www.nist.gov/dads/HTML/dataStructure.html>
- Black, Paul E. 2019. *Big-O notation*. Dictionary of Algorithms and Data Structures, National Institute of Standards and Technology. <https://www.nist.gov/dads/HTML/bigOnotation.html>
- Black, Paul E. 2022. *Hash table*. Dictionary of Algorithms and Data Structures, National Institute of Standards and Technology. <https://www.nist.gov/dads/HTML/hashtab.html>
- Black, Paul E. 2017. *Binary tree*. Dictionary of Algorithms and Data Structures, National Institute of Standards and Technology. <https://www.nist.gov/dads/HTML/binarytree.html>
- Black, Paul E. 2023. *Directed graph*. Dictionary of Algorithms and Data Structures, National Institute of Standards and Technology. <https://www.nist.gov/dads/HTML/directedGraph.html>
- Morin, Pat. 2013. *Open Data Structures*. AU Press. <https://opendatastructures.org/>
- OpenStax. 2025. *Introduction to Computer Science*. OpenStax. <https://openstax.org/details/books/introduction-computer-science>
