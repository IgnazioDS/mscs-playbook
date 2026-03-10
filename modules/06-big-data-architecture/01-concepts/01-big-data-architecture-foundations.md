# Big Data Architecture Foundations

## Key Ideas

- Big data architecture is the disciplined design of data-producing, data-moving, and data-serving systems under scale, latency, reliability, and cost constraints.
- The first design question is not which tool to adopt, but what workload, freshness requirement, and failure budget the system must satisfy.
- Durable logs, replayable storage, and explicit contracts are more important than fashionable platform labels because they determine whether the system can recover from failure safely.
- Analytical systems should be designed around data flow, ownership boundaries, and operational objectives rather than as a pile of disconnected services.
- A good architecture accepts that partial failure, late data, retries, and schema change are normal operating conditions.

## 1. What Big Data Architecture Is

Big data architecture is the structure of a data system that must ingest, store, transform, and serve large or operationally demanding datasets. "Big" does not only mean high volume. It can also mean high event rate, long retention, many downstream consumers, strict freshness expectations, or costly failures.

### 1.1 Core Definitions

- A **data producer** is a system that emits records, events, or files.
- An **ingestion layer** receives data from producers and makes it durable.
- A **processing layer** transforms, enriches, validates, or aggregates data.
- A **serving layer** exposes data for analytics, dashboards, machine learning, or operational use.
- A **service-level objective (SLO)** is a measurable target such as freshness, availability, or latency.
- A **data contract** is an explicit agreement about schema, semantics, and compatibility between producers and consumers.

### 1.2 Why This Matters

Architectures that work at small scale often fail when event volume rises, new consumers are added, or late data becomes common. Without durable ingestion, replay, observability, and governance, teams spend their time patching incidents rather than improving the platform.

## 2. The Core Architectural Questions

### 2.1 What Must the System Guarantee

The design should begin with a small set of measurable promises:

- how quickly data must become available,
- how much loss is acceptable,
- how long raw data must be retained,
- how expensive large backfills may be,
- who depends on the outputs.

### 2.2 Where Data Should Become Durable

A common architectural mistake is delaying durability until late in the pipeline. Durable ingestion matters because every later stage depends on the ability to replay, reprocess, and audit input data.

### 2.3 Which Boundaries Must Stay Loose

Producers, processors, and consumers should not be tightly coupled through undocumented schemas or hidden operational assumptions. Loose coupling makes it possible to evolve one part of the system without breaking all others.

## 3. Common Building Blocks

### 3.1 Durable Ingestion

Durable ingestion is typically implemented with an append-oriented log, object store landing zone, or both. The goal is to capture input before expensive processing decisions are made.

### 3.2 Storage Tiers

Most platforms separate:

- raw retained data,
- cleaned or normalized intermediate data,
- curated serving tables for known access patterns.

This reduces coupling between ingestion and consumption.

### 3.3 Operational Controls

A production platform also needs:

- replay and backfill mechanisms,
- schema validation,
- observability for lag and failures,
- access control and lineage,
- cost monitoring.

## 4. Worked Example: Sizing a Basic Event Pipeline

Suppose an analytics platform ingests purchase events with these requirements:

```text
average_rate = 25,000 events/second
peak_multiplier = 4
event_size = 1.5 KB
freshness_target = 10 minutes
raw_retention = 30 days
```

### 4.1 Compute Peak Ingestion Rate

```text
peak_rate = average_rate * peak_multiplier
peak_rate = 25,000 * 4 = 100,000 events/second
```

### 4.2 Estimate Average Daily Raw Volume

Average bytes per second:

```text
average_bytes_per_second = 25,000 * 1.5 KB = 37,500 KB/second
```

Convert to megabytes per second:

```text
37,500 KB/second = 37.5 MB/second
```

Daily volume:

```text
daily_volume = 37.5 MB/second * 86,400 seconds
daily_volume = 3,240,000 MB
daily_volume = 3,240 GB
daily_volume = 3.24 TB/day
```

### 4.3 Estimate Raw Retention Capacity

```text
retained_raw = 3.24 TB/day * 30 days = 97.2 TB
```

The platform therefore needs storage and operational policies sized for roughly `97.2 TB` of retained raw data, before replicas or metadata overhead.

### 4.4 Interpret the Result

This simple sizing pass already changes design choices. A pipeline at this scale needs durable ingestion, replayable raw storage, explicit retention policies, and observability around lag and storage growth. A spreadsheet-driven export workflow would not be operationally credible.

Verification: the arithmetic is internally consistent because `25,000 events/second` at `1.5 KB` each gives `37.5 MB/second`, which yields `3.24 TB/day` and `97.2 TB` over `30` days of raw retention.

## 5. Common Mistakes

1. **Tool-first architecture.** Starting from a preferred vendor or engine instead of from workload guarantees leads to brittle designs; define throughput, freshness, retention, and recovery requirements before choosing components.
2. **Durability delay.** Allowing important data to remain non-durable deep into the pipeline makes replay and audit impossible; establish the first durable handoff early.
3. **Hidden coupling.** Letting producers and consumers depend on undocumented field meanings or timing assumptions causes breakage during normal change; use explicit contracts and ownership.
4. **Happy-path design.** Designing only for normal flow ignores retries, late data, schema evolution, and partial failure; make failure handling part of the architecture, not an afterthought.
5. **Cost blindness.** Treating storage and compute as infinite creates architectures that technically work but become financially unsustainable; include retention, scan cost, and operational overhead in design decisions.

## 6. Practical Checklist

- [ ] Write down the required ingestion rate, peak rate, freshness target, and retention window before discussing tools.
- [ ] Decide where data first becomes durable and how replay will work from that point.
- [ ] Separate raw capture, transformation, and serving responsibilities clearly.
- [ ] Define data contracts and ownership boundaries for key interfaces.
- [ ] Instrument lag, throughput, failures, and storage growth from the start.
- [ ] Review the architecture against expected backfills, schema changes, and incident scenarios.

## 7. References

- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. O'Reilly Media. <https://dataintensive.net/>
- Newman, Sam. 2021. *Distributed Systems Observability*. O'Reilly Media.
- Akidau, Tyler, Slava Chernyak, and Reuven Lax. 2018. *Streaming Systems*. O'Reilly Media.
- Kimball, Ralph, and Margy Ross. 2013. *The Data Warehouse Toolkit* (3rd ed.). Wiley.
- Apache Kafka. 2026. *Introduction*. <https://kafka.apache.org/intro>
- Google Cloud. 2026. *Architecting a Data Platform*. <https://cloud.google.com/architecture>
- Snowflake. 2026. *What Is a Data Pipeline?* <https://www.snowflake.com/guides/data-pipeline>
