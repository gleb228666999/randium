"""Custom & Extensible Data Provider."""

from __future__ import annotations
import re
import string
from typing import Any, Callable
from synthgen.core.base import BaseProvider
from synthgen.core.seed_manager import SeedManager


class CustomProvider(BaseProvider):
    """Provider for custom and extensible data generation."""

    def __init__(self, seed_manager: SeedManager | None = None) -> None:
        super().__init__(seed_manager)
        self._sm = seed_manager
        self._custom_generators: dict[str, Callable] = {}

    def _get_sm(self) -> SeedManager:
        if self._sm is None:
            raise RuntimeError("SeedManager not initialized")
        return self._sm

    def register_generator(self, name: str, generator: Callable) -> None:
        """Register a custom generator function."""
        self._custom_generators[name] = generator

    def regex_string(self, pattern: str, length: int | None = None) -> str:
        """Generate a string matching a regex pattern (simplified)."""
        sm = self._get_sm()
        result = []
        i = 0
        while i < len(pattern):
            char = pattern[i]
            if char == '\\':
                i += 1
                if i < len(pattern):
                    next_char = pattern[i]
                    if next_char == 'd':
                        result.append(str(sm.random_int(0, 9)))
                    elif next_char == 'w':
                        result.append(sm.random_choice(string.ascii_letters + string.digits + '_'))
                    elif next_char == 's':
                        result.append(sm.random_choice(' \t\n'))
                    else:
                        result.append(next_char)
            elif char == '.':
                result.append(sm.random_choice(string.ascii_letters + string.digits))
            elif char == '[':
                end = pattern.find(']', i)
                if end != -1:
                    chars = pattern[i+1:end]
                    result.append(sm.random_choice(list(chars)))
                    i = end
            elif char == '{':
                end = pattern.find('}', i)
                if end != -1:
                    spec = pattern[i+1:end]
                    if ',' in spec:
                        parts = spec.split(',')
                        min_rep = int(parts[0]) if parts[0] else 0
                        max_rep = int(parts[1]) if parts[1] else 10
                    else:
                        min_rep = max_rep = int(spec)
                    count = sm.random_int(min_rep, max_rep)
                    if result:
                        last = result[-1]
                        result.extend([last] * (count - 1))
                    i = end
            elif char == '*':
                if result:
                    last = result[-1]
                    count = sm.random_int(0, 5)
                    result.extend([last] * count)
            elif char == '+':
                if result:
                    last = result[-1]
                    count = sm.random_int(1, 5)
                    result.extend([last] * count)
            elif char == '?':
                pass  # Optional, skip
            else:
                result.append(char)
            i += 1
        
        if length and len(result) < length:
            while len(result) < length:
                result.append(sm.random_choice(string.ascii_letters))
        elif length and len(result) > length:
            result = result[:length]
        
        return ''.join(result)

    def weighted_choice(self, choices: list[tuple[Any, float]]) -> Any:
        """Make a weighted random choice."""
        sm = self._get_sm()
        total = sum(w for _, w in choices)
        r = sm.random_float(0, total)
        cumulative = 0
        for item, weight in choices:
            cumulative += weight
            if r <= cumulative:
                return item
        return choices[-1][0]

    def constrained_value(
        self,
        value_type: str,
        min_val: Any = None,
        max_val: Any = None,
        options: list[Any] | None = None,
    ) -> Any:
        """Generate a constrained value."""
        sm = self._get_sm()
        if options:
            return sm.random_choice(options)
        
        if value_type == "int":
            return sm.random_int(min_val or 0, max_val or 100)
        elif value_type == "float":
            return sm.random_float(min_val or 0.0, max_val or 1.0)
        elif value_type == "str":
            length = sm.random_int(min_val or 1, max_val or 20)
            return ''.join(sm.random_sample(list(string.ascii_letters), length))
        elif value_type == "bool":
            return sm.random_bool()
        else:
            return None

    def generate(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Generate custom data based on provided specifications."""
        return {
            "regex_example": self.regex_string(r"\d{3}-\d{4}"),
            "weighted_example": self.weighted_choice([("A", 0.7), ("B", 0.2), ("C", 0.1)]),
            "constrained_int": self.constrained_value("int", min_val=1, max_val=100),
            "constrained_float": self.constrained_value("float", min_val=0.0, max_val=1.0),
        }
