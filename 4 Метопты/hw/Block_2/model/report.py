from __future__ import annotations

from pathlib import Path
from typing import Iterable

from model.analytics import StationaryPointInfo
from model.base import OptimizationResult


METHOD_NAME_RU = {
    "Coordinate Descent": "Метод покоординатного спуска",
    "Gradient Descent": "Метод градиентного спуска",
    "Steepest Descent": "Метод наискорейшего спуска",
    "Newton Method": "Метод Ньютона",
}

POINT_TYPE_RU = {
    "local minimum": "локальный минимум",
    "local maximum": "локальный максимум",
    "saddle": "седловая точка",
    "inconclusive": "тип не определен",
}


def build_report_text(
    methods_results: Iterable[OptimizationResult],
    newton_result: OptimizationResult,
    stationary_points: Iterable[StationaryPointInfo],
) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append("Отчет по домашнему заданию. Блок 2")
    lines.append("=" * 70)
    lines.append("")

    lines.append("ДЗ2.1 - Методы из ЛР4")
    for r in methods_results:
        method_name_ru = METHOD_NAME_RU.get(r.method_name, r.method_name)
        lines.append(
            f"- {method_name_ru}: итераций={r.iterations}, "
            f"x*=({r.x_star:.6f}, {r.y_star:.6f}), z*={r.z_star:.6f}"
        )
    lines.append("")

    lines.append("ДЗ2.2 - Метод Ньютона")
    newton_name_ru = METHOD_NAME_RU.get(newton_result.method_name, newton_result.method_name)
    lines.append(
        f"- {newton_name_ru}: итераций={newton_result.iterations}, "
        f"x*=({newton_result.x_star:.6f}, {newton_result.y_star:.6f}), z*={newton_result.z_star:.6f}"
    )
    lines.append("")

    lines.append("Аналитические стационарные точки")
    for p in stationary_points:
        point_type_ru = POINT_TYPE_RU.get(p.point_type, p.point_type)
        lines.append(
            f"- ({p.point[0]:.6f}, {p.point[1]:.6f}) | z={p.value:.6f} | "
            f"det(H)={p.hessian_det:.6f} | тип={point_type_ru}"
        )

    lines.append("")
    lines.append("ДЗ2.3 - Объектная модель")
    lines.append("- Базовый класс: Optimizer2D")
    lines.append("- Конкретные классы: Coordinate, Gradient, Steepest, Newton")
    lines.append("- Композиция: OptimizationResult содержит историю IterationPoint")

    return "\n".join(lines)


def save_report(text: str, out_file: str) -> None:
    path = Path(out_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
