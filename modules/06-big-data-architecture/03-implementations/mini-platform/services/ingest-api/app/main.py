"""Minimal ingestion API for the mini platform."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4

import psycopg2
from fastapi import FastAPI, HTTPException
from kafka import KafkaProducer

app = FastAPI()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def _connect_postgres(dsn: str) -> psycopg2.extensions.connection:
    conn = psycopg2.connect(dsn)
    conn.autocommit = True
    return conn


def _make_producer(bootstrap_servers: str) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


@app.on_event("startup")
def startup() -> None:
    app.state.kafka_topic = _get_env("KAFKA_TOPIC")
    app.state.producer = _make_producer(_get_env("KAFKA_BOOTSTRAP_SERVERS"))
    app.state.pg_conn = _connect_postgres(_get_env("POSTGRES_DSN"))


@app.on_event("shutdown")
def shutdown() -> None:
    producer = getattr(app.state, "producer", None)
    if producer is not None:
        producer.flush(2)
        producer.close()
    pg_conn = getattr(app.state, "pg_conn", None)
    if pg_conn is not None:
        pg_conn.close()


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest")
def ingest(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload must be a JSON object")

    event = dict(payload)
    event_id = str(uuid4())
    event["event_id"] = event_id
    event["received_at"] = _utc_now_iso()

    producer: KafkaProducer = app.state.producer
    topic = app.state.kafka_topic
    producer.send(topic, event)
    producer.flush(2)

    pg_conn = app.state.pg_conn
    with pg_conn.cursor() as cur:
        cur.execute(
            "INSERT INTO ingest_log (event_id, received_at, payload) VALUES (%s, %s, %s)",
            (event_id, datetime.now(timezone.utc), json.dumps(event)),
        )

    return {"event_id": event_id, "status": "accepted"}
