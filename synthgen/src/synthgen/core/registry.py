"""
Provider Registry with Lazy Loading.

Implements a registry pattern for managing data providers with support for:
- Automatic discovery and registration
- Lazy loading of provider modules
- Thread-safe operations
- Plugin architecture for extensibility
"""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, TypeVar
from collections.abc import Callable

if TYPE_CHECKING:
    from synthgen.core.base import BaseProvider


T = TypeVar("T", bound="BaseProvider")


class ProviderRegistry:
    """
    Central registry for all data providers.

    Uses a lazy-loading pattern to minimize startup time and memory usage.
    Providers are loaded only when first accessed.

    Thread-safe for concurrent access.

    Example:
        >>> registry = ProviderRegistry()
        >>> registry.register(MyCustomProvider)
        >>> provider = registry.get("custom")
    """

    def __init__(self) -> None:
        """Initialize the provider registry."""
        self._providers: dict[str, type[BaseProvider]] = {}
        self._instances: dict[str, BaseProvider] = {}
        self._lock = threading.RLock()
        self._lazy_loaders: dict[str, Callable[[], type[BaseProvider]]] = {}

    def register(
        self,
        provider_class: type[BaseProvider],
        name: str | None = None,
        lazy: bool = False,
        loader: Callable[[], type[BaseProvider]] | None = None,
    ) -> None:
        """
        Register a provider class.

        Args:
            provider_class: The provider class to register.
            name: Optional name override. Defaults to class name without 'Provider' suffix.
            lazy: If True, provider is loaded only on first access.
            loader: Optional loader function for lazy loading.

        Raises:
            ValueError: If a provider with the same name is already registered.
        """
        with self._lock:
            if name is None:
                # Auto-generate name from class
                name = provider_class.__name__
                if name.endswith("Provider"):
                    name = name[:-8]
                name = name.lower()

            if name in self._providers:
                raise ValueError(f"Provider '{name}' is already registered")

            if lazy and loader is not None:
                self._lazy_loaders[name] = loader
            else:
                self._providers[name] = provider_class

    def get(self, name: str, seed_manager: object | None = None) -> BaseProvider:
        """
        Get a provider instance by name.

        Args:
            name: The provider name (case-insensitive).
            seed_manager: Optional seed manager to inject.

        Returns:
            An instance of the requested provider.

        Raises:
            KeyError: If the provider is not found.
        """
        name = name.lower()

        with self._lock:
            # Check if already instantiated
            if name in self._instances:
                return self._instances[name]

            # Check lazy loaders first
            if name in self._lazy_loaders:
                provider_class = self._lazy_loaders[name]()
                del self._lazy_loaders[name]
                self._providers[name] = provider_class

            # Get provider class
            if name not in self._providers:
                available = ", ".join(sorted(self._providers.keys()))
                raise KeyError(
                    f"Provider '{name}' not found. Available: {available}"
                )

            provider_class = self._providers[name]

            # Create instance with dependency injection
            if seed_manager is not None:
                instance = provider_class(seed_manager)
            else:
                instance = provider_class()

            self._instances[name] = instance
            return instance

    def list_providers(self) -> list[str]:
        """
        List all registered provider names.

        Returns:
            Sorted list of provider names.
        """
        with self._lock:
            return sorted(set(self._providers.keys()) | set(self._lazy_loaders.keys()))

    def unregister(self, name: str) -> None:
        """
        Unregister a provider.

        Args:
            name: The provider name to remove.

        Raises:
            KeyError: If the provider is not found.
        """
        with self._lock:
            name = name.lower()
            if name in self._providers:
                del self._providers[name]
            if name in self._instances:
                del self._instances[name]
            if name in self._lazy_loaders:
                del self._lazy_loaders[name]

    def clear(self) -> None:
        """Clear all registered providers and instances."""
        with self._lock:
            self._providers.clear()
            self._instances.clear()
            self._lazy_loaders.clear()

    def is_registered(self, name: str) -> bool:
        """
        Check if a provider is registered.

        Args:
            name: The provider name.

        Returns:
            True if registered, False otherwise.
        """
        with self._lock:
            name = name.lower()
            return name in self._providers or name in self._lazy_loaders

    @property
    def count(self) -> int:
        """Get the number of registered providers."""
        with self._lock:
            return len(self._providers) + len(self._lazy_loaders)


# Global singleton registry instance
registry = ProviderRegistry()
