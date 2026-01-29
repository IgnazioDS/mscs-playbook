from src.genai.datasets import load_tiny_kb
from src.genai.rag import RAGPipeline


def test_rag_retrieve_and_synthesize():
    docs = load_tiny_kb()
    rag = RAGPipeline(docs)
    results = rag.retrieve("reset password", k=1)
    assert results[0].id == "kb-02:0"
    answer = rag.synthesize("reset password", results)
    assert "kb-02:0" in answer
