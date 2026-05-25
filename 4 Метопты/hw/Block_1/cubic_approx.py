from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np


EPS1_DEFAULT = 1e-4
EPS2_DEFAULT = 1e-4
MAX_ITER_DEFAULT = 200
ROOT_TOL = 1e-12


@dataclass
class IterationRecord:
    it: int
    a: float
    b: float
    delta: float
    y0: float
    y1: float
    dy0: float
    dy1: float
    A: float
    B: float
    C: float
    D: float
    alpha3: float
    alpha2: float
    alpha1: float
    alpha0: float
    discriminant: float
    xm: float
    fxm: float
    dfxm: float
    action: str


@dataclass
class CubicApproxResult:
    x_star: float
    f_star: float
    df_star: float
    converged: bool
    iterations: int
    records: list[IterationRecord]


def hermite_coefficients(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    x1: float,
) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float]:
    """
    Строит коэффициенты кубического многочлена Эрмита на [x0, x1]
    ровно по формулам из методички.
    """
    y0 = f(x0)
    y1 = f(x1)
    dy0 = df(x0)
    dy1 = df(x1)

    delta = x1 - x0
    if abs(delta) < ROOT_TOL:
        raise ValueError("x1 and x0 are too close")

    # Шаг 2: A, B, C, D.
    A = y0
    B = dy0 + 2.0 * y0 / delta
    C = y1
    D = -dy1 + 2.0 * y1 / delta

    # Шаг 4: коэффициенты H(x) = alpha3*x^3 + alpha2*x^2 + alpha1*x + alpha0.
    alpha3 = B - D
    alpha2 = (A - B * x0 - 2.0 * B * x1) + (C + D * x1 + 2.0 * D * x0)
    alpha1 = (-2.0 * A + 2.0 * B * x0 + B * x1) * x1 + (-2.0 * C - 2.0 * D * x1 - D * x0) * x0
    alpha0 = (A - B * x0) * x1**2 + (C + D * x1) * x0**2

    return y0, y1, dy0, dy1, A, B, C, D, alpha3, alpha2, alpha1, alpha0


def cubic_value(alpha3: float, alpha2: float, alpha1: float, alpha0: float, x: float) -> float:
    return ((alpha3 * x + alpha2) * x + alpha1) * x + alpha0


def choose_xm(
    alpha3: float,
    alpha2: float,
    alpha1: float,
    alpha0: float,
    x0: float,
    x1: float,
) -> tuple[float, float]:
    """
    Шаг 5: ищем xmin многочлена H(x) по формуле
    x = (-alpha2 ± sqrt(alpha2^2 - 3*alpha1*alpha3)) / (3*alpha3),
    затем выбираем корень внутри [x0, x1].
    """
    left, right = min(x0, x1), max(x0, x1)

    if abs(alpha3) < ROOT_TOL:
        # Производная H' вырождается в линейную: 2*alpha2*x + alpha1 = 0.
        if abs(alpha2) < ROOT_TOL:
            return 0.5 * (left + right), -1.0
        x_lin = -alpha1 / (2.0 * alpha2)
        return min(max(x_lin, left), right), -1.0

    discriminant = alpha2 * alpha2 - 3.0 * alpha1 * alpha3
    if discriminant < 0.0:
        # Нет вещественных стационарных точек у H': берём середину интервала.
        return 0.5 * (left + right), discriminant

    sqrt_disc = math.sqrt(discriminant)
    x_candidate_1 = (-alpha2 - sqrt_disc) / (3.0 * alpha3)
    x_candidate_2 = (-alpha2 + sqrt_disc) / (3.0 * alpha3)

    candidates = [x for x in (x_candidate_1, x_candidate_2) if left - 1e-12 <= x <= right + 1e-12]

    if not candidates:
        # Если по численным причинам оба корня вне интервала, берём ближайший к середине.
        mid = 0.5 * (left + right)
        nearest = min((x_candidate_1, x_candidate_2), key=lambda x: abs(x - mid))
        return min(max(nearest, left), right), discriminant

    # Если в интервал попали оба корня, выбираем тот, где H(x) меньше.
    xm = min(candidates, key=lambda x: cubic_value(alpha3, alpha2, alpha1, alpha0, x))
    return xm, discriminant


