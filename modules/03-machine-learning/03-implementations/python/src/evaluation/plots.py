"""Minimal plotting utilities."""

from __future__ import annotations

from typing import Optional, Tuple

import matplotlib.pyplot as plt


def plot_residuals(y_true, y_pred, save_path: Optional[str] = None) -> Tuple[plt.Figure, plt.Axes]:
    """Plot residuals (y_true - y_pred) against predictions.

    Returns:
        (fig, ax) for further customization or testing.
    """
    residuals = y_true - y_pred
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.scatter(y_pred, residuals, alpha=0.6)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Residual")
    ax.set_title("Residual Plot")
    if save_path:
        fig.savefig(save_path, bbox_inches="tight")
    return fig, ax
