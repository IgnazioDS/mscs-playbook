# Safety, Privacy, and Data Handling

## Key Ideas

- Generative AI systems create risks through prompts, retrieved data, tools, memory, logs, and outputs, not only through the model weights.
- Safety engineering includes preventing harmful behavior, constraining unsafe actions, and creating escalation paths when certainty is low.
- Privacy engineering includes minimizing sensitive data exposure, isolating user context, and controlling retention, access, and auditability.
- Data handling rules must cover the full lifecycle of input, retrieval, memory, logs, and outputs because each stage can leak or transform sensitive information.
- Strong safety practice combines technical controls with documentation, monitoring, and review processes rather than relying on a single prompt or filter.

## 1. Why This Is a Core Generative-AI Topic

Generative systems are often connected to user data, internal documents, tools, and workflows. That makes them application systems, not just model demos. If the surrounding system handles data poorly, even a capable model becomes a privacy or safety liability.

Typical risks include:

- prompt injection
- data exfiltration through tool calls
- leakage of sensitive context in logs
- harmful or policy-violating outputs
- cross-user memory contamination

## 2. Safety vs Privacy

These concerns overlap, but they are not identical.

- **Safety** focuses on harmful, misleading, or unauthorized behavior.
- **Privacy** focuses on restricting exposure of personal, confidential, or regulated data.

A system can be privacy-aware but still unsafe, or safe in one task while still leaking sensitive data through logs or retrieval.

## 3. Data Lifecycle View

For a generative system, inspect each stage:

1. input collection
2. preprocessing and redaction
3. retrieval and memory access
4. prompt assembly
5. tool calls
6. output handling
7. logging and retention

This lifecycle view is necessary because the same secret can leak in multiple places even if one stage seems protected.

## 4. Worked Example: Retrieval Privacy Failure

Suppose a support assistant retrieves from an internal knowledge base with documents labeled by tenant:

```text
tenant_a_doc_1
tenant_a_doc_2
tenant_b_doc_1
```

A user from tenant A asks a semantically similar question to one answered in `tenant_b_doc_1`.

### 4.1 Bad Retrieval Design

If the system retrieves purely by similarity without tenant filtering, the top result may be:

```text
tenant_b_doc_1
```

### 4.2 Consequence

Even if the generated answer hides the raw document text, the model has already been given unauthorized content.

### 4.3 Correct Design

Apply tenant filtering before prompt assembly so only tenant A documents are eligible.

Verification: authorization must be enforced at retrieval time because once unauthorized content enters the prompt, the privacy boundary has already been broken.

## 5. Operational Controls That Matter

Practical controls include:

- data minimization
- redaction of sensitive fields
- permission-aware retrieval and tool use
- log scrubbing
- memory retention limits
- red-team testing for injection and abuse

The exact mix depends on whether the system is internal, customer-facing, high-risk, or regulated.

## 6. Common Mistakes

1. **Prompt-only safety.** Relying on a warning inside the prompt does not enforce security or privacy; use application-layer controls for permissions, logging, and retention.
2. **Retrieval blind trust.** Passing retrieved content directly into prompts without authorization checks leaks data; filter and audit retrieval before prompt assembly.
3. **Unsafe logging.** Recording raw prompts, tool results, or memory snapshots can expose secrets later; scrub or minimize logs deliberately.
4. **Shared memory leakage.** Reusing long-term memory across users or tasks creates privacy breaches and answer contamination; isolate storage boundaries explicitly.
5. **One-time review.** Safety risks evolve with prompts, tools, and data; monitor and red-team the system continuously instead of treating launch review as final.

## 7. Practical Checklist

- [ ] Map the full data lifecycle from input to logs and retention.
- [ ] Minimize sensitive data before it reaches prompts or memory.
- [ ] Apply authorization checks during retrieval and tool execution.
- [ ] Scrub or reduce logs that may contain sensitive content.
- [ ] Isolate memory and cached context by user, tenant, or task boundary.
- [ ] Re-run injection and abuse tests after major prompt, tool, or retrieval changes.

## 8. References

- NIST. "AI Risk Management Framework." <https://www.nist.gov/itl/ai-risk-management-framework>
- OWASP. "Top 10 for Large Language Model Applications." <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- Bender, Emily M., et al. "On the Dangers of Stochastic Parrots." 2021. <https://dl.acm.org/doi/10.1145/3442188.3445922>
- Mitchell, Margaret, et al. "Model Cards for Model Reporting." 2019. <https://dl.acm.org/doi/10.1145/3287560.3287596>
- Gebru, Timnit, et al. "Datasheets for Datasets." 2021. <https://arxiv.org/abs/1803.09010>
- Partnership on AI. "Guidance for Safe Foundation Model Deployment." <https://partnershiponai.org/>
- OpenAI. "Safety best practices and policy documentation." <https://platform.openai.com/docs>
