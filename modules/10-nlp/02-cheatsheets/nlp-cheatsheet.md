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
