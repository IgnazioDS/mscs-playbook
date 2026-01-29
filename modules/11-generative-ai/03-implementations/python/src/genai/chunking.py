from __future__ import annotations


def chunk_text(text: str, max_chars: int, overlap: int) -> list[str]:
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")

    chunks: list[str] = []
    length = len(text)
    idx = 0

    while idx < length:
        end = min(idx + max_chars, length)
        if end < length:
            window = text[idx:end]
            split_at = window.rfind(" ")
            if split_at > 0:
                end = idx + split_at
        chunk = text[idx:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= length:
            break
        next_start = end - overlap
        if next_start <= idx:
            next_start = end
        if 0 < next_start < length and not text[next_start].isspace():
            back_ws = text.rfind(" ", idx, next_start)
            forward_ws = text.find(" ", next_start, end)
            if back_ws > idx:
                next_start = back_ws
            elif forward_ws != -1:
                next_start = forward_ws
        while next_start < length and text[next_start].isspace():
            next_start += 1
        idx = next_start

    return chunks
