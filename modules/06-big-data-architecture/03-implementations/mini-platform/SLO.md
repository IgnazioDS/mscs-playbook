# SLO and Alert Guide

Phase 4 adds machine-checkable SLO evaluation for the mini-platform. These thresholds are intended for the repo's production-like backend packaging, not for claiming broad cloud SRE readiness.

## Current SLOs

- readiness availability: `>= 99%`
- accepted-to-completed processing latency p95: `<= 30000 ms`
- DLQ backlog: `<= 5`
- replay completion rate average: `>= 10 jobs/minute` in the lightweight harness

The checker is implemented in [`scripts/slo_check.py`](scripts/slo_check.py) and evaluates telemetry plus a load report.

## Capacity Harness

Run the lightweight authenticated load smoke:

```bash
python3.11 modules/06-big-data-architecture/03-implementations/mini-platform/scripts/load_harness.py \
  --base-url http://localhost:8000 \
  --ingest-key-id local-ingest \
  --ingest-key local-demo-ingest-key \
  --operator-key-id local-ops \
  --operator-key local-demo-ops-key \
  --requests 3 \
  --output modules/06-big-data-architecture/03-implementations/mini-platform/artifacts/load-smoke.json
```

## SLO Check

```bash
python3.11 modules/06-big-data-architecture/03-implementations/mini-platform/scripts/slo_check.py \
  --base-url http://localhost:8000 \
  --operator-key-id local-ops \
  --operator-key local-demo-ops-key \
  --capacity-report modules/06-big-data-architecture/03-implementations/mini-platform/artifacts/load-smoke.json \
  --readiness-availability 1.0
```

Exit behavior:
- `0`: no SLO violations
- `1`: one or more SLO violations

## Alert Mapping

- readiness violation:
  investigate `/ready`, Postgres connectivity, and Kafka bootstrap status
- processing latency violation:
  inspect `event_processing`, replay backlog, and worker lease churn
- DLQ backlog violation:
  inspect `/ops/dlq`, `/ops/events/{event_id}`, and dependency errors in worker logs
- replay throughput violation:
  inspect `replay_jobs`, `replay_job_events`, and replay-runner ownership churn

## Caveats

- readiness availability in local or CI smoke runs is fed in as an explicit measurement input, not derived from a long-running availability window
- the load harness is a bounded operator-oriented check, not a benchmark suite
- these SLOs are intended to drive operator response and release gating, not external uptime claims
