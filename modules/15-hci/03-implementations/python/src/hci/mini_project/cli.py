from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import fmean, median, stdev
from typing import Iterable, Sequence


if __name__ == "__main__" and __package__ is None:
    module_root = Path(__file__).resolve().parents[3]
    if str(module_root) not in sys.path:
        sys.path.insert(0, str(module_root))

from src.hci_toolkit.experiments import (
    BinaryVariant,
    ContinuousVariant,
    ab_test_binary,
    ab_test_continuous,
)
from src.hci_toolkit.metrics import sus_score


SUS_QUESTIONS = [f"q{i}" for i in range(1, 11)]
TIME_COLUMNS = ("time_seconds", "time_sec", "time", "duration_seconds", "duration")
BINARY_OUTCOME_COLUMNS = ("converted", "conversion", "success", "outcome")
CONTINUOUS_VALUE_COLUMNS = ("metric_value", "value", "score", "metric")
QUAL_COLUMNS = ("code", "codes", "tag", "tags", "theme", "themes")


@dataclass(frozen=True)
class CsvFile:
    path: Path
    headers: list[str]
    rows: list[dict[str, str]]
    missing_values: int
    detected_type: str


@dataclass(frozen=True)
class ValidationIssue:
    filename: str
    message: str


def _format_float(value: float, *, decimals: int = 3) -> str:
    return f"{value:.{decimals}f}"


def _safe_float(value: str) -> float | None:
    try:
        if value.strip() == "":
            return None
        return float(value)
    except ValueError:
        return None


def _safe_int(value: str) -> int | None:
    try:
        if value.strip() == "":
            return None
        return int(float(value))
    except ValueError:
        return None


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]], int]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        rows = list(reader)

    missing = 0
    for row in rows:
        for header in headers:
            value = row.get(header, "")
            if value is None or str(value).strip() == "":
                missing += 1
    return headers, rows, missing


def _detect_type(headers: Sequence[str]) -> str:
    normalized = {header.strip().lower() for header in headers}

    if all(question in normalized for question in SUS_QUESTIONS):
        return "sus"

    if "task_id" in normalized and "success" in normalized:
        if any(col in normalized for col in TIME_COLUMNS):
            return "usability"

    if "variant" in normalized:
        if any(col in normalized for col in ("conversions", "successes")) and any(
            col in normalized for col in ("users", "trials", "n", "participants")
        ):
            return "ab_binary_agg"
        if any(col in normalized for col in BINARY_OUTCOME_COLUMNS):
            return "ab_binary_row"
        if "mean" in normalized and "std" in normalized and any(
            col in normalized for col in ("n", "count", "samples")
        ):
            return "ab_continuous_agg"
        if any(col in normalized for col in CONTINUOUS_VALUE_COLUMNS):
            return "ab_continuous_row"

    if any(col in normalized for col in QUAL_COLUMNS):
        return "qual"

    return "unknown"


def _load_csvs(input_dir: Path) -> list[CsvFile]:
    files: list[CsvFile] = []
    for path in sorted(input_dir.glob("*.csv")):
        headers, rows, missing = _read_csv(path)
        detected = _detect_type(headers)
        files.append(
            CsvFile(
                path=path,
                headers=headers,
                rows=rows,
                missing_values=missing,
                detected_type=detected,
            )
        )
    return files


def _parse_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _sus_summary(files: Sequence[CsvFile], issues: list[ValidationIssue]) -> dict[str, object] | None:
    sus_files = [file for file in files if file.detected_type == "sus"]
    if not sus_files:
        return None

    scores: list[float] = []
    question_scores: dict[str, list[int]] = {q: [] for q in SUS_QUESTIONS}

    for file in sus_files:
        valid_rows = 0
        for row in file.rows:
            responses: list[int] = []
            missing = False
            for q in SUS_QUESTIONS:
                value = _safe_int(row.get(q, ""))
                if value is None:
                    missing = True
                    break
                responses.append(value)
            if missing:
                continue
            try:
                score = sus_score(responses)
            except ValueError:
                continue
            scores.append(score)
            valid_rows += 1
            for q, response in zip(SUS_QUESTIONS, responses):
                question_scores[q].append(response)

        invalid = len(file.rows) - valid_rows
        if invalid:
            issues.append(
                ValidationIssue(
                    file.path.name,
                    f"{invalid} rows missing or invalid SUS responses",
                )
            )

    if not scores:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
            "lowest_items": [],
        }

    question_avgs = {
        q: fmean(values) for q, values in question_scores.items() if values
    }
    lowest_items = sorted(question_avgs.items(), key=lambda item: (item[1], item[0]))[:2]

    return {
        "count": len(scores),
        "mean": fmean(scores),
        "median": median(scores),
        "min": min(scores),
        "max": max(scores),
        "lowest_items": lowest_items,
    }


