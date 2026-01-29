from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from .router import route


@dataclass(frozen=True)
class GoldenCase:
    id: str
    task: str
    input: dict[str, Any]
    expected_substrings: list[str]
    expected_json: dict[str, Any] | None = None


def _matches_expected_json(result: dict[str, Any], expected: dict[str, Any]) -> bool:
    for key, value in expected.items():
        if key not in result:
            return False
        if result[key] != value:
            return False
    return True


def run_goldens(cases: list[GoldenCase]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    for case in cases:
        result = route(case.task, case.input)
        serialized = json.dumps(result, sort_keys=True)
        missing = [s for s in case.expected_substrings if s not in serialized]
        json_ok = True
        if case.expected_json is not None:
            json_ok = _matches_expected_json(result, case.expected_json)
        if missing or not json_ok:
            failures.append(
                {
                    "id": case.id,
                    "missing_substrings": missing,
                    "expected_json": case.expected_json,
                    "result": result,
                }
            )
    passed = len(cases) - len(failures)
    return {"passed": passed, "failed": len(failures), "failures": failures}
