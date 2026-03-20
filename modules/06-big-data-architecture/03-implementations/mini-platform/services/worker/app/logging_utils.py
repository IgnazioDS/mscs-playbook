"""Structured logging helpers for the worker."""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone

from mini_platform.release import ReleaseMetadata


class JsonFormatter(logging.Formatter):
    """Small JSON formatter for machine-readable worker logs."""

    def __init__(self, service: str, release_metadata: ReleaseMetadata | None = None) -> None:
        super().__init__()
        self.service = service
        self.release_metadata = release_metadata

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": self.service,
            "component": getattr(record, "component", self.service),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if self.release_metadata is not None:
            payload["release"] = self.release_metadata.as_dict()

        for field in (
            "event_id",
            "replay_job_id",
            "processing_state",
            "detail",
            "lease_seconds",
            "schema_version",
            "key_id",
        ):
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value

        if record.exc_info:
            payload["error"] = self.formatException(record.exc_info)

        return json.dumps(payload, sort_keys=True)


def configure_json_logger(
    service: str,
    level: str,
    *,
    release_metadata: ReleaseMetadata | None = None,
) -> logging.Logger:
    logger = logging.getLogger(service)
    logger.handlers.clear()
    logger.setLevel(level)
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter(service, release_metadata))
    logger.addHandler(handler)
    return logger
