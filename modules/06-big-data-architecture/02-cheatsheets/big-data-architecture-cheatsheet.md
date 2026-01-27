# Big Data Architecture Cheat Sheet

## Pattern selection guide
- **Batch**: large volumes, predictable latency, cost-optimized processing.
- **Streaming**: low-latency requirements, near real-time analytics.
- **Lakehouse**: combine low-cost storage with warehouse governance.

## Idempotency + replay checklist
- Define event_id or idempotency key
- Store processed IDs with retention window
- Make writes upsert or append-only with de-dup
- Document replay windows and backfill procedures

## Partitioning heuristics
- Partition by time for append-only facts
- Avoid high-cardinality partitions
- Keep partition size within query-friendly ranges
- Use clustering/sort keys for common filters

## Backpressure and DLQ strategy
- Bound consumer retries with exponential backoff
- Route poison messages to DLQ with metadata
- Alert on DLQ growth and retry exhaustion
- Keep reprocess tooling simple

## Minimum observability signals
- Ingestion rate, backlog, and consumer lag
- End-to-end freshness (event time to query time)
- Error rate, retry count, and DLQ volume
- Storage growth and query scan bytes
