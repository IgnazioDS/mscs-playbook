# Observability, SLOs, and Costs

## What it is
Operational visibility into pipeline health, data freshness, and cost drivers.

## Why it matters
Data systems degrade gradually: lag, cost, and quality issues must be detected
before they impact users.

## Architecture patterns
- End-to-end freshness metrics (event time to query time)
- Budget alarms and cost attribution per pipeline
- Structured logs and traceable event IDs

## Failure modes
- Silent data delays with no alerting
- Cost blowups due to unbounded retention or scans
- Misleading dashboards without data-quality checks

## Operability checklist
- Define SLOs for freshness and availability
- Track lag, throughput, error rates, and retries
- Monitor storage growth and query scan size
- Alert on missing data and schema violations

## References
- Site Reliability Engineering (Google) — https://sre.google/books/
- Observability for Data Systems — https://www.montereydata.com/blog/data-observability
