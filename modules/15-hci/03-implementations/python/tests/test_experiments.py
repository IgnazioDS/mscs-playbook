from __future__ import annotations

import csv
from pathlib import Path

import pytest

from src.hci_toolkit.experiments import (
    BinaryVariant,
    ContinuousVariant,
    ab_test_binary,
    ab_test_continuous,
    required_sample_size_binary,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_ab_binary_summary():
    with (FIXTURES / "ab_binary.csv").open() as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    variant_a = BinaryVariant(
        name=rows[0]["variant"],
        users=int(rows[0]["users"]),
        conversions=int(rows[0]["conversions"]),
    )
    variant_b = BinaryVariant(
        name=rows[1]["variant"],
        users=int(rows[1]["users"]),
        conversions=int(rows[1]["conversions"]),
    )

    result = ab_test_binary(variant_a, variant_b)
    assert result["difference"] == pytest.approx(0.1, abs=1e-6)
    assert result["z_stat"] == pytest.approx(1.727, rel=1e-3)
    assert result["p_value"] == pytest.approx(0.084, abs=0.01)


def test_ab_continuous_summary():
    with (FIXTURES / "ab_continuous.csv").open() as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    variant_a = ContinuousVariant(
        name=rows[0]["variant"],
        n=int(rows[0]["n"]),
        mean=float(rows[0]["mean"]),
        std=float(rows[0]["std"]),
    )
    variant_b = ContinuousVariant(
        name=rows[1]["variant"],
        n=int(rows[1]["n"]),
        mean=float(rows[1]["mean"]),
        std=float(rows[1]["std"]),
    )

    result = ab_test_continuous(variant_a, variant_b)
    assert result["difference"] == pytest.approx(8.0, abs=1e-6)
    assert result["t_stat"] == pytest.approx(2.33, rel=0.02)
    assert result["p_value"] == pytest.approx(0.022, abs=0.02)


def test_required_sample_size_binary():
    estimate = required_sample_size_binary(0.2, 0.05)
    assert estimate > 0
