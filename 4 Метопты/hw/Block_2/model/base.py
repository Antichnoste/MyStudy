from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class IterationPoint:
    """Одна точка итерационного процесса."""

    k: int
    x: float
    y: float
    z: float
    grad_norm: float
    step: Optional[float] = None


@dataclass
class OptimizationResult:
    """Результат работы оптимизатора."""

    method_name: str
    x_star: float
    y_star: float
    z_star: float
    iterations: int
    history: List[IterationPoint] = field(default_factory=list)


class Optimizer2D(ABC):
    """Базовый интерфейс метода минимизации f(x, y)."""

    method_name: str

    @abstractmethod
    def run(self, start_point: Tuple[float, float], eps: float, max_iter: int) -> OptimizationResult:
        """Запускает метод и возвращает историю итераций."""

        raise NotImplementedError
