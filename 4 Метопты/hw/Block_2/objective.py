from dataclasses import dataclass
from typing import Tuple
import math


@dataclass(frozen=True)
class ProblemConfig:
    """Параметры задачи оптимизации."""

    start_point: Tuple[float, float] = (-0.5, 2.5)
    eps: float = 1e-4
    max_iter: int = 10_000


def z(x: float, y: float) -> float:
    """Целевая функция из ДЗ2."""

    return x**3 + 3 * x**2 + y**3 - 5 * y**2 + 7 * y - 7


def grad(x: float, y: float) -> Tuple[float, float]:
    """Градиент функции z(x, y)."""

    dz_dx = 3 * x**2 + 6 * x
    dz_dy = 3 * y**2 - 10 * y + 7
    return dz_dx, dz_dy


def hessian(x: float, y: float) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Матрица Гессе функции z(x, y)."""

    return ((6 * x + 6, 0.0), (0.0, 6 * y - 10))


def grad_norm(x: float, y: float) -> float:
    """Евклидова норма градиента."""

    gx, gy = grad(x, y)
    return math.sqrt(gx * gx + gy * gy)
