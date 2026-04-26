"""
SynthGen - Production-Ready Random Data Generation Library

A comprehensive, extensible library for generating realistic, customizable,
and reproducible random data across all major domains.

Copyright (c) 2024 SynthGen Contributors
Licensed under the MIT License.
"""

from synthgen.core.registry import ProviderRegistry, registry
from synthgen.core.seed_manager import SeedManager, SeedContext
from synthgen.core.base import BaseProvider, GeneratorResult
from synthgen.core.config import Config

from synthgen.providers.personal import PersonalProvider
from synthgen.providers.financial import FinancialProvider
from synthgen.providers.geographic import GeographicProvider
from synthgen.providers.temporal import TemporalProvider
from synthgen.providers.technical import TechnicalProvider
from synthgen.providers.scientific import ScientificProvider
from synthgen.providers.linguistic import LinguisticProvider
from synthgen.providers.iot import IoTProvider
from synthgen.providers.gaming import GamingProvider
from synthgen.providers.custom import CustomProvider

from synthgen.engines.batch import BatchEngine
from synthgen.engines.stream import StreamEngine
from synthgen.engines.async_engine import AsyncEngine

from synthgen.validators.schema import SchemaValidator
from synthgen.validators.constraints import ConstraintValidator

__version__ = "1.0.0"
__author__ = "SynthGen Contributors"
__license__ = "MIT"

__all__ = [
    # Core
    "ProviderRegistry",
    "registry",
    "SeedManager",
    "SeedContext",
    "BaseProvider",
    "GeneratorResult",
    "Config",
    # Providers
    "PersonalProvider",
    "FinancialProvider",
    "GeographicProvider",
    "TemporalProvider",
    "TechnicalProvider",
    "ScientificProvider",
    "LinguisticProvider",
    "IoTProvider",
    "GamingProvider",
    "CustomProvider",
    # Engines
    "BatchEngine",
    "StreamEngine",
    "AsyncEngine",
    # Validators
    "SchemaValidator",
    "ConstraintValidator",
]


def create_generator(seed: int | None = None, config: Config | None = None) -> "SynthGen":
    """
    Create a new SynthGen instance with optional seed and configuration.

    Args:
        seed: Optional seed for reproducibility. If None, uses system randomness.
        config: Optional configuration object.

    Returns:
        A configured SynthGen instance.
    """
    return SynthGen(seed=seed, config=config)


class SynthGen:
    """
    Main entry point for the SynthGen library.

    Provides a unified interface to all data providers and engines.

    Example:
        >>> gen = SynthGen(seed=42)
        >>> gen.personal.name()
        'John Doe'
        >>> gen.financial.credit_card_number()
        '4532015112830366'
    """

    def __init__(self, seed: int | None = None, config: Config | None = None):
        """
        Initialize SynthGen.

        Args:
            seed: Optional seed for reproducible generation.
            config: Optional configuration for customization.
        """
        self._seed_manager = SeedManager(seed=seed)
        self._config = config or Config()
        self._registry = registry

        # Initialize all providers with shared seed manager
        self.personal = PersonalProvider(self._seed_manager)
        self.financial = FinancialProvider(self._seed_manager)
        self.geographic = GeographicProvider(self._seed_manager)
        self.temporal = TemporalProvider(self._seed_manager)
        self.technical = TechnicalProvider(self._seed_manager)
        self.scientific = ScientificProvider(self._seed_manager)
        self.linguistic = LinguisticProvider(self._seed_manager)
        self.iot = IoTProvider(self._seed_manager)
        self.gaming = GamingProvider(self._seed_manager)
        self.custom = CustomProvider(self._seed_manager)

        # Initialize engines
        self._batch_engine = BatchEngine(self._seed_manager)
        self._stream_engine = StreamEngine(self._seed_manager)

    @property
    def seed_manager(self) -> SeedManager:
        """Access the seed manager for advanced seed control."""
        return self._seed_manager

    @property
    def config(self) -> Config:
        """Access the current configuration."""
        return self._config

    def set_seed(self, seed: int) -> None:
        """Set a new seed for reproducible generation."""
        self._seed_manager.set_seed(seed)

    def reset_seed(self) -> None:
        """Reset to system randomness."""
        self._seed_manager.reset()

    def batch(self, count: int) -> BatchEngine:
        """
        Get a batch engine for vectorized generation.

        Args:
            count: Number of items to generate per batch.

        Returns:
            Configured BatchEngine instance.
        """
        return self._batch_engine.with_count(count)

    def stream(self, chunk_size: int = 100) -> StreamEngine:
        """
        Get a stream engine for memory-efficient generation.

        Args:
            chunk_size: Number of items per chunk.

        Returns:
            Configured StreamEngine instance.
        """
        return self._stream_engine.with_chunk_size(chunk_size)

    def register_provider(self, provider: BaseProvider) -> None:
        """
        Register a custom provider.

        Args:
            provider: A BaseProvider subclass instance.
        """
        self._registry.register(provider)

    def generate_schema(self, schema: dict, count: int = 1) -> list[dict]:
        """
        Generate data based on a JSON schema.

        Args:
            schema: JSON Schema defining the structure.
            count: Number of records to generate.

        Returns:
            List of generated dictionaries.
        """
        validator = SchemaValidator(schema)
        return validator.generate(count, self)
