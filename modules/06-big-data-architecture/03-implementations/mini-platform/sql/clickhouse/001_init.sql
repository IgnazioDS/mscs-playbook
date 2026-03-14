CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.schema_migrations (
  version String,
  applied_at DateTime
)
ENGINE = MergeTree
ORDER BY version;
