from src.nlp.tokenization import char_ngrams, word_tokenize


def test_word_tokenize():
    tokens = word_tokenize("Hello, world!")
    assert tokens == ["Hello", ",", "world", "!"]


def test_char_ngrams():
    assert char_ngrams("abc", 2) == ["ab", "bc"]
