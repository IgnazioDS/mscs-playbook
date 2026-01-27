from __future__ import annotations

"""Huffman coding for optimal prefix-free variable-length codes.

Problem:
    Given symbol frequencies, build a prefix-free code that minimizes
    total encoded length.

Inputs/Outputs:
    freqs: dict[str, int] -> dict[str, str] mapping symbols to bit strings.

Complexity:
    Time O(k log k) for k symbols, space O(k) for the tree and heap.

Typical use cases:
    Data compression, entropy coding, and storage optimization.
"""

from dataclasses import dataclass
import heapq
import itertools
from typing import Dict, Optional, Tuple


@dataclass
class _Node:
    """Internal node for the Huffman tree."""
    freq: int
    symbol: Optional[str] = None
    left: Optional["_Node"] = None
    right: Optional["_Node"] = None


def build_huffman_codes(freqs: Dict[str, int]) -> Dict[str, str]:
    """Build Huffman codes for a frequency table.

    Args:
        freqs: Map of symbol -> frequency (must be positive).

    Returns:
        Dict mapping symbol -> bitstring; codes are prefix-free.

    Raises:
        ValueError: If freqs is empty or contains non-positive frequencies.
    """
    if not freqs:
        raise ValueError("freqs must be non-empty")

    # Tie-breaker counter ensures deterministic heap ordering for equal frequencies.
    counter = itertools.count()
    heap: list[Tuple[int, int, _Node]] = []
    for symbol, freq in freqs.items():
        if freq <= 0:
            raise ValueError("frequencies must be positive")
        heapq.heappush(heap, (freq, next(counter), _Node(freq=freq, symbol=symbol)))

    if len(heap) == 1:
        only = heap[0][2]
        # Single-symbol alphabet needs a non-empty code to be decodable.
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
        # Left edge adds 0, right edge adds 1 (standard convention).
        _walk(node.left, prefix + "0")
        _walk(node.right, prefix + "1")

    _walk(root, "")
    return codes
