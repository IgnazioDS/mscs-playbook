# Attention and Transformers

## Overview
Transformers use self-attention to model token interactions in parallel.

## Why it matters
They scale to large datasets and dominate modern NLP tasks.

## Key ideas
- Self-attention computes weighted token interactions
- Positional encoding provides order
- Multi-head attention improves expressiveness

## Practical workflow
- Choose model size and context window
- Fine-tune or use adapters
- Monitor token usage and latency

## Failure modes
- Context length limits cause truncation
- Hallucination in generative tasks
- High compute cost

## Checklist
- Track context window usage
- Evaluate on domain-specific benchmarks
- Monitor latency and cost

## References
- Attention Is All You Need — https://arxiv.org/abs/1706.03762
- The Annotated Transformer — https://nlp.seas.harvard.edu/2018/04/03/attention.html
