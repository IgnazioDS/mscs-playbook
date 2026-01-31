# Python Implementations

Ethics Review CLI that generates deterministic Markdown reports from structured inputs.

## Quickstart
Run from the repo root:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r modules/04-ethics/03-implementations/python/requirements.txt
python3 -m pytest -q modules/04-ethics/03-implementations/python/tests
```

## CLI usage
```bash
python3 modules/04-ethics/03-implementations/python/src/ethics/mini_project/cli.py ethics-review \
  --in modules/04-ethics/03-implementations/python/tests/fixtures/review_inputs/complete \
  --out /tmp/eth04-report.md \
  --seed 42
```

## Determinism and limitations
- Outputs are deterministic and ordering is stable.
- Uses Python standard library only (JSON inputs).
- Scoring is intentionally simple for instructional purposes.
