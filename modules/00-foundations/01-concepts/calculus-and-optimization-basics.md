# Calculus and Optimization Basics

## What it is
Differentiation and basic optimization used to minimize loss functions and tune
system parameters.

## Why it matters
Optimization shows up in model training, resource allocation, and tuning system
thresholds for latency or cost.

## Core ideas
- Derivatives as local sensitivity
- Gradients for multivariate functions
- Convex vs non-convex objectives
- Learning rate and convergence intuition

## Example
Given a loss function L(w), gradient descent updates w := w - alpha * grad L(w).

## Pitfalls
- Choosing learning rates that diverge or stall
- Confusing local minima with global minima
- Ignoring scaling of features leading to slow convergence

## References
- Boyd & Vandenberghe, *Convex Optimization*
- Goodfellow et al., *Deep Learning* (optimization chapters)
