# DP Fundamentals

## Key Ideas

- Dynamic programming applies when the problem has overlapping subproblems and a recurrence whose subresults can be reused instead of recomputed.
- A correct DP solution starts with the state definition; if the state omits information needed for future decisions, the whole recurrence becomes invalid.
- Top-down memoization and bottom-up tabulation compute the same subproblem graph in different orders, so the better choice depends on dependency structure, stack depth, and implementation clarity.
- The standard time bound for DP is `number of states × transitions per state`, but space can often be reduced when each layer depends only on a small previous frontier.
- Reconstructing the actual solution usually requires storing choices or parent pointers; computing only the optimal value is a different task.

## 1. What It Is

Dynamic programming (DP) is a method for solving problems by decomposing them into smaller subproblems, solving each distinct subproblem once, and reusing those results. It is most effective when naive recursion repeats the same work many times.

DP is commonly used for optimization, counting, feasibility, and sequence problems. Classic examples include knapsack, longest common subsequence, edit distance, matrix-chain multiplication, weighted interval scheduling, and shortest paths in acyclic graphs. In each case, the core challenge is to represent partial progress with a state and connect states through a recurrence.

### 1.1 Core Definitions

- A **subproblem** is a smaller instance that contributes to the solution of a larger problem.
- A **state** is the minimal information needed to identify a subproblem uniquely.
- A **recurrence** defines the value of a state in terms of smaller states.
- A **base case** is a state whose answer is known directly, without recursion.
- **Memoization** is top-down recursion with caching.
- **Tabulation** is bottom-up evaluation in an order that satisfies all dependencies.
- A problem has **optimal substructure** if an optimal solution can be expressed in terms of optimal solutions to subproblems.
- A problem has **overlapping subproblems** if the same subproblems appear repeatedly in a naive recursive solution.

### 1.2 Why This Matters

Without DP, many recursive formulations are exponential because they recompute the same subproblems over and over. With DP, those repeated calls collapse into a polynomial-size table or cache. That difference often changes a problem from infeasible to routine.

For example, the naive Fibonacci recursion is exponential, but the DP version is linear. More importantly, DP provides a general design pattern: define the right state, write the recurrence, prove correctness, and then analyze complexity from the state graph. This pattern appears throughout algorithms, machine learning, bioinformatics, and combinatorial optimization. For the next step after this page, see [DP State Design Patterns](07-dp-state-design-patterns.md).

## 2. The DP Design Recipe

### 2.1 Define the State

The state must encode exactly the information needed to continue the computation correctly.

Examples:

- In Fibonacci, the state is just the index `n`.
- In longest common subsequence, the state is often a pair `(i, j)` representing prefixes of two strings.
- In 0/1 knapsack, the state might be `(i, w)`, meaning the best value using the first `i` items with capacity `w`.

A weak state definition is the most common reason DP solutions fail. If two situations that require different future decisions are mapped to the same state, the recurrence becomes incorrect.

### 2.2 Write the Recurrence

Once the state is defined, specify how to compute each state from smaller ones.

The recurrence should answer: if I know the optimal answers to smaller states, how do I derive the answer to this state?

For Fibonacci:

```text
F(n) = F(n - 1) + F(n - 2)
```

with base cases:

```text
F(0) = 0
F(1) = 1
```

For optimization problems, the recurrence often involves `min` or `max`. For counting problems, it often involves addition. For feasibility problems, it often involves logical `or` or `and`.

### 2.3 Choose an Evaluation Order

A top-down solution evaluates states only when needed. A bottom-up solution computes states in a dependency-safe order.

Top-down memoization is useful when:

- only a fraction of the state space is needed,
- the recurrence is easiest to express recursively,
- or the dependency graph is irregular.

Bottom-up tabulation is useful when:

- all states are needed anyway,
- recursion depth may be large,
- or a clean iteration order exists.

### 2.4 Recover the Solution if Needed

Some problems ask only for the optimal value. Others ask for the actual object, such as the chosen items, path, subsequence, or parenthesization.

If reconstruction is required, the DP usually stores one of the following:

- parent pointers,
- the selected transition,
- or enough information to recompute the choice during a backward pass.

## 3. Top-Down vs Bottom-Up

### 3.1 Top-Down Memoization

Memoization starts from the original problem and recursively explores dependencies. Before solving a state, it checks whether the answer is already cached.

Advantages:

- mirrors the recurrence directly,
- often easier to write correctly first,
- avoids computing unreachable states.

Disadvantages:

- recursion overhead,
- possible stack overflow for deep recursion,
- harder to optimize memory layout.

### 3.2 Bottom-Up Tabulation

Tabulation fills a table so that when a state is processed, all states it depends on are already available.

Advantages:

- no recursion overhead,
- predictable memory access,
- easier to compress space by keeping only recent layers.

Disadvantages:

- may compute states that are never needed,
- requires a correct dependency order, which can be subtle.

### 3.3 Space Compression

