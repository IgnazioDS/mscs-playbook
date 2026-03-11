# Prompting Patterns and Structured Output

## Overview
Prompting patterns are reusable instruction templates that improve consistency
and enable structured outputs for downstream automation.

## Why it matters
Well-structured prompts reduce hallucinations, improve determinism, and make
LLM outputs easier to validate and integrate.

## Key ideas
- Separate roles: system for policy, developer for instructions, user for input
- Use delimiters to isolate untrusted text
- Provide a clear schema or example for structured output
- Few-shot examples teach edge cases and style

## Practical workflow
- Start with a single-task prompt and add constraints incrementally
- Add a strict output format with JSON keys and types
- Include validation rules and error handling guidance
- Keep examples short and representative of real data

## Failure modes
- Format drift when instructions are ambiguous
- Hidden assumptions in examples that do not generalize
- Prompt injection through unescaped user content
- Overfitting to a single example pattern

## Checklist
- Specify the output schema and required fields
- Use consistent delimiters for inputs
- Reject or repair invalid JSON before downstream use
- Maintain a prompt changelog with versioning

## References
- Prompting Guide — https://www.promptingguide.ai/
- Structured Outputs — https://platform.openai.com/docs/guides/structured-outputs
