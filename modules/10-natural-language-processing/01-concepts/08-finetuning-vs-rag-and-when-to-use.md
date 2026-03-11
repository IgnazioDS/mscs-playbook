# Finetuning vs RAG and When to Use

## Key Ideas

- Finetuning changes model behavior by updating weights, while retrieval-augmented generation changes behavior by adding external context at inference time.
- Finetuning is usually better for stable task behavior, style control, or structured outputs when enough quality supervision exists.
- RAG is usually better for changing knowledge, traceability, and access to private or frequently updated corpora.
- The right choice depends on knowledge volatility, latency budget, labeling availability, and operational constraints rather than on trend alone.
- Hybrid systems are common because behavior adaptation and knowledge grounding are different problems.

## 1. Why This Decision Matters

Teams often ask whether they should finetune a model or build retrieval. The deeper question is what problem they are trying to solve.

If the problem is:

- "the model needs domain facts that change weekly," retrieval is often the first answer.
- "the model needs to follow a task-specific output style consistently," finetuning may help more.

These techniques intervene at different levels, so treating them as interchangeable leads to poor system design.

## 2. What Finetuning Changes

**Finetuning** updates the parameters of a pretrained model using task-specific examples.

It is often useful for:

- classification or extraction tasks with labels
- output formatting consistency
- domain-specific instruction following
- reducing prompt complexity for stable tasks

It is weaker when the main challenge is keeping knowledge fresh.

## 3. What RAG Changes

**Retrieval-augmented generation** retrieves external documents or chunks and places them into the prompt or context window before generation.

It is often useful for:

- question answering over evolving documents
- enterprise knowledge access
- source-grounded responses
- controllable knowledge updates without retraining

It is weaker when retrieval quality is low or when the needed behavior is not primarily about knowledge access.

## 4. Worked Example: Choose a Strategy

Suppose a company wants a support assistant that must:

- answer from an internal policy manual updated every week
- cite the section used
- return one of three escalation codes in a fixed JSON schema

### 4.1 Knowledge Requirement

Weekly policy updates strongly favor retrieval because hard-coding that knowledge into weights would become stale quickly.

### 4.2 Behavior Requirement

The fixed JSON schema and escalation codes may benefit from task-specific prompting or finetuning if consistency is poor.

### 4.3 Decision

A sensible first design is:

```text
RAG for policy retrieval
plus
schema-constrained prompting
```

If output consistency remains weak after that, finetuning can be considered for the formatting behavior.

Verification: retrieval solves the freshness and citation problem directly, while finetuning would not by itself make weekly policy knowledge reliable.

## 5. Decision Heuristics

Choose RAG first when:

- knowledge changes frequently
- documents must be cited
- private sources must be injected safely
- retriever quality can be measured and improved

Choose finetuning first when:

- labels exist
- the task is stable
- output behavior is the core issue
- prompt-only control is too fragile or expensive

Use both when the system needs stable behavior and grounded knowledge.

## 6. Common Mistakes

1. **Knowledge-behavior confusion.** Using finetuning to solve stale factual knowledge usually fails operationally; use retrieval when freshness is the core problem.
2. **Retriever neglect.** Blaming generation quality when retrieval recall is poor hides the real bottleneck; measure retrieval independently.
3. **Label-quality blindness.** Finetuning on noisy or inconsistent targets bakes errors into the model; audit supervision quality first.
4. **No source traceability.** Using RAG without citation or chunk inspection makes debugging hard; retain the retrieved evidence path.
5. **False dichotomy.** Assuming only one method can be used ignores hybrid designs; separate behavior control from knowledge access explicitly.

## 7. Practical Checklist

- [ ] Define whether the main problem is knowledge access, behavior control, or both.
- [ ] Measure retrieval recall before judging a RAG pipeline.
- [ ] Audit label quality before committing to finetuning.
- [ ] Compare cost and latency for prompting, retrieval, and finetuned inference.
- [ ] Preserve evidence traces when using retrieval in production.
- [ ] Start with the simpler intervention that addresses the actual bottleneck.

## 8. References

- Lewis, Patrick, et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." 2020. <https://arxiv.org/abs/2005.11401>
- Karpukhin, Vladimir, et al. "Dense Passage Retrieval for Open-Domain Question Answering." 2020. <https://aclanthology.org/2020.emnlp-main.550/>
- Gao, Yunfan, et al. "Retrieval-Augmented Generation for Large Language Models: A Survey." 2023. <https://arxiv.org/abs/2312.10997>
- Hu, Edward J., et al. "LoRA: Low-Rank Adaptation of Large Language Models." 2022. <https://arxiv.org/abs/2106.09685>
- Raffel, Colin, et al. "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer." 2020. <https://jmlr.org/papers/v21/20-074.html>
- Stanford CRFM. "HELM." <https://crfm.stanford.edu/helm/latest/>
- Hugging Face. "Task Guides and Retrieval Documentation." <https://huggingface.co/docs>
