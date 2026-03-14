CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.events (
  event_date Date,
  event_time DateTime,
  received_at DateTime,
  event_id String,
  event_type String,
  payload String
)
ENGINE = MergeTree
PARTITION BY event_date
ORDER BY (event_date, event_type, event_id);
