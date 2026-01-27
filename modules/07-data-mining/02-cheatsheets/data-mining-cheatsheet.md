# Data Mining Cheat Sheet

## Pipeline checklist (CRISP-DM style)
- Business understanding and success metrics
- Data understanding and profiling
- Data preparation (cleaning + feature engineering)
- Modeling / mining
- Evaluation and validation
- Reporting and deployment readiness

## Data quality checks
- Missingness rates per column
- Duplicates and key uniqueness
- Range and unit sanity checks
- Category cardinality

## Feature engineering patterns
- One-hot encode categoricals
- Standardize numeric features
- Aggregate transactional data to itemsets
- Target/label separation to avoid leakage

## Clustering metrics
- Silhouette (higher is better)
- Inertia / SSE (lower is better)
- Davies-Bouldin index (lower is better)

## Association rules metrics
- Support: P(X ∩ Y)
- Confidence: P(Y | X)
- Lift: Confidence / P(Y)

## Reproducibility checklist
- Fixed random seeds
- Versioned datasets and schemas
- Stable train/test splits
- Logged parameters and metrics
- Recorded library versions
