# Feature Engineering and Encoding

## What it is

Transforming raw variables into model-ready features using encoding, scaling,
and domain-driven transformations.

## Why it matters

Feature choices often matter more than algorithm choice, especially for
clustering and distance-based methods.

## Practical workflow steps

- Identify categorical vs numeric features
- Apply one-hot encoding for categoricals
- Scale numeric features
- Validate feature ranges and sparsity

## Failure modes

- Encoding leakage from target variables
- High-cardinality categories causing sparse explosions
- Mixing scaled and unscaled features in clustering

## Checklist

- Clear feature list with types
- Encoding strategy documented
- Scaling applied consistently
- Feature count and sparsity tracked

## References

- Feature Engineering for Machine Learning (Zheng, Casari) — <https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/>
- scikit-learn OneHotEncoder — <https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html>
