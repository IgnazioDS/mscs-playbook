# Foundations Toolkit CLI

Build a deterministic command-line toolkit that exercises core foundations skills: statistics, number theory, and small matrix operations. The goal is to ship a tiny but production-quality CLI with clear outputs, tests, and reproducible behavior.

## What you will build
A single CLI with three subcommands:
- `stats`: descriptive statistics from inline numbers or a CSV file.
- `number-theory`: gcd/lcm, extended gcd coefficients, and modular inverse.
- `matrix`: determinant, transpose, and multiplication for small matrices.

## How to run
From the repo root:
```bash
python3 modules/00-foundations/03-implementations/python/src/foundations/mini_project/cli.py stats --nums "1 2 3 4 5"
python3 modules/00-foundations/03-implementations/python/src/foundations/mini_project/cli.py number-theory 30 18 11
python3 modules/00-foundations/03-implementations/python/src/foundations/mini_project/cli.py matrix --json '{"a": [[1,2],[3,4]], "b": [[2,0],[1,2]]}'
```

## Expected outputs
All outputs are deterministic and formatted as:
```
task: <name>
seed: n/a
Results:
  key: value
```

## How to extend
- Add percentile and IQR to `stats`.
- Add modular exponentiation to `number-theory`.
- Add 3x3 multiplication and matrix inverse (with checks) to `matrix`.
