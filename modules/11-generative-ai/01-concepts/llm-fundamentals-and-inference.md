# LLM Fundamentals and Inference

## Overview
Large language models (LLMs) predict the next token given a context window and
use sampling to generate text.

## Why it matters
Understanding inference mechanics helps you control latency, cost, and output
quality when building production systems.

## Key ideas
- Tokens are the unit of computation and cost
- Context window limits how much the model can condition on
- Sampling settings (temperature, top-p, top-k) trade off creativity and stability
- System and developer instructions steer behavior more strongly than user text

## Practical workflow
- Estimate token budget for prompts and expected outputs
- Pick a model based on context length, latency, and cost constraints
- Start with conservative sampling, then tune for diversity
- Add stop sequences and output length caps

## Failure modes
- Truncation when prompts exceed the context window
- Overly creative outputs from high temperature
- Repetition or loops from poor sampling settings
- Silent prompt injection from untrusted input

## Checklist
- Track input and output token counts
- Enforce maximum response length
- Validate outputs against a schema or pattern
- Log prompts and responses for debugging

## References
- GPT-3: Language Models are Few-Shot Learners — https://arxiv.org/abs/2005.14165
- InstructGPT — https://arxiv.org/abs/2203.02155
