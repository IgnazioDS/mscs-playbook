from src.greedy.huffman_coding import build_huffman_codes
from src.greedy.interval_scheduling import select_max_non_overlapping


def _is_prefix_free(codes: dict[str, str]) -> bool:
    values = list(codes.values())
    for i, code in enumerate(values):
        for j, other in enumerate(values):
            if i == j:
                continue
            if other.startswith(code):
                return False
    return True


def test_interval_scheduling():
    # Happy path: classical interval scheduling example.
    intervals = [
        (1, 4),
        (3, 5),
        (0, 6),
        (5, 7),
        (3, 9),
        (5, 9),
        (6, 10),
        (8, 11),
        (8, 12),
        (2, 14),
        (12, 16),
    ]
    result = select_max_non_overlapping(intervals)
    assert len(result) == 4
    for (s1, e1), (s2, e2) in zip(result, result[1:]):
        assert e1 <= s2


def test_huffman_codes_basic():
    # Happy path: ensure prefix-free codes and expected shortest code for max freq.
    freqs = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
    codes = build_huffman_codes(freqs)
    assert set(codes.keys()) == set(freqs.keys())
    assert _is_prefix_free(codes)
    assert min(len(code) for code in codes.values()) == len(codes["f"])


def test_huffman_single_symbol():
    # Edge case: single symbol should still get a valid code.
    codes = build_huffman_codes({"x": 7})
    assert codes == {"x": "0"}
