CREATE TABLE IF NOT EXISTS ingest_log (
  id SERIAL PRIMARY KEY,
  event_id TEXT UNIQUE NOT NULL,
  received_at TIMESTAMP NOT NULL,
  payload JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS event_processing (
  event_id TEXT PRIMARY KEY,
  status TEXT NOT NULL CHECK (status IN ('processing', 'completed', 'failed')),
  reserved_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  completed_at TIMESTAMP NULL,
  last_error TEXT NULL
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
CREATE INDEX IF NOT EXISTS idx_event_processing_status ON event_processing (status);
