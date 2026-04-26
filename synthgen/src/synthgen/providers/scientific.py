"""
Scientific & Mathematical Data Provider.

Generates scientific data including:
- Statistical distributions
- Vectors and matrices
- Constants
- Units and measurements
"""

from __future__ import annotations

import math
from typing import Any

from synthgen.core.base import BaseProvider
from synthgen.core.seed_manager import SeedManager


class ScientificProvider(BaseProvider):
    """Provider for scientific and mathematical data."""

    def __init__(self, seed_manager: SeedManager | None = None) -> None:
        super().__init__(seed_manager)
        self._sm = seed_manager

    def _get_sm(self) -> SeedManager:
        if self._sm is None:
            raise RuntimeError("SeedManager not initialized")
        return self._sm

    def normal_distribution(
        self, mean: float = 0.0, std_dev: float = 1.0
    ) -> float:
        """Generate a value from normal distribution using Box-Muller transform."""
        sm = self._get_sm()
        u1 = sm.random_float(0.0001, 1.0)
        u2 = sm.random_float(0.0001, 1.0)
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        return mean + z0 * std_dev

    def uniform_distribution(self, low: float = 0.0, high: float = 1.0) -> float:
        """Generate a value from uniform distribution."""
        sm = self._get_sm()
        return sm.random_float(low, high)

    def exponential_distribution(self, lambd: float = 1.0) -> float:
        """Generate a value from exponential distribution."""
        sm = self._get_sm()
        u = sm.random_float(0.0001, 1.0)
        return -math.log(u) / lambd

    def poisson_distribution(self, lambd: float = 3.0) -> int:
        """Generate a value from Poisson distribution."""
        sm = self._get_sm()
        L = math.exp(-lambd)
        k = 0
        p = 1.0
        while p > L:
            k += 1
            p *= sm.random_float(0, 1)
        return k - 1

    def vector(self, size: int = 3, min_val: float = 0.0, max_val: float = 1.0) -> list[float]:
        """Generate a random vector."""
        sm = self._get_sm()
        return [sm.random_float(min_val, max_val) for _ in range(size)]

    def matrix(
        self, rows: int = 3, cols: int = 3, min_val: float = 0.0, max_val: float = 1.0
    ) -> list[list[float]]:
        """Generate a random matrix."""
        return [self.vector(size=cols, min_val=min_val, max_val=max_val) for _ in range(rows)]

    def generate(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Generate complete scientific profile."""
        return {
            "normal": self.normal_distribution(),
            "uniform": self.uniform_distribution(),
            "exponential": self.exponential_distribution(),
            "poisson": self.poisson_distribution(),
            "vector": self.vector(),
            "matrix": self.matrix(),
        }
