# Embeddings and Retrieval Foundations

## Key Ideas

- Embeddings convert text into dense vectors so semantically related items can be retrieved even when they do not share exact keywords.
- Retrieval quality depends on representation, chunking, metadata, and index design rather than on vector search alone.
- Similarity search provides candidate context, but application quality depends on whether those candidates are relevant, fresh, and authorized for the user.
- Embedding-based retrieval complements lexical search because semantic similarity and exact keyword matching fail in different ways.
- A retrieval pipeline must be evaluated independently before it is trusted to ground generation.

## 1. Why Retrieval Matters in Generative Systems

LLMs are good at language generation but limited by context windows and stale knowledge. Retrieval addresses that by fetching external material at inference time and injecting it into the prompt.

This changes the system from:

- "answer from internal model memory only"

to:

- "answer from the model plus current external context"

That is a powerful shift, but it works only if retrieval itself is strong.

## 2. Embedding Basics

An **embedding** is a dense vector representation of text. Nearby vectors are intended to indicate similar meaning.

Common retrieval steps:

1. convert documents into embeddings
2. store them in an index
3. embed the query
4. retrieve nearest neighbors by similarity

The system may also use metadata filters such as source, recency, tenant, or document type.

## 3. Similarity and Indexing

Dense retrieval often uses cosine similarity or dot product. To scale search, systems use approximate nearest neighbor indexes rather than exhaustive comparisons across every vector.

Important practical ideas:

- index freshness
- embedding version compatibility
- metadata filtering
- hybrid retrieval with lexical signals

These matter because semantic similarity alone cannot enforce permissions, freshness, or exact product-code matching.

## 4. Worked Example: Dense Retrieval Ranking

Suppose a system stores three document chunks with simplified 2D embeddings:

```text
d1 = [0.9, 0.8]   password reset instructions
d2 = [0.8, 0.7]   account login troubleshooting
d3 = [-0.6, 0.2]  invoice payment dispute
```

A user query `"reset my password"` has embedding:

```text
q = [0.85, 0.75]
```

### 4.1 Distances

```text
dist(q, d1) = sqrt((0.85 - 0.9)^2 + (0.75 - 0.8)^2)
            = sqrt(0.0025 + 0.0025)
            ≈ 0.071

dist(q, d2) = sqrt((0.85 - 0.8)^2 + (0.75 - 0.7)^2)
            ≈ 0.071

dist(q, d3) = sqrt((0.85 - (-0.6))^2 + (0.75 - 0.2)^2)
            = sqrt(1.45^2 + 0.55^2)
            ≈ 1.551
```

### 4.2 Interpretation

`d1` and `d2` are strong candidates, while `d3` is clearly irrelevant. The retriever should return the first two before any generation step.

Verification: the query embedding is close to the password and login documents and far from the billing document, so the retrieval stage is isolating semantically relevant context.

## 5. Why Retrieval Must Be Measured Separately

If a generative answer is wrong, the root cause may be:

- retrieval failed to fetch the right context
- the model ignored good context
- the context was stale or unauthorized

That is why retrieval should be evaluated with its own query set and relevance labels before it is embedded inside a larger RAG system.

## 6. Common Mistakes

1. **Vector-only thinking.** Assuming embeddings alone solve retrieval ignores permissions, freshness, and exact-match needs; combine semantic retrieval with metadata and sometimes lexical search.
2. **No retriever evals.** Debugging only final answers hides whether retrieval was the bottleneck; measure retrieval recall and ranking directly.
3. **Version mismatch.** Mixing queries and documents embedded by different models or preprocessing pipelines can degrade search silently; version the embedding pipeline.
4. **Filter omission.** Retrieving semantically similar but unauthorized documents is a security bug, not just a ranking bug; apply access filters before generation.
5. **Stale indexes.** Updating source data without reindexing returns outdated evidence; define index refresh rules explicitly.

## 7. Practical Checklist

- [ ] Evaluate retrieval separately from generation.
- [ ] Version embedding models and preprocessing pipelines.
- [ ] Store metadata for authorization, freshness, and citation.
- [ ] Compare dense, sparse, and hybrid retrieval on real queries.
- [ ] Monitor index freshness and re-embedding schedules.
- [ ] Log retrieved items and scores for debugging.

## 8. References

- Reimers, Nils, and Iryna Gurevych. "Sentence-BERT." 2019. <https://arxiv.org/abs/1908.10084>
- Karpukhin, Vladimir, et al. "Dense Passage Retrieval for Open-Domain Question Answering." 2020. <https://aclanthology.org/2020.emnlp-main.550/>
- Lewis, Patrick, et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." 2020. <https://arxiv.org/abs/2005.11401>
- Johnson, Jeff, Matthijs Douze, and Herve Jegou. "Billion-scale similarity search with GPUs." 2019. <https://arxiv.org/abs/1702.08734>
- Manning, Christopher D., Prabhakar Raghavan, and Hinrich Schutze. *Introduction to Information Retrieval*. <https://nlp.stanford.edu/IR-book/>
- Elastic. "Hybrid search." <https://www.elastic.co/guide/en/elasticsearch/reference/current/hybrid-search.html>
- Pinecone. "Vector search fundamentals." <https://www.pinecone.io/learn/>
