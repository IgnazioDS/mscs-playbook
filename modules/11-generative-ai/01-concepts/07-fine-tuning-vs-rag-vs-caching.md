# Fine-Tuning vs RAG vs Caching

## Key Ideas

- Fine-tuning, retrieval-augmented generation, and caching solve different system problems and should not be treated as interchangeable upgrades.
- Fine-tuning adapts model behavior, RAG injects external knowledge at inference time, and caching avoids repeating previously solved work.
- The right choice depends on task stability, data freshness, latency targets, supervision quality, and cost constraints.
- Hybrid systems are common because behavior control, knowledge grounding, and cost reduction are separate concerns.
- Choosing among these levers should be driven by evaluation evidence, not by general fashion or architecture habit.

## 1. Three Different Levers

These techniques improve generative systems in different ways:

- **Fine-tuning** changes the model's weights.
- **RAG** changes the context supplied at inference time.
- **Caching** changes whether the system needs to call the model at all for repeated work.

The engineering mistake is to ask "which one is best?" without first defining the actual bottleneck.

## 2. When Each Lever Fits

### 2.1 Fine-Tuning

Useful when:

- the task is stable
- high-quality supervision exists
- output style or task consistency is the main issue

### 2.2 RAG

Useful when:

- knowledge changes often
- answers must cite current or private sources
- prompt-time evidence matters more than weight adaptation

### 2.3 Caching

Useful when:

- many requests repeat exactly or semantically
- latency and cost matter strongly
- acceptable staleness windows can be defined

## 3. Worked Example: Choose the Right Lever

Suppose a company has an internal support assistant with these properties:

- policy documents update weekly
- users frequently ask repeated password-reset questions
- output must follow a fixed troubleshooting template

### 3.1 Fresh Knowledge

Weekly policy changes suggest RAG, because retrieval can expose the newest documents without retraining.

### 3.2 Repeated Questions

Frequent identical password-reset requests suggest caching, because repeated answers can be served faster and more cheaply if freshness rules allow it.

### 3.3 Stable Response Shape

If prompting alone cannot reliably enforce the troubleshooting template, fine-tuning may help with output consistency.

Verification: RAG solves the freshness problem, caching solves the repetition-cost problem, and fine-tuning addresses stable behavior rather than document recency.

## 4. Why Evaluation Must Drive the Choice

Before choosing any lever, measure:

- where failures come from
- how often requests repeat
- how quickly knowledge changes
- how expensive the current path is

If retrieval recall is low, fine-tuning will not fix missing evidence. If outputs are stable but expensive, caching may help more than any model change. If prompts already perform well, fine-tuning may be unnecessary.

## 5. Hybrid Designs

Many effective production systems use all three:

- caching for common answers
- RAG for up-to-date or private knowledge
- fine-tuning for stable behavior patterns

The important design question is which problem each component is supposed to solve and how it will be evaluated over time.

## 6. Common Mistakes

1. **Lever confusion.** Using fine-tuning to solve freshness or retrieval to solve behavior consistency misaligns the tool with the problem; identify the bottleneck first.
2. **No cache policy.** Caching without expiration or invalidation can return outdated answers; define freshness and invalidation rules explicitly.
3. **Weak supervision.** Fine-tuning on noisy or inconsistent examples can degrade behavior; audit data quality before training.
4. **RAG faith without recall.** Assuming retrieval helps without measuring it hides whether relevant evidence is actually found; evaluate retrieval independently.
5. **Architecture cargo cult.** Copying a hybrid system without evidence adds complexity and cost; introduce each lever only when it addresses a measured need.

## 7. Practical Checklist

- [ ] Define whether the current bottleneck is behavior, knowledge, or cost.
- [ ] Measure retrieval recall before relying on RAG.
- [ ] Audit training labels before committing to fine-tuning.
- [ ] Add cache keys, freshness rules, and invalidation policy before deploying caching.
- [ ] Compare the levers on the same eval set and latency budget.
- [ ] Document why each lever exists in the architecture.

## 8. References

- Lewis, Patrick, et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." 2020. <https://arxiv.org/abs/2005.11401>
- Hu, Edward J., et al. "LoRA: Low-Rank Adaptation of Large Language Models." 2022. <https://arxiv.org/abs/2106.09685>
- Karpukhin, Vladimir, et al. "Dense Passage Retrieval for Open-Domain Question Answering." 2020. <https://aclanthology.org/2020.emnlp-main.550/>
- OpenAI. "Fine-tuning guides." <https://platform.openai.com/docs/guides/fine-tuning>
- Gao, Yunfan, et al. "Retrieval-Augmented Generation for Large Language Models: A Survey." 2023. <https://arxiv.org/abs/2312.10997>
- Anthropic. "Prompt caching and system design documentation." <https://docs.anthropic.com/>
- Stanford CRFM. "Foundation model systems resources." <https://crfm.stanford.edu/>
