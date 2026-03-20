# Retention, Backup, and Restore

Phase 4 adds executable lifecycle controls and backup mechanics for the mini-platform. This remains a production-like backend workflow, not a managed SaaS backup product.

## Retention Scope

Authoritative control-plane retention:
- `ingest_log`
- `event_processing`
- `dlq_events`
- `replay_jobs`
- `replay_job_events`
- `operator_audit_log`
- `ingest_rejections`

Data-plane retention:
- MinIO raw objects under `raw/YYYY-MM-DD/...`
- ClickHouse analytics rows partitioned by `event_date`

Safety rules:
- active `event_processing` rows in `claimed`, `storage_written`, or `analytics_written` are not deleted
- non-terminal replay jobs are not deleted
- retention only applies outside the configured age windows
- each retention run writes a `retention_applied` audit row

Config knobs:
- `RETENTION_INGEST_LOG_DAYS`
- `RETENTION_EVENT_PROCESSING_DAYS`
- `RETENTION_DLQ_DAYS`
- `RETENTION_REPLAY_JOBS_DAYS`
- `RETENTION_AUDIT_LOG_DAYS`
- `RETENTION_INGEST_REJECTIONS_DAYS`
- `RETENTION_MINIO_RAW_DAYS`
- `RETENTION_CLICKHOUSE_DAYS`

Run retention:

```bash
python3.11 modules/06-big-data-architecture/03-implementations/mini-platform/scripts/retention.py
```

## What Is Authoritative

- Postgres is authoritative for ingest history, worker state, replay/redrive state, telemetry history, and operator audit history.
- MinIO raw objects are the authoritative retained raw payload surface for non-expired windows.
- ClickHouse analytics is a derived projection. It should be backed up when practical, but it can be rebuilt for retained windows from raw objects plus control-plane state.

## Postgres Control-plane Backup

Create a JSON snapshot:

```bash
python3.11 modules/06-big-data-architecture/03-implementations/mini-platform/scripts/backup_control_plane.py \
  --output modules/06-big-data-architecture/03-implementations/mini-platform/artifacts/control-plane-backup.json
```

Restore the snapshot:

```bash
python3.11 modules/06-big-data-architecture/03-implementations/mini-platform/scripts/restore_control_plane.py \
  modules/06-big-data-architecture/03-implementations/mini-platform/artifacts/control-plane-backup.json
```

Restore behavior:
- truncates control-plane tables in dependency-safe reverse order
- restores them in dependency-safe forward order
- preserves replay, DLQ, and audit history from the snapshot
- does not repopulate MinIO or ClickHouse automatically

## ClickHouse Backup Strategy

Schema and migration state export:

```bash
python3.11 modules/06-big-data-architecture/03-implementations/mini-platform/scripts/backup_clickhouse_schema.py \
  --host localhost \
  --port 9000 \
  --output modules/06-big-data-architecture/03-implementations/mini-platform/artifacts/clickhouse-schema.json
```

Restore expectation:
- reapply tracked ClickHouse migrations first
- restore analytics data only if you have an explicit partition or table backup
- otherwise rebuild retained analytics from retained raw objects and control-plane state

## MinIO Backup Strategy

Mirror raw objects:

```bash
python3.11 modules/06-big-data-architecture/03-implementations/mini-platform/scripts/backup_minio_objects.py \
  --endpoint localhost:9000 \
  --access-key bd06admin \
  --secret-key bd06password \
  --bucket events \
  --output-dir modules/06-big-data-architecture/03-implementations/mini-platform/artifacts/minio-backup
```

Restore expectation:
- restore mirrored raw objects back into the `events` bucket before replay-based analytics rebuilds
- if MinIO is lost and raw objects were not backed up, only non-expired control-plane history remains; raw payload recovery is then limited to what is still present in `ingest_log`

## Recovery Order

1. Restore Postgres control-plane state.
2. Recreate services and rerun Postgres and ClickHouse migrations.
3. Restore MinIO raw objects if available.
4. Restore ClickHouse analytics backup if available, or rebuild retained analytics via replay/redrive.
5. Validate `/ready`, `/ops/telemetry`, and spot-check `event_processing` and `replay_jobs`.
