# Evaluation Metrics and Error Analysis

## Overview
NLP tasks require task-specific metrics and systematic error analysis to
understand failures.

## Why it matters
Single metrics hide failure modes and bias.

## Key ideas
- Classification: accuracy, F1, AUC
- Retrieval: precision@k, recall@k, MRR
- Generation: BLEU, ROUGE, human eval

## Practical workflow
- Choose primary and secondary metrics
- Slice by category and error type
- Review qualitative examples

## Failure modes
- Metrics misaligned with product goals
- Evaluation leakage from train data
- Over-optimizing for a single metric

## Checklist
- Document metric definitions
- Track error slices over time
- Maintain a curated error set

## References
- Manning et al., IR and Web Search — https://nlp.stanford.edu/IR-book/
- BLEU — https://aclanthology.org/P02-1040/