Many DPs depend only on the previous row, column, or layer. In those cases, the full table is not necessary.

Examples:

- Fibonacci needs only the previous two values.
- Some sequence DPs need only the previous row.
- Some knapsack variants can use a 1D array with careful iteration order.

**Why this matters:** space optimization is not automatic. Compressing the table is valid only when overwritten values are no longer needed later in the same iteration.

## 4. Worked Example

Consider Fibonacci numbers defined by:

```text
F(0) = 0
F(1) = 1
F(n) = F(n - 1) + F(n - 2) for n >= 2
```

We want to compute `F(6)`.

### 4.1 Naive Recursive Structure

Without memoization, the recursion expands like this:

```text
F(6)
├─ F(5)
│  ├─ F(4)
│  │  ├─ F(3)
│  │  └─ F(2)
│  └─ F(3)
└─ F(4)
   ├─ F(3)
   └─ F(2)
```

Notice that `F(4)`, `F(3)`, and `F(2)` are recomputed multiple times. This is the overlap DP is designed to eliminate.

### 4.2 Bottom-Up Table

Compute values from smallest state upward.

| `n` | `F(n)` | Reason |
|---|---:|---|
| 0 | 0 | base case |
| 1 | 1 | base case |
| 2 | 1 | `F(1) + F(0) = 1 + 0` |
| 3 | 2 | `F(2) + F(1) = 1 + 1` |
| 4 | 3 | `F(3) + F(2) = 2 + 1` |
| 5 | 5 | `F(4) + F(3) = 3 + 2` |
| 6 | 8 | `F(5) + F(4) = 5 + 3` |

So:

```text
F(6) = 8
```

### 4.3 Complexity Interpretation

There are `n + 1` states from `0` through `n`.
Each state after the base cases uses `O(1)` transitions.
Therefore:

```text
time = O(n)
space = O(n)
```

If we keep only the previous two values, space becomes:

```text
space = O(1)
```

Verification: the bottom-up table gives `F(6) = 8`, matching the standard Fibonacci sequence `0, 1, 1, 2, 3, 5, 8`. Correct.

## 5. Pseudocode Patterns

### 5.1 Top-Down Memoization

```text
procedure fib_memo(n, memo):
    if n in memo:
        return memo[n]
    if n == 0:
        return 0
    if n == 1:
        return 1
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

Time: `O(n)` in all cases for Fibonacci because each state `0..n` is computed once. Space: `O(n)` for the memo table and recursion stack.

### 5.2 Bottom-Up Tabulation

```text
procedure fib_tab(n):
    if n == 0:
        return 0
    dp = array of length n + 1
    dp[0] = 0
    dp[1] = 1
    for i = 2 to n:
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

Time: `O(n)` in all cases. Space: `O(n)`.

### 5.3 Space-Compressed Version

```text
procedure fib_rolling(n):
    if n == 0:
        return 0
    prev2 = 0
    prev1 = 1
    for i = 2 to n:
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1
```

Time: `O(n)` in all cases. Space: `O(1)`.

## 6. Common Mistakes

1. **State definition loss.** Defining a state that omits information needed for future choices merges distinct subproblems and makes the recurrence incorrect.
2. **Recursion without memoization.** Writing the recurrence recursively but forgetting the cache leaves the algorithm exponential instead of dynamic-programming-based.
3. **Dependency-order violation.** Filling a table before all prerequisite states are available causes bottom-up code to read uninitialized or stale values.
4. **Incorrect base cases.** A recurrence can be logically correct but still fail completely if the base cases do not match the problem definition or indexing scheme.
5. **Value-only reconstruction gap.** Computing only the optimal value and then expecting to recover the actual solution later without stored choices leads to incomplete outputs.

## 7. Practical Checklist

- [ ] Write the state in one sentence before writing any code.
- [ ] Verify that different future decisions are never forced into the same state.
- [ ] List the base cases explicitly and test them separately.
- [ ] State the recurrence and identify how many transitions each state examines.
- [ ] Choose top-down or bottom-up based on dependency structure, not habit.
- [ ] Check whether space compression is valid before overwriting previous states.
- [ ] Decide early whether the task needs only the optimal value or also solution reconstruction.

## References

- Bellman, Richard. 1957. *Dynamic Programming*. Princeton University Press. <https://press.princeton.edu/books/hardcover/9780691651873/dynamic-programming>
- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Kleinberg, Jon, and Eva Tardos. 2021. *Algorithm Design*. Pearson. <https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003259/9780137546350>
- Erickson, Jeff. 2019. *Algorithms*. <https://jeffe.cs.illinois.edu/teaching/algorithms/>
- Erickson, Jeff. *Dynamic Programming* chapter PDF. <https://jeffe.cs.illinois.edu/teaching/algorithms/book/03-dynprog.pdf>
- Sedgewick, Robert, and Kevin Wayne. 2011. *Algorithms* (4th ed.). Addison-Wesley. <https://algs4.cs.princeton.edu/home/>
