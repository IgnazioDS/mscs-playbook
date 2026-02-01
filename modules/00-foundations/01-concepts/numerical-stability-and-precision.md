# Numerical Stability and Precision

## What it is
How floating-point arithmetic and finite precision impact computations.

## Why it matters
Small numeric errors can grow into large accuracy issues in statistics, ML, and
simulation pipelines.

## Core ideas
- Floating-point representation and rounding
- Catastrophic cancellation
- Stable vs unstable algorithms

## Example
Computing variance using a single-pass formula can be numerically unstable for
large values; use a stable two-pass or Welford algorithm.

## Pitfalls
- Comparing floats for exact equality
- Summing large and tiny numbers without compensation
- Ignoring units and scaling before optimization

## References
- Higham, *Accuracy and Stability of Numerical Algorithms*
- Goldberg, "What Every Computer Scientist Should Know About Floating-Point"
