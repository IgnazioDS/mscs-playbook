from src.genai.chunking import chunk_text


def test_chunk_text_overlap_whitespace():
    text = "aa bb cc dd ee ff"
    chunks = chunk_text(text, max_chars=6, overlap=1)
    assert chunks == ["aa bb", "bb cc", "cc dd", "dd ee", "ee ff"]
