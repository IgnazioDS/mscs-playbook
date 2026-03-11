# Embeddings: Word2Vec, GloVe, and FastText

## Key Ideas

- Embeddings map tokens to dense vectors so semantic and syntactic regularities can be learned from distributional patterns.
- Word2Vec learns predictive embeddings from local context, GloVe learns from global co-occurrence statistics, and FastText incorporates subword information.
- Dense embeddings improve generalization over sparse vectors when similar words should share nearby representations.
- Embedding quality depends on corpus domain, tokenization, and objective choice, not just on vector dimension.
- Static embeddings assign one vector per token type, which limits their ability to represent word meaning that changes by context.

## 1. Why Embeddings Matter

Sparse vectors treat each token as unrelated to every other token unless they co-occur explicitly. Embeddings reduce that brittleness by learning continuous representations where similar tokens occupy nearby regions of space.

This makes it easier for downstream models to share information across related words such as:

- `refund` and `reimbursement`
- `ship` and `delivery`
- `doctor` and `physician`

## 2. Distributional Intuition

The guiding idea is the distributional hypothesis: words that appear in similar contexts tend to have similar meanings. Embedding methods operationalize that idea with different training objectives.

### 2.1 Word2Vec

Word2Vec usually appears in two variants:

- **CBOW**, which predicts a center word from context
- **skip-gram**, which predicts context words from a center word

### 2.2 GloVe

GloVe uses a weighted factorization objective over global word co-occurrence counts.

### 2.3 FastText

FastText represents a word through character n-grams as well as the whole token, which helps with morphology and unseen or rare words.

## 3. What Static Embeddings Can and Cannot Do

Static embeddings are efficient and often useful in low-resource settings, but they assign one vector per token type. That means `"bank"` in a finance sentence and `"bank"` in a river sentence usually share one representation.

This limitation is one reason contextual models later became dominant. Still, static embeddings remain useful for:

- lightweight classifiers
- retrieval features
- exploratory nearest-neighbor analysis
- low-compute baselines

## 4. Worked Example: Reason About a Tiny Embedding Space

Suppose a toy system learns three 2D embeddings:

```text
refund = [0.9, 0.8]
reimbursement = [0.8, 0.7]
shipping = [-0.6, 0.2]
```

### 4.1 Compare Similar Terms

Euclidean distance between `refund` and `reimbursement`:

```text
sqrt((0.9 - 0.8)^2 + (0.8 - 0.7)^2)
= sqrt(0.01 + 0.01)
= sqrt(0.02)
≈ 0.141
```

Distance between `refund` and `shipping`:

```text
sqrt((0.9 - (-0.6))^2 + (0.8 - 0.2)^2)
= sqrt(1.5^2 + 0.6^2)
= sqrt(2.25 + 0.36)
= sqrt(2.61)
≈ 1.616
```

### 4.2 Interpretation

`refund` is much closer to `reimbursement` than to `shipping`, so the embedding space captures a semantic relationship that a bag-of-words model would not encode directly.

Verification: the learned geometry makes related financial terms near each other and pushes an unrelated logistics term farther away.

## 5. Choosing Among Word2Vec, GloVe, and FastText

- Choose Word2Vec when local context prediction is a good fit and lightweight training matters.
- Choose GloVe when global co-occurrence structure is important and a strong pretrained resource exists.
- Choose FastText when morphology, misspellings, or unseen words matter more than strict token-level lookup.

In practice, pretrained availability and domain fit often matter more than small theoretical differences.

## 6. Common Mistakes

1. **Domain mismatch.** Using generic pretrained embeddings for specialized language can distort similarity; check nearest neighbors on domain terms before relying on them.
2. **Tokenization drift.** Training or inference with token boundaries that differ from the embedding vocabulary reduces coverage; align preprocessing with embedding assumptions.
3. **Semantic overclaiming.** Reading too much meaning into nearest neighbors can hide corpus bias and frequency effects; validate embeddings on downstream tasks too.
4. **Context blindness.** Expecting static embeddings to solve polysemy ignores their one-vector-per-word limitation; use contextual models when sense variation matters strongly.
5. **OOV neglect.** Ignoring unseen-word behavior causes silent failures; consider subword methods like FastText or explicit unknown-token handling.

## 7. Practical Checklist

- [ ] Check corpus domain alignment before adopting pretrained vectors.
- [ ] Inspect coverage and unknown-token rates on real task data.
- [ ] Verify nearest neighbors for representative domain terms.
- [ ] Keep preprocessing and tokenization consistent with the embedding resource.
- [ ] Use static embeddings as a baseline before assuming a contextual model is necessary.
- [ ] Document vector source, dimension, and training corpus where possible.

## 8. References

- Mikolov, Tomas, et al. "Efficient Estimation of Word Representations in Vector Space." 2013. <https://arxiv.org/abs/1301.3781>
- Mikolov, Tomas, et al. "Distributed Representations of Words and Phrases and their Compositionality." 2013. <https://papers.nips.cc/paper/2013/hash/9aa42b31882ec039965f3c4923ce901b-Abstract.html>
- Pennington, Jeffrey, Richard Socher, and Christopher D. Manning. "GloVe." 2014. <https://aclanthology.org/D14-1162/>
- Bojanowski, Piotr, et al. "Enriching Word Vectors with Subword Information." 2017. <https://aclanthology.org/Q17-1010/>
- FastText. "Pretrained Word Vectors." <https://fasttext.cc/docs/en/english-vectors.html>
- Jurafsky, Daniel, and James H. Martin. *Speech and Language Processing* (3rd draft). <https://web.stanford.edu/~jurafsky/slp3/>
- Stanford NLP Group. "GloVe Project." <https://nlp.stanford.edu/projects/glove/>