def cubic_approximation(
    f: Callable[[float], float],
    df: Callable[[float], float],
    a: float,
    b: float,
    eps1: float = EPS1_DEFAULT,
    eps2: float = EPS2_DEFAULT,
    max_iter: int = MAX_ITER_DEFAULT,
) -> CubicApproxResult:
    """
    Метод кубической аппроксимации по схеме с фото:
    1) строим H(x) Эрмита на [a, b] по f(a), f(b), f'(a), f'(b);
    2) находим xm как стационарную точку H;
    3) обновляем [a, b] по знаку f'(xm);
    4) продолжаем, пока одновременно delta >= eps1 и |f'(xm)| >= eps2.
    """
    if a >= b:
        raise ValueError("Expected a < b")

    a_cur = float(a)
    b_cur = float(b)
    records: list[IterationRecord] = []

    x_best = 0.5 * (a_cur + b_cur)
    f_best = f(x_best)
    df_best = df(x_best)

    for it in range(1, max_iter + 1):
        # Шаг 1-4: коэффициенты Эрмита и кубического полинома H(x).
        y0, y1, dy0, dy1, A, B, C, D, alpha3, alpha2, alpha1, alpha0 = hermite_coefficients(
            f=f,
            df=df,
            x0=a_cur,
            x1=b_cur,
        )

        # Шаг 5: кандидат минимума кубики на текущем интервале.
        xm, disc = choose_xm(alpha3, alpha2, alpha1, alpha0, a_cur, b_cur)
        fxm = f(xm)
        dfxm = df(xm)

        if fxm < f_best:
            x_best, f_best, df_best = xm, fxm, dfxm

        # Знак f'(xm) определяет, какую границу двигаем.
        if dfxm < 0.0:
            a_new, b_new = xm, b_cur
            action = "f'(xm) < 0 -> a = xm"
        elif dfxm > 0.0:
            a_new, b_new = a_cur, xm
            action = "f'(xm) > 0 -> b = xm"
        else:
            a_new, b_new = a_cur, b_cur
            action = "f'(xm) = 0 -> точный стационарный минимум"

        delta_new = b_new - a_new

        records.append(
            IterationRecord(
                it=it,
                a=a_cur,
                b=b_cur,
                delta=b_cur - a_cur,
                y0=y0,
                y1=y1,
                dy0=dy0,
                dy1=dy1,
                A=A,
                B=B,
                C=C,
                D=D,
                alpha3=alpha3,
                alpha2=alpha2,
                alpha1=alpha1,
                alpha0=alpha0,
                discriminant=disc,
                xm=xm,
                fxm=fxm,
                dfxm=dfxm,
                action=action,
            )
        )

        # Критерий остановки из примера: процесс идет, пока
        # delta >= eps1 И |f'(xm)| >= eps2.
        # Значит останавливаемся, когда хотя бы одно условие нарушено.
        if not (delta_new >= eps1 and abs(dfxm) >= eps2):
            return CubicApproxResult(
                x_star=xm,
                f_star=fxm,
                df_star=dfxm,
                converged=True,
                iterations=it,
                records=records,
            )

        a_cur, b_cur = a_new, b_new

    return CubicApproxResult(
        x_star=x_best,
        f_star=f_best,
        df_star=df_best,
        converged=False,
        iterations=len(records),
        records=records,
    )


