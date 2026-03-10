# Concepts

Read these pages in numerical order. Later pages assume the platform model and
operational discipline established by the earlier ones.

- [01 Big Data Architecture Foundations](01-big-data-architecture-foundations.md): the core design questions around durability, scale, replay, and service objectives.
- [02 Data Lake, Lakehouse, and Warehouse](02-data-lake-lakehouse-and-warehouse.md): the main storage-and-serving patterns for analytical systems and how they trade flexibility, governance, and cost.
- [03 Event-Driven Architecture and Streaming](03-event-driven-architecture-and-streaming.md): durable logs, partitions, offsets, replay, and the logic of streaming data flow.
- [04 Batch vs Streaming Tradeoffs](04-batch-vs-streaming-tradeoffs.md): when each execution model is appropriate and how freshness requirements should drive the choice.
- [05 Data Modeling, Partitioning, and Indexing](05-data-modeling-partitioning-and-indexing.md): the schema and physical-layout decisions that determine scan cost and analytical usability.
- [06 Reliability, Idempotency, and the Exactly-Once Myth](06-reliability-idempotency-and-the-exactly-once-myth.md): pragmatic reliability design for retries, duplicates, and replay-safe pipelines.
- [07 Orchestration and Pipelines](07-orchestration-and-pipelines.md): scheduling, dependency management, reruns, and workflow metadata for production data systems.
- [08 Observability, SLOs, and Costs](08-observability-slos-and-costs.md): platform signals that reveal lateness, incompleteness, and unsustainable cost drift.
- [09 Security, Governance, and Data Quality](09-security-governance-and-data-quality.md): the controls that make datasets secure, traceable, and trustworthy.
