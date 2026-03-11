# Big Data Architecture

## Status

- Concepts, cheat sheet, case studies, mini-platform, and exercises are present.
- The concept sequence now follows an explicit foundational-to-operational reading path.
- The module emphasizes architecture decisions, platform reliability, and operability over vendor-specific feature tours.

## Overview

This module covers the architectural foundations of modern data platforms:
durable ingestion, storage-layer tradeoffs, event-driven design, batch versus
stream processing, analytical modeling, reliability patterns, orchestration,
observability, cost control, governance, and data quality. The focus is on how
to design a platform that can be replayed, operated, and evolved safely under
real production constraints.

## Recommended learning path

1. Start with the core platform model: architecture foundations, storage patterns, and event-driven data flow.
2. Learn the tradeoffs between batch and streaming, then how data layout affects query cost and scalability.
3. Move into the operational core: reliability, idempotency, and orchestration.
4. Finish with platform operation concerns: observability, SLOs, cost discipline, security, governance, and quality controls.

## Prerequisites

- Basic SQL familiarity
- Comfort reading architecture diagrams and data-flow descriptions
- Docker and Docker Compose for the mini-platform walkthrough

## Quickstart

- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml config`
- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml up -d`
- `bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/demo.sh`
- `bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/teardown.sh`

## Concepts (reading order)

- [01 Big Data Architecture Foundations](01-concepts/01-big-data-architecture-foundations.md)
- [02 Data Lake, Lakehouse, and Warehouse](01-concepts/02-data-lake-lakehouse-and-warehouse.md)
- [03 Event-Driven Architecture and Streaming](01-concepts/03-event-driven-architecture-and-streaming.md)
- [04 Batch vs Streaming Tradeoffs](01-concepts/04-batch-vs-streaming-tradeoffs.md)
- [05 Data Modeling, Partitioning, and Indexing](01-concepts/05-data-modeling-partitioning-and-indexing.md)
- [06 Reliability, Idempotency, and the Exactly-Once Myth](01-concepts/06-reliability-idempotency-and-the-exactly-once-myth.md)
- [07 Orchestration and Pipelines](01-concepts/07-orchestration-and-pipelines.md)
- [08 Observability, SLOs, and Costs](01-concepts/08-observability-slos-and-costs.md)
- [09 Security, Governance, and Data Quality](01-concepts/09-security-governance-and-data-quality.md)

## Concept-to-platform bridge

- Read `01` through `03` before running the mini-platform so the ingestion and storage layout have clear meaning.
- Read `04` through `06` before changing pipeline semantics, replay behavior, or reliability assumptions.
- Read `07` through `09` alongside the case studies and exercise so operational tradeoffs stay concrete.

## Cheat sheet

- [Big Data Architecture Cheat Sheet](02-cheatsheets/big-data-architecture-cheatsheet.md)

## Case studies

- [Ecommerce Events to Warehouse](04-case-studies/ecommerce-events-to-warehouse.md)
- [IoT Telemetry Streaming Pipeline](04-case-studies/iot-telemetry-streaming-pipeline.md)
- [GenAI Analytics and Monitoring Pipeline](04-case-studies/genai-analytics-and-monitoring-pipeline.md)

## Implementations

- [Mini-platform README](03-implementations/mini-platform/README.md)
- [Python reference code](03-implementations/python/README.md)

## Mini-project

- [Event Pipeline Readiness](05-exercises/mini-project-event-pipeline.md)

## Architecture decision records

- [0001 Event Bus Choice](03-implementations/mini-platform/adrs/0001-event-bus-choice.md)
- [0002 Storage Layout](03-implementations/mini-platform/adrs/0002-storage-layout.md)
- [0003 Idempotency Strategy](03-implementations/mini-platform/adrs/0003-idempotency-strategy.md)
- [0004 Observability Baseline](03-implementations/mini-platform/adrs/0004-observability-baseline.md)
