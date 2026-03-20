#!/usr/bin/env python3
"""Evaluates mini-platform SLOs from telemetry and a capacity report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import httpx

MINI_PLATFORM_ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = MINI_PLATFORM_ROOT / "shared"
if str(SHARED_ROOT) not in sys.path:
    sys.path.insert(0, str(SHARED_ROOT))

from mini_platform.ops import evaluate_slo_report


def _read_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--telemetry-file", default="")
    parser.add_argument("--capacity-report", required=True)
    parser.add_argument("--base-url", default="")
    parser.add_argument("--operator-key-id", default="")
    parser.add_argument("--operator-key", default="")
    parser.add_argument("--readiness-availability", type=float, default=1.0)
    args = parser.parse_args()

    if args.telemetry_file:
        telemetry = _read_json(args.telemetry_file)
    elif args.base_url:
        response = httpx.get(
            f"{args.base_url}/ops/telemetry",
            headers={"X-API-Key-Id": args.operator_key_id, "X-API-Key": args.operator_key},
            timeout=30,
        )
        response.raise_for_status()
        telemetry = response.json()
    else:
        raise SystemExit("telemetry input is required")

    telemetry["readiness_availability"] = args.readiness_availability
    capacity_report = _read_json(args.capacity_report)
    violations = evaluate_slo_report(telemetry, capacity_report)
    result = {"violations": violations, "ok": not violations}
    print(json.dumps(result, sort_keys=True))
    if violations:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
