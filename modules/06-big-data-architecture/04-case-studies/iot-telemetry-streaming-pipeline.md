# IoT Telemetry Streaming Pipeline

## 1. Context and requirements
- Throughput: 50k events/sec average, 200k events/sec peak (4x)
- Latency target: 99% of telemetry visible in dashboards < 30 seconds
- Retention: raw telemetry 30 days, aggregated metrics 2 years
- Compliance: device identifiers treated as sensitive; regional data residency

## 2. Proposed architecture (diagram-as-text)
Devices -> Gateway -> Ingestion API -> Event Bus ->
  Stream Processor ->
    Object Storage (raw) + Time-Series Store/Analytics (aggregates)

## 3. Data contracts
- Event schema (JSON example):
```json
{
  "event_id": "uuid",
  "device_id": "D-789",
  "event_time": "2026-01-27T12:00:00Z",
  "sensor_type": "temperature",
  "value": 21.4,
  "unit": "C",
  "firmware_version": "1.2.3",
  "region": "us-east"
}
```
- Versioning strategy: explicit schema_version field; support two versions in parallel
- Ownership and change management: device team proposes schema changes; pipeline team approves and validates

## 4. Storage layout and modeling
- Raw: object storage partitioned by event_date and region
- Analytics: ClickHouse (or time-series DB) with partitions by event_date and device_id hash
- Indexing: primary key (device_id, event_time); rollups stored in hourly aggregates
- Tradeoff: streaming-first reduces latency but increases state management complexity

## 5. Reliability plan
- Delivery semantics: at-least-once
- Idempotency strategy: de-dup by event_id before aggregation
- Retries and backoff: bounded retries; drop to DLQ after max attempts
- Dead-letter strategy: DLQ topic with device metadata for reprocessing
- Replay strategy: reprocess from object storage for historical backfills

## 6. Cost and scaling levers
- Scale drivers: device count, sampling frequency, retention
- Levers: sampling at edge, compression, TTL for raw storage, pre-aggregation
- Cost placeholder: ClickHouse storage $/TB-month, driven by retention and rollup granularity

## 7. Observability and SLOs
- SLO: 99% of telemetry visible in dashboards within 30 seconds
- Metrics: ingest throughput, consumer lag, aggregation latency, DLQ count
- Logs/traces: per-device correlation IDs
- Dashboards: latency percentiles, error rates, device-level dropouts
- Security/governance: region-based access control; encryption at rest

## 8. What can go wrong and mitigations
1) Gateway overload -> backpressure and adaptive sampling
2) Duplicate telemetry -> idempotency via event_id
3) Out-of-order events -> use event_time for aggregation windows
4) Consumer crash -> auto restart, replay from offsets
5) Storage growth -> TTL and compaction policies
6) Data residency breach -> enforce region routing and access controls

## 9. If I were the tech lead: next 30 days plan
- Finalize telemetry schema with device team
- Build ingest API with validation
- Set up stream processing job and aggregates
- Implement lag and latency dashboards
- Define retention and TTL policies
- Run load tests at peak throughput
- Build DLQ triage workflow
- Add device-level anomaly detection
- Review regional compliance requirements
- Cost model and optimization plan
