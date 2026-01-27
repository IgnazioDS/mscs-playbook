# DP Fundamentals

## What it is

Dynamic programming (DP) is a method for solving problems by breaking them into
overlapping subproblems and storing intermediate results.

## Why it matters

DP turns exponential brute force into polynomial time for many optimization and
counting tasks such as knapsack, sequence alignment, and shortest paths.

## Core idea (intuition)

Cache answers to subproblems so each one is solved once, then build the final
solution from those cached results.

## Formal definition

A problem exhibits DP structure when it has optimal substructure and
overlapping subproblems. We define a state, a recurrence (transition), base
cases, and compute an optimal value over states.

## Patterns / common techniques

- Top-down memoization vs bottom-up tabulation
- 1D/2D state compression when only the previous layer is needed
- Reconstructing a solution by storing choices
- Interval DP and subsequence DP for strings and arrays

## Complexity notes

DP typically costs O(number of states * transitions per state) in time and
O(number of states) in memory, often reducible with rolling arrays.

## Pitfalls

- Incorrect state definition that loses needed information
- Missing base cases or invalid transitions
- Using recursion without memoization and hitting timeouts

## References

- Cormen et al., Introduction to Algorithms (DP chapter)
- Competitive Programming 4 (DP patterns)
