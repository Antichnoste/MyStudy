from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
import matplotlib.pyplot as plt
import numpy as np

EPS1_DEFAULT = 1e-4
EPS2_DEFAULT = 1e-4
MAX_ITER_DEFAULT = 200


@dataclass
class IterationRecord:
    it: int
    x1: float
    x2: float
    x3: float
    f1: float
    f2: float
    f3: float
    xmin: float
    fmin: float
    xbar: float | None
    fbar: float | None
    rel_f: float | None
    rel_x: float | None
    denominator: float
    action: str


@dataclass
class QuadraticApproxResult:
    x_star: float
    f_star: float
    converged: bool
    iterations: int
    records: list[IterationRecord]


def quadratic_approximation(
    f: Callable[[float], float],
    a: float,
    b: float,
    x1: float | None = None,
    dx: float | None = None,
    eps1: float = EPS1_DEFAULT,
    eps2: float = EPS2_DEFAULT,
    max_iter: int = MAX_ITER_DEFAULT,
) -> QuadraticApproxResult:

    # Шаг 1: задать начальную точку и шаг
    x1_cur = (a + b) / 2.0 if x1 is None else x1
    step   = (b - a) / 8.0  if dx is None  else dx

    records: list[IterationRecord] = []
    rebuild = True
    x1v = x2v = x3v = 0.0
    f1  = f2  = f3  = 0.0
    x_best, f_best = x1_cur, f(x1_cur)

    for it in range(1, max_iter + 1):

        # Шаг 2: x2 = x1 + Δx
        x1v, x2v = x1_cur, x1_cur + step
        # Шаг 3: f1, f2
        f1,  f2  = f(x1v), f(x2v)

        # Шаг 4: выбор x3
        if f1 > f2:
            x3v = x1v + 2.0 * step   # случай а
        else:
            x3v = x1v - step          # случай б

        # Шаг 5: f(x3)
        f3 = f(x3v)

        # Шаг 6: F_min = min{f1, f2, f3}
        (sx1, sf1), (sx2, sf2), (sx3, sf3) = sorted(
            [(x1v, f1), (x2v, f2), (x3v, f3)], key=lambda p: p[0]
        )
        xmin, fmin = min([(x1v, f1), (x2v, f2), (x3v, f3)], key=lambda p: p[1])

        if fmin < f_best:
            x_best, f_best = xmin, fmin

        # Шаг 7: x̄ — вершина параболы
        denom = (sx2 - sx3)*sf1 + (sx3 - sx1)*sf2 + (sx1 - sx2)*sf3
        if abs(denom) < 1e-14:
            # знаменатель ноль → результат итерации прямая, x1 = x_min, шаг 2
            records.append(IterationRecord(
                it=it, x1=sx1, x2=sx2, x3=sx3,
                f1=sf1, f2=sf2, f3=sf3,
                xmin=xmin, fmin=fmin,
                xbar=None, fbar=None, rel_f=None, rel_x=None,
                denominator=denom, action="denom=0 → x1=xmin, шаг 2",
            ))
            x1_cur, rebuild = xmin, True
            continue

        numer = (sx2**2 - sx3**2)*sf1 + (sx3**2 - sx1**2)*sf2 + (sx1**2 - sx2**2)*sf3
        xbar  = 0.5 * numer / denom
        fbar  = f(xbar)

        if fbar < f_best:
            x_best, f_best = xbar, fbar

        # Шаг 8: проверка критериев останова
        rel_f = abs(fmin - fbar) / max(abs(fbar), 1e-12)
        rel_x = abs(xmin - xbar) / max(abs(xbar), 1e-12)

        if rel_f < eps1 and rel_x < eps2:
            # а) оба выполнены → x* = x̄
            records.append(IterationRecord(
                it=it, x1=sx1, x2=sx2, x3=sx3,
                f1=sf1, f2=sf2, f3=sf3,
                xmin=xmin, fmin=fmin,
                xbar=xbar, fbar=fbar, rel_f=rel_f, rel_x=rel_x,
                denominator=denom, action="сходимость → x*=x̄",
            ))
            return QuadraticApproxResult(x_star=xbar, f_star=fbar, converged=True, iterations=it, records=records)

        if sx1 <= xbar <= sx3:
            # б) x̄ ∈ [x1, x3]: выбрать лучшую точку, взять двух соседей, шаг 6
            bx = xmin if fmin <= fbar else xbar
            bf = fmin if fmin <= fbar else fbar
            all_pts = sorted([(sx1, sf1), (sx2, sf2), (sx3, sf3), (xbar, fbar)], key=lambda p: p[0])
            left_of  = [(x, fx) for x, fx in all_pts if x < bx - 1e-14]
            right_of = [(x, fx) for x, fx in all_pts if x > bx + 1e-14]
            x1v, f1 = left_of[-1]
            x2v, f2 = bx, bf
            x3v, f3 = right_of[0]
            rebuild  = False
            action   = "x̄ ∈ [x1,x3] → новая тройка, шаг 6"
        else:
            # в) x̄ ∉ [x1, x3]: x1 = x̄, шаг 2
            x1_cur, rebuild = xbar, True
            action = "x̄ ∉ [x1,x3] → x1=x̄, шаг 2"

        records.append(IterationRecord(
            it=it, x1=sx1, x2=sx2, x3=sx3,
            f1=sf1, f2=sf2, f3=sf3,
            xmin=xmin, fmin=fmin,
            xbar=xbar, fbar=fbar, rel_f=rel_f, rel_x=rel_x,
            denominator=denom, action=action,
        ))

    return QuadraticApproxResult(x_star=x_best, f_star=f_best, converged=False, iterations=max_iter, records=records)


