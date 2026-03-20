"""Validated configuration for the worker."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import timedelta
from typing import Literal
from urllib.parse import urlparse

from mini_platform.release import ReleaseMetadata


AppEnv = Literal["local", "test", "production"]
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


@dataclass(frozen=True)
class WorkerSettings:
    app_env: AppEnv
    kafka_bootstrap_servers: str
    kafka_topic: str
    kafka_dlq_topic: str
    kafka_group_id: str
    postgres_dsn: str
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str
    minio_secure: bool
    clickhouse_host: str
    clickhouse_port: int
    clickhouse_database: str
    lease_seconds: int
    replay_poll_seconds: int
    replay_lease_seconds: int
    replay_job_timeout_seconds: int
    maintenance_poll_seconds: int
    retention_ingest_days: int
    retention_processing_days: int
    retention_dlq_days: int
    retention_replay_days: int
    retention_audit_days: int
    retention_rejections_days: int
    minio_retention_days: int
    clickhouse_retention_days: int
    log_level: str
    release_metadata: ReleaseMetadata
    service_name: str = "worker"

    @property
    def lease_timeout(self) -> timedelta:
        return timedelta(seconds=self.lease_seconds)

    @property
    def replay_lease_timeout(self) -> timedelta:
        return timedelta(seconds=self.replay_lease_seconds)

    @classmethod
    def from_env(cls) -> "WorkerSettings":
        app_env = _get_env("APP_ENV", "local").lower()
        if app_env not in {"local", "test", "production"}:
            raise ValueError(f"Invalid APP_ENV: {app_env}")

        settings = cls(
            app_env=app_env,
            kafka_bootstrap_servers=_get_env("KAFKA_BOOTSTRAP_SERVERS"),
            kafka_topic=_get_env("KAFKA_TOPIC"),
            kafka_dlq_topic=_get_env("KAFKA_DLQ_TOPIC"),
            kafka_group_id=_get_env("KAFKA_GROUP_ID", "worker-group"),
            postgres_dsn=_get_env("POSTGRES_DSN"),
            minio_endpoint=_get_env("MINIO_ENDPOINT"),
            minio_access_key=_get_env("MINIO_ACCESS_KEY"),
            minio_secret_key=_get_env("MINIO_SECRET_KEY"),
            minio_bucket=_get_env("MINIO_BUCKET", "events"),
            minio_secure=_get_env_bool("MINIO_SECURE", default=False),
            clickhouse_host=_get_env("CLICKHOUSE_HOST"),
            clickhouse_port=_get_env_int("CLICKHOUSE_PORT", 9000),
            clickhouse_database=_get_env("CLICKHOUSE_DATABASE", "analytics"),
            lease_seconds=_get_env_int("WORKER_LEASE_SECONDS", 30),
            replay_poll_seconds=_get_env_int("REPLAY_RUNNER_POLL_SECONDS", 2),
            replay_lease_seconds=_get_env_int("REPLAY_JOB_LEASE_SECONDS", 30),
            replay_job_timeout_seconds=_get_env_int("REPLAY_JOB_TIMEOUT_SECONDS", 600),
            maintenance_poll_seconds=_get_env_int("MAINTENANCE_POLL_SECONDS", 30),
            retention_ingest_days=_get_env_int("RETENTION_INGEST_LOG_DAYS", 30),
            retention_processing_days=_get_env_int("RETENTION_EVENT_PROCESSING_DAYS", 30),
            retention_dlq_days=_get_env_int("RETENTION_DLQ_DAYS", 30),
            retention_replay_days=_get_env_int("RETENTION_REPLAY_JOBS_DAYS", 30),
            retention_audit_days=_get_env_int("RETENTION_AUDIT_LOG_DAYS", 90),
            retention_rejections_days=_get_env_int("RETENTION_INGEST_REJECTIONS_DAYS", 30),
            minio_retention_days=_get_env_int("RETENTION_MINIO_RAW_DAYS", 30),
            clickhouse_retention_days=_get_env_int("RETENTION_CLICKHOUSE_DAYS", 30),
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
        if self.lease_seconds <= 0:
            raise ValueError("WORKER_LEASE_SECONDS must be greater than zero")

        if self.replay_poll_seconds <= 0:
            raise ValueError("REPLAY_RUNNER_POLL_SECONDS must be greater than zero")

        if self.replay_lease_seconds <= 0:
            raise ValueError("REPLAY_JOB_LEASE_SECONDS must be greater than zero")

        if self.replay_job_timeout_seconds <= 0:
            raise ValueError("REPLAY_JOB_TIMEOUT_SECONDS must be greater than zero")

        if self.maintenance_poll_seconds <= 0:
            raise ValueError("MAINTENANCE_POLL_SECONDS must be greater than zero")

        for name, value in (
            ("RETENTION_INGEST_LOG_DAYS", self.retention_ingest_days),
            ("RETENTION_EVENT_PROCESSING_DAYS", self.retention_processing_days),
            ("RETENTION_DLQ_DAYS", self.retention_dlq_days),
            ("RETENTION_REPLAY_JOBS_DAYS", self.retention_replay_days),
            ("RETENTION_AUDIT_LOG_DAYS", self.retention_audit_days),
            ("RETENTION_INGEST_REJECTIONS_DAYS", self.retention_rejections_days),
            ("RETENTION_MINIO_RAW_DAYS", self.minio_retention_days),
            ("RETENTION_CLICKHOUSE_DAYS", self.clickhouse_retention_days),
        ):
            if value <= 0:
                raise ValueError(f"{name} must be greater than zero")

        if self.log_level not in _VALID_LOG_LEVELS:
            raise ValueError(f"Invalid LOG_LEVEL: {self.log_level}")

        if self.app_env != "production":
            return

        postgres_password = _extract_password_from_dsn(self.postgres_dsn)
        if _is_weak_secret(postgres_password):
            raise ValueError("POSTGRES_DSN uses an insecure password for production")

        if _is_weak_secret(self.minio_access_key) or _is_weak_secret(self.minio_secret_key):
            raise ValueError("MINIO credentials are missing or insecure for production")

        if not self.minio_secure:
            raise ValueError("MINIO_SECURE must be true in production")
