# p5-nlp-system

## Purpose
Ship a local natural language processing system baseline for ticket triage, semantic knowledge-base search, and deterministic evaluation.

## Scope
- Run mini-project commands for triage/search/evaluate.
- Keep outputs deterministic with fixed seeds.
- Establish a baseline for future model or retrieval improvements.

## Modules Used
- Natural Language Processing
- Generative AI

## How to Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/10-natural-language-processing/03-implementations/python/requirements.txt
python3 modules/10-natural-language-processing/03-implementations/python/src/nlp/mini_project/cli.py ticket-triage --seed 42
python3 modules/10-natural-language-processing/03-implementations/python/src/nlp/mini_project/cli.py kb-search --k 3
python3 modules/10-natural-language-processing/03-implementations/python/src/nlp/mini_project/cli.py evaluate --seed 42 --k 3
```

## How to Test
```bash
python3 -m pytest -q modules/10-natural-language-processing/03-implementations/python/tests
```

## Expected Output
- Triage command prints category predictions with confidence-oriented summaries.
- KB search returns ranked snippets.
- Evaluate command and tests pass deterministically.
