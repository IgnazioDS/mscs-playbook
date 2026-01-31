# Study Report CLI

## Objective
Build a deterministic CLI that reads a folder of CSV files and produces a Markdown study report. The report summarizes usability metrics, SUS scores, A/B experiment results, qualitative themes, and data quality notes in a stable, repeatable format.

## Inputs
The CLI expects a directory containing CSV files. It detects file types based on header schemas rather than filenames.

Supported CSV schemas include:
- SUS responses: `q1` through `q10` columns (optionally with `participant_id`).
- Usability sessions: `task_id`, `success`, `time_seconds` (or `time_sec`), `errors`.
- A/B binary results: `variant`, `conversions`, `users` (or `trials`).
- A/B continuous results: `variant`, `n`, `mean`, `std` or per-row `metric_value`.
- Qualitative codes: `code`, `tag`, or `theme` (optional `severity`).

Any unrecognized CSV files are listed in an "Unrecognized CSVs" section with their first columns.

## Usage
Run from the repo root:
```bash
python3 modules/15-hci/03-implementations/python/src/hci/mini_project/cli.py study-report \
  --in modules/15-hci/03-implementations/python/tests/fixtures/study_csvs \
  --out /tmp/hci15-report.md \
  --seed 42
```

## Expected Output
The report is deterministic and always follows the same section order:
1) Title + metadata (input directory, files count, seed)
2) Executive Summary (3 to 6 bullets)
3) SUS Summary (if present)
4) Usability Sessions Summary (if present)
5) A/B Experiment Summary (if present)
6) Qualitative Themes Summary (if present)
7) Unrecognized CSVs (if present)
8) Data Quality / Validation Notes
9) Appendix: File Inventory

## Checklist
- CLI runs from repo root and writes the report to the requested output path.
- Output is deterministic: stable ordering, fixed rounding, no timestamps.
- All required sections are present when relevant data exists.
- Data quality notes include missing values and obvious issues.
- Tests validate exact output against a golden snapshot.
