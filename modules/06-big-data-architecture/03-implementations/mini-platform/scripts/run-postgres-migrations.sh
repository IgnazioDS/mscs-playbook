#!/usr/bin/env bash
set -euo pipefail

POSTGRES_DSN="${POSTGRES_DSN:?POSTGRES_DSN is required}"
MIGRATIONS_DIR="${MIGRATIONS_DIR:-/migrations}"

psql_cmd() {
  psql "$POSTGRES_DSN" -v ON_ERROR_STOP=1 "$@"
}

psql_cmd <<'SQL'
CREATE TABLE IF NOT EXISTS schema_migrations (
  version TEXT PRIMARY KEY,
  applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
SQL

while IFS= read -r migration; do
  version="$(basename "$migration")"
  already_applied="$(psql_cmd -t -A -c "SELECT 1 FROM schema_migrations WHERE version = '$version'")"
  if [[ "$already_applied" == "1" ]]; then
    echo "skip migration $version"
    continue
  fi

  echo "apply migration $version"
  psql_cmd -f "$migration"
  psql_cmd -c "INSERT INTO schema_migrations (version) VALUES ('$version')"
done < <(find "$MIGRATIONS_DIR" -maxdepth 1 -type f -name '*.sql' | sort)
