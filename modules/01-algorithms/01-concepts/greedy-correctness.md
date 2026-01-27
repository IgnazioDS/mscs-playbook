# Greedy Correctness

## What it is

Greedy algorithms build a solution by repeatedly making a locally optimal
choice according to a rule.

## Why it matters

They are often simpler and faster than DP, and they solve many real scheduling,
selection, and routing problems.

## Core idea (intuition)

If a problem has a greedy-choice property, a locally optimal choice can be
extended to a globally optimal solution.

## Formal definition

A problem is greedy-solvable if there exists an ordering of choices such that
selecting the best local choice at each step yields an optimal solution.
Correctness is usually proven via exchange or stays-ahead arguments.

## Patterns / common techniques

- Sort by a key, then take or skip greedily
- Exchange argument: swap to show greedy choice is safe
- Stays-ahead: show partial solution is never worse than optimal
- Use priority queues to always pick the next best option

## Complexity notes

Greedy solutions are commonly O(n log n) due to sorting or heap usage.

## Pitfalls

- Greedy rules that are intuitive but incorrect without proof
- Multiple ties that change behavior if not handled carefully
- Overlooking feasibility constraints after a local choice

## References

- Cormen et al., Introduction to Algorithms (Greedy chapter)
- Kleinberg and Tardos, Algorithm Design
