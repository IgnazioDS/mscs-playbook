# Orchestration and Pipelines

## Key Ideas

- Orchestration coordinates data work across time, dependencies, retries, and operational visibility so that a platform behaves like a managed system instead of a pile of scripts.
- A pipeline is not only transformation code; it is also scheduling policy, dependency structure, metadata, rerun behavior, and failure handling.
- Good orchestration separates task logic from control logic, which makes backfills, retries, and lineage easier to manage.
- The real value of orchestration is operational clarity: which step failed, what upstream data was used, whether a rerun is safe, and how freshness objectives are affected.
- Pipelines become fragile when they hide state, depend on manual timing assumptions, or lack clear ownership and run metadata.

## 1. What Orchestration Is

Orchestration is the coordinated control of pipeline execution. It determines when work runs, in what order, under which dependencies, and what happens when something fails or needs to be rerun.

### 1.1 Core Definitions

- A **task** is a single unit of pipeline work.
- A **directed acyclic graph (DAG)** is a dependency graph in which tasks have no cycles.
- A **backfill** reruns historical intervals to fill missing or corrected outputs.
- **Lineage** records which inputs, code, and upstream runs contributed to an output.
- A **run record** is the metadata about a specific pipeline execution.

### 1.2 Why This Matters

Even simple data workflows become hard to operate once they must rerun safely, recover from upstream delays, and satisfy freshness targets. Orchestration turns an informal process into an auditable and repeatable system.

## 2. The Responsibilities of an Orchestrator

### 2.1 Scheduling and Dependencies

The orchestrator decides when tasks run and what upstream conditions must be satisfied first.

### 2.2 Retry and Failure Policy

Not every failure should trigger the same response. Some tasks should retry automatically, some should wait for manual intervention, and some should skip until upstream corrections arrive.

### 2.3 Metadata and Visibility

Operators need to know:

- which run produced a table,
- what code version was used,
- what upstream data interval was processed,
- whether a rerun changed the output.

## 3. Designing Pipelines for Safe Reruns

### 3.1 Idempotent Tasks

Tasks should either replace a known partition or produce outputs that are safe to rerun without duplication.

### 3.2 Explicit Time Windows

Pipelines should operate on explicit intervals such as "2026-03-09 hourly window" rather than on vague "latest data" assumptions.

### 3.3 Controlled Backfills

Backfills must specify:

- input interval,
- overwrite or merge behavior,
- downstream invalidation policy,
- concurrency limits.

## 4. Worked Example: Daily DAG with a Backfill

Suppose a daily analytics DAG has three tasks:

```text
task_1 = ingest_raw
task_2 = build_orders_fact
task_3 = publish_dashboard
```

Dependencies:

```text
ingest_raw -> build_orders_fact -> publish_dashboard
```

A run for `2026-03-09` fails at `build_orders_fact`.

### 4.1 Initial Execution

- `ingest_raw` succeeds for `2026-03-09`
- `build_orders_fact` fails
- `publish_dashboard` does not run because its dependency failed

### 4.2 Rerun Design

Assume `build_orders_fact` overwrites the partition for its execution date. After the bug is fixed, rerun:

```text
rerun_date = 2026-03-09
```

Execution:

- reuse successful `ingest_raw` output for `2026-03-09`
- rerun `build_orders_fact` for `2026-03-09`
- run `publish_dashboard` for `2026-03-09`

### 4.3 Why the Design Is Safe

Because the fact build is partition-scoped and overwrite-based for that date, rerunning it does not create duplicate rows for `2026-03-09`. The DAG preserves dependency order and limits the rerun to the affected interval.

Verification: the rerun is consistent because only the failed date partition is rebuilt, upstream raw ingestion for the same date is reused, and the publish step is delayed until the corrected fact partition exists.

## 5. Common Mistakes

1. **Script-pile orchestration.** Treating shell scripts and cron jobs as sufficient orchestration works only until dependencies, retries, and lineage matter; separate workflow control from task internals.
2. **Implicit-interval processing.** Running jobs against "latest" data makes reruns ambiguous and fragile; parameterize tasks by explicit time windows or partitions.
3. **Unsafe backfills.** Reprocessing history without clear overwrite or merge semantics often creates duplicates; define rerun behavior at the storage layer as well as the scheduler layer.
4. **Opaque failure handling.** Retrying everything the same way hides root causes and can amplify damage; match retry policy to task semantics.
5. **Metadata neglect.** Without run records and lineage, teams cannot explain what produced an output or whether a rerun fixed it; capture execution metadata systematically.

## 6. Practical Checklist

- [ ] Define task boundaries, dependencies, and execution intervals explicitly.
- [ ] Make rerun and backfill behavior safe before relying on automation.
- [ ] Capture run metadata, input interval, code version, and status for each execution.
- [ ] Use task-specific retry and alerting policies instead of one generic default.
- [ ] Keep workflow definitions versioned alongside transformation code.
- [ ] Test failure and backfill scenarios before the first production incident.

## 7. References

- Apache Airflow. 2026. *Documentation*. <https://airflow.apache.org/docs/>
- Dagster. 2026. *Documentation*. <https://docs.dagster.io/>
- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. O'Reilly Media. <https://dataintensive.net/>
- Dataform. 2026. *Workflow Scheduling Concepts*. <https://cloud.google.com/dataform/docs>
- dbt Labs. 2026. *Incremental Models*. <https://docs.getdbt.com/docs/build/incremental-models>
- Prefect. 2026. *Flows and Deployments*. <https://docs.prefect.io/>
- Astronomer. 2026. *Data Orchestration Concepts*. <https://www.astronomer.io/docs/>
