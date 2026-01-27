"""Worker that consumes events, writes to storage, and handles idempotency."""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import psycopg2
from clickhouse_driver import Client as ClickHouseClient
from kafka import KafkaConsumer, KafkaProducer
from minio import Minio


def _get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def _parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)


def _connect_postgres(dsn: str) -> psycopg2.extensions.connection:
    conn = psycopg2.connect(dsn)
    conn.autocommit = True
    return conn


def _ensure_bucket(client: Minio, bucket: str) -> None:
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)


def _write_minio(client: Minio, bucket: str, object_name: str, payload: bytes) -> None:
    client.put_object(bucket, object_name, data=payload, length=len(payload), content_type="application/json")


def _insert_clickhouse(client: ClickHouseClient, row: Dict[str, Any]) -> None:
    client.execute(
        "INSERT INTO analytics.events (event_date, event_time, received_at, event_id, event_type, payload) VALUES",
        [
            (
                row["event_date"],
                row["event_time"],
                row["received_at"],
                row["event_id"],
                row["event_type"],
                row["payload"],
            )
        ],
    )


def _with_retries(func, max_retries: int = 3, base_sleep: float = 0.5) -> None:
    for attempt in range(max_retries):
        try:
            func()
            return
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(base_sleep * (2 ** attempt))


def main() -> None:
    kafka_bootstrap = _get_env("KAFKA_BOOTSTRAP_SERVERS")
    topic = _get_env("KAFKA_TOPIC")
    dlq_topic = _get_env("KAFKA_DLQ_TOPIC")
    group_id = _get_env("KAFKA_GROUP_ID", "worker-group")
    pg_dsn = _get_env("POSTGRES_DSN")

    minio_endpoint = _get_env("MINIO_ENDPOINT")
    minio_access = _get_env("MINIO_ACCESS_KEY")
    minio_secret = _get_env("MINIO_SECRET_KEY")
    minio_bucket = _get_env("MINIO_BUCKET", "events")

    clickhouse_host = _get_env("CLICKHOUSE_HOST")
    clickhouse_port = int(_get_env("CLICKHOUSE_PORT", "9000"))

    producer = KafkaProducer(
        bootstrap_servers=kafka_bootstrap,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_bootstrap,
        group_id=group_id,
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )

    pg_conn = _connect_postgres(pg_dsn)
    minio_client = Minio(minio_endpoint, access_key=minio_access, secret_key=minio_secret, secure=False)
    _ensure_bucket(minio_client, minio_bucket)

    ch_client = ClickHouseClient(host=clickhouse_host, port=clickhouse_port)

    print("worker: started consuming")

    for message in consumer:
        event = message.value
        event_id = str(event.get("event_id", ""))
        if not event_id:
            continue

        def process() -> None:
            with pg_conn.cursor() as cur:
                cur.execute("SELECT 1 FROM processed_events WHERE event_id = %s", (event_id,))
                if cur.fetchone() is not None:
                    return

            event_time_raw = event.get("event_time") or event.get("received_at")
            event_time = _parse_time(event_time_raw)
            received_at = _parse_time(event.get("received_at"))
            event_type = str(event.get("event_type", "unknown"))
            payload = json.dumps(event).encode("utf-8")

            object_name = f"raw/{event_time.date().isoformat()}/{event_id}.json"
            _write_minio(minio_client, minio_bucket, object_name, payload)

            row = {
                "event_date": event_time.date(),
                "event_time": event_time,
                "received_at": received_at,
                "event_id": event_id,
                "event_type": event_type,
                "payload": payload.decode("utf-8"),
            }
            _insert_clickhouse(ch_client, row)

            with pg_conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO processed_events (event_id, processed_at) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (event_id, datetime.now(timezone.utc)),
                )

        try:
            _with_retries(process)
            consumer.commit()
        except Exception as exc:
            error_payload = {
                "event_id": event_id,
                "error": str(exc),
                "payload": event,
                "failed_at": datetime.now(timezone.utc).isoformat(),
            }
            producer.send(dlq_topic, error_payload)
            producer.flush(2)
            with pg_conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO dlq_events (event_id, error, payload, failed_at) VALUES (%s, %s, %s, %s)",
                    (event_id, str(exc), json.dumps(event), datetime.now(timezone.utc)),
                )
            consumer.commit()


if __name__ == "__main__":
    main()
