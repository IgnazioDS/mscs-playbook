ALTER TABLE analytics.events
  ADD COLUMN IF NOT EXISTS schema_version UInt16 DEFAULT 1 AFTER event_type;
