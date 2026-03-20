"""Scoped API key helpers for the mini-platform."""

from __future__ import annotations

import re
from dataclasses import dataclass


_KEY_ID_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{1,63}$")


@dataclass(frozen=True)
class APIKeyRecord:
    key_id: str
    secret: str
    scope: str


def parse_api_keys(raw_value: str, *, scope: str) -> dict[str, APIKeyRecord]:
    keys: dict[str, APIKeyRecord] = {}

    for raw_entry in raw_value.split(","):
        entry = raw_entry.strip()
        if not entry:
            continue

        if ":" not in entry:
            raise ValueError(
                f"Invalid {scope} key entry '{entry}'. Expected '<key_id>:<secret>'"
            )

        key_id, secret = entry.split(":", 1)
        key_id = key_id.strip()
        secret = secret.strip()

        if not _KEY_ID_PATTERN.match(key_id):
            raise ValueError(f"Invalid {scope} key id: {key_id}")
        if not secret:
            raise ValueError(f"Missing secret for {scope} key id: {key_id}")
        if key_id in keys:
            raise ValueError(f"Duplicate {scope} key id: {key_id}")

        keys[key_id] = APIKeyRecord(key_id=key_id, secret=secret, scope=scope)

    if not keys:
        raise ValueError(f"At least one {scope} key must be configured")

    return keys


def key_ids(keys: dict[str, APIKeyRecord]) -> list[str]:
    return sorted(keys)