def build_report(
    result: QuadraticApproxResult,
    a: float,
    b: float,
    eps1: float,
    eps2: float,
    max_iter: int,
) -> str:
    lines: list[str] = []
    lines.append(f"Interval: [{a:.10g}, {b:.10g}]")
    lines.append(f"eps1={eps1:.3e}, eps2={eps2:.3e}, max_iter={max_iter}")
    lines.append("-" * 132)
    lines.append(
        "it  x1           x2           x3           xmin         fmin         xbar         fbar         rel_f      rel_x      action"
    )
    lines.append("-" * 132)

    for r in result.records:
        xbar_text = f"{r.xbar: .8f}" if r.xbar is not None else "    None  "
        fbar_text = f"{r.fbar: .8f}" if r.fbar is not None else "    None  "
        rel_f_text = f"{r.rel_f: .2e}" if r.rel_f is not None else "   None "
        rel_x_text = f"{r.rel_x: .2e}" if r.rel_x is not None else "   None "

        lines.append(
            f"{r.it:>2d} "
            f"{r.x1: .8f} "
            f"{r.x2: .8f} "
            f"{r.x3: .8f} "
            f"{r.xmin: .8f} "
            f"{r.fmin: .8f} "
            f"{xbar_text} "
            f"{fbar_text} "
            f"{rel_f_text} "
            f"{rel_x_text} "
            f"{r.action}"
        )

    lines.append("-" * 132)
    lines.append(f"Converged: {result.converged}")
    lines.append(f"Iterations: {result.iterations}")
    lines.append(f"x* = {result.x_star:.12g}")
    lines.append(f"f(x*) = {result.f_star:.12g}")
    return "\n".join(lines)


def user_function(x: float) -> float:
    return 1 / x + math.exp(x)


def main() -> None:
    a = 0.5
    b = 1.5
    eps1 = 1e-4
    eps2 = 1e-4
    max_iter = 200

    x1 = (a + b) / 2.0
    dx = (b - a) / 8.0

    result = quadratic_approximation(
        f=user_function,
        a=a,
        b=b,
        x1=x1,
        dx=dx,
        eps1=eps1,
        eps2=eps2,
        max_iter=max_iter,
    )

    report_text = build_report(result, a=a, b=b, eps1=eps1, eps2=eps2, max_iter=max_iter)
    report_path = Path(__file__).with_name("quadratic_approx_report.txt")
    report_path.write_text(report_text, encoding="utf-8")

    print(f"x* = {result.x_star:.12g}")
    print(f"f(x*) = {result.f_star:.12g}")
    print(f"Converged: {result.converged}, iterations: {result.iterations}")
    print(f"Report written to: {report_path}")

    # Строим график по точкам последней итерации
    last = result.records[-1]
    plot_path = Path(__file__).with_name("quadratic_approx_plot.png")
    plot_func_and_parabola(
        f=user_function,
        x1=last.x1, x2=last.x2, x3=last.x3,
        f1=last.f1, f2=last.f2, f3=last.f3,
        a=a, b=b,
        filename=plot_path,
    )
    print(f"Plot saved to: {plot_path}")


def plot_func_and_parabola(f, x1, x2, x3, f1, f2, f3, a, b, filename):
    """
    Рисует график функции f(x) и параболы, проходящей через (x1, f1), (x2, f2), (x3, f3)
    на отрезке [a, b].
    """
    xs = np.linspace(a, b, 500)
    ys = [f(x) for x in xs]

    # Коэффициенты параболы q(x) = A x^2 + B x + C
    mat = np.array([
        [x1**2, x1, 1],
        [x2**2, x2, 1],
        [x3**2, x3, 1],
    ])
    vec = np.array([f1, f2, f3])
    A, B, C = np.linalg.solve(mat, vec)
    parabola = lambda x: A * x**2 + B * x + C
    yq = [parabola(x) for x in xs]

    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, label="f(x)", color="blue")
    plt.plot(xs, yq, label="Парабола интерполяции", color="orange", linestyle="--")
    plt.scatter([x1, x2, x3], [f1, f2, f3], color="red", zorder=5, label="Точки интерполяции")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("График функции и параболы интерполяции")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

if __name__ == "__main__":
    main()