def build_report(
    result: CubicApproxResult,
    a: float,
    b: float,
    eps1: float,
    eps2: float,
    max_iter: int,
) -> str:
    lines: list[str] = []
    lines.append("=" * 160)
    lines.append("ОТЧЕТ: Метод кубической аппроксимации (многочлен Эрмита)")
    lines.append(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("Функция: f(x)=1/x + exp(x)")
    lines.append(f"Стартовый интервал: [{a:.10g}, {b:.10g}]")
    lines.append(f"Критерий: delta < eps1 ИЛИ |f'(xm)| < eps2")
    lines.append(f"eps1={eps1:.3e}, eps2={eps2:.3e}, max_iter={max_iter}")
    lines.append("=" * 160)
    lines.append(
        "it  a            b            delta        xm           f(xm)        f'(xm)       alpha3       alpha2       alpha1       discr        action"
    )
    lines.append("-" * 160)

    for r in result.records:
        lines.append(
            f"{r.it:>2d} "
            f"{r.a: .8f} "
            f"{r.b: .8f} "
            f"{r.delta: .3e} "
            f"{r.xm: .8f} "
            f"{r.fxm: .8f} "
            f"{r.dfxm: .3e} "
            f"{r.alpha3: .3e} "
            f"{r.alpha2: .3e} "
            f"{r.alpha1: .3e} "
            f"{r.discriminant: .3e} "
            f"{r.action}"
        )

    lines.append("-" * 160)
    lines.append(f"Converged: {result.converged}")
    lines.append(f"Iterations: {result.iterations}")
    lines.append(f"x* = {result.x_star:.12g}")
    lines.append(f"f(x*) = {result.f_star:.12g}")
    lines.append(f"f'(x*) = {result.df_star:.12g}")
    return "\n".join(lines)


def user_function(x: float) -> float:
    return 1.0 / x + math.exp(x)


def user_derivative(x: float) -> float:
    return -1.0 / (x * x) + math.exp(x)


def plot_func_and_hermite(
    f: Callable[[float], float],
    record: IterationRecord,
    global_a: float,
    global_b: float,
    filename: Path,
) -> None:
    """Рисует f(x) и кубический Эрмитов многочлен текущей итерации."""
    grid = np.linspace(global_a, global_b, 500)
    values = [f(x) for x in grid]

    hermite_values = [
        cubic_value(record.alpha3, record.alpha2, record.alpha1, record.alpha0, x)
        for x in grid
    ]

    plt.figure(figsize=(9, 5))
    plt.plot(grid, values, label="f(x)", color="blue")
    plt.plot(grid, hermite_values, label="H(x)", color="orange", linestyle="--")
    plt.scatter([record.a, record.b], [record.y0, record.y1], color="red", zorder=5, label="Границы интервала")
    plt.scatter([record.xm], [record.fxm], color="green", zorder=6, label="xm")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Кубическая аппроксимация, итерация {record.it}")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


def main() -> None:
    a = 0.5
    b = 1.5
    eps1 = EPS1_DEFAULT
    eps2 = EPS2_DEFAULT
    max_iter = MAX_ITER_DEFAULT

    result = cubic_approximation(
        f=user_function,
        df=user_derivative,
        a=a,
        b=b,
        eps1=eps1,
        eps2=eps2,
        max_iter=max_iter,
    )

    report_text = build_report(result, a=a, b=b, eps1=eps1, eps2=eps2, max_iter=max_iter)
    report_path = Path(__file__).with_name("cubic_approx_report.txt")
    report_path.write_text(report_text, encoding="utf-8")

    print(f"x* = {result.x_star:.12g}")
    print(f"f(x*) = {result.f_star:.12g}")
    print(f"f'(x*) = {result.df_star:.12g}")
    print(f"Converged: {result.converged}, iterations: {result.iterations}")
    print(f"Report written to: {report_path}")

    if result.records:
        plot_indices = sorted({0, len(result.records) // 2, len(result.records) - 1})
        for idx in plot_indices:
            record = result.records[idx]
            plot_path = Path(__file__).with_name(f"cubic_approx_iter_{record.it}.png")
            plot_func_and_hermite(
                f=user_function,
                record=record,
                global_a=a,
                global_b=b,
                filename=plot_path,
            )
            print(f"График итерации сохранен в: {plot_path}")


if __name__ == "__main__":
    main()
