from __future__ import annotations

import json
import logging


def test_worker_json_formatter_emits_machine_readable_fields(load_service_module) -> None:
    module = load_service_module(
        "mini_platform_worker_logging",
        "services/worker/app/logging_utils.py",
    )
    formatter = module.JsonFormatter("worker")
    record = logging.LogRecord(
        name="worker",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="state transition",
        args=(),
        exc_info=None,
    )
    record.component = "worker"
    record.event_id = "evt-1"
    record.processing_state = "claimed"
    record.detail = "lease-acquired"

    payload = json.loads(formatter.format(record))

    assert payload["service"] == "worker"
    assert payload["component"] == "worker"
    assert payload["level"] == "INFO"
    assert payload["message"] == "state transition"
    assert payload["event_id"] == "evt-1"
    assert payload["processing_state"] == "claimed"
    assert payload["detail"] == "lease-acquired"
    assert "timestamp" in payload
