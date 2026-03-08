# Interpretability and Model Explanation Basics

## Key Ideas

- Interpretability asks how humans can understand a model's behavior, but there is no single notion of explanation that fits every model, audience, or risk setting.
- Global explanations describe broad model behavior, while local explanations describe one prediction or one neighborhood of the input space.
- Intrinsically simple models and post hoc explanation tools solve different problems, so explanation quality depends on what is being explained and for whom.
- Feature importance and explanation methods can be unstable, misleading, or data-distribution dependent, which is why explanations must be validated rather than taken at face value.
- Explanation is not a substitute for evaluation, robustness checks, or fairness analysis; it is one diagnostic tool among several.

## 1. What It Is

Interpretability is the degree to which a human can understand why a model behaves as it does. Model explanation is the practice of producing artifacts, summaries, or local justifications that make model behavior more legible to developers, domain experts, regulators, or affected users.

### 1.1 Core Definitions

- A **global explanation** summarizes model behavior across the input space.
- A **local explanation** describes why one specific prediction was made.
- **Feature importance** estimates how much a feature influences predictions under a chosen definition.
- A **surrogate model** is a simpler model used to approximate a more complex one for explanation purposes.
- **Partial dependence** studies how predictions change as one or more features vary while others are averaged over.
- A **counterfactual explanation** describes how an input would need to change to alter the prediction.

### 1.2 Why This Matters

Models increasingly support consequential decisions in domains where developers must answer questions such as:

- Why was this example scored as high risk?
- Which variables matter most overall?
- Is the model relying on spurious shortcuts?
- Can domain experts challenge the model's reasoning?

Without explanation tools, debugging and governance become much harder. With careless explanation tools, teams can become confidently wrong.

## 2. Main Explanation Modes

### 2.1 Intrinsic Interpretability

Some models are relatively interpretable by construction, such as small decision trees or sparse linear models. Their structure can sometimes be inspected directly.

### 2.2 Post Hoc Explanations

Complex models often require post hoc methods such as:

- permutation importance,
- partial dependence,
- SHAP-style additive attributions,
- or local surrogate explanations.

These methods do not make the model itself simple. They provide a lens on behavior under specific assumptions.

### 2.3 Global vs Local Use Cases

Global explanations help with model auditing and feature review. Local explanations help with case review, debugging, and user-facing justification. Confusing the two leads to incorrect claims such as using one local explanation to summarize the whole model.

## 3. Limits and Failure Modes

Explanations can fail because:

- features are strongly correlated,
- the explanation method is unstable,
- the data distribution at explanation time differs from training,
- or the question being asked does not match the method's semantics.

An importance score is not always causal influence, and a local explanation is not always actionable recourse.

## 4. Worked Example

Suppose a simple linear credit-risk model is:

```text
score = 0.03 * debt_ratio + 2.0 * missed_payments - 0.01 * savings_k
```

For one applicant:

```text
debt_ratio = 40
missed_payments = 1
savings_k = 20
```

### 4.1 Compute the Prediction Score

```text
score = 0.03 * 40 + 2.0 * 1 - 0.01 * 20
score = 1.2 + 2.0 - 0.2
score = 3.0
```

Assume the model classifies scores above `2.5` as high risk.

### 4.2 Interpret Feature Contributions

For this example, the additive contributions are:

```text
debt_ratio contribution = +1.2
missed_payments contribution = +2.0
savings contribution = -0.2
```

The largest positive contribution is the missed-payment feature.

### 4.3 Local Explanation

A local explanation for this one decision is:

```text
The prediction crossed the high-risk threshold mainly because one missed payment
and a high debt ratio outweighed the protective effect of savings.
```

### 4.4 Limits of the Explanation

This explanation is local to this applicant and this linear model. It does not prove causality, and it does not describe how a more complex nonlinear model would behave globally.

Verification: the computed score is `3.0`, which exceeds the `2.5` threshold, and the additive terms show that `+2.0` from missed payments is the largest single upward contribution.

## 5. Pseudocode Pattern

```text
procedure additive_feature_contributions(weights, features):
    contributions = empty_map()
    for feature_name in features:
        contributions[feature_name] = weights[feature_name] * features[feature_name]
    return contributions
```

Time: `Theta(d)` worst case for `d` features in an additive model. Space: `Theta(d)` auxiliary space to store the contribution map.

## 6. Common Mistakes

1. **Explanation-equals-truth thinking.** Treating one explanation method as the ground truth about model reasoning ignores method assumptions and approximation error; validate explanations against other evidence.
2. **Local-global confusion.** Using one local explanation to summarize the whole model overstates what the method can justify; distinguish pointwise explanation from global behavior.
3. **Correlation blindness.** Reading feature importance as causal importance when features are correlated can be deeply misleading; check dependence structure before drawing strong conclusions.
4. **Post hoc overconfidence.** Assuming a complex model is now “interpretable” because one attribution plot exists confuses visualization with understanding; explanation quality must be assessed in context.
5. **Governance substitution.** Using explanation tooling instead of evaluation, robustness checks, or fairness review leaves major risks unaddressed; explanations complement, not replace, broader validation.

## 7. Practical Checklist

- [ ] Decide whether you need a global explanation, a local explanation, or both.
- [ ] Match the explanation method to the model class and the stakeholder question.
- [ ] Test explanation stability across resamples or nearby inputs when possible.
- [ ] Check whether correlated features make importance statements ambiguous.
- [ ] Use explanations to generate hypotheses for debugging, not as automatic proof of correctness.
- [ ] Pair explanation outputs with performance, calibration, and robustness evidence.

## 8. References

- Molnar, Christoph. 2024. *Interpretable Machine Learning* (2nd ed.). <https://christophm.github.io/interpretable-ml-book/>
- Ribeiro, Marco Tulio, Sameer Singh, and Carlos Guestrin. 2016. "Why Should I Trust You?": Explaining the Predictions of Any Classifier. *KDD 2016*. <https://doi.org/10.1145/2939672.2939778>
- Lundberg, Scott M., and Su-In Lee. 2017. A Unified Approach to Interpreting Model Predictions. *NeurIPS 2017*. <https://papers.nips.cc/paper_files/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html>
- Doshi-Velez, Finale, and Been Kim. 2017. Towards A Rigorous Science of Interpretable Machine Learning. arXiv. <https://arxiv.org/abs/1702.08608>
- scikit-learn. 2025. *Inspection*. <https://scikit-learn.org/stable/inspection.html>
- Rudin, Cynthia. 2019. Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead. *Nature Machine Intelligence* 1. <https://doi.org/10.1038/s42256-019-0048-x>
- Murdoch, W. James, et al. 2019. Definitions, Methods, and Applications in Interpretable Machine Learning. *PNAS* 116(44). <https://doi.org/10.1073/pnas.1900654116>
