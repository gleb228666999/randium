"""Safety Warnings and Markers."""

from __future__ import annotations
import warnings
from typing import Any


class SafetyWarning(UserWarning):
    """Warning for synthetic data usage."""
    pass


SYNTHETIC_MARKER = "__synthgen_synthetic__"


def mark_synthetic(data: Any) -> dict[str, Any]:
    """Mark data as synthetically generated."""
    if isinstance(data, dict):
        result = data.copy()
        result[SYNTHETIC_MARKER] = True
        return result
    return {SYNTHETIC_MARKER: True, "data": data}


def is_synthetic(data: Any) -> bool:
    """Check if data is marked as synthetic."""
    if isinstance(data, dict):
        return data.get(SYNTHETIC_MARKER, False)
    return False


def warn_crypto_insecure() -> None:
    """Warn that the generator is not cryptographically secure by default."""
    warnings.warn(
        "SynthGen uses pseudo-random generation which is NOT cryptographically secure. "
        "Do not use for security-sensitive applications.",
        SafetyWarning,
        stacklevel=2,
    )


def warn_fake_financial_data() -> None:
    """Warn that financial data is fake and should not be used for real transactions."""
    warnings.warn(
        "Generated financial data (credit cards, IBANs, etc.) is syntactically valid "
        "but completely FAKE. Never use for actual payment processing.",
        SafetyWarning,
        stacklevel=2,
    )
