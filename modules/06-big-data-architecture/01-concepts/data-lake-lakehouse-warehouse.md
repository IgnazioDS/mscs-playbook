# Data Lake, Lakehouse, and Warehouse

## What it is
A set of storage paradigms for analytical data:
- Data lake: low-cost object storage for raw data
- Data warehouse: curated, structured, query-optimized storage
- Lakehouse: lake storage with warehouse-style governance and performance

## Why it matters
Choosing the wrong storage model leads to brittle pipelines, slow analytics,
and runaway costs.

## Architecture patterns
- Raw/bronze, clean/silver, and curated/gold layers
- Schema-on-read for lakes, schema-on-write for warehouses
- Table formats with versioning for lakehouse (Iceberg/Delta/Hudi)

## Failure modes
- Data swamps from uncontrolled lake ingestion
- Expensive transformations baked into queries
- Tight coupling between storage format and compute engines

## Operability checklist
- Define lifecycle policies for cold data
- Enforce naming and partitioning standards
- Track lineage from raw to curated datasets
- Validate schema evolution policies

## References
- Lakehouse: A New Generation of Open Platforms — https://databricks.com/learn/lakehouse
- Modern Data Warehouse Patterns — https://cloud.google.com/architecture/data-warehouse
