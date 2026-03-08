# Regularization and Bias/Variance

## What it is

Regularization constrains model complexity to improve generalization.

## Why it matters

It reduces variance and prevents overfitting while balancing bias.

## Core idea

Add a penalty to the loss (L1/L2) or constrain model capacity.

## Common pitfalls

- Applying heavy regularization and underfitting
- Ignoring feature scaling when using L1/L2
- Using defaults without tuning

## Debug checklist

- Plot learning curves (train vs val error)
- Compare L1 vs L2 effects on coefficients
- Check sensitivity to regularization strength

## References

- *The Elements of Statistical Learning* (Hastie et al.)
- *Deep Learning* (Goodfellow et al.)
