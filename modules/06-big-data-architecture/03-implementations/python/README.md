# Python Implementations

This folder contains lightweight reference code for the module's event-pipeline
examples.

## Contents

- `src/bd06/pipeline.py`: deterministic event-building and simple ingestion metrics logic.
- `tests/test_pipeline.py`: regression tests for event identity and aggregate metrics.

## How to run

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python3 -m pip install -r modules/06-big-data-architecture/03-implementations/python/requirements.txt`
- `python3 -m pytest -q modules/06-big-data-architecture/03-implementations/python/tests`
