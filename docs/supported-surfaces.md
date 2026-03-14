# Supported Surfaces

This repository is not a single deployable product. Phase 3 capability expansion still applies only to the mini-platform surface.

## Current Matrix

| Surface | Current status | Supported workflows | Production-aware safeguards | Explicitly not claimed |
| --- | --- | --- | --- | --- |
| `modules/06-big-data-architecture/03-implementations/mini-platform` | Primary hardened local service demo | Local Docker Compose, Python 3.11 service tests, deterministic eval suite, dedicated integration CI | Validated env modes, API-key ingress and operator auth, worker lease recovery, replay/redrive jobs, Postgres and ClickHouse migrations, structured logs, durable operator telemetry | Cloud readiness, production security completeness, multi-tenant support, major observability stack |
| `projects/p2-big-data-mini-platform` | Project wrapper for the mini-platform | Local runbook, replay/redrive usage, and verification around the mini-platform | Phase 3 operator docs, runbooks, and CI-linked run flow | Separate product deployment story |
| `modules/11-generative-ai/03-implementations/python` | Offline deterministic demo | Local Python 3.11 CLI and tests | None beyond deterministic local execution | Deployed service readiness, real agent autonomy, cloud readiness |
| `projects/p7-genai-rag-agent-app` | Project wrapper for the offline GenAI demo | Local deterministic run and test flow | None beyond deterministic local execution | Production agent app maturity or autonomous operation |

## Supported for the Mini-platform
- Local Python 3.11 workflows and service-local tests.
- Local Docker Compose with explicit Postgres and ClickHouse migrations.
- API-key protected ingestion plus authenticated `/ops` endpoints for replay jobs, DLQ inspection, redrive, durable telemetry, and event lifecycle inspection.
- Schema-versioned ingest for the supported `order_created` contract at `schema_version=1`.
- Dedicated CI coverage that validates compose config, builds images, runs migrations, starts the stack, and checks the happy path plus replay-after-completion safety.
- Deterministic scenario evaluations for normal completion, failure/recovery, replay, redrive, and operator telemetry consistency.

## Still Deferred
- Cloud deployment and infrastructure as code.
- Production security completeness such as secret managers, TLS termination, RBAC, and external identity.
- Multi-tenant support or billing.
- Prometheus, Grafana, or distributed tracing platforms.
- Exactly-once semantics across Kafka, storage, and analytics.
