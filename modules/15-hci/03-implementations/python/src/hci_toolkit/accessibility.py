from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    value = hex_color.strip().lstrip("#")
    if len(value) != 6:
        raise ValueError("hex color must be 6 characters")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def _linearize_channel(channel: int) -> float:
    srgb = channel / 255.0
    if srgb <= 0.03928:
        return srgb / 12.92
    return ((srgb + 0.055) / 1.055) ** 2.4


def contrast_ratio(foreground_hex: str, background_hex: str) -> float:
    """Compute WCAG contrast ratio between two hex colors."""
    fg = _hex_to_rgb(foreground_hex)
    bg = _hex_to_rgb(background_hex)
    fg_lum = (
        0.2126 * _linearize_channel(fg[0])
        + 0.7152 * _linearize_channel(fg[1])
        + 0.0722 * _linearize_channel(fg[2])
    )
    bg_lum = (
        0.2126 * _linearize_channel(bg[0])
        + 0.7152 * _linearize_channel(bg[1])
        + 0.0722 * _linearize_channel(bg[2])
    )

    lighter = max(fg_lum, bg_lum)
    darker = min(fg_lum, bg_lum)
    return (lighter + 0.05) / (darker + 0.05)


def contrast_report(foreground_hex: str, background_hex: str) -> dict[str, float | bool]:
    """Return contrast ratio with AA pass/fail checks."""
    ratio = contrast_ratio(foreground_hex, background_hex)
    return {
        "ratio": ratio,
        "aa_normal": ratio >= 4.5,
        "aa_large": ratio >= 3.0,
    }


@dataclass(frozen=True)
class TapTarget:
    """Represents a tap target measurement."""

    name: str
    size_px: float
    spacing_px: float


def _tap_target_checks(
    target: TapTarget, *, min_size_px: float, min_spacing_px: float
) -> dict[str, dict[str, float | bool]]:
    size_pass = target.size_px >= min_size_px
    spacing_pass = target.spacing_px >= min_spacing_px
    return {
        "min_size_px": {
            "required": min_size_px,
            "actual": target.size_px,
            "pass": size_pass,
        },
        "min_spacing_px": {
            "required": min_spacing_px,
            "actual": target.spacing_px,
            "pass": spacing_pass,
        },
    }


def tap_target_report(
    targets: Sequence[TapTarget], *, min_size_px: float = 44.0, min_spacing_px: float = 8.0
) -> dict[str, object]:
    """Generate a checklist report for tap targets and spacing."""
    items = []
    passed = 0
    for target in targets:
        checks = _tap_target_checks(
            target, min_size_px=min_size_px, min_spacing_px=min_spacing_px
        )
        item_pass = all(check["pass"] for check in checks.values())
        if item_pass:
            passed += 1
        items.append(
            {
                "name": target.name,
                "size_px": target.size_px,
                "spacing_px": target.spacing_px,
                "checks": checks,
                "passed": item_pass,
            }
        )

    total = len(targets)
    return {
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
        "items": items,
    }
