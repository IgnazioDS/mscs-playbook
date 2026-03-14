DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'event_processing'
      AND column_name = 'reserved_at'
  ) AND NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'event_processing'
      AND column_name = 'claimed_at'
  ) THEN
    ALTER TABLE event_processing RENAME COLUMN reserved_at TO claimed_at;
  END IF;
END $$;

ALTER TABLE event_processing
  ADD COLUMN IF NOT EXISTS lease_expires_at TIMESTAMP NULL,
  ADD COLUMN IF NOT EXISTS storage_written_at TIMESTAMP NULL,
  ADD COLUMN IF NOT EXISTS analytics_written_at TIMESTAMP NULL,
  ADD COLUMN IF NOT EXISTS failed_at TIMESTAMP NULL,
  ADD COLUMN IF NOT EXISTS attempt_count INTEGER NOT NULL DEFAULT 1;

UPDATE event_processing
SET status = 'claimed'
WHERE status = 'processing';

UPDATE event_processing
SET lease_expires_at = COALESCE(lease_expires_at, updated_at + INTERVAL '30 seconds')
WHERE status IN ('claimed', 'storage_written', 'analytics_written')
  AND lease_expires_at IS NULL;

UPDATE event_processing
SET failed_at = COALESCE(failed_at, updated_at)
WHERE status = 'failed'
  AND failed_at IS NULL;

ALTER TABLE event_processing DROP CONSTRAINT IF EXISTS event_processing_status_check;

ALTER TABLE event_processing
  ADD CONSTRAINT event_processing_status_check
  CHECK (status IN ('claimed', 'storage_written', 'analytics_written', 'completed', 'failed'));

CREATE INDEX IF NOT EXISTS idx_event_processing_status ON event_processing (status);
CREATE INDEX IF NOT EXISTS idx_event_processing_lease_expires_at ON event_processing (lease_expires_at);
