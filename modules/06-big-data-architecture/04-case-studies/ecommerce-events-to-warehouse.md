# Ecommerce Events to Warehouse

## 1. Context and requirements
- Throughput: 3k events/sec average, 10k events/sec peak (3.3x)
- Latency target: 99% of events available in analytics < 5 minutes
- Retention: raw events 180 days, curated tables 2 years
- Compliance: PCI and GDPR; PII minimization and access controls

## 2. Proposed architecture (diagram-as-text)
Client -> Ingestion API -> Event Bus (Kafka/Redpanda) ->
  Stream Processor/Worker ->
    Object Storage (raw) + OLTP (order state) + Analytics Warehouse (facts)

## 3. Data contracts
- Event schema (JSON example):
```json
{
  "event_id": "uuid",
  "event_type": "order_created",
  "event_time": "2026-01-27T12:00:00Z",
  "order_id": "O-123",
  "customer_id": "C-456",
  "amount": 129.99,
  "currency": "USD",
  "country": "US",
  "items": [{"sku": "SKU-1", "qty": 2}]
}
```
- Versioning strategy: semantic version in event header (v1, v2); additive changes only in minor versions
- Ownership and change management: producer team owns schema; changes reviewed via schema registry PR + backward compatibility check

## 4. Storage layout and modeling
- Raw: object storage partitioned by event_date and event_type
- Warehouse: star schema with fact_orders and dim_customer, dim_product
- Partitioning: event_date (daily) + country; clustering on order_id
- Lake/warehouse choice: warehouse for BI queries; lake for low-cost raw retention
- Tradeoff: strict warehouse schema improves query performance but adds modeling overhead

## 5. Reliability plan
- Delivery semantics: at-least-once from event bus
- Idempotency strategy: dedupe table keyed by event_id in OLTP; upsert to warehouse
- Retries and backoff: exponential backoff, max 5 attempts
- Dead-letter strategy: DLQ topic and DLQ table with error metadata
- Replay strategy: re-consume from event bus with idempotent consumers; backfill from raw lake

## 6. Cost and scaling levers
- Scale drivers: event volume, retention window, query concurrency
- Levers: compression, TTL for raw data, query caching, downsampling for long-term metrics
- Cost placeholder: object storage $/TB-month, influenced by retention and compression ratio

## 7. Observability and SLOs
- SLO: 99% of events available in warehouse within 5 minutes
- Metrics: ingest rate, consumer lag, warehouse load time, DLQ rate
- Logs/traces: trace_id per event, correlated with order_id
- Dashboards: freshness, lag, error budget burn
- Security/governance: PII fields masked in analytics; access policies per role

## 8. What can go wrong and mitigations
1) Event bus outage -> buffer on ingest, retry with circuit breaker
2) Schema breaking change -> registry compatibility checks, reject publish
3) Hot partitions -> re-partition by event_date + hash(order_id)
4) Consumer lag -> scale workers, adjust batch sizes
5) Duplicate events -> enforce idempotency via event_id
6) Warehouse load failure -> route to DLQ, reprocess from raw

## 9. If I were the tech lead: next 30 days plan
- Formalize event schema and publish contract
- Implement ingestion + idempotency store
- Stand up warehouse tables and partitions
- Build consumer metrics and lag dashboards
- Define SLOs and error budgets
- Create replay runbook and backfill procedure
- Pilot data quality checks on key fields
- Test failure drills (broker outage, schema change)
- Review PII handling and access controls
- Cost baseline and monthly reporting
