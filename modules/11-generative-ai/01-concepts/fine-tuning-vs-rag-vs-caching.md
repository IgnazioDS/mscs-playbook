# Fine-Tuning vs RAG vs Caching

## Overview
These three levers address accuracy, latency, and cost in different ways: fine-
tuning adapts behavior, RAG grounds knowledge, and caching avoids repeated work.

## Why it matters
Choosing the right lever avoids unnecessary training costs and improves system
reliability.

## Key ideas
- Fine-tuning helps with style, domain language, and task consistency
- RAG helps with up-to-date or proprietary knowledge
- Caching reduces latency and cost for repeat queries
- Hybrid systems often combine all three

## Practical workflow
- Start with prompting and RAG before fine-tuning
- Fine-tune only after you have stable data and evals
- Add semantic and exact-match caches for frequent prompts
- Re-evaluate when data changes or model versions update

## Failure modes
- Fine-tuning on noisy data amplifies errors
- RAG without good retrieval degrades accuracy
- Cache staleness returns outdated answers
- Over-optimization for cost reduces quality

## Checklist
- Define success metrics before choosing a lever
- Track data freshness for RAG and cache invalidation
- Use evals to compare prompting, RAG, and fine-tuning
- Document why each lever is used

## References
- RAG: Retrieval-Augmented Generation — https://arxiv.org/abs/2005.11401
- LoRA: Low-Rank Adaptation — https://arxiv.org/abs/2106.09685
