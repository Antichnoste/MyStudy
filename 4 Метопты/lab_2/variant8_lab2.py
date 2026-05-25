import math
from dataclasses import dataclass
from pathlib import Path
import matplotlib.pyplot as plt

A, B = 1.0, 7.0
EPS = 1e-4
MAX_ITER = 10_000
GRID_POINTS = 4000

@dataclass
class MethodPoint:
    interval_id: int
    left: float
    right: float
    method: str
    x: float
    fx: float
    dfx_abs: float
    kind: str
    iters: int


def f(x: float) -> float:
    return math.sin(x) * (1.0 + 0.3 * math.sin(10.0 * x))


def df(x: float) -> float:
    return math.cos(x) * (1.0 + 0.3 * math.sin(10.0 * x)) + 3.0 * math.sin(x) * math.cos(10.0 * x)


def d2f(x: float) -> float:
    return (
        -math.sin(x) * (1.0 + 0.3 * math.sin(10.0 * x))
        + 6.0 * math.cos(x) * math.cos(10.0 * x)
        - 30.0 * math.sin(x) * math.sin(10.0 * x)
    )


def sign(x: float) -> int:
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def classify_extremum(x: float) -> str:
    second = d2f(x)
    if second > 0:
        return "минимум"
    if second < 0:
        return "максимум"
    return "не определён"


def find_sign_change_intervals(func, left: float, right: float, grid_points: int = GRID_POINTS):
    xs = [left + (right - left) * i / grid_points for i in range(grid_points + 1)]
    vals = [func(x) for x in xs]

    intervals = []
    h = (right - left) / grid_points

    for i in range(grid_points):
        x1, x2 = xs[i], xs[i + 1]
        y1, y2 = vals[i], vals[i + 1]

        if y1 == 0.0:
            intervals.append((max(left, x1 - h), min(right, x1 + h)))
        elif y1 * y2 < 0.0:
            intervals.append((x1, x2))

    merged = []
    for l, r in intervals:
        if not merged:
            merged.append([l, r])
            continue
        if l <= merged[-1][1] + 1e-12:
            merged[-1][1] = max(merged[-1][1], r)
        else:
            merged.append([l, r])

    return [(l, r) for l, r in merged]

# Метод середин
def bisection_root(func, left: float, right: float, tol: float = EPS):
    fl = func(left)
    fr = func(right)

    if fl == 0:
        return left, 0
    if fr == 0:
        return right, 0
    if fl * fr > 0:
        raise ValueError()

    l, r = left, right
    for i in range(1, MAX_ITER + 1):
        mid = (l + r) / 2.0
        fm = func(mid)

        if abs(fm) < tol or (r - l) / 2.0 < tol:
            return mid, i

        eps_shift = max(tol * 0.1, 1e-12)
        left_probe = max(l, mid - eps_shift)
        right_probe = min(r, mid + eps_shift)

        f_left_probe = func(left_probe)
        f_right_probe = func(right_probe)

        if (f_left_probe < f_right_probe):
            l = left_probe
        else:
            r = right_probe

    return (l + r) / 2.0, MAX_ITER

# Метод хорд
def secant_root(func, x0: float, x1: float, tol: float = EPS):
    # a = x0, b = x1, x = x2
    f0 = func(x0)
    f1 = func(x1)

    for i in range(1, MAX_ITER + 1):
        denom = f1 - f0
        if abs(denom) < 1e-16:
            return x1, i

        x2 = x1 - f1 * (x1 - x0) / denom

        if abs(x2 - x1) < tol and abs(func(x2)) < 1e-8:
            return x2, i
        
        if func(x2) * func(x0) > 0:
            # a одного знака с x
            x0 = x2         # a = x
            f0 = func(x2)
        else:
            # b одного знака с x
            x1 = x2         # b = x
            f1 = func(x2)

    return x1, MAX_ITER

