CREATE TABLE IF NOT EXISTS ingest_log (
  id SERIAL PRIMARY KEY,
  event_id TEXT UNIQUE NOT NULL,
  received_at TIMESTAMP NOT NULL,
  payload JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS processed_events (
  event_id TEXT PRIMARY KEY,
  processed_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS dlq_events (
  id SERIAL PRIMARY KEY,
  event_id TEXT,
  error TEXT NOT NULL,
  payload JSONB NOT NULL,
  failed_at TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_ingest_log_received_at ON ingest_log (received_at);
