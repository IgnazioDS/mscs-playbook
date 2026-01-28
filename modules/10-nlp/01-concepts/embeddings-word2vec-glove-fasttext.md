# Embeddings: Word2Vec, GloVe, FastText

## Overview
Embeddings map tokens to dense vectors that encode semantic similarity.

## Why it matters
Dense representations improve generalization and enable semantic search.

## Key ideas
- Word2Vec: predictive embeddings (CBOW, skip-gram)
- GloVe: global co-occurrence
- FastText: subword information for OOV

## Practical workflow
- Choose pretrained vs train from scratch
- Align embeddings with tokenizer
- Evaluate with similarity or downstream tasks

## Failure modes
- Embeddings misaligned with preprocessing
- Domain mismatch from pretrained vectors
- Bias embedded in training corpora

## Checklist
- Document embedding source and version
- Validate nearest neighbors
- Use consistent tokenization

## References
- Word2Vec — https://arxiv.org/abs/1301.3781
- GloVe — https://nlp.stanford.edu/projects/glove/
- FastText — https://fasttext.cc/docs/en/english-vectors.html
