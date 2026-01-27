# Approximation Intro

## What it is

Approximation algorithms provide near-optimal solutions for NP-hard problems
with provable guarantees.

## Why it matters

Exact solutions can be infeasible at scale; approximation gives practical
results with known quality bounds.

## Core idea (intuition)

Relax the problem or use a greedy rule to get a solution that is within a
factor of optimal.

## Formal definition

An algorithm is an r-approximation if for every instance, its solution cost is
within factor r of the optimal (or 1/r for maximization).

## Patterns / common techniques

- Greedy picking with bounded loss
- LP relaxation and rounding
- Primal-dual methods for covering problems

## Complexity notes

Approximation algorithms often run in polynomial time and trade optimality for
speed and scalability.

## Pitfalls

- Confusing approximation ratio with empirical quality
- Guarantees that depend on problem formulation (min vs max)

## References

- Williamson and Shmoys, The Design of Approximation Algorithms
- Vazirani, Approximation Algorithms
