# NLP Core Toolkit (Python)

Lightweight NLP toolkit for preprocessing, vectorization, similarity, and
classification.

## Status
- Toolkit: complete
- Mini-project CLI: complete

## Quickstart
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r modules/10-nlp/03-implementations/python/requirements.txt`
- `python -m pytest -q modules/10-nlp/03-implementations/python/tests`
- `python modules/10-nlp/03-implementations/python/src/nlp/mini_project/cli.py ticket-triage --seed 42`
- `python modules/10-nlp/03-implementations/python/src/nlp/mini_project/cli.py kb-search --k 3`
- `python modules/10-nlp/03-implementations/python/src/nlp/mini_project/cli.py evaluate --seed 42 --k 3`

## Tests
- `python -m pytest -q modules/10-nlp/03-implementations/python/tests`

## API index
- `preprocessing.normalize_text`, `preprocessing.strip_accents`
- `tokenization.word_tokenize`, `tokenization.char_ngrams`
- `vectorizers.TfidfVectorizerLite`
- `similarity.topk_cosine`, `similarity.NearestNeighborsIndex`
- `classifiers.train_linear_text_classifier`
- `embeddings.train_svd_embeddings`, `embeddings.average_word_embeddings`
- `evaluation.classification_report_simple`, `evaluation.retrieval_metrics_at_k`
- `datasets.load_tiny_corpus`, `datasets.make_ticket_dataset`

## Mini-project CLI
Run the end-to-end CLI tasks from the Quickstart section.

Optional report output:
- `python modules/10-nlp/03-implementations/python/src/nlp/mini_project/cli.py ticket-triage --seed 42 --out out/triage.md`

## Reproducibility
- Fixed seeds for train/test splits and model initialization.
- Deterministic ranking via stable sorting and rounded output for reports.
- No timestamps or randomness in the CLI outputs unless explicitly provided.

## Examples
TF-IDF + top-k retrieval:
```python
from src.nlp.vectorizers import TfidfVectorizerLite
from src.nlp.similarity import topk_cosine

texts = ["alpha beta", "beta gamma", "delta"]
vec = TfidfVectorizerLite()
X = vec.fit_transform(texts)
query = vec.transform(["beta"])
idx = topk_cosine(query[0], X, k=2)
print(idx)
```

Train a classifier:
```python
from src.nlp.classifiers import train_linear_text_classifier

texts = ["urgent payment", "hello world", "refund request", "thanks"]
labels = ["finance", "general", "finance", "general"]
model = train_linear_text_classifier(texts, labels, seed=42)
```

Compute retrieval metrics:
```python
from src.nlp.evaluation import retrieval_metrics_at_k

relevant = [{"d1"}, {"d2", "d3"}]
retrieved = [["d1", "d4"], ["d3", "d2"]]
print(retrieval_metrics_at_k(relevant, retrieved, k=2))
```
