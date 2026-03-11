# Training and Regularization for Vision

## Key Ideas

- Vision model quality depends heavily on training discipline: splits, augmentation, optimization, and regularization often matter more than architecture swaps.
- Regularization reduces overfitting by making the model robust to plausible variation rather than memorizing dataset quirks.
- Vision datasets often contain leakage, imbalance, and annotation noise, so evaluation quality starts with data hygiene.
- Learning-rate schedules, weight decay, label smoothing, and augmentation interact, so they should be tuned as a system rather than independently.
- A small overfit test and strong validation protocol often reveal training issues earlier than long full-scale experiments.

## 1. Why Vision Training Is Tricky

Vision data is expensive to label and often highly correlated. Near-duplicate images, camera-specific artifacts, or biased data collection can make validation numbers look stronger than real deployment performance.

That means strong training practice starts before optimization:

- define realistic splits
- inspect data quality
- choose augmentations that preserve labels

Only then do optimizer settings become meaningful.

## 2. Common Regularization Tools

### 2.1 Data Augmentation

Augmentation is often the most important regularizer in vision because it exposes the model to plausible variation in viewpoint, lighting, crop, or noise.

### 2.2 Weight Decay and Dropout

These constrain the model from relying too heavily on specific parameter values or feature co-adaptations.

### 2.3 Label Smoothing and Reweighting

These can improve generalization, especially in noisy or imbalanced classification settings.

### 2.4 Learning-Rate Scheduling

Warmup, cosine decay, or step schedules often stabilize convergence and improve final quality.

## 3. Split Strategy Matters

Random image-level splits are not always enough. If frames from the same video, products from the same shelf, or scans from the same document source appear in both training and validation, the evaluation may be inflated.

Better split dimensions can include:

- source camera
- time period
- object identity
- site or geography

## 4. Worked Example: Tiny Overfit Test

Suppose a classifier is trained on only 20 images to confirm the pipeline works.

Observed results:

```text
epoch 1 training accuracy = 0.55
epoch 10 training accuracy = 0.70
epoch 30 training accuracy = 0.72
```

### 4.1 Interpretation

If the model cannot nearly memorize 20 clean examples, something is probably wrong:

- labels may be mismatched
- preprocessing may be inconsistent
- learning rate may be too small or too large
- augmentation may be too strong

### 4.2 Expected Healthy Result

For a simple tiny-overfit check, you would often expect training accuracy to approach:

```text
0.95 to 1.00
```

Verification: failing to overfit a tiny clean subset is a pipeline warning sign, not evidence that the model architecture is inherently weak.

## 5. Balancing Regularization

Too little regularization leads to memorization. Too much regularization leads to underfitting. The right balance depends on:

- dataset size
- label noise
- architecture capacity
- deployment variation

This is why regularization must be tuned against validation behavior rather than applied mechanically from a recipe.

## 6. Common Mistakes

1. **Split leakage.** Letting near-duplicate or related images appear across train and validation inflates quality; split by source or identity when needed.
2. **Augmentation excess.** Using transforms that change labels or destroy key detail turns regularization into data corruption; validate augmentation semantics visually.
3. **No tiny-overfit check.** Skipping a small memorization test makes it harder to catch pipeline bugs early; verify the model can fit a tiny clean subset first.
4. **Schedule neglect.** Using one default learning rate without warmup or decay often destabilizes vision training; tune optimization intentionally.
5. **Aggregate-only monitoring.** Watching only overall loss can hide class imbalance or subgroup collapse; track per-class and slice metrics too.

## 7. Practical Checklist

- [ ] Run a tiny-overfit test before long training jobs.
- [ ] Design splits that reflect deployment variation and prevent leakage.
- [ ] Validate augmentations visually and semantically.
- [ ] Tune learning-rate schedule, weight decay, and augmentation together.
- [ ] Monitor per-class metrics, not only aggregate loss.
- [ ] Record preprocessing and augmentation settings with each experiment.

## 8. References

- Goodfellow, Ian, Yoshua Bengio, and Aaron Courville. *Deep Learning*. MIT Press, 2016. <https://www.deeplearningbook.org/>
- Loshchilov, Ilya, and Frank Hutter. "Decoupled Weight Decay Regularization." 2019. <https://arxiv.org/abs/1711.05101>
- Muller, Rafael, Simon Kornblith, and Geoffrey Hinton. "When Does Label Smoothing Help?" 2019. <https://arxiv.org/abs/1906.02629>
- Zhang, Hongyi, et al. "mixup: Beyond Empirical Risk Minimization." 2018. <https://arxiv.org/abs/1710.09412>
- Yun, Sangdoo, et al. "CutMix." 2019. <https://arxiv.org/abs/1905.04899>
- Shorten, Connor, and Taghi M. Khoshgoftaar. "A survey on Image Data Augmentation for Deep Learning." 2019. <https://arxiv.org/abs/1902.06110>
- fastai. "A Recipe for Training Neural Networks." <https://course.fast.ai/>
