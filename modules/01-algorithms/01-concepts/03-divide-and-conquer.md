# Divide and Conquer

## Key Ideas

- Divide and conquer solves a problem by breaking it into smaller instances of the same form, solving them recursively, and combining their results.
- The design succeeds only when the split creates simpler subproblems and the combine step preserves the global objective correctly.
- Recurrences are the natural analysis tool because they mirror the recursive structure of the algorithm.
- Balanced subproblems often produce `Theta(n log n)` behavior, while highly unbalanced subproblems can degrade to quadratic or worse depending on the algorithm.
- Implementation details such as copying cost, recursion depth, and cache locality can determine whether a theoretically elegant design is practical.

## 1. What It Is

A divide-and-conquer algorithm has three parts:

1. **Divide** the input into smaller subproblems.
2. **Conquer** the subproblems recursively.
3. **Combine** the partial results into a full solution.

This pattern matters because it turns a large problem into repeated applications of the same reasoning. Merge sort, binary search, closest-pair algorithms, fast multiplication, and many geometric algorithms follow this structure.

The key question is not whether recursion is present. The key question is whether the problem can be decomposed into smaller self-similar pieces whose solutions can be recombined correctly.

## 2. Anatomy of the Design

### 2.1 Split, recurse, combine

A good split reduces problem size enough to justify recursion. A good combine step is both correct and asymptotically controlled.

For example:

- Binary search splits the search interval and discards half immediately.
- Merge sort splits the array into two halves and then merges two sorted arrays.
- Karatsuba multiplication splits large integers and reduces the number of recursive multiplications.

### 2.2 Analysis by recurrence

If an algorithm creates `a` subproblems of size `n / b` and performs `f(n)` combine work, the worst-case recurrence is:

```text
T(n) = aT(n / b) + f(n)
```

That connection is developed in [Recurrences and Asymptotic Analysis](../../00-foundations/01-concepts/04-recurrences-and-asymptotic-analysis.md).

### 2.3 When divide and conquer is a bad fit

The technique is weaker when:

- subproblems overlap heavily, which suggests dynamic programming instead,
- the combine step is too expensive,
- or recursion causes avoidable copying and stack overhead.

## 3. Practical Tradeoffs

### 3.1 Balance and depth

A balanced split yields recursion depth `Theta(log n)`. An unbalanced split can increase depth to `Theta(n)`, which changes both time and stack behavior.

### 3.2 Memory behavior

Recursive elegance can hide memory cost. Merge sort needs auxiliary storage for merging. Quicksort uses less extra space on average but has a worse worst-case stack depth unless the implementation is careful.

### 3.3 Correctness structure

The recursive calls usually solve subproblems correctly by induction. The real burden of proof then moves to the combine step: does combining two correct partial answers produce the correct full answer?

## 4. Worked Example

Trace merge sort on:

```text
[5, 2, 4, 7, 1, 3]
```

### 4.1 Divide phase

```text
[5, 2, 4, 7, 1, 3]
-> [5, 2, 4] and [7, 1, 3]
-> [5] and [2, 4]; [7] and [1, 3]
-> [2] and [4]; [1] and [3]
```

Single-element arrays are base cases because they are already sorted.

### 4.2 Conquer and combine

Merge `[2]` and `[4]`:

```text
compare 2 and 4 -> take 2
append remaining 4
result = [2, 4]
```

Merge `[5]` and `[2, 4]`:

```text
compare 5 and 2 -> take 2
compare 5 and 4 -> take 4
append remaining 5
result = [2, 4, 5]
```

Merge `[1]` and `[3]`:

```text
compare 1 and 3 -> take 1
append remaining 3
result = [1, 3]
```

Merge `[7]` and `[1, 3]`:

```text
compare 7 and 1 -> take 1
compare 7 and 3 -> take 3
append remaining 7
result = [1, 3, 7]
```

Final merge of `[2, 4, 5]` and `[1, 3, 7]`:

```text
compare 2 and 1 -> take 1
compare 2 and 3 -> take 2
compare 4 and 3 -> take 3
compare 4 and 7 -> take 4
compare 5 and 7 -> take 5
append remaining 7
result = [1, 2, 3, 4, 5, 7]
```

Verification: the final array is sorted in nondecreasing order and contains exactly the six original elements, so the divide, conquer, and combine steps were correct.

## 5. Pseudocode Pattern

```text
procedure merge_sort(A):
    if length(A) <= 1:
        return A

    mid = floor(length(A) / 2)
    left = merge_sort(A[0:mid])
    right = merge_sort(A[mid:length(A)])
    return merge(left, right)
```

Time: `Theta(n log n)` worst, average, and best case for arrays of length `n` when merge takes `Theta(n)` time. Space: `Theta(n)` auxiliary space in the standard array-based implementation.

This is a canonical divide-and-conquer pattern because the subproblems are self-similar and the merge step is linear.

## 6. Common Mistakes

1. **Recursive-shape confusion.** Using divide and conquer when subproblems overlap heavily causes redundant work and hides a dynamic-programming structure; check whether the recursive tree recomputes the same states.
2. **Combine-step handwaving.** Assuming subproblem solutions can simply be concatenated or merged without proof often breaks correctness; specify exactly why the combine step preserves the global objective.
3. **Case-free complexity claims.** Reporting only one bound for algorithms such as quicksort hides the difference between average and worst behavior; name the case and the input model.
4. **Copy-cost neglect.** Slicing or copying arrays at each recursive call can add substantial constant factors or extra asymptotic space; account for real implementation costs.
5. **Stack-depth blindness.** Deep recursion can overflow the call stack even when the asymptotic time is good; analyze recursion depth separately from total work.

## 7. Practical Checklist

- [ ] State the divide, conquer, and combine steps separately.
- [ ] Write the recurrence before claiming a complexity bound.
- [ ] Check whether subproblems overlap enough to suggest dynamic programming instead.
- [ ] Prove the combine step, not just the recursive calls.
- [ ] Account for recursion depth and temporary memory separately.
- [ ] Test edge cases such as empty inputs, single-element inputs, and odd split sizes.

## 8. References

- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Kleinberg, Jon, and Eva Tardos. 2005. *Algorithm Design*. Pearson. <https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003815>
- Erickson, Jeff. 2023. *Algorithms*. University of Illinois Urbana-Champaign. <https://jeffe.cs.illinois.edu/teaching/algorithms/>
- Sedgewick, Robert, and Kevin Wayne. 2011. *Algorithms* (4th ed.). Addison-Wesley. <https://algs4.cs.princeton.edu/home/>
- Akra, Mohamed, and Louay Bazzi. 1998. *On the Solution of Linear Recurrence Equations*. *Computational Optimization and Applications* 10. <https://doi.org/10.1023/A:1018373005182>
- Bentley, Jon L. 1984. *Programming Pearls*. Addison-Wesley. <https://www.pearson.com/en-us/subject-catalog/p/programming-pearls/P200000003257>
