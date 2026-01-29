from __future__ import annotations

from collections import deque
import numpy as np


def detect_objects(gray: np.ndarray, threshold: float = 0.5, min_area: int = 4) -> list[tuple[list[int], float]]:
    mask = gray > threshold
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    detections: list[tuple[list[int], float]] = []

    for y in range(height):
        for x in range(width):
            if mask[y, x] and not visited[y, x]:
                queue: deque[tuple[int, int]] = deque()
                queue.append((y, x))
                visited[y, x] = True
                coords = []
                while queue:
                    cy, cx = queue.popleft()
                    coords.append((cy, cx))
                    for ny, nx in (
                        (cy - 1, cx),
                        (cy + 1, cx),
                        (cy, cx - 1),
                        (cy, cx + 1),
                    ):
                        if 0 <= ny < height and 0 <= nx < width:
                            if mask[ny, nx] and not visited[ny, nx]:
                                visited[ny, nx] = True
                                queue.append((ny, nx))
                if len(coords) < min_area:
                    continue
                ys, xs = zip(*coords)
                x1, x2 = min(xs), max(xs)
                y1, y2 = min(ys), max(ys)
                score = float(np.mean(gray[tuple(zip(*coords))]))
                detections.append(([x1, y1, x2, y2], score))

    detections.sort(key=lambda item: (-item[1], item[0][1], item[0][0]))
    return detections
