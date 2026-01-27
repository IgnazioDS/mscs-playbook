# Big Data Architecture Foundations

## What it is
A practical framework for designing data systems that handle high volume,
velocity, and variety while meeting reliability, latency, and cost goals.

## Why it matters
Big data systems fail when scale assumptions are wrong. Solid foundations
prevent rework, outages, and spiraling costs.

## Architecture patterns
- Separation of OLTP and analytics workloads
- Event-driven ingestion with durable logs
- Batch and streaming pipelines with clear SLAs
- Data contracts and schema governance

## Failure modes
- Hot partitions and unbounded storage growth
- Implicit coupling between producers and consumers
- Hidden backpressure leading to data loss
- Observability gaps masking lag and failures

## Operability checklist
- Define SLOs for ingestion latency and data freshness
- Monitor backlog, lag, and storage growth
- Enforce schemas at ingestion
- Plan for replays and backfills
- Test failure scenarios (broker outage, slow consumers)

## References
- Designing Data-Intensive Applications (Kleppmann) — https://dataintensive.net/
- The Data Warehouse Toolkit (Kimball) — https://www.kimballgroup.com/
