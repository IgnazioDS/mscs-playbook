# Mini-Project: Data Mining Pipeline Review

## Goal
Run the clustering/anomaly pipeline on a small dataset and document the
tradeoffs in feature engineering and evaluation.

## Steps
1. Run the CLI clustering task with a fixed seed.
2. Capture metrics (silhouette, inertia) and note stability.
3. Run anomaly detection and list top outliers.

## Suggested Commands
- `python3 modules/07-data-mining/03-implementations/python/src/cli.py cluster --dataset iris --k 3 --seed 42`
- `python3 modules/07-data-mining/03-implementations/python/src/cli.py anomaly --dataset iris --seed 42`

## Success Criteria
- Reported metrics are stable across runs with the same seed.
- Outlier list includes rationale for each item.
