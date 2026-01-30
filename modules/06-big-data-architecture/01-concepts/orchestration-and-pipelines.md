# Orchestration and Pipelines

## What it is

Coordinating data workflows (batch and streaming) with scheduling, dependency
management, and operational controls.

## Why it matters

Without orchestration, pipelines drift, fail silently, and become unmaintainable.

## Architecture patterns

- DAG-based orchestration (Airflow, Dagster)
- Pipeline-as-code with versioned configs
- Backfill and rerun controls

## Failure modes

- Silent task failure without alerts
- Backfills overwriting or duplicating data
- Dependency drift between pipeline stages

## Operability checklist

- Define SLAs per pipeline stage
- Capture run metadata and lineage
- Implement retry policies and alerts
- Test backfills and reruns in staging

## References

- Apache Airflow Documentation — <https://airflow.apache.org/docs/>
- Dagster Documentation — <https://docs.dagster.io/>