def _usability_summary(
    files: Sequence[CsvFile], issues: list[ValidationIssue]
) -> dict[str, object] | None:
    usability_files = [file for file in files if file.detected_type == "usability"]
    if not usability_files:
        return None

    all_rows: list[dict[str, object]] = []
    negative_time_by_file: dict[str, int] = {}
    for file in usability_files:
        header_set = {header.strip().lower() for header in file.headers}
        time_column = next((col for col in TIME_COLUMNS if col in header_set), None)
        if time_column is None:
            continue
        for row in file.rows:
            data = {key.lower(): value for key, value in row.items()}
            time_value = _safe_float(data.get(time_column, "") or "")
            if time_value is not None and time_value < 0:
                negative_time_by_file[file.path.name] = (
                    negative_time_by_file.get(file.path.name, 0) + 1
                )
            all_rows.append(
                {
                    "task_id": data.get("task_id", "unknown").strip() or "unknown",
                    "success": data.get("success", ""),
                    "errors": data.get("errors", data.get("error_count", "")),
                    "time_value": time_value,
                }
            )

    for filename, count in negative_time_by_file.items():
        issues.append(ValidationIssue(filename, f"{count} rows with negative time"))

    if not all_rows:
        return {
            "tasks": {},
            "overall_success": 0.0,
            "worst_tasks": [],
        }

    tasks: dict[str, list[dict[str, object]]] = {}
    for row in all_rows:
        task_id = row["task_id"]
        tasks.setdefault(task_id, []).append(row)

    task_metrics: dict[str, dict[str, float | int | None]] = {}
    total_successes = 0
    total_rows = 0
    for task_id, rows in tasks.items():
        successes = 0
        times: list[float] = []
        errors = 0
        for row in rows:
            success = _parse_bool(row.get("success", ""))
            successes += 1 if success else 0
            time_value = row.get("time_value")
            if isinstance(time_value, float) and time_value >= 0:
                times.append(time_value)
            error_value = _safe_int(str(row.get("errors", "")) or "0")
            errors += error_value or 0
        total_successes += successes
        total_rows += len(rows)
        task_metrics[task_id] = {
            "success_rate": successes / len(rows) if rows else 0.0,
            "median_time": median(times) if times else None,
            "total_errors": errors,
        }

    overall_success = total_successes / total_rows if total_rows else 0.0

    worst_sorted = sorted(
        task_metrics.items(),
        key=lambda item: (
            item[1]["success_rate"],
            -(item[1]["median_time"] or -1),
            item[0],
        ),
    )
    worst_tasks = worst_sorted[:2]

    return {
        "tasks": task_metrics,
        "overall_success": overall_success,
        "worst_tasks": worst_tasks,
    }


def _ab_binary_summary(
    files: Sequence[CsvFile], issues: list[ValidationIssue]
) -> dict[str, object] | None:
    binary_files = [
        file
        for file in files
        if file.detected_type in {"ab_binary_agg", "ab_binary_row"}
    ]
    if not binary_files:
        return None

    variant_totals: dict[str, dict[str, int]] = {}
    for file in binary_files:
        normalized_headers = [header.strip().lower() for header in file.headers]
        is_aggregate = file.detected_type == "ab_binary_agg"
        for row in file.rows:
            data = {key.lower(): value for key, value in row.items()}
            variant = data.get("variant", "unknown").strip() or "unknown"
            if is_aggregate:
                conversions = _safe_int(data.get("conversions", "") or "0") or 0
                trials = (
                    _safe_int(data.get("users", "") or "")
                    or _safe_int(data.get("trials", "") or "")
                    or _safe_int(data.get("n", "") or "")
                    or 0
                )
            else:
                outcome_col = next(
                    (col for col in BINARY_OUTCOME_COLUMNS if col in normalized_headers),
                    None,
                )
                if outcome_col is None:
                    continue
                conversions = 1 if _parse_bool(data.get(outcome_col, "")) else 0
                trials = 1

            if conversions > trials:
                issues.append(
                    ValidationIssue(
                        file.path.name,
                        f"conversions greater than trials for variant {variant}",
                    )
                )
            variant_totals.setdefault(variant, {"users": 0, "conversions": 0})
            variant_totals[variant]["users"] += trials
            variant_totals[variant]["conversions"] += conversions

    if len(variant_totals) < 2:
        return None

    sorted_variants = sorted(variant_totals.items())
    first, second = sorted_variants[0], sorted_variants[1]
    variant_a = BinaryVariant(
        name=first[0],
        users=first[1]["users"],
        conversions=first[1]["conversions"],
    )
    variant_b = BinaryVariant(
        name=second[0],
        users=second[1]["users"],
        conversions=second[1]["conversions"],
    )

    summary = ab_test_binary(variant_a, variant_b)
    rate_a = variant_a.conversions / variant_a.users if variant_a.users else 0.0
    rate_b = variant_b.conversions / variant_b.users if variant_b.users else 0.0
    relative_lift = (rate_b - rate_a) / rate_a if rate_a else None

    return {
        "variants": [variant_a, variant_b],
        "rate_a": rate_a,
        "rate_b": rate_b,
        "difference": summary["difference"],
        "p_value": summary["p_value"],
        "relative_lift": relative_lift,
    }


