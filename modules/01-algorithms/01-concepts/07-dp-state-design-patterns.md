# DP State Design Patterns

## Key Ideas

- Dynamic programming succeeds or fails at the state-definition stage, because the recurrence is only correct if the state contains exactly the information needed for future decisions.
- Common DP families recur across problems: prefix states, interval states, knapsack-capacity states, DAG states, and digit or bitmask states.
- A small state is not always a good state; omitting a dependency can make the recurrence invalid even if the table is smaller.
- Transitions, base cases, and reconstruction data should be derived from the state definition rather than added afterward.
- The standard complexity model remains `number of states × transitions per state`, so state design is also complexity design.

## 1. What It Is

This page extends [DP Fundamentals](06-dp-fundamentals.md) by focusing on one question: how do you choose a DP state that is both correct and tractable?

A **state** is the minimal information needed to identify a subproblem uniquely. Different problem families suggest different state shapes. Recognizing those patterns makes new DP problems much easier to design.

## 2. Common State Families

### 2.1 Prefix and suffix states

Sequence problems often use a prefix index `i` or a pair of prefix indices `(i, j)`. The state means “best answer for the first `i` items” or “best answer for prefixes ending at `i` and `j`.”

Examples:

- longest common subsequence,
- edit distance,
- and sequence alignment.

### 2.2 Capacity and resource states

Optimization problems with budgets often use states such as `(i, w)` or `(i, budget)`.

Examples:

- 0/1 knapsack,
- bounded resource allocation,
- and scheduling with capacity limits.

### 2.3 Interval states

When a problem asks about a contiguous segment, an interval state `(l, r)` is natural.

Examples:

- matrix-chain multiplication,
- optimal BST,
- palindrome DP,
- and game problems on subarrays.

### 2.4 Bitmask or subset states

When the subproblem depends on a chosen subset rather than an ordered prefix, a bitmask state is often appropriate.

Examples:

- traveling salesperson on small `n`,
- subset coverage variants,
- and assignment on small sets.

## 3. How to Choose the State

### 3.1 Ask what future choices need to know

A good test is: if two partial histories lead to the same state, must every optimal continuation from that point be the same up to value? If not, the state is missing information.

### 3.2 Keep only decision-relevant information

A state that includes irrelevant history makes the DP too large. For example, if only current capacity matters, storing the exact order of previously chosen items is wasteful.

### 3.3 Derive transitions from the state

Once the state is fixed, transitions should follow directly. If the recurrence feels forced, the state is usually wrong.

## 4. Worked Example

Design a DP for the 0/1 knapsack problem.

Input:

```text
weights = [2, 3, 4]
values = [4, 5, 10]
capacity = 6
```

### 4.1 Choose the state

Let `dp[i][w]` be the maximum value obtainable using the first `i` items with capacity limit `w`.

This state is correct because future choices only need to know:

- which items remain available, captured by `i`, and
- how much capacity remains, captured by `w`.

### 4.2 Write the recurrence

For item `i` with weight `weight_i` and value `value_i`:

- if `weight_i > w`, we cannot take it, so use `dp[i-1][w]`
- otherwise:

```text
dp[i][w] = max(dp[i-1][w], dp[i-1][w - weight_i] + value_i)
```

### 4.3 Trace the table

Items in order:

```text
item 1: weight 2, value 4
item 2: weight 3, value 5
item 3: weight 4, value 10
```

Selected table entries:

- `dp[1][2] = 4`
- `dp[1][6] = 4`
- `dp[2][5] = max(4, 4 + 5) = 9`
- `dp[3][6] = max(dp[2][6], dp[2][2] + 10) = max(9, 4 + 10) = 14`

So the best value is `14`, obtained by taking items `1` and `3`.

Verification: items `1` and `3` have total weight `2 + 4 = 6` and total value `4 + 10 = 14`, matching `dp[3][6]`.

## 5. Pseudocode Pattern

```text
procedure knapsack_dp(weights, values, capacity):
    n = length(weights)
    dp = array of size (n + 1) x (capacity + 1) filled with 0

    for i = 1 to n:
        for w = 0 to capacity:
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                candidate = dp[i - 1][w - weights[i - 1]] + values[i - 1]
                dp[i][w] = max(dp[i][w], candidate)

    return dp[n][capacity]
```

Time: `Theta(nW)` worst case for `n` items and capacity `W`. Space: `Theta(nW)`.

## 6. Common Mistakes

1. **History omission.** Leaving out information that affects future feasibility or reward makes the recurrence incorrect; test whether two different partial histories truly become equivalent in the proposed state.
2. **History overload.** Storing extra order or path details inside the state blows up the table size unnecessarily; keep only decision-relevant information.
3. **Transition-state mismatch.** Writing transitions that require data not present in the state is a sign the state is underspecified; redesign the state before patching the recurrence.
4. **Base-case vagueness.** A state family without explicit smallest states leads to wrong initialization and table garbage; define zero-length, zero-capacity, or single-element cases cleanly.
5. **Value-solution confusion.** Computing only optimal values when the task requires the chosen objects leaves the DP incomplete; store choices or reconstruction information deliberately.

## 7. Practical Checklist

- [ ] Write the state meaning in a complete sentence before writing any recurrence.
- [ ] Check that equal states imply equivalent future decisions.
- [ ] Estimate the total number of states before committing to the design.
- [ ] Derive transitions directly from the state rather than from ad hoc intuition.
- [ ] Define the base cases before filling the table.
- [ ] Decide whether you need value-only output or full-solution reconstruction.

## 8. References

- Bellman, Richard. 1957. *Dynamic Programming*. Princeton University Press. <https://press.princeton.edu/books/hardcover/9780691651873/dynamic-programming>
- Cormen, Thomas H., Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2022. *Introduction to Algorithms* (4th ed.). MIT Press. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>
- Kleinberg, Jon, and Eva Tardos. 2005. *Algorithm Design*. Pearson. <https://www.pearson.com/en-us/subject-catalog/p/algorithm-design/P200000003815>
- Erickson, Jeff. 2023. *Algorithms*. University of Illinois Urbana-Champaign. <https://jeffe.cs.illinois.edu/teaching/algorithms/>
- Dasgupta, Sanjoy, Christos Papadimitriou, and Umesh Vazirani. 2008. *Algorithms*. McGraw-Hill. <https://cseweb.ucsd.edu/~dasgupta/book/index.html>
- Skiena, Steven S. 2020. *The Algorithm Design Manual* (3rd ed.). Springer. <https://www.algorist.com/>
