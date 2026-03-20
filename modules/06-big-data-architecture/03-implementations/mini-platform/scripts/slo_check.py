#!/usr/bin/env python3
"""Evaluates mini-platform SLOs from telemetry and a capacity report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MINI_PLATFORM_ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = MINI_PLATFORM_ROOT / "shared"
if str(SHARED_ROOT) not in sys.path:
    sys.path.insert(0, str(SHARED_ROOT))

from mini_platform.ops import evaluate_slo_report


def _read_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _fetch_json(url: str, headers: dict[str, str], timeout_seconds: int) -> dict:
    request = Request(url, method="GET")
    for name, value in headers.items():
        request.add_header(name, value)
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GET {url} failed with {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"GET {url} failed: {exc.reason}") from exc


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
        telemetry = _fetch_json(
            f"{args.base_url}/ops/telemetry",
            {"X-API-Key-Id": args.operator_key_id, "X-API-Key": args.operator_key},
            30,
        )
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
