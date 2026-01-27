import pytest

from src.dp.fibonacci_memo import fibonacci
from src.dp.knapsack_01 import knapsack_01
from src.dp.longest_increasing_subsequence import lis_length


def test_fibonacci_basic():
    # Happy path: known small Fibonacci values.
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(2) == 1
    assert fibonacci(10) == 55


def test_fibonacci_negative():
    # Edge case: negative indices are invalid.
    with pytest.raises(ValueError):
        fibonacci(-1)


def test_knapsack_01():
    # Happy path: classic 0/1 knapsack example.
    values = [60, 100, 120]
    weights = [10, 20, 30]
    assert knapsack_01(values, weights, 50) == 220
    assert knapsack_01(values, weights, 0) == 0


def test_knapsack_invalid():
    # Edge case: mismatched input lengths.
    with pytest.raises(ValueError):
        knapsack_01([1], [1, 2], 3)


def test_lis_length():
    # Happy path: standard LIS example and empty input.
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    assert lis_length(nums) == 4
    assert lis_length([]) == 0
