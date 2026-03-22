---
summary: Overview and references for 10 natural language processing 02 cheatsheets.
status: stable
---

# NLP Cheat Sheet

## Tokenization + normalization
- Lowercase? depends on task
- Preserve negations and punctuation signals
- Subword tokenizers for OOV robustness

## Baseline model choices
- TF-IDF + linear classifier
- Bag-of-ngrams + logistic regression
- Transformer encoder for strong accuracy

## Retrieval/RAG essentials
- Chunk size and overlap
- Metadata filters and recency
- Embed with domain-tuned model

## Evaluation metrics
- Classification: accuracy, F1, ROC-AUC
- Retrieval: precision@k, recall@k, MRR
- Generation: BLEU/ROUGE + human eval

## Debugging checklist
- Data leakage across splits
- Prompt sensitivity and formatting drift
- Hallucinations and unsupported claims
- Bias and toxicity in outputs


## Related Concepts

- [Text Preprocessing and Tokenization](../01-concepts/01-text-preprocessing-and-tokenization.md)
- [N-grams and Classic Language Models](../01-concepts/02-ngrams-and-classic-language-models.md)
- [Vector Space Models and Similarity](../01-concepts/03-vector-space-models-and-similarity.md)
