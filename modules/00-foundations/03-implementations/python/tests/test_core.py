import json
from pathlib import Path

import pytest

from src.foundations.mini_project.core import (
    compute_stats,
    load_numbers_from_csv,
    matrix_summary,
    number_theory_summary,
    parse_numbers,
)


FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_parse_numbers_from_string():
    numbers = parse_numbers("1 2,3\n4")
    assert numbers == [1.0, 2.0, 3.0, 4.0]


def test_load_numbers_from_csv():
    numbers = load_numbers_from_csv(FIXTURES / "numbers.csv")
    assert numbers == [1.0, 2.0, 3.0, 4.0, 5.0]


def test_compute_stats():
    stats = compute_stats([1, 2, 3, 4, 5])
    assert stats["count"] == 5
    assert stats["mean"] == pytest.approx(3.0)
    assert stats["median"] == pytest.approx(3.0)
    assert stats["variance"] == pytest.approx(2.5)
    assert stats["stddev"] == pytest.approx(2.5 ** 0.5)
    assert stats["min"] == 1
    assert stats["max"] == 5


def test_number_theory_summary():
    summary = number_theory_summary(30, 18, 11)
    assert summary["gcd"] == 6
    assert summary["lcm"] == 90
    x = summary["egcd_x"]
    y = summary["egcd_y"]
    g = summary["egcd_g"]
    assert 30 * x + 18 * y == g
    assert summary["mod_inverse"] == 7


def test_matrix_summary():
    payload = json.loads((FIXTURES / "matrices.json").read_text(encoding="utf-8"))
    summary = matrix_summary(json.dumps(payload))
    assert summary["determinant"] == pytest.approx(-2.0)
    assert summary["transpose"] == [[1.0, 3.0], [2.0, 4.0]]
    assert summary["product"] == [[4.0, 4.0], [10.0, 8.0]]
