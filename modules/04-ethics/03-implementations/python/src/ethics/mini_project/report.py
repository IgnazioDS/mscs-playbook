from __future__ import annotations

import json
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .scoring import normalize_level, risk_score

REQUIRED_FILES = ["system.json", "data.json", "model.json", "risks.json", "metrics.json"]
CRITICAL_FILES = {"system.json", "data.json", "risks.json"}


@dataclass(frozen=True)
class ReviewInputs:
    input_dir: Path
    files_present: int
    missing_files: list[str]
    system: dict[str, Any] | None
    data: dict[str, Any] | None
    model: dict[str, Any] | None
    risks: list[dict[str, Any]]
    metrics: dict[str, Any] | None


@dataclass(frozen=True)
class RiskEntry:
    risk_id: str
    risk: str
    severity: str
    likelihood: str
    mitigation: str
    residual_severity: str
    residual_likelihood: str

    @property
    def residual_score(self) -> int:
        return risk_score(self.residual_severity, self.residual_likelihood)


@dataclass(frozen=True)
class ReviewScores:
    overall_risk: str
    shipping_gate: str
    shipping_rationale: str
    issues: list[str]
    unresolved_count: int


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_inputs(input_dir: str | Path) -> ReviewInputs:
    base = Path(input_dir)
    read_base = base.resolve()
    missing: list[str] = []
    loaded: dict[str, dict[str, Any] | None] = {}

    for filename in REQUIRED_FILES:
        path = read_base / filename
        payload = _read_json(path)
        if payload is None:
            missing.append(filename)
        loaded[filename] = payload

    risks_payload = loaded["risks.json"] or {}
    risks = _normalize_risks(risks_payload)

    files_present = len(REQUIRED_FILES) - len(missing)
    return ReviewInputs(
        input_dir=base,
        files_present=files_present,
        missing_files=missing,
        system=loaded["system.json"],
        data=loaded["data.json"],
        model=loaded["model.json"],
        risks=risks,
        metrics=loaded["metrics.json"],
    )