# Метод ньютона
def newton_root(func, dfunc, x0: float, left: float, right: float, tol: float = EPS):
    x = x0

    for i in range(1, MAX_ITER + 1):
        fx = func(x)
        dfx = dfunc(x)

        if abs(dfx) < 1e-16:
            x = (left + right) / 2.0
            continue

        x_next = x - fx / dfx

        if not (left <= x_next <= right):
            x_next = (left + right) / 2.0

        if abs(x_next - x) < tol and abs(func(x_next)) < 1e-8:
            return x_next, i

        x = x_next

    return x, MAX_ITER

# Метод золотого сечения
def golden_section_extremum(func, left: float, right: float, is_maximum: bool, tol: float = EPS):
    phi = (1.0 + math.sqrt(5.0)) / 2.0 # 1 / phi = 0.6... и (1 - 1 / phi) = 0.3
    l, r = left, right

    target = (lambda x: -func(x)) if is_maximum else func

    x1 = l + (r - l) * (1 / phi)
    x2 = l + (r - l) * (1 - 1 / phi)
    f1 = target(x1)
    f2 = target(x2)

    for i in range(1, MAX_ITER + 1):
        if abs(r - l) < tol:
            return (l + r) / 2.0, i

        if f1 <= f2:
            r = x2
            x2 = x1
            f2 = f1
            x1 = r - (r - l) / phi
            f1 = target(x1)
        else:
            l = x1
            x1 = x2
            f1 = f2
            x2 = l + (r - l) / phi
            f2 = target(x2)

    return (l + r) / 2.0, MAX_ITER


def deduplicate_points(points, tol=1e-5):
    ordered = sorted(points)
    if not ordered:
        return []

    unique = [ordered[0]]
    for p in ordered[1:]:
        if abs(p - unique[-1]) > tol:
            unique.append(p)
    return unique


def bisection_first_iterations(func, left: float, right: float, steps: int = 4):
    result = []
    l, r = left, right
    fl = func(l)

    for i in range(1, steps + 1):
        mid = (l + r) / 2.0
        fm = func(mid)
        result.append((i, l, r, mid, fm))

        eps_shift = max(EPS * 0.1, 1e-12)
        left_probe = max(l, mid - eps_shift)
        right_probe = min(r, mid + eps_shift)

        f_left_probe = func(left_probe)
        if fl * f_left_probe <= 0:
            r = left_probe
        else:
            l = right_probe
            fl = func(l)

    return result


def secant_first_iterations(func, x0: float, x1: float, steps: int = 4):
    result = []
    f0 = func(x0)
    f1 = func(x1)

    for i in range(1, steps + 1):
        denom = f1 - f0
        if abs(denom) < 1e-16:
            result.append((i, x0, x1, x1, f1))
            break

        x2 = x1 - f1 * (x1 - x0) / denom
        f2 = func(x2)
        result.append((i, x0, x1, x2, f2))

        x0, x1 = x1, x2
        f0, f1 = f1, f2

    return result


def newton_first_iterations(func, dfunc, x0: float, left: float, right: float, steps: int = 4):
    result = []
    x = x0

    for i in range(1, steps + 1):
        fx = func(x)
        dfx = dfunc(x)

        if abs(dfx) < 1e-16:
            x_next = (left + right) / 2.0
        else:
            x_next = x - fx / dfx
            if not (left <= x_next <= right):
                x_next = (left + right) / 2.0

        result.append((i, x, fx, dfx, x_next, func(x_next)))
        x = x_next

    return result


def golden_first_iterations(func, left: float, right: float, is_maximum: bool, steps: int = 4):
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    target = (lambda x: -func(x)) if is_maximum else func
    l, r = left, right

    x1 = r - (r - l) / phi
    x2 = l + (r - l) / phi
    f1 = target(x1)
    f2 = target(x2)

    result = []
    for i in range(1, steps + 1):
        center = (l + r) / 2.0
        result.append((i, l, r, x1, x2, center, func(center)))

        if f1 <= f2:
            r = x2
            x2 = x1
            f2 = f1
            x1 = r - (r - l) / phi
            f1 = target(x1)
        else:
            l = x1
            x1 = x2
            f1 = f2
            x2 = l + (r - l) / phi
            f2 = target(x2)

    return result


