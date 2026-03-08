from src.nlp.preprocessing import normalize_text, strip_accents


def test_strip_accents():
    assert strip_accents("café") == "cafe"


def test_normalize_text():
    assert normalize_text("Hello,  world!") == "hello , world !"
