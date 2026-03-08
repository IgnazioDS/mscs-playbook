# Recurrences and Asymptotic Analysis

## Key Ideas

- A recurrence expresses the cost of a larger instance in terms of smaller instances, which is why it is the natural analysis tool for recursive and divide-and-conquer algorithms.
- Asymptotic analysis describes growth for large inputs, but the claim is meaningful only when the case is named and the recurrence assumptions are explicit.
- Recursion trees, substitution, and master-style theorems are complementary tools rather than competing ones.
- A recurrence is only as accurate as the model behind it; ignoring partition balance, base-case cost, or combine work leads to false bounds.
- Tight bounds should be written as `Theta(...)` when both upper and lower growth are justified.

## 1. What It Is

A **recurrence** defines a function by relating larger inputs to smaller inputs. In algorithm analysis, the function is usually runtime, space usage, or the number of primitive operations.

For example, if an algorithm splits an input of size `n` into two subproblems of size `n / 2` and then does `n` units of combine work, its worst-case runtime can be written as:

```text
T(n) = 2T(n / 2) + n
```

with a base case such as `T(1) = 1`.

The goal of asymptotic analysis is to describe the growth of `T(n)` for large `n`, not to compute every constant exactly. The analysis must still match the actual algorithmic structure.

## 2. Core Solution Methods

### 2.1 Expansion and recursion trees

A recursion tree expands the recurrence level by level. It is useful because it reveals where the total work comes from.

For `T(n) = 2T(n / 2) + n`, level `i` has `2^i` subproblems of size `n / 2^i`, so the nonrecursive work at that level is:

```text
2^i * (n / 2^i) = n
```

If there are `log_2 n` levels before reaching size `1`, the total is `n log_2 n` plus the leaf cost.

### 2.2 Substitution

Substitution means guessing a bound and proving it by induction. It is the most reliable method when theorem conditions are borderline or when logarithmic factors appear.

For example, to prove `T(n) = Theta(n log n)`, show both:

- `T(n) = O(n log n)` by an inductive upper bound, and
- `T(n) = Omega(n log n)` by an inductive lower bound or by level-counting.

### 2.3 Master-style theorems

For recurrences of the form

```text
T(n) = aT(n / b) + f(n)
```

with constants `a >= 1` and `b > 1`, the key comparison is between `f(n)` and `n^(log_b a)`.

- If `f(n)` is asymptotically smaller, the recursive work dominates.
- If `f(n)` matches, the cost is usually multiplied by an additional logarithmic factor.
- If `f(n)` is asymptotically larger and satisfies the regularity conditions, the nonrecursive work dominates.

This is fast and useful, but it does not apply to every recurrence. Uneven splits or additive shifts often require substitution or stronger theorems such as Akra-Bazzi.

## 3. Why the Model Matters

The same algorithmic idea can yield different recurrences depending on the case.

### 3.1 Case-sensitive claims

Quicksort is a standard example:

- Best case: `Theta(n log n)` when partitions are balanced.
- Average case: `Theta(n log n)` under a random pivot model.
- Worst case: `Theta(n^2)` when partitions are extremely unbalanced.

A complexity statement that omits the case is incomplete.

### 3.2 Space recurrences

Recurrences can describe stack depth or temporary storage as well as time. For merge sort, the worst-case auxiliary space is `Theta(n)` for merging, while the recursion depth is `Theta(log n)`. These are different resources and should not be collapsed into a single sentence.

This topic connects directly to [Divide and Conquer](../../01-algorithms/01-concepts/03-divide-and-conquer.md), where the recurrence comes from the algorithm design itself.

## 4. Worked Example

Solve the recurrence:

```text
T(n) = 2T(n / 2) + n
T(1) = 1
```

Assume `n` is a power of two.

### 4.1 Build the recursion tree

Level `0`:

```text
1 subproblem of size n
nonrecursive work = n
```

Level `1`:

```text
2 subproblems of size n / 2
nonrecursive work = 2 * (n / 2) = n
```

