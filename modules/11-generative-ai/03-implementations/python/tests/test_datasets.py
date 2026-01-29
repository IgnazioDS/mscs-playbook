from src.genai.datasets import load_goldens, load_tiny_kb


def test_load_tiny_kb():
    docs = load_tiny_kb()
    assert len(docs) >= 10
    assert docs[0].id == "kb-01"


def test_load_goldens():
    cases = load_goldens()
    assert len(cases) >= 5
    assert cases[0].id.startswith("golden-")
