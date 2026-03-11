# Prompting Patterns and Structured Output

## Key Ideas

- Prompting is the practice of specifying task intent, constraints, and context so the model's probabilistic behavior is steered toward reliable outcomes.
- Structured outputs reduce integration risk because downstream code can validate schemas instead of parsing free-form prose heuristically.
- Good prompts separate policy, task instructions, and untrusted input so the model can distinguish what must be obeyed from what must be analyzed.
- Few-shot examples are useful when they teach a stable pattern, but they can overfit the prompt if they encode hidden assumptions.
- Prompt quality is not measured by elegance; it is measured by whether the system behaves consistently on real task variations.

## 1. Why Prompt Design Matters

A powerful model can still produce weak application behavior if the prompt is ambiguous, underspecified, or vulnerable to input contamination. Prompting is therefore a design problem: the engineer must define the task boundary, the permitted output shape, and the handling of edge cases.

In production systems, the prompt is often part of the application interface. Changes to prompts can create regressions just like code changes do.

## 2. Common Prompting Patterns

Useful patterns include:

- explicit task decomposition
- role and constraint separation
- delimiter-wrapped untrusted input
- schema-first output instructions
- few-shot exemplars for tricky edge cases

These are not magic formulas. Each pattern is a way to reduce ambiguity in a specific failure mode.

## 3. Why Structured Output Is Valuable

If a system needs JSON, function arguments, or typed records, free-form text is fragile. A better approach is to specify a schema directly and reject or repair invalid output before using it downstream.

That changes the integration problem from:

- "can we parse whatever the model wrote?"

to:

- "did the model satisfy the required contract?"

This is much safer for automation.

## 4. Worked Example: Ticket Classification Prompt

Suppose a support tool must classify tickets into:

- `billing`
- `account`
- `technical`

It must return JSON with fields:

```text
label
confidence
rationale
```

### 4.1 Better Prompt Structure

```text
System: You are a classification component. Return only valid JSON.
Developer: Use one label from [billing, account, technical]. Confidence must be between 0 and 1.
User: Classify this ticket: <<<I was charged twice for my subscription>>>
```

### 4.2 Expected Output

```text
{
  "label": "billing",
  "confidence": 0.94,
  "rationale": "The user reports a duplicate charge."
}
```

### 4.3 Why This Is Better

The task, label set, schema, and input boundary are all explicit. That makes validation and debugging easier than if the model were simply asked, "What is this about?"

Verification: the prompt states one allowed label set and one explicit JSON schema, so the downstream component can validate the result mechanically.

## 5. Prompt Iteration in Practice

Prompt tuning should be driven by failure analysis:

- which edge cases fail
- which fields drift
- which inputs inject or override instructions
- which examples improve or hurt generalization

This is why prompt changes should be versioned and evaluated on a fixed set of representative tasks.

## 6. Common Mistakes

1. **Schema vagueness.** Asking for "structured output" without exact keys or types leads to drift; specify the contract explicitly.
2. **Role collapse.** Mixing policy, instructions, and user text in one block makes priority ambiguous; separate trusted roles clearly.
3. **Example overfitting.** Using too few or too narrow few-shot examples teaches accidental patterns; include representative variation or remove the examples.
4. **No validation path.** Accepting raw model output directly into automation invites failures; validate and reject malformed output first.
5. **Prompt drift silence.** Editing prompts without regression evaluation hides quality changes; treat prompt revisions like code changes with tests.

## 7. Practical Checklist

- [ ] Define the exact task, constraints, and output contract.
- [ ] Separate trusted instructions from untrusted input with clear delimiters.
- [ ] Use examples only when they teach a stable pattern.
- [ ] Validate structured outputs before downstream use.
- [ ] Keep prompt versions and evaluate changes on fixed cases.
- [ ] Add recovery behavior for invalid or missing fields.

## 8. References

- Wei, Jason, et al. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." 2022. <https://arxiv.org/abs/2201.11903>
- Kojima, Takeshi, et al. "Large Language Models are Zero-Shot Reasoners." 2022. <https://arxiv.org/abs/2205.11916>
- Reynolds, Laria, and Kyle McDonell. "Prompt Programming for Large Language Models: Beyond the Few-Shot Paradigm." 2021. <https://arxiv.org/abs/2102.07350>
- OpenAI. "Structured outputs guide." <https://platform.openai.com/docs/guides/structured-outputs>
- Anthropic. "Prompt engineering overview." <https://docs.anthropic.com/>
- Prompt Engineering Guide. <https://www.promptingguide.ai/>
- Ribeiro, Marco Tulio, et al. "Semantic uncertainty and prompt robustness resources." <https://aclanthology.org/>
