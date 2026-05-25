import math
from datetime import datetime


# ============================================================
# Вариант 8
# f(x1, x2) = 5*x1^2 + 3*x1*x2 + 5*x2^2 - 14*x1 + 14*x2 + 28
# Начальная точка: (-3, 1), epsilon = 0.0001
# ============================================================

# --- Целевая функция ---
def f(x1, x2):
    return 5*x1**2 + 3*x1*x2 + 5*x2**2 - 14*x1 + 14*x2 + 28


# --- Частные производные (аналитические) ---
# df/dx1 = 10*x1 + 3*x2 - 14
# df/dx2 = 3*x1 + 10*x2 + 14
def df_dx1(x1, x2):
    return 10*x1 + 3*x2 - 14


def df_dx2(x1, x2):
    return 3*x1 + 10*x2 + 14


# --- Модуль градиента ---
def grad_norm(x1, x2):
    g1 = df_dx1(x1, x2)
    g2 = df_dx2(x1, x2)
    return math.sqrt(g1**2 + g2**2)


# --- Метод половинного деления (деление отрезка пополам) ---
def bisection_min(phi, a, b, eps):
    """
    Находит минимум унимодальной функции phi на отрезке [a, b]
    методом деления отрезка пополам с точностью eps.
    """
    while b - a > 2 * eps:
        x1 = (a + b - eps) / 2
        x2 = (a + b + eps) / 2
        if phi(x1) > phi(x2):
            a = x1
        else:
            b = x2
    return (a + b) / 2


# --- Евклидово расстояние между двумя точками ---
def distance(x1, x2, y1, y2):
    return math.sqrt((x1 - y1)**2 + (x2 - y2)**2)


# ============================================================
# 1. МЕТОД ПОКООРДИНАТНОГО СПУСКА
# ============================================================
def coordinate_descent(x1_0, x2_0, eps=0.0001, max_iter=10000):
    """
    Метод покоординатного спуска.
    На каждом цикле поочередно минимизируем по x1 (при фиксированном x2),
    затем по x2 (при фиксированном x1).
    Минимум по каждой переменной находим методом половинного деления.
    Критерий останова: |f(x^k+1) - f(x^k)| <= eps или ||x^(k+1) - x^(k)|| <= eps
    """
    history = []
    x1, x2 = x1_0, x2_0
    history.append((x1, x2, f(x1, x2)))

    for k in range(max_iter):
        x1_old, x2_old = x1, x2

        # Шаг 1: Фиксируем x2, минимизируем по x1 методом половинного деления
        phi1 = lambda t: f(t, x2)
        x1 = bisection_min(phi1, -100, 100, eps)
        history.append((x1, x2, f(x1, x2)))

        # Шаг 2: Фиксируем x1, минимизируем по x2 методом половинного деления
        phi2 = lambda t: f(x1, t)
        x2 = bisection_min(phi2, -100, 100, eps)
        history.append((x1, x2, f(x1, x2)))

        # Проверяем критерий останова
        dist = distance(x1, x2, x1_old, x2_old)
        if dist <= eps or abs(f(x1, x2) - f(x1_old, x2_old)) <= eps:
            break

    return x1, x2, f(x1, x2), history, k + 1


# ============================================================
# 2. МЕТОД ГРАДИЕНТНОГО СПУСКА (с постоянным шагом)
# ============================================================
def gradient_descent(x1_0, x2_0, eps=0.0001, step=0.1, max_iter=10000):
    """
    Метод градиентного спуска с постоянным шагом.
    Формула: x^(k+1) = x^(k) - step * grad f(x^(k))
    Если функция увеличивается — шаг делится пополам.
    Критерий останова: |f(x^(k)) - f(x^(k-1))| < eps
    """
    history = []
    x1, x2 = x1_0, x2_0
    f_prev = f(x1, x2)
    history.append((x1, x2, f_prev))

    for k in range(max_iter):
        g1 = df_dx1(x1, x2)
        g2 = df_dx2(x1, x2)

        # Пробуем шаг; если функция увеличивается — делим шаг пополам
        x1_new = x1 - step * g1
        x2_new = x2 - step * g2
        f_new = f(x1_new, x2_new)

        while f_new >= f_prev:
            step = step / 2
            x1_new = x1 - step * g1
            x2_new = x2 - step * g2
            f_new = f(x1_new, x2_new)

        x1, x2 = x1_new, x2_new
        f_curr = f_new
        history.append((x1, x2, f_curr))

        if abs(f_curr - f_prev) < eps:
            break

        f_prev = f_curr

    return x1, x2, f(x1, x2), history, k + 1


