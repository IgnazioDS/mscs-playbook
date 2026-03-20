---
summary: Support matrix for the repository's production-aware surfaces and their current operational boundaries.
tags:
  - archive
  - support
  - operations
status: stable
format: support-matrix
difficulty: intermediate
---

# Supported Surfaces

This repository is not a single deployable product. Phase 4 scale and productization still apply only to the mini-platform surface.

## Current Matrix

| Surface | Current status | Supported workflows | Production-aware safeguards | Explicitly not claimed |
| --- | --- | --- | --- | --- |
| `modules/06-big-data-architecture/03-implementations/mini-platform` | Primary production-like backend package | Local Docker Compose, Python 3.11 service tests, deterministic eval suite, dedicated integration CI, release/rollback scripts, retention and backup tooling | Validated env modes, scoped ingest/operator keys, fenced worker and replay leases, replay cancellation/timeouts, Postgres and ClickHouse migrations, structured logs, durable telemetry, load/SLO scripts, release metadata | Cloud readiness, full security platform completeness, multi-tenant support, major observability vendor stack |
| `projects/p2-big-data-mini-platform` | Project wrapper for the mini-platform | Local runbook, production-like env examples, release/rollback guidance, and verification around the mini-platform | Phase 4 operator docs, lifecycle controls, and packaged command surface | Separate product deployment story |
| `modules/11-generative-ai/03-implementations/python` | Offline deterministic demo | Local Python 3.11 CLI and tests | None beyond deterministic local execution | Deployed service readiness, real agent autonomy, cloud readiness |
| `projects/p7-genai-rag-agent-app` | Project wrapper for the offline GenAI demo | Local deterministic run and test flow | None beyond deterministic local execution | Production agent app maturity or autonomous operation |

## Supported for the Mini-platform
- Local Python 3.11 workflows and service-local tests.
- Local Docker Compose with explicit Postgres and ClickHouse migrations.
- Scoped API-key protected ingestion plus authenticated `/ops` endpoints for replay jobs, cancellation, DLQ inspection, redrive, durable telemetry, and event lifecycle inspection.
- Schema-versioned ingest for the supported `order_created` contract at `schema_version=1`.
- Dedicated CI coverage that validates compose config, builds images, runs migrations, starts the stack, and checks the happy path plus replay-after-completion safety.
- Deterministic scenario evaluations for normal completion, failure/recovery, replay, redrive, and operator telemetry consistency.
- Production-like packaging via env examples, Makefile entrypoints, release metadata, retention scripts, backup/restore scripts, load smoke, and SLO evaluation.

## Still Deferred
- Cloud deployment and infrastructure as code.
- Production security completeness such as secret managers, TLS termination, RBAC, and external identity.
- Multi-tenant support or billing.
- Prometheus, Grafana, or distributed tracing platforms.
- Exactly-once semantics across Kafka, storage, and analytics.
