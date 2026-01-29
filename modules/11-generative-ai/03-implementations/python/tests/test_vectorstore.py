from src.genai.datasets import load_tiny_kb
from src.genai.vectorstore import TfidfVectorStore


def test_vectorstore_top1():
    docs = load_tiny_kb()
    store = TfidfVectorStore()
    store.fit(docs)
    results = store.query("reset password", k=1)
    assert results
    assert results[0].id == "kb-02"
