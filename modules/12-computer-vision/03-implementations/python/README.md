# Python Implementations

Local-first CV toolkit with deterministic utilities for preprocessing, classical
features, toy detection/segmentation, and evaluation. No external APIs required.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r modules/12-computer-vision/03-implementations/python/requirements.txt
```

## Run tests (repo root)
```bash
python -m pytest -q modules/12-computer-vision/03-implementations/python/tests
```

## Examples

### Preprocessing pipeline
```python
import numpy as np
from src.cv.preprocess import resize, normalize, random_flip

image = np.ones((32, 32, 3), dtype=np.float32)
image = resize(image, (64, 64))
image = normalize(image, mean=[0.5, 0.5, 0.5], std=[0.2, 0.2, 0.2])
image = random_flip(image, seed=7)
```

### Edges, corners, keypoints
```python
from src.cv.features import sobel_edges, harris_corners, topk_keypoints
from src.cv.io import to_grayscale

gray = to_grayscale(image)
edges = sobel_edges(gray)
response = harris_corners(gray)
keypoints = topk_keypoints(response, k=5)
```

### Toy detection and segmentation
```python
from src.cv.detection import detect_objects
from src.cv.segmentation import segment_threshold

objects = detect_objects(gray, threshold=0.5)
mask = segment_threshold(gray, threshold=0.5)
```

### Metrics usage
```python
from src.cv.metrics import accuracy, detection_precision_recall

acc = accuracy([0, 1, 1], [0, 0, 1])
precision, recall = detection_precision_recall([[0, 0, 4, 4]], [[0, 0, 4, 4]])
```
