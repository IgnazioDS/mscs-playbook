"""Text preprocessing utilities."""

from __future__ import annotations

import re
import unicodedata


def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"([.,!?;:()\[\]{}])", r" \1 ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
