# Security, Governance, and Data Quality

## Key Ideas

- Security, governance, and data quality are architectural responsibilities because they determine who can trust the platform, not just who can query it.
- Data systems need explicit control over access, lineage, retention, schema change, and validation because analytical errors and compliance failures often originate in weak platform controls.
- Governance is most useful when it clarifies ownership and change management rather than merely adding approval overhead.
- Data quality is not just row-count checking; it includes schema validity, completeness, semantic consistency, and timeliness.
- The strongest platforms embed these controls into ingestion, transformation, and serving paths instead of treating them as external audits.

## 1. What These Control Layers Are

Security protects data from unauthorized access or misuse. Governance defines ownership, standards, and accountability. Data quality ensures that the data remains fit for intended use.

### 1.1 Core Definitions

- **Least privilege** means users and services receive only the permissions they actually need.
- **Lineage** is the trace of how a dataset was produced from upstream sources.
- A **retention policy** defines how long data is kept and when it is deleted.
- A **quality check** is a validation rule such as schema conformity, null-rate threshold, or referential consistency.
- A **data steward** or **data owner** is the accountable party for a dataset's meaning and lifecycle.

### 1.2 Why This Matters

An accurate but insecure platform is unacceptable. A secure but low-quality platform is also unacceptable. In real systems, trust comes from the combination of controlled access, understandable lineage, and reliable dataset quality.

## 2. Security and Governance Responsibilities

### 2.1 Access Control

Access should be controlled at ingestion, storage, transformation, and query layers. Sensitive fields often require masking, tokenization, or separate handling by role.

### 2.2 Ownership and Change Management

Every important dataset should have a clear owner who approves schema changes, quality expectations, and retention policies.

### 2.3 Lineage and Audit

Lineage and audit trails matter because they let teams answer:

- where this field came from,
- which job changed it,
- who had access,
- which downstream systems depend on it.

## 3. Data Quality as a Platform Concern

### 3.1 Structural Quality

Structural checks verify schema, types, required fields, and compatibility rules.

### 3.2 Content Quality

Content checks verify null rates, valid ranges, deduplication, and business rules such as "refund amount should not be positive."

### 3.3 Timeliness Quality

Data can be structurally correct but operationally useless if it arrives too late. Freshness is therefore part of quality.

## 4. Worked Example: Evaluating a Quality Gate

Suppose a daily `orders_curated` dataset has these validation rules:

```text
rule_1: required order_id must be non-null
rule_2: duplicate rate must be <= 0.1%
rule_3: freshness must be <= 30 minutes
```

Observed run metrics:

```text
rows = 200,000
null_order_id_rows = 120
duplicate_rows = 260
freshness = 18 minutes
```

### 4.1 Check Null Rate

```text
null_rate = 120 / 200,000 = 0.0006 = 0.06%
```

The null-rate outcome does not violate a zero-null rule for required IDs, because any nonzero count fails.

### 4.2 Check Duplicate Rate

```text
duplicate_rate = 260 / 200,000 = 0.0013 = 0.13%
```

Allowed duplicate rate:

```text
0.13% > 0.1%
```

This rule fails.

### 4.3 Check Freshness

```text
18 minutes <= 30 minutes
```

This rule passes.

### 4.4 Interpret the Result

Even though the dataset is fresh, it should not pass the quality gate because the required identifier rule fails and the duplicate-rate threshold is exceeded.

Verification: the validation outcome is consistent because `120` null `order_id` rows violate a non-null requirement, `260` duplicates over `200,000` rows yields `0.13%`, and only the freshness check passes at `18` minutes.

## 5. Common Mistakes

1. **Compliance-only governance.** Treating governance as paperwork instead of ownership and change discipline makes it slow without making it useful; tie governance to concrete dataset responsibilities.
2. **Role-sprawl permissions.** Granting broad access "temporarily" creates long-lived exposure; enforce least privilege and review roles regularly.
3. **Lineage omission.** Without lineage, teams cannot assess impact or audit changes; capture upstream and downstream relationships as part of normal operation.
4. **Shallow quality checks.** Checking only row counts misses schema drift, semantic errors, and timeliness failures; build multi-layer quality validation.
5. **Human-only enforcement.** Relying on manual review for retention, access, and quality controls does not scale; automate policy checks and gates where possible.

## 6. Practical Checklist

- [ ] Assign a clear owner for each important dataset and schema boundary.
- [ ] Enforce least-privilege access at storage and query layers.
- [ ] Track lineage from source ingestion through curated outputs.
- [ ] Define quality checks for structure, content, and timeliness.
- [ ] Automate retention, deletion, and masking policies for sensitive data.
- [ ] Fail or quarantine outputs that violate critical quality gates.

## 7. References

- NIST. 2026. *Privacy Framework*. <https://www.nist.gov/privacy-framework>
- DAMA International. 2026. *DAMA-DMBOK Overview*. <https://www.dama.org/>
- OpenLineage. 2026. *Documentation*. <https://openlineage.io/docs/>
- Great Expectations. 2026. *Documentation*. <https://docs.greatexpectations.io/>
- Soda. 2026. *Data Quality Testing*. <https://docs.soda.io/>
- Google Cloud. 2026. *Data Governance Best Practices*. <https://cloud.google.com/architecture>
- Snowflake. 2026. *Access Control Overview*. <https://docs.snowflake.com/en/user-guide/security-access-control-overview>
