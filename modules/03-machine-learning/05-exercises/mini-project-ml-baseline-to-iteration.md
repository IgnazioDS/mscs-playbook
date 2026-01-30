# Mini Project: ML Baseline to Iteration

## Goal

Run a simple end-to-end ML workflow: dataset selection → split → pipeline → evaluation → results.

## Requirements

- Python 3.10+
- venv
- Dependencies installed from `03-implementations/python/requirements.txt`

## What “done” looks like

- CLI runs for classification, regression, and clustering
- Output includes dataset info, metrics, and a brief interpretation

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r modules/03-machine-learning/03-implementations/python/requirements.txt

python modules/03-machine-learning/03-implementations/python/src/cli.py train-classifier --dataset iris --seed 42
python modules/03-machine-learning/03-implementations/python/src/cli.py train-regressor --dataset california_housing --seed 42
python modules/03-machine-learning/03-implementations/python/src/cli.py cluster --dataset iris --k 3 --seed 42
```

## Suggested iterations

- Add feature scaling toggles and compare metrics
- Try stronger regularization (higher alpha for ridge)
- Tune decision thresholds for precision/recall tradeoffs
