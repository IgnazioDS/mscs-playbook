# Release and Rollback

Phase 4 packages the mini-platform with explicit release metadata and repeatable local or production-like command surfaces.

## Release Metadata

Services expose release metadata from:
- `APP_VERSION`
- `APP_BUILD_SHA`
- `APP_BUILD_TIME`

The same metadata appears in:
- JSON logs
- `/telemetry`
- `/ops/telemetry`
- OCI image labels in the service Dockerfiles

## Command Surface

Primary packaged commands:

```bash
make -C modules/06-big-data-architecture/03-implementations/mini-platform compose-config
make -C modules/06-big-data-architecture/03-implementations/mini-platform up-local
make -C modules/06-big-data-architecture/03-implementations/mini-platform up-prod-like
make -C modules/06-big-data-architecture/03-implementations/mini-platform down
make -C modules/06-big-data-architecture/03-implementations/mini-platform retention
make -C modules/06-big-data-architecture/03-implementations/mini-platform backup-control-plane
```

Env flows:
- local: [`.env.local.example`](.env.local.example)
- production-like: [`.env.production.example`](.env.production.example)

## Upgrade Procedure

1. Create a control-plane backup.
2. Update env values for the new `APP_VERSION`, `APP_BUILD_SHA`, and rotated keys if needed.
3. Run compose build or pull for the new images.
4. Run Postgres and ClickHouse migrations.
5. Bring the stack up and wait for `/ready`.
6. Check `/ops/telemetry` and confirm release metadata matches the intended version.
7. Run the lightweight load harness and SLO check if this is a production-like validation window.

## Rollback Procedure

1. Stop new ingest traffic if possible.
2. Bring the stack down.
3. Restore the previous env values and image metadata.
4. Restore Postgres control-plane backup if the failed rollout mutated control-plane state incompatibly.
5. Bring the previous stack back up.
6. Validate `/ready`, `/ops/telemetry`, and replay queue state before re-enabling ingest.

Rollback caveats:
- ClickHouse rows written by a failed rollout are still analytics-side effects unless you restore or rebuild that projection.
- Postgres control-plane restore is authoritative for replay and DLQ history.
- This repo does not yet provide zero-downtime rollback orchestration.
