# Security, Governance, and Data Quality

## What it is

Policies and controls that protect data, enforce compliance, and maintain
accuracy across the data lifecycle.

## Why it matters

Data breaches, non-compliance, and poor data quality can destroy trust and
lead to legal and financial penalties.

## Architecture patterns

- Access control at storage and query layers
- Data classification and retention policies
- Data quality checks at ingestion and transformation

## Failure modes

- Over-permissioned access and data leaks
- Silent schema drift causing incorrect analytics
- Incomplete data lineage for compliance audits

## Operability checklist

- Enforce least privilege and audit access
- Automate data quality checks and alerts
- Track lineage from source to consumption
- Review retention and deletion policies

## References

- NIST Privacy Framework — <https://www.nist.gov/privacy-framework>
- Data Management Body of Knowledge (DAMA-DMBOK) — <https://www.dama.org/page/publications>
