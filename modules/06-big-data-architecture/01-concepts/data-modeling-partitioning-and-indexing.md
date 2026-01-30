# Data Modeling, Partitioning, and Indexing

## What it is

Designing schemas and storage layouts that balance query performance, cost,
and operational simplicity.

## Why it matters

Poor modeling causes slow queries, expensive scans, and operational pain.

## Architecture patterns

- Star/snowflake schemas for analytics
- Append-only fact tables with time partitioning
- Sort keys and clustering for query locality

## Failure modes

- Over-partitioning causing small-file explosion
- Hot partitions from skewed keys
- Unbounded indexes and write amplification

## Operability checklist

- Choose partition keys aligned with common filters
- Set retention and compaction strategies
- Monitor query scan size and index bloat
- Test with realistic data volume and skew

## References

- The Data Warehouse Toolkit (Kimball) — <https://www.kimballgroup.com/>
- ClickHouse Partitioning — <https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree>
