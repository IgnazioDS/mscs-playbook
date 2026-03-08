# p2-big-data-mini-platform

## Purpose
Run an end-to-end local data platform (ingest -> log -> object storage -> analytics) and validate basic reliability checks.

## Scope
- Stand up the mini-platform stack using Docker Compose.
- Execute deterministic ingestion/demo flow.
- Verify operational outputs in Postgres, ClickHouse, and MinIO.

## Modules Used
- 06-big-data-architecture
- 07-data-mining

## How to Run
```bash
docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml up -d
bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/demo.sh
```

## How to Test
```bash
python3 -m pytest -q modules/06-big-data-architecture/03-implementations/python/tests
docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T postgres psql -U bd06 -d bd06 -c "select count(*) from ingest_log;"
docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml exec -T clickhouse clickhouse-client --query "select count(*) from analytics.events;"
```

## Expected Output
- Demo script ingests events without runtime errors.
- Postgres `ingest_log` and ClickHouse `analytics.events` contain rows.
- Python pipeline tests pass.
