from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .vectorstore import Doc

_DATA_DIR = Path(__file__).resolve().parents[3] / "data"


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def load_tiny_kb() -> list[Doc]:
    path = _DATA_DIR / "tiny_kb.jsonl"
    records = _load_jsonl(path)
    return [Doc(id=rec["id"], text=rec["text"], meta=rec.get("meta", {})) for rec in records]


def load_goldens() -> list[Any]:
    from .evals import GoldenCase

    path = _DATA_DIR / "goldens.jsonl"
    records = _load_jsonl(path)
    cases: list[GoldenCase] = []
    for rec in records:
        cases.append(
            GoldenCase(
                id=rec["id"],
                task=rec["task"],
                input=rec["input"],
                expected_substrings=rec.get("expected_substrings", []),
                expected_json=rec.get("expected_json"),
            )
        )
    return cases
