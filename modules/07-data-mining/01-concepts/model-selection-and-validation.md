# Model Selection and Validation

## What it is
Choosing models and hyperparameters using robust validation strategies that
reduce overfitting and bias.

## Why it matters
Without validation, mining results often reflect noise rather than signal.

## Practical workflow steps
- Define train/validation/test splits
- Use cross-validation where applicable
- Compare models with consistent metrics
- Lock evaluation before final reporting

## Failure modes
- Tuning on the test set
- Inconsistent preprocessing between splits
- Non-reproducible random splits

## Checklist
- Split strategy documented (random, time-based)
- Seeds recorded
- Metrics reported with variance
- Baseline model included

## References
- Elements of Statistical Learning (Hastie et al.) — https://web.stanford.edu/~hastie/ElemStatLearn/
- scikit-learn Model Selection — https://scikit-learn.org/stable/model_selection.html