def format_header(title: str) -> str:
    return f"\n{'=' * 92}\n{title}\n{'=' * 92}"


def calculate_method_rows():
    intervals = find_sign_change_intervals(df, A, B)

    if not intervals:
        return intervals, []

    rows: list[MethodPoint] = []

    for idx, (l, r) in enumerate(intervals, 1):
        x_bis, it_bis = bisection_root(df, l, r)
        x_sec, it_sec = secant_root(df, l, r)
        x_new, it_new = newton_root(df, d2f, (l + r) / 2.0, l, r)

        left_sign = sign(df(l))
        right_sign = sign(df(r))
        is_max = left_sign > 0 and right_sign < 0
        x_gold, it_gold = golden_section_extremum(f, l, r, is_maximum=is_max)

        method_points = [
            ("Половинное деление", x_bis, it_bis),
            ("Хорд (секущих)", x_sec, it_sec),
            ("Ньютона", x_new, it_new),
            ("Золотого сечения", x_gold, it_gold),
        ]

        for method_name, x, n_iter in method_points:
            rows.append(
                MethodPoint(
                    interval_id=idx,
                    left=l,
                    right=r,
                    method=method_name,
                    x=x,
                    fx=f(x),
                    dfx_abs=abs(df(x)),
                    kind=classify_extremum(x),
                    iters=n_iter,
                )
            )

    return intervals, rows


