# RAG Design: Chunking, Indexing, Retrieval

## Overview
Retrieval-augmented generation (RAG) combines search with generation to ground
responses in external knowledge sources.

## Why it matters
Good RAG design boosts factuality, enables citations, and reduces retraining
needs for fast-changing data.

## Key ideas
- Chunking balances context coverage and relevance
- Indexing strategies include dense, sparse, and hybrid search
- Re-ranking improves top-k relevance
- Query rewriting improves recall for long or vague questions

## Practical workflow
- Define source corpus, freshness SLAs, and permissions
- Start with 300 to 800 token chunks and 10 to 20 percent overlap
- Use hybrid retrieval when keywords matter
- Add a re-ranker before generation for higher precision

## Failure modes
- Overlapping chunks cause redundant context and wasted tokens
- High recall but low precision leads to noisy answers
- Retrieval bias toward popular sources
- Missing citations when sources are not tracked

## Checklist
- Measure recall and precision at k for target queries
- Log retrieved passages with scores for debugging
- Add citation metadata to outputs
- Validate that retrieved content is within the model context window

## References
- RAG: Retrieval-Augmented Generation — https://arxiv.org/abs/2005.11401
- Hybrid Search Overview — https://www.elastic.co/guide/en/elasticsearch/reference/current/hybrid-search.html