Level `2`:

```text
4 subproblems of size n / 4
nonrecursive work = 4 * (n / 4) = n
```

After `log_2 n` levels, we reach subproblems of size `1`.

### 4.2 Sum the work

There are `log_2 n` internal levels, each contributing `n`, so the internal work is:

```text
n log_2 n
```

At the leaves there are `n` subproblems of size `1`, each costing `T(1) = 1`, so leaf work is:

```text
n
```

Therefore:

```text
T(n) = n log_2 n + n = Theta(n log n)
```

### 4.3 Verify on a concrete value

Take `n = 8`.

- Level `0` work: `8`
- Level `1` work: `8`
- Level `2` work: `8`
- Leaf work: `8`

Total:

```text
T(8) = 8 + 8 + 8 + 8 = 32
```

Now compute directly from the recurrence:

```text
T(8) = 2T(4) + 8
T(4) = 2T(2) + 4
T(2) = 2T(1) + 2 = 4
T(4) = 2 * 4 + 4 = 12
T(8) = 2 * 12 + 8 = 32
```

Verification: both the recursion-tree sum and direct expansion give `T(8) = 32`, consistent with `Theta(n log n)` growth.

## 5. Pseudocode Pattern

```text
procedure divide_and_conquer(problem):
    if is_base_case(problem):
        return solve_base_case(problem)

    subproblems = split(problem)
    partial_results = empty_list()

    for subproblem in subproblems:
        append(partial_results, divide_and_conquer(subproblem))

    return combine(problem, partial_results)
```

Time: if `a` subproblems of size `n / b` are created and combine work is `f(n)`, the worst-case runtime recurrence is `T(n) = aT(n / b) + f(n)`. Space: depends on recursion depth and temporary storage created by `combine`.

The point of the pseudocode is not the syntax; it is the mapping from algorithm structure to recurrence structure.

## 6. Common Mistakes

1. **Case omission.** Quoting one asymptotic bound without naming best, average, expected, amortised, or worst case makes the claim incomplete; state the input model or adversarial setting explicitly.
2. **Base-case erasure.** Dropping the base case from the recurrence can invalidate an induction proof or distort the exact level count; keep the stopping size and its cost visible.
3. **Master-theorem overreach.** Applying a master-style formula to recurrences with uneven splits or nonstandard terms produces incorrect bounds; switch to substitution, recursion trees, or Akra-Bazzi when the form does not match.
4. **Leaf-cost neglect.** Summing only internal levels can miss a dominant leaf contribution in some recurrences; compute the leaves separately before concluding the bound.
5. **Upper-bound inflation.** Writing `O(...)` when the analysis actually proves a matching lower bound hides useful precision; use `Theta(...)` when the argument justifies it.

## 7. Practical Checklist

- [ ] Write the recurrence directly from the algorithm’s split, recursive calls, and combine work.
- [ ] State the case being analyzed before solving the recurrence.
- [ ] Keep the base case explicit and consistent with the implementation.
- [ ] Use a recursion tree when you need to see which level dominates.
- [ ] Use substitution when theorem conditions are not obviously satisfied.
- [ ] Separate time, stack depth, and auxiliary space instead of merging them.

## 8. References

- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Kleinberg, Jon, and Eva Tardos. 2005. *Algorithm Design*. Pearson. <https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003815>
- Erickson, Jeff. 2023. *Algorithms*. University of Illinois Urbana-Champaign. <https://jeffe.cs.illinois.edu/teaching/algorithms/>
- Akra, Mohamed, and Louay Bazzi. 1998. *On the Solution of Linear Recurrence Equations*. *Computational Optimization and Applications* 10. <https://doi.org/10.1023/A:1018373005182>
- MIT OpenCourseWare. 2011. *Introduction to Algorithms*. <https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/>
- Sedgewick, Robert, and Kevin Wayne. 2011. *Algorithms* (4th ed.). Addison-Wesley. <https://algs4.cs.princeton.edu/home/>
