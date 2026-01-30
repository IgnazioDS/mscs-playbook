"""HCI Measurement Toolkit: metrics, experiments, research, and accessibility."""

from .metrics import (
    UsabilitySession,
    task_metrics,
    task_success_rate,
    completion_rate,
    error_rate,
    time_on_task_summary,
    sus_score,
    sus_scores,
    sus_aggregate,
)
from .experiments import (
    BinaryVariant,
    ContinuousVariant,
    ab_test_binary,
    ab_test_continuous,
    required_sample_size_binary,
)
from .research import (
    HeuristicFinding,
    heuristic_report,
    qualitative_theme_report,
    parse_tags,
)
from .accessibility import (
    contrast_ratio,
    contrast_report,
    TapTarget,
    tap_target_report,
)

__all__ = [
    "UsabilitySession",
    "task_metrics",
    "task_success_rate",
    "completion_rate",
    "error_rate",
    "time_on_task_summary",
    "sus_score",
    "sus_scores",
    "sus_aggregate",
    "BinaryVariant",
    "ContinuousVariant",
    "ab_test_binary",
    "ab_test_continuous",
    "required_sample_size_binary",
    "HeuristicFinding",
    "heuristic_report",
    "qualitative_theme_report",
    "parse_tags",
    "contrast_ratio",
    "contrast_report",
    "TapTarget",
    "tap_target_report",
]
