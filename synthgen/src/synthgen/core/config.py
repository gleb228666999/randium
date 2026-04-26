"""
Configuration and constants for SynthGen.

Provides a centralized configuration system for customization.
"""

from dataclasses import dataclass, field
from typing import Any
from enum import Enum


class SafetyLevel(Enum):
    """Safety levels for data generation."""

    STANDARD = "standard"  # Normal synthetic data
    GDPR_SAFE = "gdpr_safe"  # GDPR-compliant mock data
    HIPAA_SAFE = "hipaa_safe"  # HIPAA-compliant synthetic records
    CRYPTO_SECURE = "crypto_secure"  # Cryptographically secure (slower)


class OutputFormat(Enum):
    """Supported output formats."""

    JSON = "json"
    CSV = "csv"
    YAML = "yaml"
    PARQUET = "parquet"
    SQL = "sql"
    RAW = "raw"


@dataclass
class Config:
    """
    Configuration for SynthGen.

    Attributes:
        safety_level: Data safety/compliance level.
        locale: Default locale for localized data (e.g., 'en_US', 'de_DE').
        timezone: Default timezone for temporal data.
        include_sensitive: Whether to include sensitive fields by default.
        max_batch_size: Maximum items per batch operation.
        custom_settings: Additional custom settings.
    """

    safety_level: SafetyLevel = SafetyLevel.STANDARD
    locale: str = "en_US"
    timezone: str = "UTC"
    include_sensitive: bool = False
    max_batch_size: int = 10000
    custom_settings: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.max_batch_size <= 0:
            raise ValueError("max_batch_size must be positive")
        if not self.locale:
            raise ValueError("locale cannot be empty")

    def with_safety(self, level: SafetyLevel) -> "Config":
        """Return a new config with updated safety level."""
        return Config(
            safety_level=level,
            locale=self.locale,
            timezone=self.timezone,
            include_sensitive=self.include_sensitive,
            max_batch_size=self.max_batch_size,
            custom_settings=self.custom_settings.copy(),
        )

    def with_locale(self, locale: str) -> "Config":
        """Return a new config with updated locale."""
        return Config(
            safety_level=self.safety_level,
            locale=locale,
            timezone=self.timezone,
            include_sensitive=self.include_sensitive,
            max_batch_size=self.max_batch_size,
            custom_settings=self.custom_settings.copy(),
        )

    def with_timezone(self, timezone: str) -> "Config":
        """Return a new config with updated timezone."""
        return Config(
            safety_level=self.safety_level,
            locale=self.locale,
            timezone=timezone,
            include_sensitive=self.include_sensitive,
            max_batch_size=self.max_batch_size,
            custom_settings=self.custom_settings.copy(),
        )

    def get(self, key: str, default: Any = None) -> Any:
        """Get a custom setting by key."""
        return self.custom_settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a custom setting."""
        self.custom_settings[key] = value
