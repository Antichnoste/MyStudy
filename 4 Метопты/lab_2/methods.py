import math

EPS = 1e-4
MAX_ITER = 10_000


def _target(func, find: str):
    if find not in ("min", "max"):
        raise ValueError("Параметр find должен быть 'min' или 'max'.")
    if find == "max":
        return lambda x: -func(x)
    return func

def midpoint_extremum(func, left: float, right: float, eps: float = EPS, find: str = "min"):
    target = _target(func, find)
    a, b = left, right

    if b <= a:
        raise ValueError("Нужен отрезок: left < right")

    for i in range(1, MAX_ITER+1):
        if ((b - a) <= 2.0 * eps):
            break    

        x1 = (a + b - eps) / 2.0
        x2 = (a + b + eps) / 2.0
        y1 = target(x1)
        y2 = target(x2)

        if y1 > y2:
            a = x1
        else:
            b = x2

    xm = (a + b) / 2.0
    return xm, i

def golden_section_extremum(func, left: float, right: float, tol: float = EPS, find: str = "min"):
    target = _target(func, find)

    a, b = left, right
    tau1 = (3.0 - math.sqrt(5.0)) / 2.0  # ~0.381966
    tau2 = (math.sqrt(5.0) - 1.0) / 2.0  # ~0.618034

    x1 = a + tau1 * (b - a)
    x2 = a + tau2 * (b - a)
    f1 = target(x1)
    f2 = target(x2)

    for i in range(1, MAX_ITER + 1):
        if (b - a) < tol:
            return (a + b) / 2.0, i

        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + tau1 * (b - a)
            f1 = target(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + tau2 * (b - a)
            f2 = target(x2)

    return (a + b) / 2.0, MAX_ITER

def chord_extremum(func, dfunc, left: float, right: float, tol: float = EPS, find: str = "min"):
    sign = -1.0 if find == "max" else 1.0
    F = lambda x: sign * dfunc(x)

    a, b = left, right
    Fa, Fb = F(a), F(b)

    if Fa == 0:
        return a, 0
    if Fb == 0:
        return b, 0
    if Fa * Fb > 0:
        raise ValueError("Для метода хорд требуется смена знака F(x) на [a,b].")

    for i in range(1, MAX_ITER + 1):
        denom = Fa - Fb
        if abs(denom) < 1e-16:
            return (a + b) / 2.0, i

        x = a - (Fa / denom) * (a - b)
        Fx = F(x)

        if abs(Fx) <= tol:
            return x, i

        if Fa * Fx <= 0:
            b, Fb = x, Fx
        else:
            a, Fa = x, Fx

    return (a + b) / 2.0, MAX_ITER

def newton_extremum(func, dfunc, d2func, x0: float, left: float, right: float, tol: float = EPS, find: str = "min"):
    sign = -1.0 if find == "max" else 1.0
    F = lambda x: sign * dfunc(x)
    Fp = lambda x: sign * d2func(x)

    x = x0
    for i in range(1, MAX_ITER + 1):
        Fx = F(x)
        Fpx = Fp(x)

        if abs(Fx) <= tol:
            return x, i

        if abs(Fpx) < tol:
            x = (left + right) / 2.0
            continue

        x_next = x - Fx / Fpx
        
        x = x_next

    return x, MAX_ITER