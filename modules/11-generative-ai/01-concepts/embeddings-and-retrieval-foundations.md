# Embeddings and Retrieval Foundations

## Overview
Embeddings map text into vectors so similar meaning clusters in vector space,
enabling semantic search and retrieval.

## Why it matters
Retrieval reduces hallucinations by grounding generation in trusted sources and
improves coverage for domain-specific knowledge.

## Key ideas
- Cosine similarity or dot product measures semantic closeness
- Approximate nearest neighbor (ANN) indexes scale retrieval
- Chunking strategy affects recall and precision
- Metadata filters improve relevance and access control

## Practical workflow
- Normalize and clean text before embedding
- Choose a chunk size that fits the model context window
- Build an ANN index and test recall at k
- Store metadata for filtering and attribution

## Failure modes
- Too-large chunks reduce relevance and introduce noise
- Poor chunk boundaries break semantic coherence
- Stale indexes lead to outdated answers
- Embedding drift after model upgrades

## Checklist
- Evaluate retrieval quality with labeled queries
- Track index freshness and re-embed schedules
- Store source IDs for citation and auditing
- Monitor latency for embedding and ANN search

## References
- Sentence-BERT — https://arxiv.org/abs/1908.10084
- Approximate Nearest Neighbors — https://en.wikipedia.org/wiki/Nearest_neighbor_search
