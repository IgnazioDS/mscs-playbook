ALTER TABLE event_processing
  ADD COLUMN IF NOT EXISTS owner_token TEXT NULL,
  ADD COLUMN IF NOT EXISTS lease_generation BIGINT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS heartbeat_at TIMESTAMPTZ NULL;

UPDATE event_processing
SET lease_generation = CASE WHEN lease_generation < 1 THEN 1 ELSE lease_generation END,
    heartbeat_at = COALESCE(heartbeat_at, updated_at),
    owner_token = COALESCE(owner_token, CONCAT('legacy-', event_id, '-', EXTRACT(EPOCH FROM updated_at)::BIGINT))
WHERE lease_generation < 1
   OR heartbeat_at IS NULL
   OR owner_token IS NULL;

CREATE INDEX IF NOT EXISTS idx_event_processing_owner_token
  ON event_processing (owner_token);
CREATE INDEX IF NOT EXISTS idx_event_processing_heartbeat_at
  ON event_processing (heartbeat_at);

ALTER TABLE replay_jobs
  ADD COLUMN IF NOT EXISTS skipped_events INTEGER NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS owner_token TEXT NULL,
  ADD COLUMN IF NOT EXISTS lease_generation BIGINT NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS heartbeat_at TIMESTAMPTZ NULL,
  ADD COLUMN IF NOT EXISTS cancel_requested_at TIMESTAMPTZ NULL,
  ADD COLUMN IF NOT EXISTS cancelled_at TIMESTAMPTZ NULL,
  ADD COLUMN IF NOT EXISTS deadline_at TIMESTAMPTZ NULL,
  ADD COLUMN IF NOT EXISTS timed_out_at TIMESTAMPTZ NULL,
  ADD COLUMN IF NOT EXISTS terminal_reason TEXT NULL,
  ADD COLUMN IF NOT EXISTS terminal_detail TEXT NULL;

UPDATE replay_jobs
SET lease_generation = CASE WHEN lease_generation < 1 THEN 1 ELSE lease_generation END,
    heartbeat_at = COALESCE(heartbeat_at, updated_at),
    owner_token = COALESCE(owner_token, CONCAT('legacy-replay-', replay_job_id)),
    deadline_at = COALESCE(deadline_at, requested_at + INTERVAL '30 minutes')
WHERE lease_generation < 1
   OR heartbeat_at IS NULL
   OR owner_token IS NULL
   OR deadline_at IS NULL;

ALTER TABLE replay_jobs DROP CONSTRAINT IF EXISTS replay_jobs_status_check;

ALTER TABLE replay_jobs
  ADD CONSTRAINT replay_jobs_status_check
  CHECK (status IN ('requested', 'running', 'completed', 'failed', 'cancelled', 'timed_out'));

ALTER TABLE replay_job_events DROP CONSTRAINT IF EXISTS replay_job_events_status_check;

ALTER TABLE replay_job_events
  ADD CONSTRAINT replay_job_events_status_check
  CHECK (status IN ('pending', 'published', 'completed', 'failed', 'skipped'));

CREATE INDEX IF NOT EXISTS idx_replay_jobs_deadline_at
  ON replay_jobs (deadline_at);
CREATE INDEX IF NOT EXISTS idx_replay_jobs_lease_expires_at
  ON replay_jobs (lease_expires_at);
CREATE INDEX IF NOT EXISTS idx_replay_jobs_cancel_requested_at
  ON replay_jobs (cancel_requested_at);
CREATE INDEX IF NOT EXISTS idx_replay_jobs_owner_token
  ON replay_jobs (owner_token);
