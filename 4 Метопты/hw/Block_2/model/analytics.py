from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from objective import grad, hessian, z


@dataclass
class StationaryPointInfo:
    point: Tuple[float, float]
    value: float
    hessian_det: float
    hessian_trace: float
    point_type: str


def classify_point(x: float, y: float) -> StationaryPointInfo:
    """Классификация точки по матрице Гессе."""

    h = hessian(x, y)
    h11, h12 = h[0]
    h21, h22 = h[1]
    det = h11 * h22 - h12 * h21
    trace = h11 + h22

    if det > 0 and h11 > 0:
        point_type = "local minimum"
    elif det > 0 and h11 < 0:
        point_type = "local maximum"
    elif det < 0:
        point_type = "saddle"
    else:
        point_type = "inconclusive"

    return StationaryPointInfo((x, y), z(x, y), det, trace, point_type)


def find_stationary_points_analytic() -> List[StationaryPointInfo]:
    """Аналитические стационарные точки для варианта ДЗ2."""

    # dz/dx = 3x^2 + 6x = 3x(x+2) => x in {0, -2}
    xs = [0.0, -2.0]
    # dz/dy = 3y^2 - 10y + 7 = 0 => y in {1, 7/3}
    ys = [1.0, 7.0 / 3.0]

    points: List[StationaryPointInfo] = []
    for x in xs:
        for y in ys:
            gx, gy = grad(x, y)
            if abs(gx) < 1e-10 and abs(gy) < 1e-10:
                points.append(classify_point(x, y))

    return points
