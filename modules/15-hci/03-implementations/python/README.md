# Python Implementations

HCI Measurement Toolkit for usability metrics, experiment analysis, qualitative research helpers, and accessibility checks.

## Quickstart
Run from the repo root:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r modules/15-hci/03-implementations/python/requirements.txt
python -m pytest -q modules/15-hci/03-implementations/python/tests
```

## Usage

### Usability metrics
```python
from src.hci_toolkit.metrics import UsabilitySession, task_metrics, sus_score

sessions = [
    UsabilitySession("signup", "u1", True, 42, 0),
    UsabilitySession("signup", "u2", False, 0, 2),
]
summary = task_metrics(sessions)
score = sus_score([3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
```

### Experiment analysis
```python
from src.hci_toolkit.experiments import (
    BinaryVariant,
    ContinuousVariant,
    ab_test_binary,
    ab_test_continuous,
    required_sample_size_binary,
)

binary = ab_test_binary(BinaryVariant("A", 100, 20), BinaryVariant("B", 120, 36))
continuous = ab_test_continuous(
    ContinuousVariant("A", 50, 100, 15),
    ContinuousVariant("B", 55, 108, 20),
)
needed = required_sample_size_binary(0.2, 0.05)
```

### UX research helpers
```python
from src.hci_toolkit.research import HeuristicFinding, heuristic_report, qualitative_theme_report

findings = [HeuristicFinding("Consistency", 2), HeuristicFinding("Visibility", 1)]
heuristics = heuristic_report(findings)

codes = ["login, confusion", "search, positive", "login, slow"]
qual = qualitative_theme_report(codes, top_n=3)
```

### Accessibility checks
```python
from src.hci_toolkit.accessibility import TapTarget, contrast_report, tap_target_report

contrast = contrast_report("#111111", "#ffffff")
report = tap_target_report([TapTarget("Primary CTA", 48, 10)])
```

## Determinism and limitations
- All calculations are deterministic and use the Python standard library only.
- A/B test statistics use normal and Welch-style approximations (no exact distribution fitting).
- Sample size estimates are rough and assume independent samples and stable baseline rates.