def _ab_continuous_summary(
    files: Sequence[CsvFile], issues: list[ValidationIssue]
) -> dict[str, object] | None:
    cont_files = [
        file
        for file in files
        if file.detected_type in {"ab_continuous_agg", "ab_continuous_row"}
    ]
    if not cont_files:
        return None

    variant_values: dict[str, list[float]] = {}
    variant_stats: dict[str, tuple[int, float, float]] = {}

    for file in cont_files:
        normalized_headers = [header.strip().lower() for header in file.headers]
        is_aggregate = file.detected_type == "ab_continuous_agg"
        for row in file.rows:
            data = {key.lower(): value for key, value in row.items()}
            variant = data.get("variant", "unknown").strip() or "unknown"
            if is_aggregate:
                n = _safe_int(data.get("n", "") or "") or _safe_int(
                    data.get("count", "") or ""
                )
                mean_value = _safe_float(data.get("mean", "") or "")
                std_value = _safe_float(data.get("std", "") or "")
                if n is None or mean_value is None or std_value is None:
                    continue
                variant_stats[variant] = (n, mean_value, std_value)
            else:
                value_col = next(
                    (col for col in CONTINUOUS_VALUE_COLUMNS if col in normalized_headers),
                    None,
                )
                if value_col is None:
                    continue
                value = _safe_float(data.get(value_col, "") or "")
                if value is None:
                    continue
                variant_values.setdefault(variant, []).append(value)

    if variant_values:
        for variant, values in variant_values.items():
            if len(values) < 2:
                std_value = 0.0
            else:
                std_value = stdev(values)
            variant_stats[variant] = (len(values), fmean(values), std_value)

    if len(variant_stats) < 2:
        return None

    sorted_variants = sorted(variant_stats.items())
    first, second = sorted_variants[0], sorted_variants[1]
    variant_a = ContinuousVariant(
        name=first[0], n=first[1][0], mean=first[1][1], std=first[1][2]
    )
    variant_b = ContinuousVariant(
        name=second[0], n=second[1][0], mean=second[1][1], std=second[1][2]
    )

    summary = ab_test_continuous(variant_a, variant_b)

    return {
        "variants": [variant_a, variant_b],
        "difference": summary["difference"],
        "p_value": summary["p_value"],
    }


def _qual_summary(files: Sequence[CsvFile]) -> dict[str, object] | None:
    qual_files = [file for file in files if file.detected_type == "qual"]
    if not qual_files:
        return None

    counts: dict[str, int] = {}
    severity_counts: dict[int, int] = {}
    total_quotes = 0

    for file in qual_files:
        normalized_headers = [header.strip().lower() for header in file.headers]
        code_col = next((col for col in QUAL_COLUMNS if col in normalized_headers), None)
        severity_col = "severity" if "severity" in normalized_headers else None
        if code_col is None:
            continue

        for row in file.rows:
            data = {key.lower(): value for key, value in row.items()}
            codes_raw = data.get(code_col, "")
            codes = [code.strip().lower() for code in codes_raw.split(",") if code.strip()]
            if not codes:
                continue
            total_quotes += 1
            for code in dict.fromkeys(codes):
                counts[code] = counts.get(code, 0) + 1
            if severity_col:
                severity_value = _safe_int(data.get(severity_col, "") or "")
                if severity_value is not None:
                    severity_counts[severity_value] = severity_counts.get(severity_value, 0) + 1

    top_themes = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:5]
    return {
        "total_quotes": total_quotes,
        "top_themes": top_themes,
        "severity_counts": dict(sorted(severity_counts.items())),
    }


