# Mini-project: NLP Toolkit CLI

## Goals
- Run a deterministic end-to-end NLP pipeline using the module toolkit.
- Exercise both classification (ticket triage) and retrieval (KB search).
- Produce simple evaluation summaries that are easy to reason about.

## Commands
From repo root:

```bash
python modules/10-nlp/03-implementations/python/src/nlp/mini_project/cli.py ticket-triage --seed 42
python modules/10-nlp/03-implementations/python/src/nlp/mini_project/cli.py kb-search --k 3
python modules/10-nlp/03-implementations/python/src/nlp/mini_project/cli.py evaluate --seed 42 --k 3
```

## Expected outputs (high level)
- Ticket triage prints train/test sizes, label distribution, model summary, and macro metrics.
- KB search prints each query, top-k doc ids, short snippets, and cosine scores.
- Evaluation combines classification metrics with retrieval metrics at k.

## Extension ideas
- Swap TF-IDF for a different vectorizer (BM25 or character n-grams).
- Add calibration or confidence thresholds for triage.
- Add error analysis: confusion matrix, per-label precision/recall.
- Expand the KB corpus and add hard negatives.
