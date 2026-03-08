# Dimensionality Reduction

## Key Ideas

- Dimensionality reduction replaces a high-dimensional representation with a smaller one so that the data becomes easier to model, visualize, or store without discarding the most important structure.
- The main reasons to reduce dimension are noise reduction, compression, visualization, and improved numerical behavior, not merely making a dataset "smaller."
- Linear methods such as principal component analysis preserve variance along orthogonal directions, while nonlinear methods try to preserve other notions of structure.
- Reduction can improve downstream learning, but it can also remove task-relevant signal if the preserved structure is not aligned with the real prediction problem.
- Any fitted reducer must be trained on the training split only, because the reduction parameters are estimated from data and can leak validation information.

## 1. What Dimensionality Reduction Is

Dimensionality reduction maps observations from a space with many features to a space with fewer features. The purpose is to preserve useful structure while discarding redundancy, noise, or inconvenient coordinate systems.

### 1.1 Core Definitions

- A **dimension** is one coordinate or feature in the data representation.
- A **projection** maps data from one vector space to another, often lower-dimensional, space.
- A **principal component** is a direction that captures as much remaining variance as possible subject to orthogonality constraints.
- **Explained variance ratio** is the fraction of total variance captured by a chosen set of principal components.
- A **latent representation** is a reduced internal description of the data.

### 1.2 Why This Matters

High-dimensional data can be noisy, redundant, expensive to store, and difficult to visualize. It can also create numerical instability and make distance-based methods less informative. Dimensionality reduction is therefore both an exploratory tool and a practical engineering tool.

## 2. Main Families of Methods

### 2.1 Linear Reduction

Principal component analysis, singular value decomposition, and related methods search for low-dimensional linear structure. These methods are often appropriate when the important variation lies near a linear subspace.

### 2.2 Nonlinear Reduction

Methods such as t-SNE, UMAP, and autoencoders can preserve neighborhood relationships or learn nonlinear manifolds. These methods are often useful for visualization or expressive representations, but their outputs can be harder to interpret geometrically.

### 2.3 Supervised vs Unsupervised Use

Some reduction is purely unsupervised, such as PCA. Other representations are learned with a downstream prediction objective in mind. The important question is whether the chosen reduction preserves the information the later task actually needs.

## 3. Principal Component Analysis Intuition

### 3.1 What PCA Optimizes

PCA finds orthogonal directions that maximize projected variance one component at a time. The first component captures the largest possible variance, the second captures the largest remaining variance subject to orthogonality, and so on.

### 3.2 Why Variance Can Help

Large variance directions often reflect informative structure rather than measurement noise. This is not guaranteed, but it makes PCA a useful default when redundancy is high and labels are unavailable.

### 3.3 When PCA Fails

PCA can fail when:

- small-variance directions carry the important label signal,
- nonlinear structure dominates,
- features are badly scaled,
- interpretability of components is critical and rotated combinations are hard to explain.

## 4. Worked Example: Two-Dimensional PCA Compression

Suppose centered data contains three observations:

```text
x_1 = (2, 2)
x_2 = (3, 3)
x_3 = (-2, -2)
```

These points lie on the line `y = x`, so almost all variation is along the direction `(1, 1)`.

### 4.1 Normalize the Principal Direction

The first principal direction is:

```text
v_1 = (1 / sqrt(2), 1 / sqrt(2))
```

### 4.2 Project Each Point onto the First Component

For `x_1 = (2, 2)`:

```text
score_1 = x_1 dot v_1
score_1 = 2 * (1 / sqrt(2)) + 2 * (1 / sqrt(2))
score_1 = 4 / sqrt(2) = 2 * sqrt(2)
```

For `x_2 = (3, 3)`:

```text
score_2 = 3 * (1 / sqrt(2)) + 3 * (1 / sqrt(2))
score_2 = 6 / sqrt(2) = 3 * sqrt(2)
```

For `x_3 = (-2, -2)`:

```text
score_3 = -2 * (1 / sqrt(2)) + -2 * (1 / sqrt(2))
score_3 = -4 / sqrt(2) = -2 * sqrt(2)
```

### 4.3 Interpret the Compression

The original two-dimensional points can now be represented approximately by one number each:

```text
x_1 -> 2 * sqrt(2)
x_2 -> 3 * sqrt(2)
x_3 -> -2 * sqrt(2)
```

Because all points lie exactly on one line, no information is lost by reducing from two dimensions to one in this example.

Verification: each projected score preserves the ordering of the original points along the line `y = x`, and because the data lies exactly on that line, one principal component is sufficient to reconstruct the geometric structure.

## 5. Practical Use in a Learning Pipeline

### 5.1 Fit on Training Data Only

If PCA or another reducer is fit before the train-validation split, the learned components absorb information from held-out data and invalidate the evaluation.

### 5.2 Tune the Retained Dimension

The number of retained dimensions is a hyperparameter. It should be chosen using validation performance, explained variance, computational constraints, or interpretability needs.

### 5.3 Distinguish Visualization from Modeling

Two-dimensional visualizations are often helpful, but methods that produce visually separated clusters do not automatically create better features for downstream models. Visualization quality and predictive utility are different objectives.

## 6. Common Mistakes

1. **Variance-equals-signal thinking.** Assuming the highest-variance directions are always the most predictive can remove important low-variance information; check downstream performance instead of relying on intuition alone.
2. **Pre-split fitting.** Fitting PCA or another reducer on the full dataset before validation leaks held-out structure into training; fit the reducer inside the training pipeline only.
3. **Visualization overclaiming.** Treating a clean two-dimensional plot as proof of cluster truth or predictive usefulness confuses exploratory graphics with validated conclusions; use it as a clue, not a verdict.
4. **Overcompression.** Reducing too aggressively can discard task-relevant structure and harm performance; tune the retained dimension rather than selecting it arbitrarily.
5. **Scale neglect.** Applying variance-based reduction to features on incomparable scales distorts the components; standardize when the method assumes comparable feature magnitudes.

## 7. Practical Checklist

- [ ] Clarify whether the goal is compression, denoising, visualization, or downstream prediction support.
- [ ] Standardize numeric features when the reduction method is scale-sensitive.
- [ ] Fit the reduction method on the training split only.
- [ ] Tune the retained number of dimensions using validation evidence.
- [ ] Compare downstream performance with and without reduction.
- [ ] Keep track of how components or embeddings are defined so the pipeline remains reproducible.

## 8. References

- Jolliffe, I. T., and Jorge Cadima. 2016. Principal Component Analysis: A Review and Recent Developments. *Philosophical Transactions of the Royal Society A* 374(2065). <https://doi.org/10.1098/rsta.2015.0202>
- Bishop, Christopher M. 2006. *Pattern Recognition and Machine Learning*. Springer.
- Murphy, Kevin P. 2022. *Probabilistic Machine Learning: An Introduction*. MIT Press.
- Hastie, Trevor, Robert Tibshirani, and Jerome Friedman. 2009. *The Elements of Statistical Learning* (2nd ed.). Springer. <https://hastie.su.domains/ElemStatLearn/>
- Géron, Aurelien. 2022. *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media.
- van der Maaten, Laurens, and Geoffrey Hinton. 2008. Visualizing Data using t-SNE. *Journal of Machine Learning Research* 9. <https://jmlr.org/papers/v9/vandermaaten08a.html>
- McInnes, Leland, John Healy, and James Melville. 2020. UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. <https://arxiv.org/abs/1802.03426>