def _unrecognized(files: Sequence[CsvFile]) -> list[tuple[str, list[str]]]:
    unknown = []
    for file in files:
        if file.detected_type == "unknown":
            columns = [col.strip() for col in file.headers][:5]
            unknown.append((file.path.name, columns))
    return unknown


def _data_quality_notes(files: Sequence[CsvFile], issues: Sequence[ValidationIssue]) -> list[str]:
    issue_map: dict[str, list[str]] = {}
    for issue in issues:
        issue_map.setdefault(issue.filename, []).append(issue.message)

    notes = []
    for file in sorted(files, key=lambda item: item.path.name):
        messages = issue_map.get(file.path.name, [])
        if messages:
            issue_text = "; ".join(messages)
        else:
            issue_text = "none"
        notes.append(
            f"- {file.path.name}: missing_values={file.missing_values}; issues={issue_text}"
        )
    return notes


def _file_inventory(files: Sequence[CsvFile]) -> list[str]:
    label_map = {
        "sus": "SUS responses",
        "usability": "Usability sessions",
        "ab_binary_agg": "A/B binary",
        "ab_binary_row": "A/B binary",
        "ab_continuous_agg": "A/B continuous",
        "ab_continuous_row": "A/B continuous",
        "qual": "Qualitative codes",
        "unknown": "Unrecognized",
    }
    lines = []
    for file in sorted(files, key=lambda item: item.path.name):
        label = label_map.get(file.detected_type, "Unrecognized")
        lines.append(f"- {file.path.name} — {label}")
    return lines


def _executive_summary(
    sus: dict[str, object] | None,
    usability: dict[str, object] | None,
    ab_binary: dict[str, object] | None,
    ab_continuous: dict[str, object] | None,
    qual: dict[str, object] | None,
    files: Sequence[CsvFile],
) -> list[str]:
    bullets: list[str] = []

    if sus and sus["count"]:
        bullets.append(
            "SUS mean "
            f"{_format_float(sus['mean'])} (n={sus['count']}, "
            f"range {_format_float(sus['min'])}-{_format_float(sus['max'])})."
        )
    if usability:
        worst = usability["worst_tasks"]
        if worst:
            worst_task = worst[0]
            metrics = worst_task[1]
            bullets.append(
                "Usability success rate "
                f"{_format_float(usability['overall_success'])} with worst task "
                f"{worst_task[0]} (success "
                f"{_format_float(metrics['success_rate'])})."
            )
    if ab_binary:
        bullets.append(
            "Binary experiment diff "
            f"{_format_float(ab_binary['difference'])} (p="
            f"{_format_float(ab_binary['p_value'])})."
        )
    if ab_continuous:
        bullets.append(
            "Continuous experiment diff "
            f"{_format_float(ab_continuous['difference'])} (p="
            f"{_format_float(ab_continuous['p_value'])})."
        )
    if qual and qual["top_themes"]:
        themes = ", ".join(
            f"{name} ({count})" for name, count in qual["top_themes"][:3]
        )
        bullets.append(f"Top qualitative themes: {themes}.")

    if len(bullets) < 3:
        bullets.append(f"Files analyzed: {len(files)}.")
    if len(bullets) < 3:
        types = sorted({file.detected_type for file in files})
        bullets.append(f"Detected types: {', '.join(types)}.")

    return bullets[:6]


