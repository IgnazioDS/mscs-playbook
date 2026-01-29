# Mini-project: CV Local Toolkit

## Goals
- Build a deterministic CLI for toy detection, OCR-lite, and shelf availability
- Demonstrate classic CV preprocessing and metrics without heavy dependencies
- Provide reproducible evaluation checks for regression testing

## Commands and expected outputs

### Defect detection
```bash
python modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py defect-detect --seed 42
```
Expected output (short):
```
task: defect-detect
seed: 42
iou: 0.5
images: 12
predicted_boxes_total: ...
metrics: precision=..., recall=...
```

### Document OCR-lite
```bash
python modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py doc-ocr-lite --seed 42
```
Expected output (short):
```
task: doc-ocr-lite
seed: 42
tokens: 5
predicted_tokens: ...
metrics: precision=..., recall=...
```

### Shelf availability
```bash
python modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py shelf-availability --seed 42
```
Expected output (short):
```
task: shelf-availability
seed: 42
metrics: accuracy=..., f1_macro=...
confusion_matrix: ...
```

### Deterministic evaluation
```bash
python modules/12-computer-vision/03-implementations/python/src/cv/mini_project/cli.py evaluate
```
Expected output (short):
```
task: evaluate
scenarios: 3
passed: 3
failed: 0
```

## How to extend to a real CV stack later
- Replace toy detection with YOLO or Faster R-CNN
- Swap OCR-lite with modern OCR + layout models
- Add real datasets and augmentation pipelines
- Move from synthetic shelf data to store images

## Pitfalls
- Label noise and inconsistent annotation rules
- Domain shift across cameras or environments
- Privacy risk when capturing people or documents
