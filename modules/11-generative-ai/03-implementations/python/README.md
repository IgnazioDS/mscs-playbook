# Python Implementations

Local-first Generative AI toolkit with deterministic outputs for prompts, retrieval, tool routing, and evaluation. This is an offline demo surface, not a deployed service.

## Phase 1 Status
- Supported: local Python 3.11 CLI and test workflows.
- Demo-grade: no external APIs, no network I/O, and no real agent autonomy.
- Not claimed: cloud readiness, production security readiness, multi-tenant support, or production deployment maturity.

## Quickstart (repo root)
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python3.11 -m pip install -r modules/11-generative-ai/03-implementations/python/requirements.txt
python3.11 -m pytest -q modules/11-generative-ai/03-implementations/python/tests
python3.11 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py support-assistant --query "reset password" --k 3
python3.11 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py meeting-summarize
python3.11 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py agentic-analyst --question "What is (12*7) + 5?"
python3.11 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py evaluate
```

## API Index
- PromptTemplate (`src/genai/prompts.py`)
- validate_json (`src/genai/schemas.py`)
- chunk_text (`src/genai/chunking.py`)
- TfidfVectorStore (`src/genai/vectorstore.py`)
- RAGPipeline (`src/genai/rag.py`)
- ToolSpec (`src/genai/tools.py`)
- route (`src/genai/router.py`)
- run_goldens (`src/genai/evals.py`)
- mini_project CLI (`src/genai/mini_project/cli.py`)

## Determinism and Limits
- Offline stubs only; no model calls or network I/O.
- TF-IDF retrieval is lexical and may miss semantic matches.
- Rule-based routing is simplistic and task-specific.
- Safe calc supports only `+`, `-`, `*`, `/`, parentheses, and ints or floats.

## Mini-project CLI
Run from the repo root:
```bash
python3.11 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py support-assistant --query "reset password" --k 3
python3.11 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py meeting-summarize
python3.11 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py agentic-analyst --question "What is (12*7) + 5?"
python3.11 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py evaluate
```
