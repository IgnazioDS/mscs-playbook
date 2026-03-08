# Text Preprocessing and Tokenization

## Overview
Preprocessing standardizes raw text and tokenization splits it into units for
modeling.

## Why it matters
Poor preprocessing yields noisy features, unstable vocabularies, and brittle
models.

## Key ideas
- Normalization: casing, punctuation, whitespace
- Tokenization: word, subword, character
- Vocabulary control: stopwords, min frequency

## Practical workflow
- Define task and preserve needed signals
- Choose tokenizer aligned with model
- Track preprocessing steps for reproducibility

## Failure modes
- Removing meaningful tokens (negations)
- Inconsistent preprocessing across train/test
- Tokenization mismatch with pretrained models

## Checklist
- Preprocessing steps documented
- Tokenization verified on samples
- Vocabulary size controlled
- Train/test pipelines aligned

## References
- Jurafsky & Martin, Speech and Language Processing — https://web.stanford.edu/~jurafsky/slp3/
- spaCy Tokenization — https://spacy.io/usage/linguistic-features#tokenization
