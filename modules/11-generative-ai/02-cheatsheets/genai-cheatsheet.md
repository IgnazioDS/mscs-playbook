# Generative AI Cheat Sheet

## Prompt templates

### Classification
```text
System: You are a strict classifier.
Task: Classify the input into one label from: {labels}.
Rules:
- Output JSON only: {"label": "...", "confidence": 0-1}
- If unsure, choose the closest label and set confidence < 0.6
Input:
"""
{input}
"""
```

### Extraction
```text
System: Extract structured fields from the input.
Output JSON schema:
{
  "entities": [{"type": "", "value": ""}],
  "dates": [""],
  "notes": ""
}
Input:
"""
{input}
"""
```

### Summarization
```text
System: Summarize for {audience}.
Constraints:
- Max 5 bullets
- Keep facts only, no speculation
Input:
"""
{input}
"""
```

### Planning
```text
System: You are a planner.
Return JSON:
{"goal": "...", "steps": [{"id": 1, "task": "...", "needs_tool": true}]}
Input:
"""
{input}
"""
```

## Structured output rules (JSON schema tips)
- Use explicit types and required fields
- Provide a minimal example of valid output
- Enforce a single top-level object
- Validate JSON and repair or retry on failure
- Reject extra keys unless explicitly allowed

## RAG quick rules
- Chunk size: 300 to 800 tokens; overlap: 10 to 20 percent
- Store metadata for source, section, and timestamp
- Use hybrid retrieval when keyword precision matters
- Add re-ranking for better top-k precision
- Log retrieved passages with scores

## Tool-calling dos and donts
- Do define narrow tools with clear schemas
- Do validate tool inputs and outputs
- Do add timeouts and retries
- Dont allow tools to bypass auth or policy checks
- Dont leak secrets in tool responses

## Evals and monitoring
- Maintain a golden set per task and run nightly regressions
- Track format compliance, factuality, and safety flags
- Add hallucination checks with retrieval grounding
- Review high-severity failures within 24 hours

## Safety and privacy checklist
- Minimize data sent to models
- Redact PII before prompting
- Apply least-privilege tool permissions
- Log access and enforce retention limits
- Run prompt-injection tests before release
