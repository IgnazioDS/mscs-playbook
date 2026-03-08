# Sorting and Selection

## Key Ideas

- Sorting organizes items by key, while selection asks for one or more order statistics such as the minimum, median, or `k`-th smallest element.
- Comparison-based sorting has an `Omega(n log n)` worst-case lower bound, so faster general-purpose algorithms must exploit additional structure such as bounded integer keys.
- The right algorithm depends on the case that matters: merge sort gives predictable `Theta(n log n)` worst-case time, quicksort gives `Theta(n log n)` average time with `Theta(n^2)` worst-case time, and heapsort gives `Theta(n log n)` worst-case time with different constant factors.
- Selection can often be solved more cheaply than full sorting; expected-linear-time quickselect is a standard example.
- Stability, memory usage, input distribution, and implementation complexity are part of the algorithm choice, not afterthoughts.

## 1. What It Is

A **sorting** algorithm reorders a collection so that its keys appear in nondecreasing or nonincreasing order. A **selection** algorithm finds an item of a specified rank without necessarily ordering everything else.

These problems appear everywhere:

- ranking results,
- scheduling by deadline or weight,
- computing quantiles,
- preprocessing for deduplication,
- and enabling later binary search or sweep-line logic.

The conceptual distinction matters because full sorting can do unnecessary work when only a single rank is needed.

## 2. Comparison Sorting Landscape

### 2.1 Lower bound intuition

In a comparison model, the algorithm learns order only by asking questions like `a[i] < a[j]`. The possible outcomes form a decision tree. Since there are `n!` possible total orders, any comparison sort must distinguish among them, which implies a worst-case lower bound of `Omega(n log n)` comparisons.

That is why general-purpose comparison sorts cannot beat `Theta(n log n)` in the worst case.

### 2.2 Practical choices

- **Merge sort**: `Theta(n log n)` worst, average, and best case; stable; typically `Theta(n)` auxiliary space.
- **Quicksort**: `Theta(n log n)` average or expected time with a random pivot, `Theta(n^2)` worst case; usually in-place with `Theta(log n)` expected recursion depth.
- **Heapsort**: `Theta(n log n)` worst, average, and best case; not stable; `Theta(1)` auxiliary space beyond the array.

### 2.3 When non-comparison sorting applies

Counting sort and radix sort can beat `n log n` when keys come from a bounded structure such as fixed-width integers or fixed-length strings. The faster bound depends on extra assumptions, so it should not be described as a contradiction of the comparison lower bound.

## 3. Selection and Order Statistics

The `k`-th smallest element is an **order statistic**.

### 3.1 Why selection is cheaper than sorting

If you only need the median, fully sorting every element is stronger than necessary. Quickselect partitions the array as quicksort does, but recurses only into the side containing the desired rank.

### 3.2 Complexity claims

- Quickselect with a random pivot has `Theta(n)` expected time and `Theta(n^2)` worst-case time.
- Median-of-medians selection has `Theta(n)` worst-case time but larger constants.

This distinction is important in implementation work: predictable worst-case behavior and lower average constant factors are different goals.

## 4. Worked Example

Find the 4th smallest element in:

```text
[9, 1, 8, 2, 7, 3, 6]
```

using quickselect with pivot chosen as the last element of the current subarray.

### 4.1 First partition

Pivot = `6`.

Partition elements into those smaller than `6` and those larger than `6`:

```text
[1, 2, 3, 6, 9, 8, 7]
```

Now `6` is in sorted position index `3` using zero-based indexing, so it is the 4th smallest element.

### 4.2 Why the algorithm can stop

Quickselect does not need to sort `[1, 2, 3]` or `[9, 8, 7]` completely. Once the pivot lands at rank `k`, the answer is known.

If we had asked for the 2nd smallest element instead, only the left subarray `[1, 2, 3]` would need further processing.

Verification: sorting the original array gives `[1, 2, 3, 6, 7, 8, 9]`, whose 4th smallest element is indeed `6`.

## 5. Pseudocode Pattern

```text
procedure quickselect(A, left, right, k):
    if left == right:
        return A[left]

    pivot_index = partition(A, left, right)

    if k == pivot_index:
        return A[k]
    if k < pivot_index:
        return quickselect(A, left, pivot_index - 1, k)
    return quickselect(A, pivot_index + 1, right, k)
```

Time: `Theta(n)` expected time with a random pivot and `Theta(n^2)` worst case. Space: `Theta(log n)` expected recursion depth and `Theta(n)` worst-case recursion depth.

For comparison, full merge sort requires `Theta(n log n)` time even when only a single rank is needed.

## 6. Common Mistakes

1. **Sort-when-select suffices.** Fully sorting when only one rank is needed wastes work and can change the performance profile; use selection when the task is an order statistic.
2. **Lower-bound misreading.** Claiming counting sort disproves the `Omega(n log n)` lower bound ignores that the lower bound applies only to comparison sorting; state the model assumptions explicitly.
3. **Pivot-model omission.** Reporting quicksort or quickselect as simply `O(n log n)` or `O(n)` without naming average, expected, or worst case hides the role of pivot selection; specify the case and pivot strategy.
4. **Stability neglect.** Choosing an unstable sort in a pipeline that depends on preserving equal-key order can silently break downstream logic; check whether stability is required.
5. **Partition invariant bugs.** Implementing partitioning without a clear invariant often produces off-by-one errors or lost elements; write and test the invariant around the pivot region.

## 7. Practical Checklist

- [ ] Decide whether the task requires full order or only selected ranks.
- [ ] Name the case for every complexity claim.
- [ ] Check whether key structure enables counting or radix-based methods.
- [ ] Record whether stability is required by downstream consumers.
- [ ] Test partition logic on repeated keys, sorted input, and reverse-sorted input.
- [ ] Measure memory use as well as runtime when choosing among merge sort, quicksort, and heapsort.

## 8. References

- Hoare, C. A. R. 1962. *Quicksort*. *The Computer Journal* 5 (1). <https://academic.oup.com/comjnl/article-abstract/5/1/10/395338>
- Blum, Manuel, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest, and Robert E. Tarjan. 1973. *Time Bounds for Selection*. *Journal of Computer and System Sciences* 7 (4). <https://doi.org/10.1016/S0022-0000(73)80033-9>
- Knuth, Donald E. 1998. *The Art of Computer Programming, Volume 3: Sorting and Searching* (2nd ed.). Addison-Wesley. <https://www-cs-faculty.stanford.edu/~knuth/taocp.html>
- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Sedgewick, Robert, and Kevin Wayne. 2011. *Algorithms* (4th ed.). Addison-Wesley. <https://algs4.cs.princeton.edu/home/>
- Kleinberg, Jon, and Eva Tardos. 2005. *Algorithm Design*. Pearson. <https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003815>