def build_report(
    input_dir: Path,
    files: Sequence[CsvFile],
    *,
    title: str,
    seed: int,
) -> str:
    issues: list[ValidationIssue] = []
    sus = _sus_summary(files, issues)
    usability = _usability_summary(files, issues)
    ab_binary = _ab_binary_summary(files, issues)
    ab_continuous = _ab_continuous_summary(files, issues)
    qual = _qual_summary(files)
    unknown = _unrecognized(files)

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- input_dir: {input_dir}")
    lines.append(f"- files_count: {len(files)}")
    lines.append(f"- seed: {seed}")
    lines.append("")

    lines.append("## Executive Summary")
    for bullet in _executive_summary(sus, usability, ab_binary, ab_continuous, qual, files):
        lines.append(f"- {bullet}")
    lines.append("")

    if sus is not None:
        lines.append("## SUS Summary")
        lines.append(f"- responses: {sus['count']}")
        if sus["count"]:
            lines.append(f"- mean: {_format_float(sus['mean'])}")
            lines.append(f"- median: {_format_float(sus['median'])}")
            lines.append(
                f"- range: {_format_float(sus['min'])} to {_format_float(sus['max'])}"
            )
            lowest = ", ".join(
                f"{item[0]} ({_format_float(item[1])})" for item in sus["lowest_items"]
            )
            lines.append(f"- lowest_items: {lowest}")
        lines.append("")

    if usability is not None:
        lines.append("## Usability Sessions Summary")
        lines.append(f"- tasks_analyzed: {len(usability['tasks'])}")
        lines.append(
            f"- overall_success_rate: {_format_float(usability['overall_success'])}"
        )
        lines.append("- per_task_metrics:")
        for task_id in sorted(usability["tasks"].keys()):
            metrics = usability["tasks"][task_id]
            median_time = metrics["median_time"]
            median_text = _format_float(median_time) if median_time is not None else "n/a"
            lines.append(
                "  - "
                f"{task_id}: success_rate={_format_float(metrics['success_rate'])}, "
                f"median_time={median_text}, total_errors={metrics['total_errors']}"
            )
        lines.append("- worst_tasks:")
        for task_id, metrics in usability["worst_tasks"]:
            median_time = metrics["median_time"]
            median_text = _format_float(median_time) if median_time is not None else "n/a"
            lines.append(
                "  - "
                f"{task_id}: success_rate={_format_float(metrics['success_rate'])}, "
                f"median_time={median_text}"
            )
        lines.append("")

    if ab_binary is not None or ab_continuous is not None:
        lines.append("## A/B Experiment Summary")
        if ab_binary is not None:
            lines.append("- binary_conversion:")
            for variant in ab_binary["variants"]:
                rate = variant.conversions / variant.users if variant.users else 0.0
                lines.append(
                    "  - "
                    f"{variant.name}: users={variant.users}, conversions={variant.conversions}, "
                    f"rate={_format_float(rate)}"
                )
            relative_lift = (
                _format_float(ab_binary["relative_lift"])
                if ab_binary["relative_lift"] is not None
                else "n/a"
            )
            lines.append(
                "  - "
                f"diff={_format_float(ab_binary['difference'])}, "
                f"relative_lift={relative_lift}, "
                f"p_value={_format_float(ab_binary['p_value'])}"
            )
        if ab_continuous is not None:
            lines.append("- continuous_metric:")
            for variant in ab_continuous["variants"]:
                lines.append(
                    "  - "
                    f"{variant.name}: n={variant.n}, mean={_format_float(variant.mean)}, "
                    f"std={_format_float(variant.std)}"
                )
            lines.append(
                "  - "
                f"diff={_format_float(ab_continuous['difference'])}, "
                f"p_value={_format_float(ab_continuous['p_value'])}"
            )
        lines.append("")

    if qual is not None:
        lines.append("## Qualitative Themes Summary")
        lines.append(f"- coded_quotes: {qual['total_quotes']}")
        lines.append("- top_themes:")
        for name, count in qual["top_themes"]:
            lines.append(f"  - {name}: {count}")
        if qual["severity_counts"]:
            severity_text = ", ".join(
                f"{key}:{value}" for key, value in qual["severity_counts"].items()
            )
            lines.append(f"- severity_distribution: {severity_text}")
        lines.append("")

    if unknown:
        lines.append("## Unrecognized CSVs")
        for filename, columns in unknown:
            column_text = ", ".join(columns) if columns else ""
            lines.append(f"- {filename}: columns={column_text}")
        lines.append("")

    if any(file.detected_type != "unknown" for file in files):
        lines.append("## Data Quality / Validation Notes")
        lines.extend(_data_quality_notes(files, issues))
        lines.append("")

    lines.append("## Appendix: File Inventory")
    lines.extend(_file_inventory(files))
    lines.append("")

    return "\n".join(lines)


def run_study_report(
    input_dir: Path, output_path: Path, *, title: str, seed: int
) -> str:
    random.seed(seed)
    files = _load_csvs(input_dir)
    report = build_report(input_dir, files, title=title, seed=seed)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HCI study report CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    study_report = subparsers.add_parser("study-report", help="Generate a study report")
    study_report.add_argument("--in", dest="input_dir", required=True)
    study_report.add_argument("--out", dest="output_path", required=True)
    study_report.add_argument("--title", default="HCI Study Report")
    study_report.add_argument("--seed", type=int, default=42)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "study-report":
        report = run_study_report(
            Path(args.input_dir),
            Path(args.output_path),
            title=args.title,
            seed=args.seed,
        )
        sys.stdout.write(report)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
