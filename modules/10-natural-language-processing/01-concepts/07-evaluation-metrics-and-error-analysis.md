# Evaluation Metrics and Error Analysis

## Key Ideas

- NLP evaluation must match the task because classification, retrieval, tagging, and generation each fail in different ways.
- A single aggregate score can hide systematic weakness on important slices such as minority classes, long documents, or domain-specific terminology.
- Error analysis complements metrics by showing why a model fails rather than only how often it fails.
- Good evaluation requires a clean split strategy and frozen test set assumptions, or improvements may be artifacts of leakage.
- Model selection should consider calibration, latency, cost, and safety alongside task metrics when the system will be deployed.

## 1. Why Evaluation Is Hard in NLP

Natural language tasks often involve ambiguity, class imbalance, multiple valid outputs, and changing user goals. That makes evaluation more subtle than simply reporting accuracy.

For example:

- a classifier may have high accuracy because one class dominates
- a retriever may return relevant items, but too low in the ranking
- a generator may produce fluent text that is factually wrong

The metric must reflect what success means operationally.

## 2. Task-Specific Metrics

### 2.1 Classification

Common metrics include:

- accuracy
- precision
- recall
- F1 score

### 2.2 Retrieval

Common metrics include:

- precision@k
- recall@k
- mean reciprocal rank
- normalized discounted cumulative gain

### 2.3 Generation

Common metrics may include:

- BLEU
- ROUGE
- exact match
- human judgment

Automatic generation metrics are useful, but they rarely capture full task quality by themselves.

## 3. Error Analysis Workflow

Error analysis means reading failures systematically and grouping them into categories. Useful categories include:

- label confusion
- domain mismatch
- tokenization errors
- retrieval misses
- hallucinated generation

This step often reveals improvements that aggregate metrics do not suggest directly.

## 4. Worked Example: Why Accuracy Is Misleading

Suppose a ticket classifier predicts whether a ticket is `billing` or `general`.

Test set:

```text
90 general
10 billing
```

Model A predicts every ticket as `general`.

### 4.1 Accuracy

```text
accuracy = 90 / 100 = 0.90
```

That looks strong.

### 4.2 Billing Recall

```text
true billing predicted as billing = 0
billing recall = 0 / 10 = 0
```

### 4.3 Interpretation

If the operational goal is to route billing issues correctly, this model is unusable despite 90% accuracy.

Verification: the example shows that class imbalance can make accuracy appear strong while the metric that matters for the rare class is actually zero.

## 5. Evaluation Design Principles

Strong evaluation practice includes:

- separate train, validation, and test data
- stable metric definitions
- slice-based reporting
- qualitative review of representative errors
- task-aware acceptance criteria

The test set should answer "does this system meet the real objective?" not merely "did the loss decrease?"

## 6. Common Mistakes

1. **Metric mismatch.** Optimizing a metric that does not reflect the real product goal leads to false progress; choose metrics based on operational impact.
2. **Leakage in splits.** Allowing near-duplicate or future data across splits inflates reported quality; enforce realistic split boundaries.
3. **Aggregate-only reporting.** Looking only at one score hides important subpopulation failures; add slices by class, source, length, or domain.
4. **No qualitative review.** Ignoring concrete failures makes it hard to improve the system intelligently; inspect real examples regularly.
5. **Frozen-benchmark illusion.** Treating one benchmark score as complete validation ignores changing production distributions; reevaluate with live-like data too.

## 7. Practical Checklist

- [ ] Define success metrics that match the task and deployment objective.
- [ ] Keep train, validation, and test splits clean and stable.
- [ ] Report both aggregate and slice-level metrics.
- [ ] Maintain an error taxonomy and review examples from each bucket.
- [ ] Track calibration, latency, and cost when they affect production quality.
- [ ] Re-run evaluation whenever tokenization, prompting, or retrieval changes materially.

## 8. References

- Manning, Christopher D., Prabhakar Raghavan, and Hinrich Schutze. *Introduction to Information Retrieval*. Cambridge University Press, 2008. <https://nlp.stanford.edu/IR-book/>
- Sokolova, Marina, and Guy Lapalme. "A Systematic Analysis of Performance Measures for Classification Tasks." 2009. <https://link.springer.com/article/10.1007/s10994-009-5119-5>
- Papineni, Kishore, et al. "BLEU: a Method for Automatic Evaluation of Machine Translation." 2002. <https://aclanthology.org/P02-1040/>
- Lin, Chin-Yew. "ROUGE: A Package for Automatic Evaluation of Summaries." 2004. <https://aclanthology.org/W04-1013/>
- Ribeiro, Marco Tulio, Tongshuang Wu, Carlos Guestrin, and Sameer Singh. "Beyond Accuracy: Behavioral Testing of NLP Models with CheckList." 2020. <https://aclanthology.org/2020.acl-main.442/>
- Jurafsky, Daniel, and James H. Martin. *Speech and Language Processing* (3rd draft). <https://web.stanford.edu/~jurafsky/slp3/>
- Stanford CRFM. "Holistic Evaluation of Language Models." <https://crfm.stanford.edu/helm/latest/>
