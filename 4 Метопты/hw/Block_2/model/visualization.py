from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple

import numpy as np

from model.base import IterationPoint, OptimizationResult
from objective import z


def _strict_levels_from_history(zs: List[float]) -> List[float]:
    """Строит строго возрастающий список уровней той же длины, что и история."""

    if not zs:
        raise ValueError("Список значений функции пуст.")

    indexed = sorted((value, idx) for idx, value in enumerate(zs))
    eps = 1e-9
    adjusted = [0.0] * len(zs)

    prev = None
    for value, idx in indexed:
        if prev is None:
            new_value = value
        else:
            new_value = value if value > prev else prev + eps
        adjusted[idx] = new_value
        prev = new_value

    # contour ожидает возрастающий список уровней.
    return sorted(adjusted)


def _extract_path(history: Iterable[IterationPoint]) -> Tuple[List[float], List[float], List[float]]:
    xs, ys, zs = [], [], []
    for p in history:
        xs.append(p.x)
        ys.append(p.y)
        zs.append(p.z)
    return xs, ys, zs


def plot_contours_with_path(result: OptimizationResult, out_file: str, margin: float = 1.5) -> None:
    """ДЗ2.1: линии уровня через вершины ломаной истории."""

    import matplotlib.pyplot as plt

    xs, ys, zs = _extract_path(result.history)
    if not xs:
        raise ValueError("История итераций пуста.")

    x_min, x_max = min(xs) - margin, max(xs) + margin
    y_min, y_max = min(ys) - margin, max(ys) + margin

    x_grid = np.linspace(x_min, x_max, 300)
    y_grid = np.linspace(y_min, y_max, 300)
    xx, yy = np.meshgrid(x_grid, y_grid)
    zz = z(xx, yy)

    # Количество уровней равно количеству приближений (ДЗ2.1).
    levels = _strict_levels_from_history(zs)

    fig, ax = plt.subplots(figsize=(8, 6))
    contour = ax.contour(xx, yy, zz, levels=levels, linewidths=1.1)
    ax.clabel(contour, inline=True, fontsize=8)

    ax.plot(xs, ys, "o-r", linewidth=1.8, markersize=4)
    ax.set_title(f"{result.method_name}: contour path")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(alpha=0.25)

    out_path = Path(out_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
