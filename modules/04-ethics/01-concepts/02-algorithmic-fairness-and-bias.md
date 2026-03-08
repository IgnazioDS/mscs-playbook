# Algorithmic Fairness and Bias

## Key Ideas

- Fairness in machine learning is not one thing: demographic parity, equalized odds, calibration, and individual fairness formalize different moral intuitions.
- When base rates differ across groups, important fairness criteria cannot all be satisfied simultaneously by the same imperfect predictor.
- Bias enters before training, during training, and after deployment through labels, proxies, optimization targets, and feedback loops.
- Technical mitigation can reduce measurable disparities, but it cannot by itself repair unjust institutions, bad labels, or unfair policy goals.
- In high-stakes systems, the responsible question is not "is the model fair?" but "fair by which criterion, for which stakeholders, and at what cost?"

## 1. What It Is

Algorithmic fairness studies how predictive systems distribute errors,
opportunities, and burdens across people and groups. The topic matters because
models are often used in settings where an error is not just a wrong number but
a denial of credit, liberty, employment, housing, or medical attention.

### 1.1 Core definitions

Assume binary prediction with protected groups `A` and `B`.

- **Demographic parity** requires `P(Y_hat = 1 | G = A) = P(Y_hat = 1 | G = B)`.
- **Equalized odds** requires equal true-positive and false-positive rates
  across groups: `P(Y_hat = 1 | Y = y, G = A) = P(Y_hat = 1 | Y = y, G = B)`
  for `y in {0, 1}`.
- **Calibration / predictive parity** requires that the same score mean the
  same empirical risk across groups.
- **Individual fairness** requires that similar individuals receive similar
  treatment under a task-relevant similarity metric.

### 1.2 Why fairness is hard

Each definition protects a different moral concern.

- Demographic parity focuses on outcomes.
- Equalized odds focuses on error burdens.
- Calibration focuses on score meaning.
- Individual fairness focuses on consistency between like cases.

The definitions are useful precisely because they differ. They make hidden
value choices explicit.

## 2. Main Fairness Criteria

| Criterion | Mathematical idea | Ethical intuition | Best fit | Main weakness |
| --- | --- | --- | --- | --- |
| Demographic parity | Equal positive decision rates across groups | Benefits and burdens should not be distributed by group membership | Resource allocation or outreach when selection itself is the concern | Can ignore different qualification rates and hide error asymmetry |
| Equalized odds | Equal TPR and FPR across groups | No group should bear systematically worse error rates | High-stakes classification such as recidivism or screening | Often reduces overall accuracy and may conflict with calibration |
| Calibration / predictive parity | Same score implies same realized risk across groups | A score should mean the same thing for everyone | Risk scoring and ranking systems | Compatible with unequal error burdens |
| Individual fairness | Similar people treated similarly | Like cases should be treated alike | When a defensible similarity metric exists | Similarity metric is often the hardest part |

## 3. Why the Criteria Conflict

### 3.1 Equalized odds versus predictive parity

Let `pi_g = P(Y = 1 | G = g)` be the base rate for group `g`. For a classifier
with true-positive rate `TPR` and false-positive rate `FPR`, the positive
predictive value for group `g` is:

```text
PPV_g = (pi_g * TPR) / (pi_g * TPR + (1 - pi_g) * FPR)
```

If equalized odds holds, then `TPR` and `FPR` are the same across groups. If
the base rates `pi_A` and `pi_B` differ and the classifier is imperfect so
`0 < FPR < 1`, then `PPV_A != PPV_B`. So predictive parity fails.

This is the core impossibility result emphasized by Kleinberg et al. and
Chouldechova: when groups have different prevalences, an imperfect risk model
cannot generally be both calibrated and equal-error-rate.

### 3.2 Demographic parity versus calibration

Suppose a calibrated score reflects real risk and one group has a higher base
rate of the target outcome. Using a common threshold on that calibrated score
will usually produce different positive rates. For demographic parity to hold,
the system must either:

- change thresholds by group,
- distort score meaning,
- or intervene before modeling so the underlying opportunity structure changes.

So demographic parity is not a free add-on. It encodes a choice about which
kind of equality matters.

### 3.3 Numerical example

Assume two groups of 100 people each.

Group A:

```text
TP = 40, FP = 10, FN = 10, TN = 40
positive rate = 50 / 100 = 0.50
TPR = 40 / 50 = 0.80
FPR = 10 / 50 = 0.20
PPV = 40 / 50 = 0.80
```

Group B:

```text
TP = 24, FP = 16, FN = 6, TN = 54
positive rate = 40 / 100 = 0.40
TPR = 24 / 30 = 0.80
FPR = 16 / 70 ≈ 0.229
PPV = 24 / 40 = 0.60
```

Interpretation:

- The model is close on equal opportunity because TPR is the same.
- It fails demographic parity because positive rates differ.
- It fails predictive parity because PPV differs sharply.

The same confusion matrices support different fairness verdicts depending on
which criterion is treated as the governing one.

## 4. Sources of Bias and Mitigation

### 4.1 Where bias enters

Bias can enter at multiple stages:

- **Data collection**: underrepresentation, sampling bias, survivorship bias.
- **Labels**: the label itself may encode past discrimination or policing
  patterns rather than ground truth.
- **Features**: proxy variables can recreate protected categories without
  naming them.
- **Optimization**: a single global loss can hide concentrated group harm.
- **Deployment**: feedback loops can make the model train on its own past
  effects.

