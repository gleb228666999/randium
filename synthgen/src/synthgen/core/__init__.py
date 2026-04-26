"""
SynthGen Core Module

Contains the fundamental building blocks:
- Registry for provider management
- Seed manager for reproducibility
- Base classes for all providers
- Configuration system
"""

from synthgen.core.registry import ProviderRegistry, registry
from synthgen.core.seed_manager import SeedManager, SeedContext
from synthgen.core.base import BaseProvider, GeneratorResult
from synthgen.core.config import Config

__all__ = [
    "ProviderRegistry",
    "registry",
    "SeedManager",
    "SeedContext",
    "BaseProvider",
    "GeneratorResult",
    "Config",
]
