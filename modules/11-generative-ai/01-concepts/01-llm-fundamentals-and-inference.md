# LLM Fundamentals and Inference

## Key Ideas

- A large language model generates text by predicting the next token conditioned on prior tokens in the context window.
- Inference behavior is shaped by tokenization, context limits, decoding strategy, and the instruction hierarchy presented to the model.
- Sampling settings trade off stability and diversity, so output quality depends on choosing decoding behavior that matches the task rather than on maximizing creativity by default.
- Production inference is constrained by latency, token budget, and reliability, not only by model capability.
- Understanding inference mechanics is necessary for diagnosing truncation, repetition, instability, and prompt-injection exposure.

## 1. What an LLM Does During Inference

An LLM receives a sequence of tokens and estimates a probability distribution over the next token. The model then either selects or samples one token, appends it to the context, and repeats the process until it reaches a stop condition.

This means generation is iterative. Even a short response may involve dozens or hundreds of next-token decisions, each conditioned on the evolving context.

### 1.1 Core Terms

- A **token** is the unit of text processed by the model.
- The **context window** is the maximum number of tokens the model can condition on at once.
- **Decoding** is the procedure used to choose the next token from the model's predicted distribution.
- A **stop condition** can be an explicit stop token, length cap, or tool handoff.

## 2. Why Token Budget and Context Matter

Token count drives three practical constraints:

- cost
- latency
- truncation risk

If the prompt plus expected response exceeds the context window, some information must be dropped or the request will fail. This is why production systems often budget tokens explicitly before sending prompts.

Instruction hierarchy also matters. System-level policies and developer instructions typically shape behavior more strongly than user content, so prompt design must account for how trusted and untrusted text are separated.

## 3. Decoding Choices

Common decoding controls include:

- **temperature**, which changes how flat or sharp the sampling distribution is
- **top-p**, which restricts sampling to the smallest probability mass above a threshold
- **top-k**, which restricts sampling to the highest-probability `k` tokens

Lower-variance settings are usually better for deterministic tasks such as extraction or routing. Higher-variance settings can help with brainstorming or creative generation, but they also increase instability.

## 4. Worked Example: Budget a Response

Suppose a support assistant must answer a user question with:

- 900 input tokens of instructions and context
- 700 retrieved tokens
- a model context limit of 2,048 tokens
- a target response cap of 300 tokens

### 4.1 Total Requested Tokens

```text
input_total = 900 + 700 = 1,600
requested_total = 1,600 + 300 = 1,900
```

### 4.2 Remaining Headroom

```text
remaining = 2,048 - 1,900 = 148
```

This request fits, but the margin is small. If retrieval returns one more 250-token chunk, the total becomes:

```text
1,600 + 250 + 300 = 2,150
```

Now the system exceeds the context window and must truncate or reject part of the input.

Verification: the first configuration is valid because `1,900 < 2,048`, while adding one more chunk would force truncation or prompt restructuring.

## 5. Practical Inference Design

A robust inference pipeline typically decides:

- how many tokens to reserve for output
- how to truncate or summarize long context
- which decoding settings match the task
- what schema or stop conditions define a valid answer

This is why inference engineering is not just "call the model." It is the discipline of turning probabilistic generation into controlled application behavior.

## 6. Common Mistakes

1. **Token-budget blindness.** Sending prompts without explicit budget calculations causes truncation and unstable behavior; reserve space for both retrieved context and the response.
2. **Wrong decoding defaults.** Using high temperature for extraction or routing tasks increases error rates; match decoding settings to the task's tolerance for variability.
3. **Instruction mixing.** Blending trusted instructions with untrusted user text makes injection easier; separate roles and delimiters clearly.
4. **Context overstuffing.** Adding every available document to the prompt dilutes relevance and increases latency; include only the context needed to answer.
5. **No stop strategy.** Allowing unconstrained generation raises cost and formatting risk; use response caps, schema validation, or explicit stop conditions.

## 7. Practical Checklist

- [ ] Estimate prompt and response token budgets before inference.
- [ ] Reserve output tokens explicitly instead of filling the whole context window.
- [ ] Choose conservative decoding for deterministic tasks.
- [ ] Separate system, developer, and user content clearly.
- [ ] Add truncation or summarization rules for long context.
- [ ] Log token counts and failure modes for debugging.

## 8. References

- Brown, Tom B., et al. "Language Models are Few-Shot Learners." 2020. <https://arxiv.org/abs/2005.14165>
- Ouyang, Long, et al. "Training language models to follow instructions with human feedback." 2022. <https://arxiv.org/abs/2203.02155>
- Vaswani, Ashish, et al. "Attention Is All You Need." 2017. <https://arxiv.org/abs/1706.03762>
- Jurafsky, Daniel, and James H. Martin. *Speech and Language Processing* (3rd draft). <https://web.stanford.edu/~jurafsky/slp3/>
- OpenAI. "Text generation and prompting guides." <https://platform.openai.com/docs>
- Hugging Face. "Generation strategies." <https://huggingface.co/docs/transformers/generation_strategies>
- Stanford CRFM. "Foundation Models and Evaluation." <https://crfm.stanford.edu/>
