# 10-nlp

## Status

- Docs: complete
- Python implementations: complete
- Mini-project: complete

## Overview

This module covers practical NLP foundations: preprocessing, representation,
classic models, transformers, evaluation, and production tradeoffs. It is
written as an engineering playbook with actionable checklists.

## Prerequisites

- Python 3.10+
- Basic linear algebra and probability

## Quickstart

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/10-nlp/03-implementations/python/requirements.txt`
- `python -m pytest -q modules/10-nlp/03-implementations/python/tests`
- `python modules/10-nlp/03-implementations/python/src/nlp/mini_project/cli.py ticket-triage --seed 42`
- `python modules/10-nlp/03-implementations/python/src/nlp/mini_project/cli.py kb-search --k 3`
- `python modules/10-nlp/03-implementations/python/src/nlp/mini_project/cli.py evaluate --seed 42 --k 3`

## Concepts

- [Text Preprocessing and Tokenization](01-concepts/text-preprocessing-and-tokenization.md)
- [N-grams and Classic Language Models](01-concepts/ngrams-and-classic-language-models.md)
- [Vector Space Models and Similarity](01-concepts/vector-space-models-and-similarity.md)
- [Embeddings: Word2Vec, GloVe, FastText](01-concepts/embeddings-word2vec-glove-fasttext.md)
- [Sequence Models: RNN, LSTM, GRU](01-concepts/sequence-models-rnn-lstm-gru.md)
- [Attention and Transformers](01-concepts/attention-and-transformers.md)
- [Finetuning vs RAG and When to Use](01-concepts/finetuning-vs-rag-and-when-to-use.md)
- [Evaluation Metrics and Error Analysis](01-concepts/evaluation-metrics-and-error-analysis.md)
- [Bias, Safety, and Data Quality for NLP](01-concepts/bias-safety-and-data-quality-for-nlp.md)

## Cheat sheet

- [NLP Cheat Sheet](02-cheatsheets/nlp-cheatsheet.md)

## Case studies

- [Support Ticket Triage](04-case-studies/support-ticket-triage.md)
- [Semantic Search for Knowledge Base](04-case-studies/semantic-search-for-knowledge-base.md)
- [Entity Extraction for Compliance](04-case-studies/entity-extraction-for-compliance.md)

## Implementations

- [Python implementations](03-implementations/python/README.md)

## Mini-project

- [Mini-project CLI exercise](05-exercises/mini-project-nlp-toolkit-cli.md)
- [Mini-project CLI entry](03-implementations/python/src/nlp/mini_project/cli.py)
