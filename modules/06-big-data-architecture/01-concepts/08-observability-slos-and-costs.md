# Observability, SLOs, and Costs

## Key Ideas

- A data platform is only as trustworthy as its ability to detect lateness, loss, quality regressions, and runaway cost before downstream users discover them.
- Observability in data systems must cover data freshness and correctness in addition to infrastructure metrics such as CPU or memory.
- Service-level objectives turn vague expectations such as "near real time" into measurable promises that can guide architecture and incident response.
- Cost is an operational signal, not just a finance topic, because scan size, retention, and backlog behavior often reveal architectural problems.
- Useful monitoring connects technical metrics to business-facing outcomes such as missing dashboards, stale features, or delayed reports.

## 1. What Observability Means for Data Platforms

Observability is the ability to infer the internal state of the data platform from its outputs, metrics, logs, and traces. In data systems, that includes not only software health but also data availability, freshness, and correctness.

### 1.1 Core Definitions

- A **service-level indicator (SLI)** is a measured property such as freshness or successful run rate.
- A **service-level objective (SLO)** is the target value for that indicator.
- **Freshness** measures how current served data is relative to event or source time.
- **Backlog** is unprocessed or delayed data waiting to be handled.
- **Cost attribution** maps storage or compute expense back to workloads, teams, or datasets.

### 1.2 Why This Matters

Many data incidents are silent. Dashboards still load, but they show stale or incomplete data. Costs still rise, but nobody sees that one job now scans ten times more data than last month. Observability is what turns slow failure into visible signal.

## 2. The Signals That Matter Most

### 2.1 Freshness and Latency

For pipelines, freshness is often more important than raw compute metrics because it expresses whether the data is useful now.

### 2.2 Completeness and Error Rate

A platform should measure whether expected records arrived and whether tasks, loads, or validations are failing.

### 2.3 Cost and Growth

Storage growth, query scan bytes, and retry amplification are all operational indicators because they often signal architectural drift.

## 3. Turning Signals into SLOs

### 3.1 SLO Design

A useful SLO is specific, measurable, and tied to a consumer outcome. For example:

- `99%` of events available in analytics within `5` minutes
- daily revenue table complete by `06:15 UTC`
- monthly platform storage growth below a defined threshold

### 3.2 Error Budgets

An error budget makes it explicit how much missed performance is acceptable over a time window. This helps teams choose between feature work and reliability work.

### 3.3 Alerting Discipline

Alerts should point to actionable failures such as freshness breach, backlog growth, or data-quality check failure. Dashboards without actionable thresholds are not enough.

## 4. Worked Example: Freshness SLO Evaluation

Suppose a pipeline declares this weekly SLO:

```text
SLO = 99% of hourly loads finish within 15 minutes
```

In one week there are:

```text
7 days * 24 hourly loads = 168 total loads
```

During the week, `4` hourly loads exceed `15` minutes.

### 4.1 Compute Successful Loads

```text
successful_loads = 168 - 4 = 164
```

### 4.2 Compute Achieved Reliability

```text
achieved_rate = 164 / 168 = 0.97619...
achieved_rate = 97.62%
```

### 4.3 Compare to the SLO

Required target:

```text
target = 99%
```

Observed rate:

```text
97.62% < 99%
```

The team missed the freshness SLO for the week.

Verification: the result is correct because `164` successful hourly loads out of `168` total loads yields about `97.62%`, which is below the `99%` target.

## 5. Common Mistakes

1. **Infrastructure-only monitoring.** Tracking CPU and container health without measuring freshness or completeness misses the failures users actually feel; monitor data outcomes, not just machines.
2. **Vague target language.** Terms like "near real time" are not actionable; define explicit SLIs and SLOs with units and thresholds.
3. **Dashboard without alerting.** Seeing a metric on a graph is not the same as having operational protection; attach alert rules to meaningful breaches.
4. **Cost afterthought.** Treating cost as a monthly finance review instead of an operational signal delays detection of scan explosions and retention drift; observe cost drivers continuously.
5. **Unowned metrics.** Metrics with no clear owner become decorative; assign responsibility for reviewing and responding to each critical signal.

## 6. Practical Checklist

- [ ] Define freshness, completeness, and failure-rate indicators for critical pipelines.
- [ ] Turn important indicators into explicit SLOs with thresholds and review cadence.
- [ ] Alert on actionable breaches such as lag growth, stale tables, or quality-check failures.
- [ ] Attribute storage and compute cost to major datasets or workloads.
- [ ] Review error-budget burn before adding architectural complexity.
- [ ] Keep dashboards focused on signals that explain user-facing reliability.

## 7. References

- Beyer, Betsy, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds. 2016. *Site Reliability Engineering*. O'Reilly Media. <https://sre.google/books/>
- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. O'Reilly Media. <https://dataintensive.net/>
- Monte Carlo. 2026. *Data Observability*. <https://www.montecarlodata.com/data-observability/>
- Datadog. 2026. *Data Jobs Monitoring*. <https://docs.datadoghq.com/data_jobs/>
- Google Cloud. 2026. *SLO Monitoring and Alerting*. <https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring>
- Snowflake. 2026. *Cost Monitoring*. <https://docs.snowflake.com/en/user-guide/cost-understanding-overall>
- OpenLineage. 2026. *Documentation*. <https://openlineage.io/docs/>