# ============================================================
# 3. МЕТОД НАИСКОРЕЙШЕГО СПУСКА
# ============================================================
def steepest_descent(x1_0, x2_0, eps=0.0001, max_iter=10000):
    """
    Метод наискорейшего спуска.
    Направление спуска: антиградиент S = -grad f(x^(k)).
    Оптимальный шаг h находим методом половинного деления.
    Критерий останова: ||grad f(x^(k))|| < eps
    """
    history = []
    x1, x2 = x1_0, x2_0
    history.append((x1, x2, f(x1, x2)))

    for k in range(max_iter):
        g1 = df_dx1(x1, x2)
        g2 = df_dx2(x1, x2)

        gn = math.sqrt(g1**2 + g2**2)
        if gn < eps:
            break

        # Находим оптимальный шаг h методом половинного деления
        # Минимизируем phi(h) = f(x1 - h*g1, x2 - h*g2) на отрезке [0, h_max]
        phi = lambda h: f(x1 - h * g1, x2 - h * g2)
        h_opt = bisection_min(phi, 0, 10, eps)

        x1 = x1 - h_opt * g1
        x2 = x2 - h_opt * g2
        history.append((x1, x2, f(x1, x2)))

    return x1, x2, f(x1, x2), history, k + 1


# ============================================================
# Формирование отчёта
# ============================================================
def generate_report(filename="report.txt"):
    x1_0, x2_0 = -3, 1
    eps = 0.0001

    lines = []
    lines.append("=" * 70)
    lines.append("ОТЧЁТ: Лабораторная работа №4, Вариант 8")
    lines.append(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("Целевая функция: f(x1, x2) = 5*x1^2 + 3*x1*x2 + 5*x2^2 - 14*x1 + 14*x2 + 28")
    lines.append(f"Начальная точка: ({x1_0}, {x2_0})")
    lines.append(f"f(x0) = {f(x1_0, x2_0)}")
    lines.append(f"Критерий останова: eps = {eps}")
    lines.append("")

    # --- 1. Покоординатный спуск ---
    lines.append("-" * 70)
    lines.append("1. МЕТОД ПОКООРДИНАТНОГО СПУСКА")
    lines.append("-" * 70)
    lines.append("Алгоритм:")
    lines.append("  На каждом цикле:")
    lines.append("    1) Фиксируем x2, минимизируем f по x1 методом половинного деления")
    lines.append("    2) Фиксируем x1, минимизируем f по x2 методом половинного деления")
    lines.append("  Критерий останова: ||x^(k+1) - x^(k)|| < eps")
    lines.append("")

    x1, x2, fval, hist, iters = coordinate_descent(x1_0, x2_0, eps)

    lines.append(f"{'Шаг':<6} {'x1':>14} {'x2':>14} {'f(x1,x2)':>14}")
    lines.append("-" * 50)
    for i, (hx1, hx2, hf) in enumerate(hist):
        lines.append(f"{i:<6} {hx1:>14.8f} {hx2:>14.8f} {hf:>14.8f}")
    lines.append("")
    lines.append(f"Количество циклов (итераций): {iters}")
    lines.append(f"Найденный минимум: x* = ({x1:.8f}, {x2:.8f})")
    lines.append(f"f(x*) = {fval:.8f}")
    lines.append(f"||grad f(x*)|| = {grad_norm(x1, x2):.10f}")
    lines.append("")

    # --- 2. Градиентный спуск ---
    step = 0.1
    lines.append("-" * 70)
    lines.append("2. МЕТОД ГРАДИЕНТНОГО СПУСКА (постоянный шаг)")
    lines.append("-" * 70)
    lines.append("Алгоритм:")
    lines.append(f"  x^(k+1) = x^(k) - alpha * grad f(x^(k)), alpha_0 = {step}")
    lines.append("  Если f(x^(k+1)) >= f(x^(k)), то alpha = alpha / 2 (дробление шага)")
    lines.append("  Критерий останова: |f(x^(k)) - f(x^(k-1))| < eps")
    lines.append("")

    x1, x2, fval, hist, iters = gradient_descent(x1_0, x2_0, eps, step)

    lines.append(f"{'Шаг':<6} {'x1':>14} {'x2':>14} {'f(x1,x2)':>14} {'|delta f|':>14}")
    lines.append("-" * 65)
    for i, (hx1, hx2, hf) in enumerate(hist):
        if i == 0:
            df_val = "-"
        else:
            df_val = f"{abs(hf - hist[i-1][2]):>14.8f}"
        lines.append(f"{i:<6} {hx1:>14.8f} {hx2:>14.8f} {hf:>14.8f} {df_val:>14}")
    lines.append("")
    lines.append(f"Количество итераций: {iters}")
    lines.append(f"Найденный минимум: x* = ({x1:.8f}, {x2:.8f})")
    lines.append(f"f(x*) = {fval:.8f}")
    lines.append(f"||grad f(x*)|| = {grad_norm(x1, x2):.10f}")
    lines.append("")

    # --- 3. Наискорейший спуск ---
    lines.append("-" * 70)
    lines.append("3. МЕТОД НАИСКОРЕЙШЕГО СПУСКА")
    lines.append("-" * 70)
    lines.append("Алгоритм:")
    lines.append("  x^(k+1) = x^(k) - h_k * grad f(x^(k))")
    lines.append("  h_k находим методом половинного деления: min phi(h) = f(x - h*grad)")
    lines.append("  Критерий останова: ||grad f(x^(k))|| < eps")
    lines.append("")

    x1, x2, fval, hist, iters = steepest_descent(x1_0, x2_0, eps)

    lines.append(f"{'Шаг':<6} {'x1':>14} {'x2':>14} {'f(x1,x2)':>14} {'||grad||':>14}")
    lines.append("-" * 65)
    for i, (hx1, hx2, hf) in enumerate(hist):
        gn = grad_norm(hx1, hx2)
        lines.append(f"{i:<6} {hx1:>14.8f} {hx2:>14.8f} {hf:>14.8f} {gn:>14.8f}")
    lines.append("")
    lines.append(f"Количество итераций: {iters}")
    lines.append(f"Найденный минимум: x* = ({x1:.8f}, {x2:.8f})")
    lines.append(f"f(x*) = {fval:.8f}")
    lines.append(f"||grad f(x*)|| = {grad_norm(x1, x2):.10f}")
    lines.append("")

    # --- Сравнение методов ---
    lines.append("=" * 70)
    lines.append("СРАВНЕНИЕ МЕТОДОВ")
    lines.append("=" * 70)

    r1 = coordinate_descent(x1_0, x2_0, eps)
    r2 = gradient_descent(x1_0, x2_0, eps, step)
    r3 = steepest_descent(x1_0, x2_0, eps)

    lines.append(f"{'Метод':<30} {'Итерации':>10} {'x1*':>12} {'x2*':>12} {'f(x*)':>12}")
    lines.append("-" * 78)
    lines.append(f"{'Покоординатный спуск':<30} {r1[4]:>10} {r1[0]:>12.6f} {r1[1]:>12.6f} {r1[2]:>12.6f}")
    lines.append(f"{'Градиентный спуск':<30} {r2[4]:>10} {r2[0]:>12.6f} {r2[1]:>12.6f} {r2[2]:>12.6f}")
    lines.append(f"{'Наискорейший спуск':<30} {r3[4]:>10} {r3[0]:>12.6f} {r3[1]:>12.6f} {r3[2]:>12.6f}")
    lines.append("")

    report = "\n".join(lines)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)

    print(report)
    print(f"\nОтчёт сохранён в файл: {filename}")


# ============================================================
# Запуск
# ============================================================
if __name__ == "__main__":
    generate_report("report.txt")
