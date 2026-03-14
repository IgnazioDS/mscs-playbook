"""Structured logging helpers for the ingest API."""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """Small JSON formatter for machine-readable service logs."""

    def __init__(self, service: str) -> None:
        super().__init__()
        self.service = service

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": self.service,
            "component": getattr(record, "component", self.service),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        for field in (
            "event_id",
            "replay_job_id",
            "processing_state",
            "path",
            "status_code",
            "detail",
            "request_size",
            "schema_version",
        ):
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value

        if record.exc_info:
            payload["error"] = self.formatException(record.exc_info)

        return json.dumps(payload, sort_keys=True)


def configure_json_logger(service: str, level: str) -> logging.Logger:
    logger = logging.getLogger(service)
    logger.handlers.clear()
    logger.setLevel(level)
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter(service))
    logger.addHandler(handler)
    return logger
