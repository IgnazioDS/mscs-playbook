# GenAI Analytics and Monitoring Pipeline

## 1. Context and requirements
- Throughput: 1k requests/sec average, 5k requests/sec peak (5x)
- Latency target: 99% of usage metrics available < 2 minutes
- Retention: raw prompts/responses 30 days, aggregated metrics 1 year
- Compliance: PII redaction, prompt data classification, audit logging

## 2. Proposed architecture (diagram-as-text)
App -> Inference Gateway -> Ingestion API -> Event Bus ->
  Worker ->
    Object Storage (raw) + OLTP (audit log) + Analytics Store (metrics)

## 3. Data contracts
- Event schema (JSON example):
```json
{
  "event_id": "uuid",
  "request_id": "R-123",
  "user_id": "U-456",
  "event_time": "2026-01-27T12:00:00Z",
  "model": "gpt-4o-mini",
  "latency_ms": 780,
  "token_count": 1420,
  "policy_flags": ["pii_redacted"],
  "region": "us"
}
```
- Versioning strategy: include schema_version and model_version
- Ownership and change management: platform team owns schema; security signs off on new fields

## 4. Storage layout and modeling
- Raw: object storage partitioned by event_date and region; redact PII before write
- Analytics: ClickHouse or warehouse table partitioned by event_date, clustered on model
- Indexing: primary key (event_time, model); materialized views for daily metrics
- Tradeoff: streaming metrics provide quick feedback but can miss late-arriving events

## 5. Reliability plan
- Delivery semantics: at-least-once
- Idempotency strategy: dedupe by event_id, upsert metrics
- Retries and backoff: exponential backoff, bounded retries
- Dead-letter strategy: DLQ topic with schema and validation errors
- Replay strategy: reprocess raw object storage for backfills

## 6. Cost and scaling levers
- Scale drivers: request volume, model size, retention
- Levers: sampling for long-term metrics, compression, TTL for raw data
- Cost placeholder: analytics compute $/TB scanned, driven by query frequency and table design

## 7. Observability and SLOs
- SLO: 99% of metrics visible within 2 minutes
- Metrics: ingestion rate, lag, error rate, token usage, policy flag rates
- Logs/traces: trace per request_id, linked to policy decisions
- Dashboards: latency percentile, model utilization, policy violations
- Security/governance: prompt redaction, access audits, data classification

## 8. What can go wrong and mitigations
1) PII leakage -> redaction at ingest, audit logs
2) Schema drift -> schema registry checks and versioning
3) Model burst traffic -> autoscale workers and backpressure
4) Metrics lag -> increase consumer throughput
5) Query cost spikes -> caching and pre-aggregations
6) Missing audit logs -> dual-write with retries

## 9. If I were the tech lead: next 30 days plan
- Define data classification and redaction policy
- Implement ingestion and schema validation
- Build metrics tables and dashboards
- Add policy flag monitoring and alerts
- Run load tests with burst traffic
- Establish retention and deletion policies
- Build replay and backfill tooling
- Review access controls and audit requirements
- Cost baseline and optimization opportunities
- Security review for prompt handling
