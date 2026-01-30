# HCI Study Report

- input_dir: modules/15-hci/03-implementations/python/tests/fixtures/study_csvs
- files_count: 6
- seed: 42

## Executive Summary
- SUS mean 75.000 (n=2, range 50.000-100.000).
- Usability success rate 0.800 with worst task login (success 0.667).
- Binary experiment diff 0.100 (p=0.084).
- Continuous experiment diff 8.000 (p=0.022).
- Top qualitative themes: confusion (3), login (2), search (2).

## SUS Summary
- responses: 2
- mean: 75.000
- median: 75.000
- range: 50.000 to 100.000
- lowest_items: q10 (2.000), q2 (2.000)

## Usability Sessions Summary
- tasks_analyzed: 2
- overall_success_rate: 0.800
- per_task_metrics:
  - login: success_rate=0.667, median_time=25.000, total_errors=3
  - search: success_rate=1.000, median_time=37.500, total_errors=0
- worst_tasks:
  - login: success_rate=0.667, median_time=25.000
  - search: success_rate=1.000, median_time=37.500

## A/B Experiment Summary
- binary_conversion:
  - A: users=100, conversions=20, rate=0.200
  - B: users=120, conversions=36, rate=0.300
  - diff=0.100, relative_lift=0.500, p_value=0.084
- continuous_metric:
  - A: n=50, mean=100.000, std=15.000
  - B: n=55, mean=108.000, std=20.000
  - diff=8.000, p_value=0.022

## Qualitative Themes Summary
- coded_quotes: 5
- top_themes:
  - confusion: 3
  - login: 2
  - search: 2
  - slow: 2
  - error: 1

## Unrecognized CSVs
- notes.csv: columns=id, category, detail, owner, priority

## Data Quality / Validation Notes
- ab_binary.csv: missing_values=0; issues=none
- ab_continuous.csv: missing_values=0; issues=none
- notes.csv: missing_values=0; issues=none
- qual_codes.csv: missing_values=0; issues=none
- sus_responses.csv: missing_values=0; issues=none
- usability_sessions.csv: missing_values=0; issues=none

## Appendix: File Inventory
- ab_binary.csv — A/B binary
- ab_continuous.csv — A/B continuous
- notes.csv — Unrecognized
- qual_codes.csv — Qualitative codes
- sus_responses.csv — SUS responses
- usability_sessions.csv — Usability sessions
