from __future__ import annotations

import math
from typing import Tuple

from model.base import IterationPoint, OptimizationResult, Optimizer2D
from objective import grad, grad_norm, hessian, z


def _bisection_min(phi, a: float, b: float, eps: float) -> float:
    """Минимизация одномерной унимодальной функции на [a, b]."""

    while (b - a) > 2.0 * eps:
        x1 = (a + b - eps) / 2.0
        x2 = (a + b + eps) / 2.0
        if phi(x1) > phi(x2):
            a = x1
        else:
            b = x2
    return (a + b) / 2.0


class CoordinateDescentOptimizer(Optimizer2D):
    method_name = "Coordinate Descent"
    
    def __init__(self, span: float = 2.0):
        self.span = span

    def run(self, start_point: Tuple[float, float], eps: float, max_iter: int) -> OptimizationResult:
        # На каждом цикле две 1D-минимизации методом половинного деления.
        x, y = start_point
        history = [IterationPoint(0, x, y, z(x, y), grad_norm(x, y), None)]

        iterations = 0
        for k in range(1, max_iter + 1):
            x_old, y_old = x, y
            f_old = z(x_old, y_old)

            phi1 = lambda t: z(t, y)
            x = _bisection_min(phi1, x - self.span, x + self.span, eps)
            history.append(IterationPoint(len(history), x, y, z(x, y), grad_norm(x, y), None))

            phi2 = lambda t: z(x, t)
            y = _bisection_min(phi2, y - self.span, y + self.span, eps)
            history.append(IterationPoint(len(history), x, y, z(x, y), grad_norm(x, y), None))

            iterations = k
            dist = math.sqrt((x - x_old) ** 2 + (y - y_old) ** 2)
            if dist <= eps or abs(z(x, y) - f_old) <= eps:
                break

        return OptimizationResult(self.method_name, x, y, z(x, y), iterations, history)


class GradientDescentOptimizer(Optimizer2D):
    method_name = "Gradient Descent"

    def __init__(self, step: float = 0.05):
        self.step = step

    def run(self, start_point: Tuple[float, float], eps: float, max_iter: int) -> OptimizationResult:
        # Если функция не уменьшается, шаг дробится пополам.
        x, y = start_point
        f_prev = z(x, y)
        history = [IterationPoint(0, x, y, f_prev, grad_norm(x, y), self.step)]

        step = self.step

        iterations = 0
        for k in range(1, max_iter + 1):
            gx, gy = grad(x, y)

            x_new = x - step * gx
            y_new = y - step * gy
            f_new = z(x_new, y_new)

            while f_new >= f_prev:
                step = step / 2.0
                x_new = x - step * gx
                y_new = y - step * gy
                f_new = z(x_new, y_new)

            x, y = x_new, y_new
            f_curr = f_new
            history.append(IterationPoint(len(history), x, y, f_curr, grad_norm(x, y), step))

            iterations = k
            if abs(f_curr - f_prev) < eps:
                break
            f_prev = f_curr

        return OptimizationResult(self.method_name, x, y, z(x, y), iterations, history)


class SteepestDescentOptimizer(Optimizer2D):
    method_name = "Steepest Descent"

    def __init__(self, h_span: float = 1.0, h_start: float = 0.0):
        self.h_span = h_span
        self.h_start = h_start

    def run(self, start_point: Tuple[float, float], eps: float, max_iter: int) -> OptimizationResult:
        # h_k ищется локально методом половинного деления вокруг предыдущего h.
        x, y = start_point
        history = [IterationPoint(0, x, y, z(x, y), grad_norm(x, y), None)]
        h_center = self.h_start

        iterations = 0
        for k in range(1, max_iter + 1):
            gx, gy = grad(x, y)
            gnorm = math.sqrt(gx * gx + gy * gy)
            if gnorm < eps:
                break

            phi = lambda h: z(x - h * gx, y - h * gy)
            left = max(0.0, h_center - self.h_span)
            right = h_center + self.h_span
            h_opt = _bisection_min(phi, left, right, eps)

            x = x - h_opt * gx
            y = y - h_opt * gy
            history.append(IterationPoint(len(history), x, y, z(x, y), grad_norm(x, y), h_opt))
            h_center = h_opt
            iterations = k

        return OptimizationResult(self.method_name, x, y, z(x, y), iterations, history)


class NewtonOptimizer2D(Optimizer2D):
    method_name = "Newton Method"

    def run(self, start_point: Tuple[float, float], eps: float, max_iter: int) -> OptimizationResult:
        # Классический Ньютон для системы grad z(x, y) = 0.
        x, y = start_point
        history = [IterationPoint(0, x, y, z(x, y), grad_norm(x, y), None)]

        iterations = 0
        for k in range(1, max_iter + 1):
            gx, gy = grad(x, y)
            gnorm = math.sqrt(gx * gx + gy * gy)
            if gnorm < eps:
                break

            h = hessian(x, y)
            h11, h12 = h[0]
            h21, h22 = h[1]
            det = h11 * h22 - h12 * h21

            if abs(det) < 1e-12:
                # Если Гессиан вырожден, делаем малый шаг антиградиента.
                step = 1e-2
                x = x - step * gx
                y = y - step * gy
            else:
                # Решаем H * delta = grad, затем x_{k+1} = x_k - delta.
                dx = (h22 * gx - h12 * gy) / det
                dy = (-h21 * gx + h11 * gy) / det
                x = x - dx
                y = y - dy

            history.append(IterationPoint(len(history), x, y, z(x, y), grad_norm(x, y), None))
            iterations = k

        return OptimizationResult(self.method_name, x, y, z(x, y), iterations, history)
