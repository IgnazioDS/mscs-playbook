# p7-genai-rag-agent-app

## Purpose
Provide an offline generative AI application baseline with retrieval-augmented generation, tool-routed responses, and deterministic evaluation.

## Scope
- Run support-assistant, meeting-summarizer, and agentic-analyst scenarios.
- Verify retrieval + citation behavior with fixed inputs.
- Keep outputs deterministic and API-free for repeatable checks.

## Modules Used
- Natural Language Processing
- Generative AI
- Big Data Architecture

## How to Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/11-generative-ai/03-implementations/python/requirements.txt
python3 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py support-assistant --query "reset password" --k 3
python3 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py meeting-summarize
python3 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py agentic-analyst --question "What is (12*7) + 5?"
python3 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py evaluate
```

## How to Test
```bash
python3 -m pytest -q modules/11-generative-ai/03-implementations/python/tests
```

## Expected Output
- Support assistant output includes retrieved chunk ids and source citations.
- Meeting and analyst commands print structured deterministic reports.
- Evaluate command and tests pass.