def build_report(intervals, rows: list[MethodPoint]) -> str:
    lines = []

    lines.append(format_header("ЛАБОРАТОРНАЯ 2 — ВАРИАНТ 8 (ВЕРСИЯ ДЛЯ ЗАЩИТЫ)"))
    lines.append("f(x) = sin(x) * (1 + 0.3*sin(10x)),  x ∈ [1, 7]")
    lines.append("Ищем все экстремумы через 4 метода: половинного деления, хорд, Ньютона, золотого сечения.")
    lines.append("Классификация: по знаку второй производной f''(x): >0 минимум, <0 максимум.")

    if not intervals:
        lines.append("\nНа сетке не найдены интервалы со сменой знака f'(x).")
        return "\n".join(lines)

    lines.append(format_header("1) ИНТЕРВАЛЫ СМЕНЫ ЗНАКА f'(x)"))
    for i, (l, r) in enumerate(intervals, 1):
        lines.append(f"{i:2d}) [{l:.6f}, {r:.6f}]")

    methods_order = [
        "Половинное деление",
        "Хорд (секущих)",
        "Ньютона",
        "Золотого сечения",
    ]

    lines.append(format_header("2) ТАБЛИЦА РЕЗУЛЬТАТОВ"))
    lines.append(
        "№  | Метод               | x*       | f(x*)    | |f'(x*)|   | Тип        | Итераций"
    )
    lines.append("-" * 92)

    for row in rows:
        lines.append(
            f"{row.interval_id:2d} | {row.method:<19} | {row.x:8.4f} | {row.fx:8.4f} | {row.dfx_abs:10.2e} | {row.kind:<10} | {row.iters:8d}"
        )

    lines.append(format_header("3) СВОДКА ПО КАЖДОМУ МЕТОДУ"))
    for method in methods_order:
        method_x = [r.x for r in rows if r.method == method]
        unique_x = deduplicate_points(method_x, tol=1e-5)

        min_count = sum(1 for x in unique_x if classify_extremum(x) == "минимум")
        max_count = sum(1 for x in unique_x if classify_extremum(x) == "максимум")

        lines.append(f"{method}: экстремумов = {len(unique_x)}, минимумов = {min_count}, максимумов = {max_count}")

    lines.append(format_header("4) ОКРУГЛЁННЫЕ ТОЧКИ (ДЛЯ СДАЧИ, 4 ЗНАКА)"))
    lines.append("(по методу Ньютона — как наиболее быстрый в этой задаче)")

    newton_rows = [r for r in rows if r.method == "Ньютона"]
    for r in newton_rows:
        lines.append(f"{r.interval_id:2d}) x = {r.x:.4f}, f(x) = {r.fx:.4f}, тип: {r.kind}")

    lines.append(format_header("5) ПЕРВЫЕ 4 ИТЕРАЦИИ ДЛЯ 3-ГО ИНТЕРВАЛА (ВСЕ МЕТОДЫ)"))
    if len(intervals) < 3:
        lines.append("Третий интервал отсутствует.")
        return "\n".join(lines)

    l3, r3 = intervals[2]
    lines.append(f"3-й интервал: [{l3:.6f}, {r3:.6f}]")

    lines.append("\nМетод половинного деления:")
    for i, l, r, mid, fmid in bisection_first_iterations(df, l3, r3, steps=4):
        lines.append(f"итерация {i}: l={l:.6f}, r={r:.6f}, mid={mid:.6f}, f'(mid)={fmid:.6e}")

    lines.append("\nМетод хорд (секущих):")
    for i, x0, x1, x2, f2 in secant_first_iterations(df, l3, r3, steps=4):
        lines.append(f"итерация {i}: x0={x0:.6f}, x1={x1:.6f}, x2={x2:.6f}, f'(x2)={f2:.6e}")

    lines.append("\nМетод Ньютона:")
    start = (l3 + r3) / 2.0
    for i, x, fx, dfx, x_next, f_next in newton_first_iterations(df, d2f, start, l3, r3, steps=4):
        lines.append(
            f"итерация {i}: x={x:.6f}, f'(x)={fx:.6e}, f''(x)={dfx:.6e}, x_next={x_next:.6f}, f'(x_next)={f_next:.6e}"
        )

    lines.append("\nМетод золотого сечения:")
    left_sign = sign(df(l3))
    right_sign = sign(df(r3))
    is_max = left_sign > 0 and right_sign < 0
    for i, l, r, x1, x2, center, fcenter in golden_first_iterations(f, l3, r3, is_maximum=is_max, steps=4):
        lines.append(
            f"итерация {i}: l={l:.6f}, r={r:.6f}, x1={x1:.6f}, x2={x2:.6f}, center={center:.6f}, f(center)={fcenter:.6f}"
        )

    return "\n".join(lines)


def save_extrema_plot(rows: list[MethodPoint], output_path: Path):
    newton_rows = [r for r in rows if r.method == "Ньютона"]
    x_unique = deduplicate_points([r.x for r in newton_rows], tol=1e-5)

    minima_x = [x for x in x_unique if classify_extremum(x) == "минимум"]
    maxima_x = [x for x in x_unique if classify_extremum(x) == "максимум"]

    graph_points = 2500
    xs = [A + (B - A) * i / graph_points for i in range(graph_points + 1)]
    ys = [f(x) for x in xs]

    plt.figure(figsize=(11, 6))
    plt.plot(xs, ys, label="f(x)", linewidth=2)

    if minima_x:
        plt.scatter(minima_x, [f(x) for x in minima_x], color="red", s=45, label="Минимумы", zorder=3)
    if maxima_x:
        plt.scatter(maxima_x, [f(x) for x in maxima_x], color="green", s=45, label="Максимумы", zorder=3)

    plt.title("Вариант 8: график функции и точки экстремумов")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()



intervals, rows = calculate_method_rows()
report = build_report(intervals, rows)

out_file = Path(__file__).with_name("variant8_lab2  .txt")
out_file.write_text(report, encoding="utf-8")

plot_file = Path(__file__).with_name("variant8_lab2_extrema_plot.png")
if rows:
    save_extrema_plot(rows, plot_file)
    print(f"\nГрафик сохранён: {plot_file}")

print(f"Отчёт сохранён: {out_file}")