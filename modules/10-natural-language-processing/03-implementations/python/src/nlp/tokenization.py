"""Tokenization utilities."""

from __future__ import annotations

import re
from typing import List


def word_tokenize(text: str) -> List[str]:
    tokens = re.findall(r"[\w']+|[.,!?;]", text)
    return tokens


def char_ngrams(text: str, n: int) -> List[str]:
    if n <= 0:
        raise ValueError("n must be positive")
    return [text[i : i + n] for i in range(len(text) - n + 1)]
