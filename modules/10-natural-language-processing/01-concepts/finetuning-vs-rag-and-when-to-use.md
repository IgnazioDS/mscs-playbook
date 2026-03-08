# Finetuning vs RAG and When to Use

## Overview
Finetuning adapts model weights to a task; RAG augments prompts with retrieved
context. The choice depends on data, latency, and update frequency.

## Why it matters
Choosing the wrong approach increases cost and reduces accuracy.

## Key ideas
- Finetuning: strong for stable tasks with labeled data
- RAG: strong for fresh knowledge and traceability
- Hybrid patterns combine both

## Practical workflow
- Start with retrieval baseline
- Evaluate finetuning if labels are available
- Monitor drift and update cadence

## Failure modes
- RAG retrieval mismatch or poor chunking
- Finetuning on noisy labels
- Latency blowups from retrieval

## Checklist
- Measure retrieval recall
- Track model drift and data freshness
- Compare cost/latency tradeoffs

## References
- RAG (Lewis et al.) — https://arxiv.org/abs/2005.11401
- Finetuning Best Practices — https://platform.openai.com/docs/guides/fine-tuning
