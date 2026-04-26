"""Stream Generation Engine."""

from __future__ import annotations
from typing import Any, Callable, Iterator
from synthgen.core.seed_manager import SeedManager


class StreamEngine:
    """Engine for memory-efficient streaming data generation."""

    def __init__(self, seed_manager: SeedManager) -> None:
        self._sm = seed_manager
        self._chunk_size = 100
        self._generators: dict[str, tuple[Callable, dict]] = {}

    def with_chunk_size(self, chunk_size: int) -> "StreamEngine":
        """Set the chunk size."""
        self._chunk_size = chunk_size
        return self

    def add_generator(self, name: str, generator: Callable, **kwargs: Any) -> "StreamEngine":
        """Add a generator to the stream."""
        self._generators[name] = (generator, kwargs)
        return self

    def generate(self, count: int | None = None) -> Iterator[dict[str, Any]]:
        """Generate streaming data as an iterator."""
        generated = 0
        while count is None or generated < count:
            record = {}
            for name, (gen, kwargs) in self._generators.items():
                record[name] = gen(**kwargs) if kwargs else gen()
            yield record
            generated += 1

    def generate_chunks(self, count: int) -> Iterator[list[dict[str, Any]]]:
        """Generate data in chunks."""
        chunk = []
        for i, record in enumerate(self.generate(count)):
            chunk.append(record)
            if len(chunk) >= self._chunk_size or i == count - 1:
                yield chunk
                chunk = []
