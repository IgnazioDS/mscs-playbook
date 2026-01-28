# N-grams and Classic Language Models

## Overview
N-gram models approximate language by estimating the probability of a token
from the previous n-1 tokens.

## Why it matters
They provide strong baselines and are interpretable for simple tasks.

## Key ideas
- Markov assumption
- Smoothing to handle unseen n-grams
- Perplexity as evaluation

## Practical workflow
- Choose n based on data size
- Apply smoothing (Laplace, Kneser-Ney)
- Evaluate on held-out data

## Failure modes
- Data sparsity for large n
- Overfitting on small corpora
- Ignoring domain shift

## Checklist
- Use proper train/validation split
- Report perplexity consistently
- Compare against unigram baseline

## References
- Jurafsky & Martin, Speech and Language Processing — https://web.stanford.edu/~jurafsky/slp3/
- Katz Smoothing — https://aclanthology.org/J87-3002/
