# Natural Language Processing

## Overview

This module covers how text is represented, modeled, evaluated, and deployed in practical NLP systems. The reading path starts with preprocessing and classical baselines, moves through neural sequence models and transformers, and ends with system-level choices around evaluation, retrieval, and safety.

## Reading Path

1. [Text Preprocessing and Tokenization](01-concepts/01-text-preprocessing-and-tokenization.md)
2. [N-grams and Classic Language Models](01-concepts/02-ngrams-and-classic-language-models.md)
3. [Vector Space Models and Similarity](01-concepts/03-vector-space-models-and-similarity.md)
4. [Embeddings: Word2Vec, GloVe, and FastText](01-concepts/04-embeddings-word2vec-glove-and-fasttext.md)
5. [Sequence Models: RNN, LSTM, and GRU](01-concepts/05-sequence-models-rnn-lstm-and-gru.md)
6. [Attention and Transformers](01-concepts/06-attention-and-transformers.md)
7. [Evaluation Metrics and Error Analysis](01-concepts/07-evaluation-metrics-and-error-analysis.md)
8. [Finetuning vs RAG and When to Use](01-concepts/08-finetuning-vs-rag-and-when-to-use.md)
9. [Bias, Safety, and Data Quality for NLP](01-concepts/09-bias-safety-and-data-quality-for-nlp.md)

## Module Map

- Concepts: [ordered concept index](01-concepts/README.md)
- Cheat sheet: [NLP cheat sheet](02-cheatsheets/nlp-cheatsheet.md)
- Python implementations: [NLP core toolkit](03-implementations/python/README.md)
- TypeScript implementations: [implementation notes](03-implementations/typescript/README.md)
- Case studies: [case study index](04-case-studies/README.md)
- Exercises: [exercise index](05-exercises/README.md)
- Notes: [further notes](06-notes/README.md)

## Quickstart

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python3 -m pip install -r modules/10-natural-language-processing/03-implementations/python/requirements.txt`
- `python3 -m pytest -q modules/10-natural-language-processing/03-implementations/python/tests`
- `python3 modules/10-natural-language-processing/03-implementations/python/src/nlp/mini_project/cli.py ticket-triage --seed 42`
- `python3 modules/10-natural-language-processing/03-implementations/python/src/nlp/mini_project/cli.py kb-search --k 3`
- `python3 modules/10-natural-language-processing/03-implementations/python/src/nlp/mini_project/cli.py evaluate --seed 42 --k 3`
