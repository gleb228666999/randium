"""Batch Generation Engine."""

from __future__ import annotations
from typing import Any, Callable
from synthgen.core.seed_manager import SeedManager


class BatchEngine:
    """Engine for vectorized batch data generation."""

    def __init__(self, seed_manager: SeedManager) -> None:
        self._sm = seed_manager
        self._count = 100
        self._generators: dict[str, tuple[Callable, dict]] = {}

    def with_count(self, count: int) -> "BatchEngine":
        """Set the batch count."""
        self._count = count
        return self

    def add_generator(self, name: str, generator: Callable, **kwargs: Any) -> "BatchEngine":
        """Add a generator to the batch."""
        self._generators[name] = (generator, kwargs)
        return self

    def generate(self) -> list[dict[str, Any]]:
        """Generate batch data."""
        results = []
        for _ in range(self._count):
            record = {}
            for name, (gen, kwargs) in self._generators.items():
                record[name] = gen(**kwargs) if kwargs else gen()
            results.append(record)
        return results

    def generate_flat(self, generator: Callable, **kwargs: Any) -> list[Any]:
        """Generate a flat list from a single generator."""
        return [generator(**kwargs) if kwargs else generator() for _ in range(self._count)]
