# Generative AI

## Status

- Docs: complete
- Python implementations: complete
- Mini-project: complete

## Overview

This module covers practical generative AI engineering: model selection, prompting,
retrieval, tool use, evaluation, and safety. It is written as an engineering
playbook with actionable checklists.

## Prerequisites

- Python 3.10+
- Basic machine learning and natural language processing concepts
- Familiarity with APIs and JSON

## Quickstart

Run from the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/11-generative-ai/03-implementations/python/requirements.txt
python3 -m pytest -q modules/11-generative-ai/03-implementations/python/tests
python3 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py support-assistant --query "reset password" --k 3
python3 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py meeting-summarize
python3 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py agentic-analyst --question "What is (12*7) + 5?"
python3 modules/11-generative-ai/03-implementations/python/src/genai/mini_project/cli.py evaluate
```

## Reproducibility notes

- All workflows are offline and deterministic (no external APIs).
- Retrieval uses TF-IDF over the bundled tiny knowledge base.
- Tool routing is rule-based; outputs are stable for fixed inputs.

## Concepts

- [LLM Fundamentals and Inference](01-concepts/llm-fundamentals-and-inference.md)
- [Prompting Patterns and Structured Output](01-concepts/prompting-patterns-and-structured-output.md)
- [Embeddings and Retrieval Foundations](01-concepts/embeddings-and-retrieval-foundations.md)
- [RAG Design: Chunking, Indexing, Retrieval](01-concepts/rag-design-chunking-indexing-retrieval.md)
- [Tool Use and Function Calling](01-concepts/tool-use-and-function-calling.md)
- [Agents: Planning, Memory, and Evals](01-concepts/agents-planning-memory-and-evals.md)
- [Fine-Tuning vs RAG vs Caching](01-concepts/fine-tuning-vs-rag-vs-caching.md)
- [Evaluation for LLMs and Guardrails](01-concepts/evaluation-for-llms-and-guardrails.md)
- [Safety, Privacy, and Data Handling](01-concepts/safety-privacy-and-data-handling.md)

## Cheat sheet

- [Generative AI Cheat Sheet](02-cheatsheets/genai-cheatsheet.md)

## Case studies

- [RAG Support Assistant](04-case-studies/rag-support-assistant.md)
- [Meeting Notes Summarizer](04-case-studies/meeting-notes-summarizer.md)
- [Agentic Data Analyst](04-case-studies/agentic-data-analyst.md)

## Implementations

- [Python implementations](03-implementations/python/README.md)
- [TypeScript implementations](03-implementations/typescript/README.md)

## Mini-project

- [Mini-project writeup](05-exercises/mini-project-genai-local-toolkit.md)
- [Mini-project CLI entry](03-implementations/python/src/genai/mini_project/cli.py)
