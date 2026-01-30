from __future__ import annotations

import json
import math
import re
from collections import OrderedDict
from pathlib import Path
from statistics import fmean, median, stdev, variance
from typing import Any


_NUMBER_SPLIT_RE = re.compile(r"[\s,]+")


def parse_numbers(text: str) -> list[float]:
    tokens = [token for token in _NUMBER_SPLIT_RE.split(text.strip()) if token]
    if not tokens:
        return []
    return [float(token) for token in tokens]


def load_numbers_from_csv(path: str | Path) -> list[float]:
    content = Path(path).read_text(encoding="utf-8")
    return parse_numbers(content)


def compute_stats(numbers: list[float]) -> OrderedDict[str, float | int]:
    if not numbers:
        raise ValueError("no numbers provided")

    count = len(numbers)
    mean_value = fmean(numbers)
    median_value = median(numbers)
    if count > 1:
        variance_value = variance(numbers)
        stdev_value = stdev(numbers)
    else:
        variance_value = 0.0
        stdev_value = 0.0

    results: OrderedDict[str, float | int] = OrderedDict()
    results["count"] = count
    results["mean"] = mean_value
    results["median"] = float(median_value)
    results["variance"] = variance_value
    results["stddev"] = stdev_value
    results["min"] = min(numbers)
    results["max"] = max(numbers)
    return results


def gcd_lcm(a: int, b: int) -> tuple[int, int]:
    g = math.gcd(a, b)
    if a == 0 or b == 0:
        return g, 0
    return g, abs(a * b) // g


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    g = old_r
    x = old_s
    y = old_t
    if g < 0:
        g, x, y = -g, -x, -y
    return g, x, y


def modular_inverse(a: int, m: int) -> int | None:
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m


def number_theory_summary(a: int, b: int, m: int) -> OrderedDict[str, int | None]:
    g, l = gcd_lcm(a, b)
    egcd_g, egcd_x, egcd_y = extended_gcd(a, b)
    inv = modular_inverse(a, m)

    results: OrderedDict[str, int | None] = OrderedDict()
    results["gcd"] = g
    results["lcm"] = l
    results["egcd_x"] = egcd_x
    results["egcd_y"] = egcd_y
    results["egcd_g"] = egcd_g
    results["mod_inverse"] = inv
    return results


def _ensure_matrix(matrix: Any, name: str) -> list[list[float]]:
    if not isinstance(matrix, list) or not matrix:
        raise ValueError(f"{name} must be a non-empty matrix")
    out: list[list[float]] = []
    for row in matrix:
        if not isinstance(row, list) or not row:
            raise ValueError(f"{name} has invalid rows")
        out.append([float(value) for value in row])
    return out


def load_matrices(json_text: str | None) -> tuple[list[list[float]], list[list[float]]]:
    if json_text:
        data = json.loads(json_text)
        matrix_a = _ensure_matrix(data.get("a"), "a")
        matrix_b = _ensure_matrix(data.get("b"), "b")
        return matrix_a, matrix_b

    matrix_a = [[1.0, 2.0], [3.0, 4.0]]
    matrix_b = [[2.0, 0.0], [1.0, 2.0]]
    return matrix_a, matrix_b


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*matrix)]


def multiply(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    if len(a[0]) != len(b):
        raise ValueError("incompatible dimensions for multiplication")
    result: list[list[float]] = []
    for i in range(len(a)):
        row: list[float] = []
        for j in range(len(b[0])):
            total = 0.0
            for k in range(len(b)):
                total += a[i][k] * b[k][j]
            row.append(total)
        result.append(row)
    return result


def determinant(matrix: list[list[float]]) -> float | None:
    if len(matrix) == 2 and len(matrix[0]) == 2 and len(matrix[1]) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if len(matrix) == 3 and all(len(row) == 3 for row in matrix):
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return None


def _round_nested(value: Any, decimals: int = 3) -> Any:
    if isinstance(value, float):
        return round(value, decimals)
    if isinstance(value, int):
        return value
    if isinstance(value, list):
        return [_round_nested(item, decimals) for item in value]
    if isinstance(value, dict):
        return {key: _round_nested(val, decimals) for key, val in value.items()}
    return value


def format_value(value: Any, decimals: int = 3) -> str:
    if isinstance(value, float):
        return f"{value:.{decimals}f}"
    if isinstance(value, int):
        return str(value)
    if value is None:
        return "none"
    if isinstance(value, (list, dict)):
        rounded = _round_nested(value, decimals)
        return json.dumps(rounded)
    return str(value)


def matrix_summary(json_text: str | None) -> OrderedDict[str, Any]:
    matrix_a, matrix_b = load_matrices(json_text)
    results: OrderedDict[str, Any] = OrderedDict()
    results["determinant"] = determinant(matrix_a)
    results["transpose"] = transpose(matrix_a)
    results["product"] = multiply(matrix_a, matrix_b)
    return results
