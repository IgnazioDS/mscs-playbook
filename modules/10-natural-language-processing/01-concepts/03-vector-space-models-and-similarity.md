# Vector Space Models and Similarity

## Key Ideas

- Vector space models represent documents or queries as numeric vectors so similarity can be computed geometrically.
- Sparse bag-of-words and TF-IDF representations remain strong baselines for retrieval, clustering, and linear classification.
- Similarity measures such as cosine similarity matter because vector magnitude and document length can distort naive comparisons.
- Classical vector spaces provide interpretability and fast iteration, which is why they remain useful even in embedding-heavy systems.
- Vocabulary design, weighting, and normalization choices often matter as much as the similarity formula itself.

## 1. Why Vector Spaces Matter

Many NLP tasks reduce to comparing pieces of text:

- is this ticket like earlier finance tickets?
- which knowledge-base article best matches a query?
- which documents belong in the same cluster?

Vector space models answer those questions by mapping text into coordinates. Once text is numeric, the system can compute similarity, nearest neighbors, and ranking systematically.

## 2. From Bag of Words to TF-IDF

### 2.1 Bag of Words

A **bag-of-words** vector counts how often each vocabulary item appears, ignoring order.

### 2.2 Term Frequency

**Term frequency** measures how often a term appears in a document.

### 2.3 Inverse Document Frequency

**Inverse document frequency** downweights common terms that appear in many documents and carry little discriminative value.

The TF-IDF weight of a term is larger when the term is frequent in one document but rare across the collection.

## 3. Cosine Similarity

Two vectors can be compared by the cosine of the angle between them:

```text
cosine(x, y) = (x · y) / (||x|| ||y||)
```

Cosine similarity is useful because it compares direction rather than raw length. This reduces the effect of document size when vectors are normalized.

## 4. Worked Example: Compare Two Documents

Suppose the vocabulary is:

```text
[refund, payment, shipping]
```

Document A:

```text
"refund payment payment"
```

Document B:

```text
"refund shipping"
```

Query:

```text
"refund payment"
```

### 4.1 Term Count Vectors

```text
A = [1, 2, 0]
B = [1, 0, 1]
Q = [1, 1, 0]
```

### 4.2 Dot Products

```text
Q · A = 1*1 + 1*2 + 0*0 = 3
Q · B = 1*1 + 1*0 + 0*1 = 1
```

### 4.3 Norms

```text
||Q|| = sqrt(1^2 + 1^2) = sqrt(2)
||A|| = sqrt(1^2 + 2^2) = sqrt(5)
||B|| = sqrt(1^2 + 1^2) = sqrt(2)
```

### 4.4 Cosine Similarities

```text
cosine(Q, A) = 3 / sqrt(10) ≈ 0.949
cosine(Q, B) = 1 / 2 = 0.5
```

So document A is the closer match.

Verification: document A ranks above document B because it shares both query terms and gives extra weight to `payment`, which the query also contains.

## 5. When Classical Vector Spaces Still Win

TF-IDF pipelines are often better than expected when:

- data is limited
- interpretability matters
- latency must be low
- the domain uses exact terminology consistently

They are often weaker when semantic similarity depends on paraphrase, world knowledge, or cross-lingual matching. That is where dense embeddings usually help more.

## 6. Common Mistakes

1. **Length bias.** Comparing raw counts without normalization over-rewards long documents; normalize vectors or use cosine similarity.
2. **Vocabulary leakage.** Building the vocabulary on the full dataset leaks evaluation information; fit vectorizers on training data only.
3. **Stopword dogma.** Removing common words blindly can discard task-specific signal; decide stopword handling based on the task.
4. **Similarity misreading.** Treating cosine values as absolute semantic truth overstates what sparse overlap can represent; inspect errors qualitatively too.
5. **Premature replacement.** Abandoning sparse baselines before measuring them can hide whether a more complex model is actually better.

## 7. Practical Checklist

- [ ] Build a sparse baseline before introducing dense retrieval.
- [ ] Fit the vocabulary and IDF statistics on training data only.
- [ ] Normalize vectors before cosine-based ranking.
- [ ] Inspect the top weighted terms in representative documents.
- [ ] Evaluate ranking quality with task-appropriate retrieval metrics.
- [ ] Keep the sparse baseline as a diagnostic comparator during later experiments.

## 8. References

- Manning, Christopher D., Prabhakar Raghavan, and Hinrich Schutze. *Introduction to Information Retrieval*. Cambridge University Press, 2008. <https://nlp.stanford.edu/IR-book/>
- Salton, Gerard, A. Wong, and C. S. Yang. "A Vector Space Model for Automatic Indexing." 1975. <https://dl.acm.org/doi/10.1145/361219.361220>
- Ramos, Juan. "Using TF-IDF to Determine Word Relevance in Document Queries." 2003. <https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=c4fcef9c2fdbeb3bca6b27a5f84f45b9d4d6d474>
- scikit-learn. "Text Feature Extraction." <https://scikit-learn.org/stable/modules/feature_extraction.html>
- Singhal, Amit. "Modern Information Retrieval: A Brief Overview." 2001. <https://ieeexplore.ieee.org/document/989498>
- Witten, Ian H., Alistair Moffat, and Timothy C. Bell. *Managing Gigabytes* (2nd ed.). Morgan Kaufmann, 1999.
- Leskovec, Jure, Anand Rajaraman, and Jeffrey Ullman. *Mining of Massive Datasets* (3rd ed.). Cambridge University Press, 2020. <http://www.mmds.org/>
