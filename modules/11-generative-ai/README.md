# Generative AI

## Overview

This module covers practical generative-AI system design: inference behavior, prompting, retrieval, tool use, evaluation, agent workflows, and safety. The reading path moves from single-call model behavior toward multi-component application systems with stronger grounding and control requirements.

## Reading Path

1. [LLM Fundamentals and Inference](01-concepts/01-llm-fundamentals-and-inference.md)
2. [Prompting Patterns and Structured Output](01-concepts/02-prompting-patterns-and-structured-output.md)
3. [Embeddings and Retrieval Foundations](01-concepts/03-embeddings-and-retrieval-foundations.md)
4. [RAG Design: Chunking, Indexing, and Retrieval](01-concepts/04-rag-design-chunking-indexing-and-retrieval.md)
5. [Tool Use and Function Calling](01-concepts/05-tool-use-and-function-calling.md)
6. [Evaluation for LLMs and Guardrails](01-concepts/06-evaluation-for-llms-and-guardrails.md)
7. [Fine-Tuning vs RAG vs Caching](01-concepts/07-fine-tuning-vs-rag-vs-caching.md)
8. [Agents: Planning, Memory, and Evals](01-concepts/08-agents-planning-memory-and-evals.md)
9. [Safety, Privacy, and Data Handling](01-concepts/09-safety-privacy-and-data-handling.md)

## Module Map

- Concepts: [ordered concept index](01-concepts/README.md)
- Cheat sheet: [Generative AI cheat sheet](02-cheatsheets/genai-cheatsheet.md)
- Python implementations: [local-first GenAI toolkit](03-implementations/python/README.md)
- TypeScript implementations: [implementation notes](03-implementations/typescript/README.md)
- Case studies: [case study index](04-case-studies/README.md)
- Exercises: [exercise index](05-exercises/README.md)
- Notes: [further notes](06-notes/README.md)

## Quickstart

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
