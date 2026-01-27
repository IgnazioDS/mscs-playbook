# Mini Platform (Docker Compose)

Local, laptop-friendly big data platform that demonstrates ingestion, event bus,
object storage, OLTP logging, and analytics materialization.

## Quickstart
- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml up -d`
- `bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/demo.sh`
- `bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/teardown.sh`

## Service endpoints
- Ingest API: `http://localhost:8000/ingest`
- Ingest API docs: `http://localhost:8000/docs`
- MinIO console: `http://localhost:9001`
- Redpanda (Kafka API): `localhost:9092`
- ClickHouse HTTP: `http://localhost:8123`
- Postgres: `localhost:5432`

## Queries
Postgres:
- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T postgres psql -U bd06 -d bd06 -c "select count(*) from ingest_log;"`

ClickHouse:
- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T clickhouse clickhouse-client --query "select count(*) from analytics.events;"`

MinIO objects:
- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T minio sh -c "find /data -type f | head -n 5"`

Redpanda topics:
- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T redpanda rpk topic list`

## Verification checklist
Ingest a sample event:
- `curl -fsS -X POST http://localhost:8000/ingest -H "Content-Type: application/json" -d '{"event_type":"order_created","event_time":"2026-01-27T12:00:00Z","order_id":"O-1","amount":10,"currency":"USD","customer_id":"C-1"}'`

Postgres counts:
- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T postgres psql -U bd06 -d bd06 -c "select count(*) from ingest_log;"`
- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T postgres psql -U bd06 -d bd06 -c "select count(*) from processed_events;"`

ClickHouse counts:
- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T clickhouse clickhouse-client --query "select count(*) from analytics.events;"`

MinIO objects:
- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T minio sh -c "find /data -type f | head -n 5"`

Redpanda topics:
- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T redpanda rpk topic list`

## What this teaches
- Event-driven ingestion with a durable log (Redpanda)
- Idempotent consumers with replay safety
- Raw storage in object store (MinIO)
- OLTP logging in Postgres
- Analytics materialization in ClickHouse
- Operability: lag, retries, DLQ, and replay

## ADRs
- [0001 Event Bus Choice](adrs/0001-event-bus-choice.md)
- [0002 Storage Layout](adrs/0002-storage-layout.md)
- [0003 Idempotency Strategy](adrs/0003-idempotency-strategy.md)
- [0004 Observability Baseline](adrs/0004-observability-baseline.md)
