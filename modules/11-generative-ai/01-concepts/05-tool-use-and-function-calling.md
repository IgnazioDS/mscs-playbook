# Tool Use and Function Calling

## Key Ideas

- Tool use lets a language model delegate deterministic work such as retrieval, calculation, or API access to external components.
- Function calling is useful because it constrains model output into structured arguments that application code can validate before execution.
- Tools should be designed as narrow, permission-aware capabilities rather than as broad escape hatches around business logic.
- Reliable tool use requires schema validation, execution controls, error handling, and clear separation between planning and action.
- The model should not be trusted to authorize actions by itself; authorization belongs in the application layer.

## 1. Why Tool Use Matters

LLMs are good at language generation but weak at exact arithmetic, current data access, and stateful system integration. Tools fill that gap by letting the model request an external action instead of improvising an answer.

This shifts some tasks from:

- "generate a plausible response"

to:

- "produce a structured call that a deterministic system can execute"

That makes many workflows more reliable.

## 2. What Function Calling Adds

Without structured tool calls, the application must parse free-form text to infer what action to take. Function calling improves this by asking the model to emit arguments that match a defined schema.

That gives the application a validation point:

- are required fields present?
- are argument types valid?
- is the requested tool allowed?

Only after those checks should the tool execute.

## 3. Tool Design Principles

Good tools are:

- small in scope
- deterministic where possible
- protected by least privilege
- explicit about inputs and outputs

The tool layer is part of the application's trust boundary, so it should be designed like an API surface, not like a convenience wrapper.

## 4. Worked Example: Structured Tool Call

Suppose a support assistant has one tool:

```text
lookup_order(order_id: string) -> {status: string, shipped_at: string}
```

The user asks:

```text
"Where is order 4312?"
```

### 4.1 Desired Function Call

```text
tool_name = lookup_order
arguments = {"order_id": "4312"}
```

### 4.2 Validation

The application checks:

- `order_id` exists
- `order_id` is a string
- the current user may access order `4312`

Only then does the system execute the call.

### 4.3 Result Handling

If the tool returns:

```text
{"status": "shipped", "shipped_at": "2026-03-09"}
```

the assistant can generate a grounded reply using that structured result instead of guessing.

Verification: the model contributes the action intent and arguments, but the application still controls validation, authorization, and execution.

## 5. Planning vs Acting

One useful design separation is:

- the model proposes what tool to call and with which arguments
- the application decides whether the call is valid and permitted

This reduces the risk that the model can directly trigger unsafe or over-broad operations. It also improves observability, because proposed and executed actions can be logged separately.

## 6. Common Mistakes

1. **God tools.** Exposing one broad tool with many hidden powers weakens authorization and debugging; define narrow capabilities instead.
2. **Schema ambiguity.** Loose argument definitions cause invalid or incomplete calls; make required fields and types explicit.
3. **Model-side authorization.** Trusting the model to decide access rights is unsafe; enforce permissions in application code.
4. **No execution guardrails.** Missing timeouts, retries, and failure handling turns tool use into a reliability hazard; wrap tools with operational controls.
5. **Free-form fallbacks.** Letting the model bypass structured calls and invent answers defeats grounding; prefer validated tool paths when exact data is required.

## 7. Practical Checklist

- [ ] Define tools with explicit schemas and narrow permissions.
- [ ] Validate tool arguments before execution.
- [ ] Enforce authorization outside the model.
- [ ] Add timeouts, retries, and circuit breakers for external tools.
- [ ] Log proposed calls, executed calls, and returned results.
- [ ] Prefer deterministic tool execution for exact data or actions.

## 8. References

- Schick, Timo, et al. "Toolformer." 2023. <https://arxiv.org/abs/2302.04761>
- Yao, Shunyu, et al. "ReAct: Synergizing Reasoning and Acting in Language Models." 2023. <https://arxiv.org/abs/2210.03629>
- OpenAI. "Function calling and structured outputs guides." <https://platform.openai.com/docs>
- Anthropic. "Tool use documentation." <https://docs.anthropic.com/>
- Mialon, Grégoire, et al. "Augmented Language Models: a Survey." 2023. <https://arxiv.org/abs/2302.07842>
- OWASP. "Top 10 for Large Language Model Applications." <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- Stanford CRFM. "Foundation model systems design resources." <https://crfm.stanford.edu/>
