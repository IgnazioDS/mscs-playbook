from __future__ import annotations

from dataclasses import dataclass
import heapq
import itertools
from typing import Dict, Optional, Tuple


@dataclass
class _Node:
    freq: int
    symbol: Optional[str] = None
    left: Optional["_Node"] = None
    right: Optional["_Node"] = None


def build_huffman_codes(freqs: Dict[str, int]) -> Dict[str, str]:
    """Build Huffman codes for a frequency table."""
    if not freqs:
        raise ValueError("freqs must be non-empty")

    counter = itertools.count()
    heap: list[Tuple[int, int, _Node]] = []
    for symbol, freq in freqs.items():
        if freq <= 0:
            raise ValueError("frequencies must be positive")
        heapq.heappush(heap, (freq, next(counter), _Node(freq=freq, symbol=symbol)))

    if len(heap) == 1:
        only = heap[0][2]
        return {only.symbol: "0"}

    while len(heap) > 1:
        left = heapq.heappop(heap)[2]
        right = heapq.heappop(heap)[2]
        parent = _Node(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, (parent.freq, next(counter), parent))

    root = heap[0][2]
    codes: Dict[str, str] = {}

    def _walk(node: _Node, prefix: str) -> None:
        if node.symbol is not None:
            codes[node.symbol] = prefix
            return
        _walk(node.left, prefix + "0")
        _walk(node.right, prefix + "1")

    _walk(root, "")
    return codes
