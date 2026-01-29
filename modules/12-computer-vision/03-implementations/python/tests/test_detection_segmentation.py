import numpy as np

from src.cv.detection import detect_objects
from src.cv.segmentation import segment_threshold


def test_detect_two_objects():
    gray = np.zeros((10, 10), dtype=np.float32)
    gray[1:3, 1:3] = 1.0
    gray[6:8, 6:8] = 1.0
    detections = detect_objects(gray, threshold=0.5, min_area=3)
    boxes = [det[0] for det in detections]
    assert len(boxes) == 2
    assert [1, 1, 2, 2] in boxes
    assert [6, 6, 7, 7] in boxes


def test_segment_threshold():
    gray = np.zeros((8, 8), dtype=np.float32)
    gray[2:6, 2:6] = 1.0
    mask = segment_threshold(gray, threshold=0.5, iterations=1)
    assert mask.shape == (8, 8)
    assert mask.sum() >= 12
