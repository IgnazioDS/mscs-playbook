from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Tuple


@dataclass(frozen=True)
class BinaryVariant:
    """Binary conversion variant summary."""

    name: str
    users: int
    conversions: int


@dataclass(frozen=True)
class ContinuousVariant:
    """Continuous metric variant summary."""

    name: str
    n: int
    mean: float
    std: float


def _normal_cdf(value: float) -> float:
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def _normal_ppf(prob: float) -> float:
    if prob <= 0.0 or prob >= 1.0:
        raise ValueError("prob must be between 0 and 1")

    # Acklam approximation
    a = [
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    ]
    b = [
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464968e00,
        2.938163982698783e00,
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e00,
        3.754408661907416e00,
    ]

    plow = 0.02425
    phigh = 1 - plow

    if prob < plow:
        q = math.sqrt(-2 * math.log(prob))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q) + 1
        )
    if prob > phigh:
        q = math.sqrt(-2 * math.log(1 - prob))
        return -(
            (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
            / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
        )

    q = prob - 0.5
    r = q * q
    return (
        (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q
    ) / (
        (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    )


def _t_pdf(value: float, df: float) -> float:
    numerator = math.gamma((df + 1) / 2)
    denominator = math.sqrt(df * math.pi) * math.gamma(df / 2)
    return (numerator / denominator) * (1 + (value**2) / df) ** (-(df + 1) / 2)


def _simpson_integral(func, a: float, b: float, steps: int) -> float:
    if steps % 2 == 1:
        steps += 1
    h = (b - a) / steps
    total = func(a) + func(b)
    for i in range(1, steps):
        coef = 4 if i % 2 == 1 else 2
        total += coef * func(a + i * h)
    return total * h / 3


def _t_cdf(value: float, df: float, *, steps: int = 2000) -> float:
    if value == 0:
        return 0.5
    sign = 1 if value > 0 else -1
    area = _simpson_integral(lambda x: _t_pdf(x, df), 0.0, abs(value), steps)
    return 0.5 + sign * area


def _t_ppf(prob: float, df: float) -> float:
    if prob <= 0.0 or prob >= 1.0:
        raise ValueError("prob must be between 0 and 1")

    if prob == 0.5:
        return 0.0

    target = prob
    if prob < 0.5:
        target = 1 - prob

    low, high = 0.0, 10.0
    while _t_cdf(high, df) < target:
        high *= 2
        if high > 100:
            break

    for _ in range(60):
        mid = (low + high) / 2
        if _t_cdf(mid, df) < target:
            low = mid
        else:
            high = mid

    result = (low + high) / 2
    return -result if prob < 0.5 else result


def ab_test_binary(
    variant_a: BinaryVariant,
    variant_b: BinaryVariant,
    *,
    alpha: float = 0.05,
) -> dict[str, float]:
    """Summarize an A/B test for binary conversion using normal approximation."""
    p1 = variant_a.conversions / variant_a.users
    p2 = variant_b.conversions / variant_b.users
    diff = p2 - p1
    se = math.sqrt(p1 * (1 - p1) / variant_a.users + p2 * (1 - p2) / variant_b.users)

    if se == 0:
        return {
            "difference": diff,
            "z_stat": 0.0,
            "p_value": 1.0,
            "ci_low": diff,
            "ci_high": diff,
        }

    z_stat = diff / se
    p_value = 2 * (1 - _normal_cdf(abs(z_stat)))
    z_crit = _normal_ppf(1 - alpha / 2)
    ci_low = diff - z_crit * se
    ci_high = diff + z_crit * se

    return {
        "difference": diff,
        "z_stat": z_stat,
        "p_value": p_value,
        "ci_low": ci_low,
        "ci_high": ci_high,
    }


def ab_test_continuous(
    variant_a: ContinuousVariant,
    variant_b: ContinuousVariant,
    *,
    alpha: float = 0.05,
) -> dict[str, float]:
    """Summarize an A/B test for continuous metrics with Welch's approximation."""
    diff = variant_b.mean - variant_a.mean
    se = math.sqrt(
        (variant_a.std**2) / variant_a.n + (variant_b.std**2) / variant_b.n
    )
    if se == 0:
        return {
            "difference": diff,
            "t_stat": 0.0,
            "df": float("inf"),
            "p_value": 1.0,
            "ci_low": diff,
            "ci_high": diff,
        }

    t_stat = diff / se
    numerator = (variant_a.std**2 / variant_a.n + variant_b.std**2 / variant_b.n) ** 2
    denominator = (
        (variant_a.std**2 / variant_a.n) ** 2 / (variant_a.n - 1)
        + (variant_b.std**2 / variant_b.n) ** 2 / (variant_b.n - 1)
    )
    df = numerator / denominator if denominator != 0 else float("inf")

    if math.isinf(df):
        p_value = 2 * (1 - _normal_cdf(abs(t_stat)))
        t_crit = _normal_ppf(1 - alpha / 2)
    else:
        p_value = 2 * (1 - _t_cdf(abs(t_stat), df))
        t_crit = _t_ppf(1 - alpha / 2, df)

    ci_low = diff - t_crit * se
    ci_high = diff + t_crit * se

    return {
        "difference": diff,
        "t_stat": t_stat,
        "df": df,
        "p_value": p_value,
        "ci_low": ci_low,
        "ci_high": ci_high,
    }


def required_sample_size_binary(
    baseline_rate: float,
    min_detectable_effect: float,
    *,
    alpha: float = 0.05,
    power: float = 0.8,
) -> int:
    """Estimate per-variant sample size for a binary metric.

    Uses a normal approximation for two-proportion tests.
    """
    if baseline_rate <= 0 or baseline_rate >= 1:
        raise ValueError("baseline_rate must be between 0 and 1")
    if min_detectable_effect == 0:
        raise ValueError("min_detectable_effect must be non-zero")

    p1 = baseline_rate
    p2 = min(0.999, max(0.001, baseline_rate + min_detectable_effect))
    p_bar = (p1 + p2) / 2

    z_alpha = _normal_ppf(1 - alpha / 2)
    z_beta = _normal_ppf(power)

    term1 = z_alpha * math.sqrt(2 * p_bar * (1 - p_bar))
    term2 = z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    n = ((term1 + term2) ** 2) / ((p2 - p1) ** 2)
    return math.ceil(n)
