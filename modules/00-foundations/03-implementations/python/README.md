# Python Implementations

Foundations Toolkit CLI for core statistics, number theory, and small matrix operations.

## Quickstart
Run from the repo root:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/00-foundations/03-implementations/python/requirements.txt
python3 -m pytest -q modules/00-foundations/03-implementations/python/tests
```

## CLI usage
### Stats
```bash
python3 modules/00-foundations/03-implementations/python/src/foundations/mini_project/cli.py stats --nums "1 2 3 4 5"
python3 modules/00-foundations/03-implementations/python/src/foundations/mini_project/cli.py stats --csv modules/00-foundations/03-implementations/python/tests/fixtures/numbers.csv
```

### Number theory
```bash
python3 modules/00-foundations/03-implementations/python/src/foundations/mini_project/cli.py number-theory 30 18 11
```

### Matrix
```bash
python3 modules/00-foundations/03-implementations/python/src/foundations/mini_project/cli.py matrix
python3 modules/00-foundations/03-implementations/python/src/foundations/mini_project/cli.py matrix --json '{"a": [[1,2],[3,4]], "b": [[2,0],[1,2]]}'
```

## API index
```python
from src.foundations.mini_project.core import compute_stats, number_theory_summary, matrix_summary
```

## Determinism and limitations
- Deterministic outputs with fixed formatting.
- Uses Python standard library only.
- Matrix determinant supports 2x2 and 3x3.
