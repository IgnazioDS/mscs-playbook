# Advanced Data Structures Intro

## What it is

Data structures that support efficient queries and updates beyond arrays and
hash tables, such as union-find and segment trees.

## Why it matters

They enable near-linear algorithms for graphs, scheduling, and range queries
that would otherwise be too slow.

## Core idea (intuition)

Maintain extra structure so common operations are logarithmic or inverse
Ackermann time instead of linear.

## Formal definition

A data structure defines a set of operations with stated time bounds, often
amortized, such as union-find with path compression or segment trees with
range aggregation.

## Patterns / common techniques

- Union-find with union by rank and path compression
- Segment trees for range queries with point updates
- Heaps for repeated min/max extraction
- Balanced BSTs for ordered maps and sets

## Complexity notes

- Union-find: near O(1) amortized (inverse Ackermann)
- Segment tree: O(log n) per update/query

## Pitfalls

- Off-by-one indexing in segment trees
- Forgetting path compression or rank in union-find

## References

- Cormen et al., Introduction to Algorithms (Data structures chapters)
- Competitive Programming 4 (Union-find, segment trees)
