"""Validated configuration for the ingest API."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlparse

from mini_platform.auth import APIKeyRecord, parse_api_keys
from mini_platform.release import ReleaseMetadata


AppEnv = Literal["local", "test", "production"]
DEMO_INGEST_API_KEY = "local-demo-ingest-key"
DEMO_OPERATOR_API_KEY = "local-demo-ops-key"
_VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
_WEAK_SECRET_VALUES = {
    "",
    "bd06",
    "bd06admin",
    "bd06password",
    "changeme",
    "change-me",
    "password",
    "secret",
    DEMO_INGEST_API_KEY,
    DEMO_OPERATOR_API_KEY,
}
_PLACEHOLDER_PREFIXES = ("replace-", "example-", "placeholder-", "changeme-")


def _get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Missing required env var: {name}")
    return value.strip()


def _get_env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default

    value = raw.strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"Invalid boolean value for {name}: {raw}")


def _get_env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"Invalid integer value for {name}: {raw}") from exc


def _extract_password_from_dsn(dsn: str) -> str | None:
    if "://" in dsn:
        parsed = urlparse(dsn)
        return parsed.password

    match = re.search(r"(?:^|\s)password=([^\s]+)", dsn)
    return match.group(1) if match else None


def _is_weak_secret(value: str | None) -> bool:
    if value is None:
        return True

    normalized = value.strip().lower()
    if normalized in _WEAK_SECRET_VALUES:
        return True
    return any(normalized.startswith(prefix) for prefix in _PLACEHOLDER_PREFIXES)


def _load_scoped_keys(
    *,
    env_name: str,
    legacy_env_name: str,
    default_value: str,
    scope: str,
) -> dict[str, APIKeyRecord]:
    raw = os.getenv(env_name)
    if raw:
        return parse_api_keys(raw, scope=scope)

    legacy = os.getenv(legacy_env_name)
    if legacy:
        default_key_id = "legacy-ingest" if scope == "ingest" else "legacy-ops"
        return parse_api_keys(f"{default_key_id}:{legacy}", scope=scope)

    return parse_api_keys(default_value, scope=scope)


@dataclass(frozen=True)
class IngestAPISettings:
    app_env: AppEnv
    kafka_bootstrap_servers: str
    kafka_topic: str
    postgres_dsn: str
    auth_enabled: bool
    ingest_api_keys: dict[str, APIKeyRecord]
    operator_api_keys: dict[str, APIKeyRecord]
    allow_interactive_docs: bool
    max_request_bytes: int
    replay_job_timeout_seconds: int
    log_level: str
    release_metadata: ReleaseMetadata
    service_name: str = "ingest-api"
    auth_header_name: str = "X-API-Key"
    auth_key_id_header_name: str = "X-API-Key-Id"

    @property
    def docs_enabled(self) -> bool:
        if self.app_env == "production":
            return self.allow_interactive_docs
        return True

    @classmethod
    def from_env(cls) -> "IngestAPISettings":
        app_env = _get_env("APP_ENV", "local").lower()
        if app_env not in {"local", "test", "production"}:
            raise ValueError(f"Invalid APP_ENV: {app_env}")

        allow_interactive_docs = _get_env_bool(
            "INGEST_ALLOW_INTERACTIVE_DOCS",
            default=app_env != "production",
        )

        settings = cls(
            app_env=app_env,
            kafka_bootstrap_servers=_get_env("KAFKA_BOOTSTRAP_SERVERS"),
            kafka_topic=_get_env("KAFKA_TOPIC"),
            postgres_dsn=_get_env("POSTGRES_DSN"),
            auth_enabled=_get_env_bool("INGEST_AUTH_ENABLED", default=True),
            ingest_api_keys=_load_scoped_keys(
                env_name="INGEST_API_KEYS",
                legacy_env_name="INGEST_API_KEY",
                default_value=f"local-ingest:{DEMO_INGEST_API_KEY}",
                scope="ingest",
            ),
            operator_api_keys=_load_scoped_keys(
                env_name="OPERATOR_API_KEYS",
                legacy_env_name="OPERATOR_API_KEY",
                default_value=f"local-ops:{DEMO_OPERATOR_API_KEY}",
                scope="operator",
            ),
            allow_interactive_docs=allow_interactive_docs,
            max_request_bytes=_get_env_int("INGEST_MAX_REQUEST_BYTES", 16_384),
            replay_job_timeout_seconds=_get_env_int("REPLAY_JOB_TIMEOUT_SECONDS", 600),
            log_level=_get_env("LOG_LEVEL", "INFO").upper(),
            release_metadata=ReleaseMetadata(
                version=_get_env("APP_VERSION", "dev"),
                build_sha=_get_env("APP_BUILD_SHA", "local"),
                build_time=_get_env("APP_BUILD_TIME", "unknown"),
            ),
        )
        settings._validate()
        return settings

    def _validate(self) -> None:
        if self.max_request_bytes <= 0:
            raise ValueError("INGEST_MAX_REQUEST_BYTES must be greater than zero")

        if self.replay_job_timeout_seconds <= 0:
            raise ValueError("REPLAY_JOB_TIMEOUT_SECONDS must be greater than zero")

        if self.log_level not in _VALID_LOG_LEVELS:
            raise ValueError(f"Invalid LOG_LEVEL: {self.log_level}")

        if self.auth_enabled:
            if not self.ingest_api_keys:
                raise ValueError("INGEST_API_KEYS must define at least one ingest key")
            if not self.operator_api_keys:
                raise ValueError("OPERATOR_API_KEYS must define at least one operator key")

        ingest_secrets = {record.secret for record in self.ingest_api_keys.values()}
        operator_secrets = {record.secret for record in self.operator_api_keys.values()}
        if ingest_secrets & operator_secrets:
            raise ValueError("INGEST_API_KEYS and OPERATOR_API_KEYS must use different secrets")

        if self.app_env != "production":
            return

        if not self.auth_enabled:
            raise ValueError("INGEST_AUTH_ENABLED must be true in production")

        for record in self.ingest_api_keys.values():
            if _is_weak_secret(record.secret):
                raise ValueError(f"INGEST_API_KEYS contains an insecure secret for key id {record.key_id}")

        for record in self.operator_api_keys.values():
            if _is_weak_secret(record.secret):
                raise ValueError(f"OPERATOR_API_KEYS contains an insecure secret for key id {record.key_id}")

        postgres_password = _extract_password_from_dsn(self.postgres_dsn)
        if _is_weak_secret(postgres_password):
            raise ValueError("POSTGRES_DSN uses an insecure password for production")
