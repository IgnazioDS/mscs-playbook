# Foundations Cheat Sheet

## Descriptive stats
- Mean: sum(x)/n
- Median: middle value after sorting
- Variance (sample): sum((x - mean)^2)/(n - 1)
- Std dev: sqrt(variance)

## Probability
- P(A|B) = P(A ∩ B) / P(B)
- Bayes: P(A|B) = P(B|A)P(A)/P(B)
- Expected value: E[X] = sum x * P(X=x)

## Distributions
- Bernoulli(p): P(X=1)=p
- Binomial(n,p): number of successes in n trials
- Poisson(λ): count in a time window
- Normal(μ,σ): symmetric around μ

## Linear algebra
- Dot product: a · b = sum(a_i b_i)
- Norm: ||a|| = sqrt(sum(a_i^2))
- Matrix multiply: (m x n) * (n x k) -> (m x k)

## Optimization
- Gradient descent: w := w - alpha * grad L(w)
- Convex: any local minimum is global
- Learning rate too high -> divergence

## Complexity
- O(1): constant
- O(log n): logarithmic
- O(n): linear
- O(n log n): sorting
- O(n^2): nested loops

## Numerical stability
- Avoid subtracting nearly equal numbers
- Use stable variance (two-pass or Welford)
- Compare floats with tolerance

## Unit discipline
- Standardize units internally
- Convert at boundaries
- Label units in code and docs
