from __future__ import annotations

import pytest

from src.hci_toolkit.accessibility import TapTarget, contrast_ratio, contrast_report, tap_target_report


def test_contrast_ratio_black_white():
    assert contrast_ratio("#000000", "#ffffff") == pytest.approx(21.0, abs=0.01)
    report = contrast_report("#777777", "#ffffff")
    assert report["ratio"] == pytest.approx(4.48, abs=0.05)
    assert report["aa_normal"] is False
    assert report["aa_large"] is True


def test_tap_target_report():
    targets = [
        TapTarget("Primary CTA", 48, 10),
        TapTarget("Secondary", 40, 6),
    ]
    report = tap_target_report(targets)
    assert report["summary"]["total"] == 2
    assert report["summary"]["passed"] == 1
    assert report["items"][0]["passed"] is True
    assert report["items"][1]["passed"] is False
