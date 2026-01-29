# Tool Use and Function Calling

## Overview
Tool use lets LLMs call deterministic functions to access data, run actions, or
compute results that improve reliability.

## Why it matters
Function calling reduces hallucinations, enables integration with real systems,
and keeps business logic outside the model.

## Key ideas
- Define clear tool schemas with typed arguments
- Keep tools small and deterministic
- Provide tool selection guidance in prompts
- Verify tool outputs before generation

## Practical workflow
- List tools by capability and permission level
- Add argument validation and input sanitization
- Implement retries and fallbacks for tool errors
- Log tool calls with inputs and outputs

## Failure modes
- Overly broad tools that bypass authorization
- Ambiguous schemas causing invalid arguments
- Tools that are slow or non-deterministic
- Leaking sensitive data in tool results

## Checklist
- Require structured arguments and validate types
- Scope tool permissions to least privilege
- Add tool timeouts and circuit breakers
- Test with adversarial prompts and injection attempts

## References
- Toolformer — https://arxiv.org/abs/2302.04761
- ReAct: Synergizing Reasoning and Acting — https://arxiv.org/abs/2210.03629
