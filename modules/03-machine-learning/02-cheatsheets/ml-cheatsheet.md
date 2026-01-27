# ML Cheat Sheet

## Metric selection
| Task | Primary metrics | Notes |
| --- | --- | --- |
| Regression | MAE, RMSE, R^2 | RMSE penalizes large errors |
| Classification (balanced) | Accuracy, F1 | F1 balances precision/recall |
| Classification (imbalanced) | ROC-AUC, PR-AUC | PR-AUC preferred |

## CV checklist
- Fix random seed
- Use stratified CV for classification
- Avoid leakage (pipeline all preprocessing)
- Keep test set untouched until final evaluation

## Leakage checklist
- Fit scalers/encoders on training only
- Ensure temporal splits for time series
- Remove target-derived features

## Regularization quick guide
- L2 (Ridge): reduces large weights, good default
- L1 (Lasso): sparse features, feature selection
- ElasticNet: mix of L1/L2

## Clustering + DR selection
- KMeans for spherical clusters
- DBSCAN for density-based clusters
- PCA for linear variance reduction
- t-SNE/UMAP for visualization (not for downstream modeling)
