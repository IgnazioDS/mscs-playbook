# Vector Space Models and Similarity

## Overview
Vector space models represent documents as vectors and compare them via
similarity measures.

## Why it matters
They are the foundation for search, clustering, and retrieval baselines.

## Key ideas
- Bag-of-words and TF-IDF
- Cosine similarity
- Sparse vs dense representations

## Practical workflow
- Build vocabulary and compute TF-IDF
- Normalize vectors
- Evaluate with retrieval metrics

## Failure modes
- Vocabulary mismatch across corpora
- Ignoring stopwords or rare terms incorrectly
- Misinterpreting cosine similarity scale

## Checklist
- Document the vectorization settings
- Use train-only vocabulary for evaluation
- Inspect nearest neighbors for sanity

## References
- Manning et al., IR and Web Search — https://nlp.stanford.edu/IR-book/
- scikit-learn TF-IDF — https://scikit-learn.org/stable/modules/feature_extraction.html
