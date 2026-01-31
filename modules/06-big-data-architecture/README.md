# 06-big-data-architecture

## Status

- Docs complete
- Case studies complete
- Mini platform complete
- ADRs complete

## Overview

This module focuses on practical big data architecture: event-driven ingestion,
reliable processing, storage tradeoffs (lake/lakehouse/warehouse), and
operability. The emphasis is on production-facing decisions, failure modes, and
runbooks rather than large codebases.

## Prerequisites

- Docker and docker compose
- curl

## Quickstart

- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml config`
- `docker compose -f modules/06-big-data-architecture/03-implementations/mini-platform/docker-compose.yml up -d`
- `bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/demo.sh`
- `bash modules/06-big-data-architecture/03-implementations/mini-platform/scripts/teardown.sh`

## Concepts

- [Big Data Architecture Foundations](01-concepts/big-data-architecture-foundations.md)
- [Data Lake, Lakehouse, and Warehouse](01-concepts/data-lake-lakehouse-warehouse.md)
- [Event-Driven Architecture and Streaming](01-concepts/event-driven-architecture-and-streaming.md)
- [Batch vs Streaming Tradeoffs](01-concepts/batch-vs-streaming-tradeoffs.md)
- [Data Modeling, Partitioning, and Indexing](01-concepts/data-modeling-partitioning-and-indexing.md)
- [Reliability, Idempotency, and the Exactly-Once Myth](01-concepts/reliability-idempotency-and-exactly-once-myth.md)
- [Orchestration and Pipelines](01-concepts/orchestration-and-pipelines.md)
- [Observability, SLOs, and Costs](01-concepts/observability-slos-and-costs.md)
- [Security, Governance, and Data Quality](01-concepts/security-governance-and-data-quality.md)

## Cheat sheet

- [Big Data Architecture Cheat Sheet](02-cheatsheets/big-data-architecture-cheatsheet.md)

## Case studies

- [Ecommerce Events to Warehouse](04-case-studies/ecommerce-events-to-warehouse.md)
- [IoT Telemetry Streaming Pipeline](04-case-studies/iot-telemetry-streaming-pipeline.md)
- [GenAI Analytics and Monitoring Pipeline](04-case-studies/genai-analytics-and-monitoring-pipeline.md)

## Mini platform

- [Mini platform README](03-implementations/mini-platform/README.md)

## ADRs

- [0001 Event Bus Choice](03-implementations/mini-platform/adrs/0001-event-bus-choice.md)
- [0002 Storage Layout](03-implementations/mini-platform/adrs/0002-storage-layout.md)
- [0003 Idempotency Strategy](03-implementations/mini-platform/adrs/0003-idempotency-strategy.md)
- [0004 Observability Baseline](03-implementations/mini-platform/adrs/0004-observability-baseline.md)
