# Mini-project: GenAI Local Toolkit

## Goals
- Build a deterministic, offline CLI that mirrors common GenAI workflows
- Demonstrate RAG retrieval with citations and stable formatting
- Produce structured meeting summaries and tool-routed answers
- Add a lightweight evaluation routine for regression checks

## Commands and expected outputs

### RAG support assistant
```bash
python modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py support-assistant --query "reset password" --k 3
```
Expected output (short):
```
task: support-assistant
k: 3
query: reset password
retrieved:
- kb-02:0 (...)
answer: Answer: Use retrieved context to respond to 'reset password'. Sources: [chunk:kb-02:0, ...]
```

### Meeting notes summarizer
```bash
python modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py meeting-summarize
```
Expected output (short):
```
task: meeting-summarize
summary:
...
bullets:
- ...
```

### Agentic data analyst
```bash
python modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py agentic-analyst --question "What is (12*7) + 5?"
```
Expected output (short):
```
task: agentic-analyst
plan:
1. Parse the question
...
final_answer:
Computed result: 89.000
```

### Deterministic evaluation
```bash
python modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py evaluate
```
Expected output (short):
```
task: evaluate
scenarios: 4
passed: 4
failed: 0
```

## How to extend to a real LLM provider later
- Replace the synthesis stub in `rag.py` with a provider call that takes contexts
- Swap `tools.py` summary heuristic with an LLM-backed summarizer
- Expand `router.py` to use model-based intent classification
- Add adapters that map provider responses into the Pydantic schemas

## Pitfalls
- Hallucinations when retrieval returns low-quality context
- Evaluation drift when prompts or tool routing changes
- Privacy leakage if user data is logged or cached without controls
