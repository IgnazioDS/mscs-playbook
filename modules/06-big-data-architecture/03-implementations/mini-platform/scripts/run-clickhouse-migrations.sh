#!/usr/bin/env bash
set -euo pipefail

CLICKHOUSE_HOST="${CLICKHOUSE_HOST:-clickhouse}"
CLICKHOUSE_PORT="${CLICKHOUSE_PORT:-9000}"
MIGRATIONS_DIR="${MIGRATIONS_DIR:-/migrations}"
MIGRATIONS_TABLE="${MIGRATIONS_TABLE:-analytics.schema_migrations}"

clickhouse() {
  clickhouse-client --host "$CLICKHOUSE_HOST" --port "$CLICKHOUSE_PORT" --query "$1"
}

bootstrap_migrations_table() {
  clickhouse "CREATE DATABASE IF NOT EXISTS analytics"
  clickhouse "
    CREATE TABLE IF NOT EXISTS ${MIGRATIONS_TABLE} (
      version String,
      applied_at DateTime
    )
    ENGINE = MergeTree
    ORDER BY version
  "
}

bootstrap_migrations_table

for migration in "$MIGRATIONS_DIR"/*.sql; do
  version="$(basename "$migration" .sql)"
  applied_count="$(clickhouse "SELECT count() FROM ${MIGRATIONS_TABLE} WHERE version = '${version}'" | tr -d '[:space:]')"

  if [[ "$applied_count" != "0" ]]; then
    echo "skipping clickhouse migration ${version}"
    continue
  fi

  echo "applying clickhouse migration ${version}"
  clickhouse-client --host "$CLICKHOUSE_HOST" --port "$CLICKHOUSE_PORT" --multiquery < "$migration"
  clickhouse "INSERT INTO ${MIGRATIONS_TABLE} (version, applied_at) VALUES ('${version}', now())"
done
