ALTER TABLE ingest_log
  ADD COLUMN IF NOT EXISTS event_type TEXT,
  ADD COLUMN IF NOT EXISTS schema_version INTEGER,
  ADD COLUMN IF NOT EXISTS event_time TIMESTAMPTZ;

UPDATE ingest_log
SET event_type = COALESCE(event_type, payload->>'event_type'),
    schema_version = COALESCE(
      schema_version,
      NULLIF(payload->>'schema_version', '')::INTEGER,
      1
    ),
    event_time = COALESCE(
      event_time,
      NULLIF(payload->>'event_time', '')::TIMESTAMPTZ
    )
WHERE event_type IS NULL
   OR schema_version IS NULL
   OR event_time IS NULL;

ALTER TABLE ingest_log
  ALTER COLUMN event_type SET NOT NULL,
  ALTER COLUMN schema_version SET NOT NULL,
  ALTER COLUMN event_time SET NOT NULL;

CREATE INDEX IF NOT EXISTS idx_ingest_log_event_time ON ingest_log (event_time);
CREATE INDEX IF NOT EXISTS idx_ingest_log_event_type_schema_version
  ON ingest_log (event_type, schema_version);

CREATE TABLE IF NOT EXISTS ingest_rejections (
  id BIGSERIAL PRIMARY KEY,
  path TEXT NOT NULL,
  status_code INTEGER NOT NULL,
  reason TEXT NOT NULL,
  detail JSONB NOT NULL DEFAULT '{}'::JSONB,
  rejected_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_ingest_rejections_rejected_at
  ON ingest_rejections (rejected_at DESC);

CREATE TABLE IF NOT EXISTS replay_jobs (
  replay_job_id TEXT PRIMARY KEY,
  job_type TEXT NOT NULL CHECK (job_type IN ('replay', 'redrive')),
  selector_type TEXT NOT NULL CHECK (selector_type IN ('event_id', 'time_range', 'dlq_event')),
  selector JSONB NOT NULL,
  source_type TEXT NOT NULL CHECK (source_type IN ('ingest_log', 'dlq_events')),
  status TEXT NOT NULL CHECK (status IN ('requested', 'running', 'completed', 'failed')),
  requested_by TEXT NOT NULL,
  requested_at TIMESTAMPTZ NOT NULL,
  started_at TIMESTAMPTZ NULL,
  completed_at TIMESTAMPTZ NULL,
  failed_at TIMESTAMPTZ NULL,
  updated_at TIMESTAMPTZ NOT NULL,
  lease_expires_at TIMESTAMPTZ NULL,
  attempt_count INTEGER NOT NULL DEFAULT 0,
  total_events INTEGER NOT NULL DEFAULT 0,
  published_events INTEGER NOT NULL DEFAULT 0,
  completed_events INTEGER NOT NULL DEFAULT 0,
  failed_events INTEGER NOT NULL DEFAULT 0,
  last_error TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_replay_jobs_status ON replay_jobs (status);
CREATE INDEX IF NOT EXISTS idx_replay_jobs_requested_at ON replay_jobs (requested_at DESC);

CREATE TABLE IF NOT EXISTS replay_job_events (
  replay_job_id TEXT NOT NULL REFERENCES replay_jobs (replay_job_id) ON DELETE CASCADE,
  event_id TEXT NOT NULL,
  source_type TEXT NOT NULL CHECK (source_type IN ('ingest_log', 'dlq_events')),
  source_row_id BIGINT NULL,
  event_payload JSONB NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending', 'published', 'completed', 'failed', 'skipped')),
  published_at TIMESTAMPTZ NULL,
  completed_at TIMESTAMPTZ NULL,
  failed_at TIMESTAMPTZ NULL,
  updated_at TIMESTAMPTZ NOT NULL,
  last_error TEXT NULL,
  last_observed_processing_status TEXT NULL,
  PRIMARY KEY (replay_job_id, event_id)
);

CREATE INDEX IF NOT EXISTS idx_replay_job_events_event_id ON replay_job_events (event_id);
CREATE INDEX IF NOT EXISTS idx_replay_job_events_status ON replay_job_events (status);

CREATE TABLE IF NOT EXISTS operator_audit_log (
  id BIGSERIAL PRIMARY KEY,
  action TEXT NOT NULL,
  actor TEXT NOT NULL,
  target_type TEXT NOT NULL,
  target_id TEXT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}'::JSONB,
  created_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_operator_audit_log_created_at
  ON operator_audit_log (created_at DESC);
