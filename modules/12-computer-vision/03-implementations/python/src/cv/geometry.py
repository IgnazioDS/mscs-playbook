from __future__ import annotations

from typing import Iterable


def box_area(box: Iterable[int | float]) -> float:
    x1, y1, x2, y2 = box
    return max(0.0, x2 - x1 + 1) * max(0.0, y2 - y1 + 1)


def clip_box(box: Iterable[int | float], width: int, height: int) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    x1 = max(0, min(int(x1), width - 1))
    y1 = max(0, min(int(y1), height - 1))
    x2 = max(0, min(int(x2), width - 1))
    y2 = max(0, min(int(y2), height - 1))
    return x1, y1, x2, y2
