# Data Modeling, Partitioning, and Indexing

## Key Ideas

- Data modeling defines what the platform promises to downstream users, while partitioning and indexing determine whether those promises remain affordable at scale.
- Analytical modeling is about stable consumption patterns, not just raw schema translation from source systems.
- Partitioning reduces the amount of data scanned by aligning storage layout with common filters, but poor partition keys can create hot spots, small files, or expensive metadata.
- Indexing, clustering, and sort order improve locality for common queries, but they also introduce maintenance cost and write-time tradeoffs.
- Good storage layout is driven by actual query patterns, data distribution, and retention behavior rather than by generic best-practice slogans.

## 1. What These Design Choices Control

Data modeling decides how facts and dimensions are represented for use. Partitioning decides how data is physically grouped. Indexing or clustering decides how the system narrows or accelerates common access paths.

### 1.1 Core Definitions

- A **fact table** stores measurable events such as orders or clicks.
- A **dimension table** stores descriptive context such as customer or product attributes.
- A **partition key** is the field or fields used to divide stored data into physical segments.
- **Clustering** or **sorting** arranges data within partitions to improve locality for common filters.
- An **index** is an auxiliary structure that speeds lookups or selective scans.

### 1.2 Why This Matters

Poor layout decisions silently increase cost. The platform still works, but queries scan too much data, writes create too many small files, and operations teams spend time on compaction, repartitioning, and emergency scaling.

## 2. Modeling for Analytical Consumption

### 2.1 Raw Versus Curated Models

Raw ingestion models preserve source fidelity. Curated analytical models should instead optimize for understandable, stable consumption patterns.

### 2.2 Facts and Dimensions

A common analytical design keeps large append-oriented facts separate from smaller reusable descriptive dimensions. This makes aggregation and filtering more predictable for downstream users.

### 2.3 Incremental Change

The model should also support late-arriving events, corrections, and history policies. Data modeling is incomplete if it only describes the happy path.

## 3. Choosing Partition and Index Strategy

### 3.1 Good Partition Keys

Good keys are strongly aligned with common query filters, have manageable cardinality, and distribute writes reasonably evenly.

### 3.2 Bad Partition Keys

Poor choices include:

- extremely high-cardinality fields,
- fields rarely used in filtering,
- keys that concentrate almost all new writes into one partition.

### 3.3 Clustering and Sort Order

After partitioning, clustering or sorting can reduce scan work further by keeping related rows close together for selective queries.

## 4. Worked Example: Estimating Partition Pruning

Suppose an `orders` fact table stores:

```text
daily_volume = 500 GB/day
retention = 30 days
```

Assume a common dashboard query asks for:

```text
country = "US"
event_date = one specific day
```

### 4.1 Unpartitioned Scan

If the table is not partitioned by date, the query may scan the full retained dataset:

```text
full_scan = 500 GB/day * 30 days = 15,000 GB = 15 TB
```

### 4.2 Date-Partitioned Scan

If the table is partitioned by `event_date`, the query only needs one day:

```text
date_partition_scan = 500 GB
```

### 4.3 Add Clustering by Country

Assume clustering by `country` allows the engine to narrow the one-day scan to about `20%` of that partition for this workload:

```text
clustered_scan = 500 GB * 0.20 = 100 GB
```

### 4.4 Interpret the Result

The storage layout reduces the query from `15 TB` to `500 GB`, and then to about `100 GB` for the stated access pattern. This is why physical design matters operationally even when the logical schema stays the same.

Verification: the scan-reduction arithmetic is consistent because `30` retained days at `500 GB/day` gives `15 TB`, while one date partition is `500 GB`, and taking `20%` of that partition yields `100 GB`.

## 5. Common Mistakes

1. **Source-schema mirroring.** Copying operational schemas directly into analytical serving layers creates awkward queries and poor performance; model for the consumer workload instead.
2. **High-cardinality partitioning.** Partitioning by identifiers with too many unique values produces tiny files and metadata overhead; choose keys with manageable grouping behavior.
3. **Filter-mismatch layout.** Using partition keys unrelated to common query filters prevents scan pruning; align physical layout with real access patterns.
4. **Indexing without cost accounting.** Adding indexes or clustering without considering write amplification and maintenance can hurt ingestion performance; balance read gains against operational cost.
5. **Static-model complacency.** Leaving the model untouched as workload shape changes eventually causes cost blowups; revisit modeling and layout when query patterns drift.

## 6. Practical Checklist

- [ ] Identify the top analytical queries before choosing partitions or clustering.
- [ ] Separate raw ingestion models from curated consumption models where necessary.
- [ ] Use partition keys with sensible cardinality and strong filter alignment.
- [ ] Measure actual scan size and file counts instead of assuming layout quality.
- [ ] Plan compaction, retention, and correction workflows alongside the schema.
- [ ] Re-evaluate physical design after major changes in volume, query patterns, or retention.

## 7. References

- Kimball, Ralph, and Margy Ross. 2013. *The Data Warehouse Toolkit* (3rd ed.). Wiley.
- Kleppmann, Martin. 2017. *Designing Data-Intensive Applications*. O'Reilly Media. <https://dataintensive.net/>
- ClickHouse. 2026. *MergeTree*. <https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree>
- Snowflake. 2026. *Micro-Partitions and Data Clustering*. <https://docs.snowflake.com/>
- Apache Iceberg. 2026. *Partitioning*. <https://iceberg.apache.org/docs/latest/partitioning/>
- Google Cloud. 2026. *Best Practices for Partitioning and Clustering*. <https://cloud.google.com/bigquery/docs/clustered-tables>
- Databricks. 2026. *Data Layout Best Practices*. <https://docs.databricks.com/>
