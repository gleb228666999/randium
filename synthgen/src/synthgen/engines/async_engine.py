"""Async Generation Engine."""

from __future__ import annotations
import asyncio
from typing import Any, Callable, AsyncIterator
from synthgen.core.seed_manager import SeedManager


class AsyncEngine:
    """Engine for asynchronous data generation."""

    def __init__(self, seed_manager: SeedManager) -> None:
        self._sm = seed_manager
        self._generators: dict[str, tuple[Callable, dict]] = {}

    def add_generator(self, name: str, generator: Callable, **kwargs: Any) -> "AsyncEngine":
        """Add a generator to the async engine."""
        self._generators[name] = (generator, kwargs)
        return self

    async def generate(self, count: int) -> AsyncIterator[dict[str, Any]]:
        """Generate data asynchronously."""
        for _ in range(count):
            record = {}
            for name, (gen, kwargs) in self._generators.items():
                if asyncio.iscoroutinefunction(gen):
                    record[name] = await gen(**kwargs) if kwargs else await gen()
                else:
                    record[name] = gen(**kwargs) if kwargs else gen()
            yield record

    async def generate_parallel(
        self, count: int, max_concurrency: int = 10
    ) -> list[dict[str, Any]]:
        """Generate data in parallel with concurrency limit."""
        semaphore = asyncio.Semaphore(max_concurrency)

        async def generate_one() -> dict[str, Any]:
            async with semaphore:
                record = {}
                for name, (gen, kwargs) in self._generators.items():
                    if asyncio.iscoroutinefunction(gen):
                        record[name] = await gen(**kwargs) if kwargs else await gen()
                    else:
                        record[name] = gen(**kwargs) if kwargs else gen()
                return record

        tasks = [generate_one() for _ in range(count)]
        return await asyncio.gather(*tasks)
