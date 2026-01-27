"""Dataset loaders for data mining exercises."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from sklearn import datasets


SKLEARN_DATASETS = {
    "iris": datasets.load_iris,
    "wine": datasets.load_wine,
    "breast_cancer": datasets.load_breast_cancer,
    "california_housing": datasets.fetch_california_housing,
}


def load_sklearn_dataset(name: str, as_frame: bool = True) -> Tuple[pd.DataFrame, Optional[pd.Series], Dict[str, Any]]:
    """Load a sklearn dataset by name."""
    if name not in SKLEARN_DATASETS:
        raise ValueError(f"Unsupported dataset: {name}")

    loader = SKLEARN_DATASETS[name]
    dataset = loader(as_frame=as_frame)

    if as_frame:
        X_df = dataset.data
        y = dataset.target if hasattr(dataset, "target") else None
    else:
        X_df = pd.DataFrame(dataset.data, columns=dataset.feature_names)
        y = pd.Series(dataset.target) if hasattr(dataset, "target") else None

    target_names = getattr(dataset, "target_names", None)
    if isinstance(target_names, (list, tuple)) and target_names:
        target_name = target_names[0]
    else:
        target_name = getattr(dataset, "target_name", None)

    meta = {
        "feature_names": list(dataset.feature_names),
        "target_name": target_name,
        "n_rows": X_df.shape[0],
    }
    return X_df, y, meta


def load_basket_dataset(name: str = "tiny_baskets") -> List[List[str]]:
    """Load a small basket dataset from CSV.

    Format: transaction_id,item
    """
    if name != "tiny_baskets":
        raise ValueError(f"Unsupported basket dataset: {name}")

    data_path = Path(__file__).resolve().parent / "data" / "tiny_baskets.csv"
    df = pd.read_csv(data_path)
    if "transaction_id" not in df.columns or "item" not in df.columns:
        raise ValueError("Basket CSV must have transaction_id and item columns")

    transactions: Dict[Any, List[str]] = {}
    for _, row in df.iterrows():
        tid = row["transaction_id"]
        item = str(row["item"])
        transactions.setdefault(tid, []).append(item)

    return list(transactions.values())
