# N-grams and Classic Language Models

## Key Ideas

- An n-gram language model estimates the probability of the next token from the previous `n - 1` tokens under a Markov assumption.
- These models are simple, interpretable baselines that make data sparsity and smoothing tradeoffs explicit.
- Smoothing is essential because unseen n-grams are common even in moderately sized corpora, and zero probabilities destroy sequence likelihood estimates.
- Perplexity summarizes how well a model predicts held-out text, but it is meaningful only when tokenization and vocabulary are comparable.
- Classic language models remain useful for baseline reasoning, error analysis, and understanding why modern models need richer context representations.

## 1. Why N-gram Models Matter

Before neural language models, n-grams were the standard way to estimate sequential text probabilities. They remain pedagogically important because they isolate the core predictive problem:

```text
P(w_t | w_1, ..., w_{t-1})
```

An n-gram model approximates that full conditional with only the most recent context:

```text
P(w_t | w_{t-n+1}, ..., w_{t-1})
```

This is a simplifying assumption, but it turns impossible estimation into a count-based problem.

## 2. Counting and Probability Estimation

For a bigram model:

```text
P(w_t | w_{t-1}) = count(w_{t-1}, w_t) / count(w_{t-1})
```

For a trigram model:

```text
P(w_t | w_{t-2}, w_{t-1}) = count(w_{t-2}, w_{t-1}, w_t) / count(w_{t-2}, w_{t-1})
```

As `n` grows, context becomes more specific, but the number of unseen combinations grows quickly too. That is the central sparsity problem.

## 3. Smoothing and Backoff

**Smoothing** redistributes some probability mass from seen events to unseen events.

Common approaches include:

- add-one or Laplace smoothing
- Katz backoff
- Kneser-Ney smoothing

The best classical methods do not simply add small counts everywhere. They try to preserve informative count structure while still reserving probability for unseen sequences.

## 4. Worked Example: Bigram Estimation with Smoothing

Suppose the training corpus is:

```text
<s> i like nlp </s>
<s> i like pizza </s>
<s> i study nlp </s>
```

Assume the vocabulary is:

```text
{<s>, i, like, study, nlp, pizza, </s>}
```

### 4.1 Raw Counts

The token `i` is followed by:

- `like` twice
- `study` once

So:

```text
count(i) = 3
count(i, like) = 2
count(i, study) = 1
count(i, pizza) = 0
```

### 4.2 UnsMoothed Probability

```text
P(like | i) = 2 / 3
P(study | i) = 1 / 3
P(pizza | i) = 0 / 3 = 0
```

### 4.3 Add-One Smoothing

With vocabulary size `V = 7`:

```text
P(pizza | i) = (0 + 1) / (3 + 7) = 1 / 10 = 0.1
P(like | i) = (2 + 1) / (3 + 7) = 3 / 10 = 0.3
```

This avoids zero probability, though add-one smoothing is usually too blunt for strong performance.

Verification: smoothing changes unseen bigrams from impossible to unlikely, which keeps whole-sequence probabilities usable on held-out text.

## 5. Perplexity and Evaluation

**Perplexity** is the exponentiated average negative log probability of held-out tokens. Lower perplexity means the model assigns higher probability to the evaluation text.

Perplexity is useful only when:

- tokenization is fixed
- the vocabulary treatment is comparable
- the evaluation set is separate from training

Comparing perplexity across incompatible tokenizations can be misleading.

## 6. Common Mistakes

1. **Ignoring sparsity.** Using raw maximum-likelihood counts alone produces many zero probabilities; apply smoothing or backoff before evaluation.
2. **Inflating `n` blindly.** Larger context without enough data usually hurts generalization; choose `n` based on corpus size and sparsity, not ambition.
3. **Perplexity misuse.** Comparing perplexity across different vocabularies or tokenizations confuses the metric; keep the evaluation setting fixed.
4. **Train-set evaluation.** Reporting perplexity on the training corpus hides overfitting; evaluate on held-out text.
5. **Baseline dismissal.** Treating n-grams as obsolete misses their diagnostic value; use them to ground expectations and reveal data issues.

## 7. Practical Checklist

- [ ] Start with unigram, bigram, and trigram baselines before moving to complex models.
- [ ] Fit counts on training data only.
- [ ] Choose and document a smoothing method explicitly.
- [ ] Report tokenization and vocabulary treatment alongside perplexity.
- [ ] Inspect frequent and improbable n-grams for data quality issues.
- [ ] Compare classical baselines to neural methods on the same held-out split.

## 8. References

- Jurafsky, Daniel, and James H. Martin. *Speech and Language Processing* (3rd draft). <https://web.stanford.edu/~jurafsky/slp3/>
- Chen, Stanley F., and Joshua Goodman. "An Empirical Study of Smoothing Techniques for Language Modeling." 1999. <https://aclanthology.org/P99-1094/>
- Katz, Slava M. "Estimation of Probabilities from Sparse Data for the Language Model Component of a Speech Recognizer." 1987. <https://aclanthology.org/J87-3002/>
- Kneser, Reinhard, and Hermann Ney. "Improved Backing-Off for M-gram Language Modeling." 1995. <https://ieeexplore.ieee.org/document/479394>
- Manning, Christopher D., and Hinrich Schutze. *Foundations of Statistical Natural Language Processing*. MIT Press, 1999.
- Brants, Thorsten, et al. "Large Language Models in Machine Translation." 2007. <https://aclanthology.org/D07-1090/>
- Stanford NLP. "Speech and Language Processing Draft Chapter on N-gram Language Models." <https://web.stanford.edu/~jurafsky/slp3/3.pdf>