def _normalize_risks(payload: dict[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("risks")
    if raw is None and isinstance(payload, list):
        raw = payload
    if not raw:
        return []

    normalized: list[dict[str, Any]] = []
    for idx, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            continue
        risk_id = str(item.get("id") or f"R{idx:02d}")
        residual = item.get("residual") if isinstance(item.get("residual"), dict) else {}
        normalized.append(
            {
                "risk_id": risk_id,
                "risk": str(item.get("risk", "unknown")),
                "severity": normalize_level(item.get("severity")),
                "likelihood": normalize_level(item.get("likelihood")),
                "mitigation": str(item.get("mitigation", "")).strip(),
                "residual_severity": normalize_level(
                    item.get("residual_severity") or residual.get("severity") or item.get("severity")
                ),
                "residual_likelihood": normalize_level(
                    item.get("residual_likelihood")
                    or residual.get("likelihood")
                    or item.get("likelihood")
                ),
            }
        )

    normalized.sort(key=lambda entry: entry["risk_id"])
    return normalized


def _risk_entries(risks: list[dict[str, Any]]) -> list[RiskEntry]:
    entries = [
        RiskEntry(
            risk_id=risk["risk_id"],
            risk=risk["risk"],
            severity=risk["severity"],
            likelihood=risk["likelihood"],
            mitigation=risk["mitigation"],
            residual_severity=risk["residual_severity"],
            residual_likelihood=risk["residual_likelihood"],
        )
        for risk in risks
    ]
    entries.sort(key=lambda entry: entry.risk_id)
    return entries


def _overall_risk(missing_files: list[str], entries: list[RiskEntry]) -> str:
    if any(name in CRITICAL_FILES for name in missing_files):
        return "HIGH"
    if any(entry.residual_score >= 6 for entry in entries):
        return "HIGH"
    if entries:
        avg_score = sum(entry.residual_score for entry in entries) / len(entries)
        if avg_score >= 3:
            return "MED"
    return "LOW"


def _compliance_checks(inputs: ReviewInputs, entries: list[RiskEntry]) -> list[tuple[str, bool, str]]:
    data = inputs.data or {}
    model = inputs.model or {}
    system = inputs.system or {}
    metrics = inputs.metrics or {}

    pii_fields = data.get("pii_fields") or []
    retention_days = data.get("retention_days")
    consent = str(data.get("consent", "")).strip().lower()
    access_controls = str(data.get("access_controls", "")).strip()

    privacy_ok = (
        bool(pii_fields)
        and consent in {"yes", "true", "y"}
        and isinstance(retention_days, int)
        and retention_days <= 365
        and bool(access_controls)
    )
    privacy_detail = (
        f"consent={consent or 'unknown'}, pii_fields={len(pii_fields)}, "
        f"retention_days={retention_days}, access_controls={access_controls or 'none'}"
    )

    fairness = metrics.get("fairness") if isinstance(metrics, dict) else None
    fairness_ok = isinstance(fairness, dict) and fairness.get("metric") not in {None, "n/a"}
    fairness_detail = "metric=n/a"
    if fairness_ok:
        fairness_detail = (
            f"metric={fairness.get('metric')}, value={fairness.get('value')}, "
            f"threshold={fairness.get('threshold')}"
        )

    transparency_ok = bool(system.get("purpose")) and bool(model.get("limitations"))
    transparency_detail = "purpose set, limitations provided" if transparency_ok else "purpose/limitations missing"

    high_risks = [entry for entry in entries if entry.severity == "high"]
    high_mitigated = [entry for entry in high_risks if entry.mitigation]
    safety_ok = bool(entries) and len(high_risks) == len(high_mitigated)
    safety_detail = f"high-risk mitigations present ({len(high_mitigated)}/{len(high_risks)})"

    governance_ok = bool(system.get("owner")) and bool(system.get("review_date"))
    governance_detail = "owner and review_date set" if governance_ok else "owner/review_date missing"

    return [
        ("privacy", privacy_ok, privacy_detail),
        ("fairness", fairness_ok, fairness_detail),
        ("transparency", transparency_ok, transparency_detail),
        ("safety", safety_ok, safety_detail),
        ("governance", governance_ok, governance_detail),
    ]


def _review_scores(inputs: ReviewInputs, entries: list[RiskEntry]) -> ReviewScores:
    overall = _overall_risk(inputs.missing_files, entries)
    missing_critical = [name for name in inputs.missing_files if name in CRITICAL_FILES]
    mitigations_present = any(entry.mitigation for entry in entries)
    unresolved = [entry for entry in entries if entry.residual_score >= 4 or not entry.mitigation]

    if missing_critical:
        gate = "FAIL"
        rationale = "missing critical inputs"
    elif overall == "HIGH":
        gate = "CONDITIONAL" if mitigations_present else "FAIL"
        rationale = "high risk with mitigations" if mitigations_present else "high risk without mitigations"
    elif overall == "MED":
        gate = "CONDITIONAL"
        rationale = "medium risk requires mitigation follow-up"
    else:
        gate = "PASS"
        rationale = "low risk and critical inputs present"

    issues = []
    for name in missing_critical:
        issues.append(f"Missing input: {name}")

    sorted_entries = sorted(entries, key=lambda entry: (-entry.residual_score, entry.risk_id))
    for entry in sorted_entries:
        issues.append(f"{entry.risk_id}: {entry.risk} (score {entry.residual_score})")

    return ReviewScores(
        overall_risk=overall,
        shipping_gate=gate,
        shipping_rationale=rationale,
        issues=issues[:3],
        unresolved_count=len(unresolved),
    )


def generate_report(inputs: ReviewInputs, *, seed: int | None = None) -> str:
    entries = _risk_entries(inputs.risks)
    scores = _review_scores(inputs, entries)
    checks = _compliance_checks(inputs, entries)

    lines: list[str] = []
    lines.append("# Ethics Review Report")
    lines.append("")
    lines.append("## Metadata")
    lines.append(f"- input_dir: {inputs.input_dir}")
    lines.append(f"- files_present: {inputs.files_present}/{len(REQUIRED_FILES)}")
    lines.append(f"- seed: {seed if seed is not None else 'n/a'}")
    lines.append("")
    lines.append("## Missing Inputs")
    if inputs.missing_files:
        for name in inputs.missing_files:
            lines.append(f"- {name}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append(f"- overall_risk: {scores.overall_risk}")
    lines.append("- top_issues:")
    if scores.issues:
        for issue in scores.issues:
            lines.append(f"  - {issue}")
    else:
        lines.append("  - None")
    lines.append("")
    lines.append("## Compliance Checklist")
    for name, ok, detail in checks:
        mark = "x" if ok else " "
        lines.append(f"- [{mark}] {name}: {detail}")
    lines.append("")
    lines.append("## Risk Register")
    lines.append("| id | risk | severity | likelihood | mitigation | residual | residual_score |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    if entries:
        for entry in entries:
            residual = f"{entry.residual_severity}/{entry.residual_likelihood}"
            mitigation = entry.mitigation or "n/a"
            lines.append(
                "| "
                + " | ".join(
                    [
                        entry.risk_id,
                        entry.risk,
                        entry.severity,
                        entry.likelihood,
                        mitigation,
                        residual,
                        str(entry.residual_score),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| n/a | n/a | n/a | n/a | n/a | n/a | n/a |")
    lines.append("")
    lines.append("## Data Handling Summary")
    data = inputs.data or {}
    sources = data.get("sources") or []
    pii_fields = data.get("pii_fields") or []
    lines.append(f"- sources: {', '.join(sources) if sources else 'n/a'}")
    lines.append(f"- pii_fields: {', '.join(pii_fields) if pii_fields else 'n/a'}")
    lines.append(f"- retention_days: {data.get('retention_days', 'n/a')}")
    lines.append(f"- consent: {data.get('consent', 'n/a')}")
    lines.append(f"- access_controls: {data.get('access_controls', 'n/a')}")
    lines.append("")
    lines.append("## Evaluation & Monitoring Plan")
    metrics = inputs.metrics or {}
    fairness = metrics.get("fairness") if isinstance(metrics, dict) else None
    quality = metrics.get("quality") if isinstance(metrics, dict) else None
    monitoring = metrics.get("monitoring") if isinstance(metrics, dict) else None

    if isinstance(fairness, dict) and fairness.get("metric"):
        lines.append(
            f"- fairness: {fairness.get('metric')}={fairness.get('value')} "
            f"(threshold {fairness.get('threshold')})"
        )
    else:
        lines.append("- fairness: n/a")

    if isinstance(quality, dict) and quality.get("metric"):
        lines.append(
            f"- quality: {quality.get('metric')}={quality.get('value')} "
            f"(threshold {quality.get('threshold')})"
        )
    else:
        lines.append("- quality: n/a")

    if isinstance(monitoring, list) and monitoring:
        lines.append(f"- monitoring: {', '.join(monitoring)}")
    else:
        lines.append("- monitoring: n/a")

    lines.append("")
    lines.append("## Shipping Gate")
    lines.append(f"- gate: {scores.shipping_gate}")
    lines.append(
        "- rationale: "
        f"overall risk {scores.overall_risk.lower()}; {scores.shipping_rationale}"
    )

    return "\n".join(lines) + "\n"
