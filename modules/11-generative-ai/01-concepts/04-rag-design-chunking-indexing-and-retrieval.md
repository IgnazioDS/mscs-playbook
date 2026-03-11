# RAG Design: Chunking, Indexing, and Retrieval

## Key Ideas

- Retrieval-augmented generation succeeds only when chunking, indexing, ranking, and prompt assembly work together as one system.
- Chunk size and overlap determine whether relevant information is retrievable without flooding the prompt with noise.
- Hybrid retrieval and reranking often outperform a single retrieval method because exact keywords and semantic similarity capture different relevance signals.
- RAG systems must budget context carefully because too much retrieved text can reduce answer quality instead of improving it.
- Source attribution and retrieval logging are necessary for debugging, governance, and user trust.

## 1. Why RAG Design Is a System Problem

RAG is not "store documents in a vector database and retrieve top-k." The quality of grounded generation depends on multiple coupled decisions:

- how source documents are split
- how chunks are embedded and indexed
- how candidate passages are ranked
- how many passages are sent to the model
- how citations are preserved

Weakness in any one stage can degrade the final answer.

## 2. Chunking Tradeoffs

A **chunk** is a unit of source text stored and retrieved independently.

If chunks are too large:

- retrieval precision drops
- irrelevant context consumes prompt budget

If chunks are too small:

- important context gets fragmented
- citations lose coherence

Overlap can help preserve continuity, but too much overlap causes redundancy and wasted context.

## 3. Indexing and Ranking Choices

Common retrieval choices include:

- dense vector search
- sparse lexical search
- hybrid retrieval
- reranking of the top candidates

Hybrid retrieval helps when exact identifiers, product names, or policy codes matter. Reranking helps when the initial retrieval step has decent recall but weak precision.

## 4. Worked Example: Chunking Budget

Suppose a system has:

- model context budget for retrieval: 1,000 tokens
- average chunk size: 220 tokens
- overlap: 20 tokens
- desired top-k retrieval: 5 chunks

### 4.1 Raw Retrieval Budget

Ignoring metadata wrappers, total retrieved tokens are approximately:

```text
5 * 220 = 1,100
```

This already exceeds the retrieval budget.

### 4.2 Revised Plan

Possible fixes:

- reduce `k` to 4
- shrink chunk size
- rerank and keep only the strongest passages

If `k = 4`:

```text
4 * 220 = 880
```

Now the retrieved context fits inside the 1,000-token retrieval allocation.

Verification: the original top-5 plan exceeds the available retrieval budget, while reducing to 4 chunks makes prompt assembly feasible without truncation.

## 5. Design Questions to Answer Early

Before building a RAG system, decide:

- what corpus is authoritative
- how freshness will be maintained
- how permissions will be enforced
- how retrieval will be evaluated
- what evidence must be cited back to the user

These choices determine whether RAG is a trustworthy grounding mechanism or just a loosely attached search component.

## 6. Common Mistakes

1. **Default chunking.** Using arbitrary chunk sizes without query-based evaluation leads to low recall or noisy prompts; tune chunking on representative retrieval tasks.
2. **Top-k inflation.** Retrieving more passages than the prompt can support adds noise and cost; reserve context deliberately.
3. **No attribution path.** Dropping source IDs during retrieval makes debugging and citation impossible; keep traceable identifiers with each chunk.
4. **Single-stage faith.** Assuming the first retrieval pass is enough wastes easy gains from reranking; add a second ranking stage when precision matters.
5. **Permission gaps.** Retrieving relevant but unauthorized chunks is a system failure; apply tenant and policy filters during retrieval, not after generation.

## 7. Practical Checklist

- [ ] Tune chunk size and overlap on representative retrieval queries.
- [ ] Measure retrieval recall and prompt-fit budget together.
- [ ] Compare dense, sparse, and hybrid retrieval strategies.
- [ ] Preserve source IDs and document metadata through the pipeline.
- [ ] Use reranking when top-k recall is acceptable but precision is weak.
- [ ] Enforce access control before prompt assembly.

## 8. References

- Lewis, Patrick, et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." 2020. <https://arxiv.org/abs/2005.11401>
- Gao, Yunfan, et al. "Retrieval-Augmented Generation for Large Language Models: A Survey." 2023. <https://arxiv.org/abs/2312.10997>
- Karpukhin, Vladimir, et al. "Dense Passage Retrieval for Open-Domain Question Answering." 2020. <https://aclanthology.org/2020.emnlp-main.550/>
- Nogueira, Rodrigo, and Kyunghyun Cho. "Passage Re-ranking with BERT." 2019. <https://arxiv.org/abs/1901.04085>
- Elastic. "Hybrid search." <https://www.elastic.co/guide/en/elasticsearch/reference/current/hybrid-search.html>
- Anthropic. "Building effective retrieval systems." <https://docs.anthropic.com/>
- Pinecone. "RAG best practices." <https://www.pinecone.io/learn/retrieval-augmented-generation/>
