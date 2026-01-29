from __future__ import annotations

import re
from typing import Callable

from .defect_detection import run_defect_detection
from .document_ocr_lite import run_doc_ocr_lite
from .shelf_availability import run_shelf_availability


def _extract_metric(output: str, key: str) -> float | None:
    match = re.search(rf"{key}=([0-9.]+)", output)
    if not match:
        return None
    return float(match.group(1))


def _check_range(value: float | None, low: float = 0.0, high: float = 1.0) -> bool:
    return value is not None and low <= value <= high


def run_evaluate() -> tuple[bool, str]:
    scenarios: list[tuple[str, Callable[[], str], list[str]]] = [
        ("defect", lambda: run_defect_detection(seed=42, iou=0.5, out=None), ["defect-detect", "precision", "recall"]),
        ("ocr", lambda: run_doc_ocr_lite(seed=42, out=None), ["doc-ocr-lite", "precision", "recall"]),
        ("shelf", lambda: run_shelf_availability(seed=42, out=None), ["shelf-availability", "accuracy", "f1_macro"]),
    ]

    failures: list[str] = []
    for name, fn, expected in scenarios:
        output = fn()
        missing = [token for token in expected if token not in output]
        if missing:
            failures.append(f"{name}: missing {missing}")
            continue
        precision = _extract_metric(output, "precision")
        recall = _extract_metric(output, "recall")
        accuracy = _extract_metric(output, "accuracy")
        f1 = _extract_metric(output, "f1_macro")
        if "precision" in output and not _check_range(precision):
            failures.append(f"{name}: precision out of range")
        if "recall" in output and not _check_range(recall):
            failures.append(f"{name}: recall out of range")
        if "accuracy" in output and not _check_range(accuracy):
            failures.append(f"{name}: accuracy out of range")
        if "f1_macro" in output and not _check_range(f1):
            failures.append(f"{name}: f1_macro out of range")

    passed = len(failures) == 0
    summary_lines = [
        "task: evaluate",
        f"scenarios: {len(scenarios)}",
        f"passed: {len(scenarios) - len(failures)}",
        f"failed: {len(failures)}",
    ]
    if failures:
        summary_lines.append("failures:")
        summary_lines.extend(f"- {failure}" for failure in failures)
    report = "\n".join(summary_lines)
    return passed, report
