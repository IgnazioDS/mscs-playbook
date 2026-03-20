#!/usr/bin/env python3
"""Runs a lightweight authenticated load scenario against the mini-platform."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import uuid4

MINI_PLATFORM_ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = MINI_PLATFORM_ROOT / "shared"
if str(SHARED_ROOT) not in sys.path:
    sys.path.insert(0, str(SHARED_ROOT))

from mini_platform.ops import summarize_capacity_run


def _request_json(
    method: str,
    url: str,
    headers: dict[str, str],
    payload: dict | None,
    timeout_seconds: int,
) -> dict:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(url, data=body, method=method)
    for name, value in headers.items():
        request.add_header(name, value)
    if body is not None:
        request.add_header("Content-Type", "application/json")
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed with {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"{method} {url} failed: {exc.reason}") from exc


def _post_json(url: str, headers: dict[str, str], payload: dict, timeout_seconds: int) -> tuple[dict, float]:
    started = time.perf_counter()
    response = _request_json("POST", url, headers, payload, timeout_seconds)
    elapsed_ms = (time.perf_counter() - started) * 1000
    return response, elapsed_ms


def _wait_for_event_completion(
    base_url: str,
    operator_headers: dict[str, str],
    event_id: str,
    timeout_seconds: int,
) -> float:
    started = time.perf_counter()
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        payload = _request_json(
            "GET",
            f"{base_url}/ops/events/{event_id}",
            operator_headers,
            None,
            timeout_seconds,
        )
        state = payload.get("processing_state") or {}
        if state.get("status") == "completed":
            return (time.perf_counter() - started) * 1000
        time.sleep(0.5)
    raise TimeoutError(f"event {event_id} did not complete within {timeout_seconds}s")


def _wait_for_replay_completion(
    base_url: str,
    operator_headers: dict[str, str],
    replay_job_id: str,
    timeout_seconds: int,
) -> float:
    started = time.perf_counter()
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        payload = _request_json(
            "GET",
            f"{base_url}/ops/replays/{replay_job_id}",
            operator_headers,
            None,
            timeout_seconds,
        )
        if payload["replay_job"]["status"] in {"completed", "failed", "cancelled", "timed_out"}:
            duration_minutes = max((time.perf_counter() - started) / 60.0, 1e-6)
            return 1.0 / duration_minutes
        time.sleep(0.5)
    raise TimeoutError(f"replay job {replay_job_id} did not finish within {timeout_seconds}s")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--ingest-key-id", required=True)
    parser.add_argument("--ingest-key", required=True)
    parser.add_argument("--operator-key-id", required=True)
    parser.add_argument("--operator-key", required=True)
    parser.add_argument("--requests", type=int, default=5)
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    ingest_headers = {"X-API-Key-Id": args.ingest_key_id, "X-API-Key": args.ingest_key}
    operator_headers = {"X-API-Key-Id": args.operator_key_id, "X-API-Key": args.operator_key}
    accepted = 0
    completed = 0
    failed = 0
    ingest_latencies_ms: list[float] = []
    processing_latencies_ms: list[float] = []
    replay_rates: list[float] = []
    event_ids: list[str] = []

    for index in range(args.requests):
        payload = {
            "schema_version": 1,
            "event_type": "order_created",
            "event_time": datetime.now(timezone.utc).isoformat(),
            "order_id": f"O-load-{index}",
            "amount": 42.0,
            "currency": "USD",
            "customer_id": f"C-load-{index}",
        }
        try:
            response_json, latency_ms = _post_json(
                f"{args.base_url}/ingest",
                ingest_headers,
                payload,
                args.timeout_seconds,
            )
            event_id = response_json["event_id"]
            event_ids.append(event_id)
            ingest_latencies_ms.append(latency_ms)
            accepted += 1
            processing_latencies_ms.append(
                _wait_for_event_completion(args.base_url, operator_headers, event_id, args.timeout_seconds)
            )
            completed += 1
        except Exception:
            failed += 1

    if event_ids:
        replay_response, _ = _post_json(
            f"{args.base_url}/ops/replays",
            operator_headers,
            {"selector_type": "event_id", "event_id": event_ids[0]},
            args.timeout_seconds,
        )
        replay_rates.append(
            _wait_for_replay_completion(
                args.base_url,
                operator_headers,
                replay_response["replay_job_id"],
                args.timeout_seconds,
            )
        )

    report = summarize_capacity_run(
        ingest_latencies_ms=ingest_latencies_ms,
        processing_latencies_ms=processing_latencies_ms,
        replay_completion_rates_per_minute=replay_rates,
        accepted=accepted,
        completed=completed,
        failed=failed,
    )

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
