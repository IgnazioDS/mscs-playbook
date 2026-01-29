# Python Implementations

Local-first GenAI toolkit with deterministic outputs for prompts, RAG, tool
calling, and evaluation. No external APIs required.

## Status
- Docs: complete
- Toolkit: complete
- Mini-project: complete

## Quickstart (repo root)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r modules/11-generative-ai/03-implementations/python/requirements.txt
python -m pytest -q modules/11-generative-ai/03-implementations/python/tests
python modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py support-assistant --query "reset password" --k 3
python modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py meeting-summarize
python modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py agentic-analyst --question "What is (12*7) + 5?"
python modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py evaluate
```

## API index
- PromptTemplate (`src/genai/prompts.py`)
- validate_json (`src/genai/schemas.py`)
- chunk_text (`src/genai/chunking.py`)
- TfidfVectorStore (`src/genai/vectorstore.py`)
- RAGPipeline (`src/genai/rag.py`)
- ToolSpec (`src/genai/tools.py`)
- route (`src/genai/router.py`)
- run_goldens (`src/genai/evals.py`)
- mini_project CLI (`src/genai/mini_project/cli.py`)

## Determinism and limitations
- Offline stubs only; no model calls or network I/O.
- TF-IDF retrieval is lexical and may miss semantic matches.
- Rule-based routing is simplistic and task-specific.
- Safe calc supports only +, -, *, /, parentheses, ints/floats.

## Examples

### Render a prompt template
```python
from src.genai.prompts import get_template

prompt = get_template("classify")
print(prompt.render(labels="billing,support", input="Please resend my invoice"))
```

### Validate a structured output
```python
from src.genai.schemas import ClassificationResult, validate_json

payload = {"label": "billing", "confidence": 0.9}
result = validate_json(ClassificationResult, payload)
print(result)
```

### Run a RAG query
```python
from src.genai.datasets import load_tiny_kb
from src.genai.rag import RAGPipeline

rag = RAGPipeline(load_tiny_kb())
contexts = rag.retrieve("reset password", k=2)
print(rag.synthesize("reset password", contexts))
```

### Run golden evals
```python
from src.genai.datasets import load_goldens
from src.genai.evals import run_goldens

report = run_goldens(load_goldens())
print(report)
```

## Mini-project CLI
Run from the repo root:
```bash
python modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py support-assistant --query "reset password" --k 3
python modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py meeting-summarize
python modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py agentic-analyst --question "What is (12*7) + 5?"
python modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py evaluate
```
