"""
Base Classes for Data Providers.

Defines the abstract base classes and interfaces that all providers must implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar
from datetime import datetime


T = TypeVar("T")


@dataclass
class GeneratorResult(Generic[T]):
    """
    Wrapper for generator results with metadata.

    Attributes:
        value: The generated value.
        metadata: Optional metadata about the generation.
        timestamp: When the value was generated.
    """

    value: T
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __bool__(self) -> bool:
        """Truthiness based on value."""
        return bool(self.value)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "value": self.value,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }


class BaseProvider(ABC):
    """
    Abstract base class for all data providers.

    All providers must inherit from this class and implement
    the required methods.

    Example:
        >>> class MyProvider(BaseProvider):
        ...     def generate(self):
        ...         return "custom_value"
    """

    def __init__(self, seed_manager: object | None = None) -> None:
        """
        Initialize the provider.

        Args:
            seed_manager: Optional seed manager for reproducibility.
        """
        self._seed_manager = seed_manager

    @property
    def name(self) -> str:
        """
        Get the provider name.

        Returns:
            Provider name (defaults to class name without 'Provider' suffix).
        """
        class_name = self.__class__.__name__
        if class_name.endswith("Provider"):
            return class_name[:-8].lower()
        return class_name.lower()

    @abstractmethod
    def generate(self, *args: Any, **kwargs: Any) -> Any:
        """
        Generate a single data item.

        This is the primary method that subclasses must implement.

        Args:
            *args: Positional arguments for generation.
            **kwargs: Keyword arguments for generation.

        Returns:
            Generated data item.
        """
        pass

    def generate_batch(self, count: int, *args: Any, **kwargs: Any) -> list[Any]:
        """
        Generate multiple items.

        Default implementation calls generate() repeatedly.
        Subclasses can override for optimized batch generation.

        Args:
            count: Number of items to generate.
            *args: Positional arguments passed to generate().
            **kwargs: Keyword arguments passed to generate().

        Returns:
            List of generated items.
        """
        return [self.generate(*args, **kwargs) for _ in range(count)]

    def generate_stream(self, count: int | None = None, *args: Any, **kwargs: Any):
        """
        Generate items as a lazy iterator.

        Default implementation yields from generate() repeatedly.
        Subclasses can override for streaming optimizations.

        Args:
            count: Number of items to generate, or None for infinite.
            *args: Positional arguments passed to generate().
            **kwargs: Keyword arguments passed to generate().

        Yields:
            Generated items one at a time.
        """
        i = 0
        while count is None or i < count:
            yield self.generate(*args, **kwargs)
            i += 1

    def validate(self, value: Any) -> bool:
        """
        Validate a generated value.

        Default implementation always returns True.
        Subclasses can override with specific validation logic.

        Args:
            value: Value to validate.

        Returns:
            True if valid, False otherwise.
        """
        return True

    def get_metadata(self) -> dict[str, Any]:
        """
        Get provider metadata.

        Returns:
            Dictionary with provider information.
        """
        return {
            "name": self.name,
            "class": self.__class__.__name__,
            "module": self.__class__.__module__,
        }

    def __repr__(self) -> str:
        """String representation of the provider."""
        return f"{self.__class__.__name__}(name='{self.name}')"


class CompositeProvider(BaseProvider):
    """
    Provider that combines multiple providers.

    Useful for creating complex generators from simpler ones.

    Example:
        >>> composite = CompositeProvider()
        >>> composite.add_provider("name", personal_provider)
        >>> composite.add_provider("email", email_provider)
        >>> result = composite.generate()  # Returns dict with both
    """

    def __init__(self, seed_manager: object | None = None) -> None:
        """Initialize the composite provider."""
        super().__init__(seed_manager)
        self._providers: dict[str, BaseProvider] = {}
        self._weights: dict[str, float] = {}

    def add_provider(
        self, name: str, provider: BaseProvider, weight: float = 1.0
    ) -> None:
        """
        Add a sub-provider.

        Args:
            name: Name for the sub-provider.
            provider: The provider instance.
            weight: Weight for selection (used in choose mode).
        """
        self._providers[name] = provider
        self._weights[name] = weight

    def remove_provider(self, name: str) -> None:
        """
        Remove a sub-provider.

        Args:
            name: Name of the provider to remove.
        """
        if name in self._providers:
            del self._providers[name]
        if name in self._weights:
            del self._weights[name]

    def generate(self, mode: str = "all") -> Any:
        """
        Generate data from sub-providers.

        Args:
            mode: Generation mode:
                - "all": Return dict with all providers
                - "random": Choose one provider randomly (weighted)
                - "sequence": Return list in order

        Returns:
            Generated data based on mode.
        """
        if not self._providers:
            return None

        if mode == "all":
            return {
                name: provider.generate() for name, provider in self._providers.items()
            }
        elif mode == "random":
            # Weighted random selection
            if self._seed_manager is None:
                import random

                chosen = random.choices(
                    list(self._providers.keys()),
                    weights=list(self._weights.values()),
                )[0]
            else:
                # Use seed manager
                total = sum(self._weights.values())
                r = (
                    self._seed_manager.random_float(0, total)
                    if hasattr(self._seed_manager, "random_float")
                    else 0.5 * total
                )
                cumulative = 0
                chosen = list(self._providers.keys())[0]
                for name, weight in self._weights.items():
                    cumulative += weight
                    if r <= cumulative:
                        chosen = name
                        break
            return self._providers[chosen].generate()
        elif mode == "sequence":
            return [
                provider.generate() for provider in self._providers.values()
            ]
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def generate_batch(self, count: int, mode: str = "all") -> list[Any]:
        """Generate batches from sub-providers."""
        return [self.generate(mode=mode) for _ in range(count)]

    def get_metadata(self) -> dict[str, Any]:
        """Get metadata including sub-provider info."""
        base_meta = super().get_metadata()
        base_meta["sub_providers"] = list(self._providers.keys())
        return base_meta