### 4.2 Technical mitigation

- **Pre-processing**: re-weighting, re-sampling, label review, representation
  repair.
- **In-processing**: fairness constraints, adversarial debiasing,
  regularization against disparity.
- **Post-processing**: threshold adjustment, calibrated equalized odds, human
  review for edge cases.

These methods are useful. None can turn an unjust target variable into a just
one.

## 5. Case Study

**Case: COMPAS recidivism scoring**

**Descriptive register. Situation:**  
The COMPAS risk tool was used to estimate likelihood of reoffending in criminal
justice settings. ProPublica's 2016 investigation reported that Black
defendants were more likely than white defendants to be labeled high risk and
not reoffend, while Northpointe argued the tool was calibrated across groups.
The dispute became a canonical example because both sides were using real but
different fairness criteria.

**Analytical register. Ethical analysis:**  
From a consequentialist perspective, unequal false positives matter because a
false high-risk score can contribute to detention, harsher bail conditions, or
sentencing outcomes with life-changing effects. Even if the model improves some
aggregate predictive accuracy, concentrated error burdens remain ethically
significant.  
From a contractualist perspective, a justice system is difficult to justify if
one demographic group bears systematically higher false accusation costs. Equal
error burdens therefore become morally salient, not just statistically
convenient.  
From a deontological perspective, opaque scoring in a coercive state setting
raises autonomy and due-process concerns. A person subject to the score has a
strong claim to explanation and contestability.

**Analytical register. Competing considerations:**  
The strongest argument for COMPAS-style tools is that structured models can be
more consistent than unaided human judgment, which is itself error-prone and
biased. The strongest argument against uncritical adoption is that consistency
is not enough if the model reproduces unjust labels or distributes coercive
errors in a systematically unequal way.

**Normative register. What a responsible professional would do:**  
Do not treat average predictive performance as sufficient. In high-stakes
settings, publish group-level error rates, state which fairness criterion is
being optimized, provide recourse, and avoid deployment if the target label or
institutional process is itself too biased to justify the model.

## 6. Common Mistakes

1. **Talking about fairness without naming a criterion.** "The model is fair"
   is usually content-free unless the document specifies whether fairness means
   equal error rates, equal selection rates, calibration, or something else.
   The result is teams arguing past one another while believing they disagree
   about facts rather than values.
2. **Assuming historical labels are ground truth.** Arrests, defaults, churn,
   fraud flags, and performance ratings are often institutionally produced
   labels, not neutral facts. If the label is biased, the model can become a
   cleaner way to scale the same injustice.
3. **Optimizing aggregate metrics in high-stakes settings.** AUC or overall
   accuracy can improve while one subgroup absorbs a much worse false-positive
   burden. That is a design failure, not an acceptable side effect.
4. **Treating debiasing as a one-time preprocessing step.** Fairness failures
   often reappear after launch through drift, feedback loops, and policy
   changes. Monitoring is part of fairness work, not a postscript.
5. **Believing technical fixes are the whole answer.** Threshold tuning cannot
   solve a structurally unjust decision process. When the policy target is
   wrong, the right mitigation may be organizational change rather than model
   adjustment.

## 7. Practical Checklist

- [ ] Define the decision, the protected groups, and the relevant harms before
      selecting any fairness metric.
- [ ] Compute base rates, confusion matrices, and score calibration by group,
      not just overall accuracy.
- [ ] Document why a particular fairness criterion is appropriate for this
      domain and what trade-offs it creates with the others.
- [ ] Audit the target label and the highest-importance proxy features for
      historical or institutional bias.
- [ ] Test whether post-deployment feedback loops could amplify current
      disparities.
- [ ] Provide recourse or appeal whenever the system affects credit, liberty,
      employment, housing, health, or education.
- [ ] Re-run fairness evaluation after major data shifts, retraining cycles,
      or policy changes.

## 8. References

- Rawls, John. 1971. *A Theory of Justice*. Harvard University Press.
- Dwork, Cynthia, Moritz Hardt, Toniann Pitassi, Omer Reingold, and Richard Zemel. 2012. Fairness Through Awareness. *ITCS 2012*. <https://doi.org/10.1145/2090236.2090255>
- Hardt, Moritz, Eric Price, and Nati Srebro. 2016. Equality of Opportunity in Supervised Learning. *arXiv*. <https://arxiv.org/abs/1610.02413>
- Kleinberg, Jon, Sendhil Mullainathan, and Manish Raghavan. 2016. Inherent Trade-Offs in the Fair Determination of Risk Scores. *arXiv*. <https://arxiv.org/abs/1609.05807>
- Chouldechova, Alexandra. 2017. Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data* 5(2). <https://doi.org/10.1089/big.2016.0047>
- Buolamwini, Joy, and Timnit Gebru. 2018. Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *FAccT 2018*. <https://doi.org/10.1145/3287560.3287596>
- Dressel, Julia, and Hany Farid. 2018. The Accuracy, Fairness, and Limits of Predicting Recidivism. *Science Advances* 4(1). <https://doi.org/10.1126/sciadv.aao5580>
- Angwin, Julia, Jeff Larson, Surya Mattu, and Lauren Kirchner. 2016. Machine Bias. *ProPublica*. <https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing>
- ACM. 2018. ACM Code of Ethics and Professional Conduct. <https://www.acm.org/code-of-ethics>
