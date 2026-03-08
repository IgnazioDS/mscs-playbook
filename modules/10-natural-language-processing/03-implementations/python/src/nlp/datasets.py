"""Small bundled datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


def load_tiny_corpus() -> List[Dict[str, str]]:
    path = Path(__file__).resolve().parents[2] / "data" / "tiny_corpus.jsonl"
    items = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            items.append(json.loads(line))
    return items


def make_ticket_dataset() -> Dict[str, List[str]]:
    texts = [
        "refund request for order",
        "payment failed error",
        "how to reset password",
        "login issue on mobile",
        "billing question about invoice",
        "feature request for export",
        "new product feature idea",
    ]
    labels = ["finance", "finance", "support", "support", "finance", "product", "product"]
    return {"texts": texts, "labels": labels}
