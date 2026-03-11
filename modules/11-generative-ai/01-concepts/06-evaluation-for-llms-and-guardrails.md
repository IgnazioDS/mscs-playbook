# Evaluation for LLMs and Guardrails

## Key Ideas

- LLM evaluation must measure task success, factual grounding, format reliability, and safety rather than relying on one benchmark score.
- Guardrails are runtime controls such as schema validation, retrieval checks, tool gating, and policy filters that keep model behavior inside application constraints.
- Offline evaluation catches predictable regressions before release, while online evaluation detects drift and failure modes that only appear in live traffic.
- Good eval design isolates model quality from retrieval, tool, and prompt failures so teams can diagnose the real bottleneck.
- Guardrails should reduce risk without hiding useful signals or silently masking systemic defects.

## 1. Why LLM Evaluation Is Different

Generative systems can fail while still producing fluent text. That makes naive qualitative impressions dangerous. A response may sound confident, obey formatting loosely, and still be factually wrong, unsafe, or unsupported by retrieved evidence.

This is why LLM evaluation must go beyond "did the answer look good?" and define explicit acceptance criteria for the application.

## 2. What to Measure

Useful categories include:

- task completion quality
- factual grounding or citation support
- format validity
- latency and cost
- safety and policy compliance

For RAG systems, retrieval and answer generation should often be measured separately. For tool-using systems, tool-selection accuracy and execution safety also deserve independent checks.

## 3. What Guardrails Do

**Guardrails** are controls applied before, during, or after model generation.

Examples:

- input filtering
- output schema validation
- tool-permission checks
- citation requirements
- refusal and escalation rules

A guardrail is not the same as an eval. The eval tells you how the system behaves. The guardrail constrains what it is allowed to do at runtime.

## 4. Worked Example: Format Guardrail

Suppose a support classifier must return JSON with:

```text
label
confidence
```

One model output is:

```text
The ticket is billing with high confidence.
```

### 4.1 Without a Guardrail

Downstream automation may fail or try to parse the prose heuristically.

### 4.2 With a Guardrail

The system validates the response against the expected schema. Since the response is not valid JSON and lacks the required fields, the application can:

- reject it
- reprompt
- or route to fallback handling

### 4.3 Why This Helps

The guardrail does not make the model smarter. It prevents an invalid response from being treated as if it were production-safe output.

Verification: schema validation catches the invalid prose response before automation uses it, so the failure becomes visible and recoverable instead of silent.

## 5. Evaluation Workflow in Practice

A healthy workflow usually includes:

1. a fixed offline evaluation set
2. automated checks for format, retrieval, and safety
3. qualitative review of failure clusters
4. online monitoring after release

This keeps the team from overfitting to a single benchmark or missing new regressions caused by prompt, model, or retriever changes.

## 6. Common Mistakes

1. **Fluency confusion.** Treating polished language as proof of correctness hides factual and grounding failures; score the properties that matter directly.
2. **Eval bottleneck blur.** Measuring only final answers makes it hard to tell whether retrieval, prompting, or tool use failed; break evaluations into components.
3. **Guardrail overreach.** Using rigid rules that reject many good outputs hurts usefulness; tune guardrails to risk rather than enforcing brittle perfection.
4. **Static-only evaluation.** Relying only on offline tests misses drift in live data; add online monitoring and sampled review.
5. **Unversioned changes.** Updating prompts, models, or retrievers without rerunning evals creates silent regressions; tie every change to evaluation results.

## 7. Practical Checklist

- [ ] Define quality, grounding, format, and safety criteria explicitly.
- [ ] Keep a representative offline eval set under version control.
- [ ] Measure retrieval and tool behavior separately when relevant.
- [ ] Add runtime validation for schemas, citations, and permissions.
- [ ] Review live failures regularly instead of relying only on dashboard aggregates.
- [ ] Re-run evals after every prompt, model, or retrieval change.

## 8. References

- Liang, Percy, et al. "Holistic Evaluation of Language Models." 2023. <https://arxiv.org/abs/2211.09110>
- EleutherAI. "Language Model Evaluation Harness." <https://github.com/EleutherAI/lm-evaluation-harness>
- Ribeiro, Marco Tulio, et al. "Beyond Accuracy: Behavioral Testing of NLP Models with CheckList." 2020. <https://aclanthology.org/2020.acl-main.442/>
- OpenAI. "Evals design and structured outputs guides." <https://platform.openai.com/docs>
- Anthropic. "Evaluating model behavior." <https://docs.anthropic.com/>
- Stanford CRFM. "HELM documentation." <https://crfm.stanford.edu/helm/latest/>
- OWASP. "Top 10 for Large Language Model Applications." <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
