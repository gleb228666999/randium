"""
Seed Manager for Reproducible Random Data Generation.

Provides deterministic random number generation with:
- Global and per-instance seed control
- Seed contexts for isolated randomness
- Cryptographically secure option (when needed)
- Thread-local state for safety
"""

from __future__ import annotations

import random
import hashlib
import threading
import secrets
from contextlib import contextmanager
from typing import Any


class SeedManager:
    """
    Manages random seeds for reproducible data generation.

    Supports both standard pseudo-random generation (fast, reproducible)
    and cryptographically secure generation (slower, non-reproducible).

    Thread-safe with thread-local state.

    Example:
        >>> sm = SeedManager(seed=42)
        >>> sm.random_int(1, 100)
        82
        >>> sm.reset()
        >>> sm.random_int(1, 100)
        82  # Same result after reset
    """

    def __init__(self, seed: int | None = None, crypto_secure: bool = False) -> None:
        """
        Initialize the seed manager.

        Args:
            seed: Optional seed for reproducibility. If None, uses system randomness.
            crypto_secure: If True, use cryptographically secure random (ignores seed).
        """
        self._default_seed = seed
        self._crypto_secure = crypto_secure
        self._local = threading.local()
        self._lock = threading.Lock()

        # Initialize thread-local state
        self._init_thread_state()

    def _init_thread_state(self) -> None:
        """Initialize random state for current thread."""
        if not hasattr(self._local, "random"):
            self._local.random = random.Random()
        if self._default_seed is not None and not self._crypto_secure:
            self._local.random.seed(self._default_seed)

    def _get_random(self) -> random.Random:
        """Get the thread-local random instance."""
        if not hasattr(self._local, "random"):
            self._init_thread_state()
        return self._local.random  # type: ignore

    def set_seed(self, seed: int) -> None:
        """
        Set a new seed for reproducibility.

        Args:
            seed: The seed value.
        """
        if self._crypto_secure:
            return  # Ignore seed in crypto mode
        rng = self._get_random()
        rng.seed(seed)

    def reset(self) -> None:
        """Reset to the default seed or system randomness."""
        if self._crypto_secure:
            return
        if self._default_seed is not None:
            self.set_seed(self._default_seed)
        else:
            # Reinitialize with system randomness
            self._local.random = random.Random()

    def random_int(self, min_val: int, max_val: int) -> int:
        """
        Generate a random integer in range [min_val, max_val].

        Args:
            min_val: Minimum value (inclusive).
            max_val: Maximum value (inclusive).

        Returns:
            Random integer in the specified range.
        """
        if self._crypto_secure:
            # Use secrets for crypto-safe generation
            range_size = max_val - min_val + 1
            return min_val + int(secrets.randbelow(range_size))
        return self._get_random().randint(min_val, max_val)

    def random_float(self, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """
        Generate a random float in range [min_val, max_val).

        Args:
            min_val: Minimum value (inclusive).
            max_val: Maximum value (exclusive).

        Returns:
            Random float in the specified range.
        """
        if self._crypto_secure:
            # Approximate crypto-safe float
            return min_val + (max_val - min_val) * (secrets.randbits(53) / (2**53))
        return self._get_random().uniform(min_val, max_val)

    def random_choice(self, seq: list[Any]) -> Any:
        """
        Choose a random element from a sequence.

        Args:
            seq: Non-empty sequence to choose from.

        Returns:
            Random element from the sequence.

        Raises:
            IndexError: If sequence is empty.
        """
        if not seq:
            raise IndexError("Cannot choose from empty sequence")
        if self._crypto_secure:
            return secrets.choice(seq)
        return self._get_random().choice(seq)

    def random_sample(self, population: list[Any], k: int) -> list[Any]:
        """
        Sample k unique elements from a population.

        Args:
            population: Population to sample from.
            k: Number of elements to sample.

        Returns:
            List of k unique elements.

        Raises:
            ValueError: If k > len(population).
        """
        if k > len(population):
            raise ValueError("Sample size cannot exceed population size")
        if self._crypto_secure:
            # Crypto-safe sampling
            pop_copy = list(population)
            result = []
            for _ in range(k):
                idx = secrets.randbelow(len(pop_copy))
                result.append(pop_copy.pop(idx))
            return result
        return self._get_random().sample(population, k)

    def shuffle(self, seq: list[Any]) -> None:
        """
        Shuffle a list in place.

        Args:
            seq: List to shuffle.
        """
        if self._crypto_secure:
            # Fisher-Yates with crypto random
            for i in range(len(seq) - 1, 0, -1):
                j = secrets.randbelow(i + 1)
                seq[i], seq[j] = seq[j], seq[i]
        else:
            self._get_random().shuffle(seq)

    def random_bool(self, probability: float = 0.5) -> bool:
        """
        Generate a random boolean with given probability of True.

        Args:
            probability: Probability of returning True (0.0 to 1.0).

        Returns:
            Random boolean.
        """
        return self.random_float(0.0, 1.0) < probability

    def random_bytes(self, length: int) -> bytes:
        """
        Generate random bytes.

        Args:
            length: Number of bytes to generate.

        Returns:
            Random bytes.
        """
        if self._crypto_secure:
            return secrets.token_bytes(length)
        return bytes(self._get_random().randint(0, 255) for _ in range(length))

    def derive_seed(self, *args: Any) -> int:
        """
        Derive a deterministic seed from input values.

        Useful for creating reproducible sub-generators.

        Args:
            args: Values to hash into a seed.

        Returns:
            A 32-bit integer seed.
        """
        hasher = hashlib.sha256()
        for arg in args:
            hasher.update(str(arg).encode())
        return int(hasher.hexdigest()[:8], 16)

    @contextmanager
    def seeded_context(self, seed: int):
        """
        Context manager for temporary seed override.

        Args:
            seed: Temporary seed to use within the context.

        Example:
            >>> with sm.seeded_context(123):
            ...     value = sm.random_int(1, 100)
        """
        if self._crypto_secure:
            yield
            return

        rng = self._get_random()
        old_state = rng.getstate()
        try:
            rng.seed(seed)
            yield
        finally:
            rng.setstate(old_state)

    @property
    def is_crypto_secure(self) -> bool:
        """Check if crypto-secure mode is enabled."""
        return self._crypto_secure

    def clone(self) -> "SeedManager":
        """
        Create a copy of this seed manager.

        Returns:
            A new SeedManager with the same configuration.
        """
        return SeedManager(
            seed=self._default_seed, crypto_secure=self._crypto_secure
        )


class SeedContext:
    """
    Context manager for isolated seed management.

    Creates a temporary SeedManager for isolated operations.

    Example:
        >>> with SeedContext(42) as sm:
        ...     value = sm.random_int(1, 100)
    """

    def __init__(self, seed: int | None = None, crypto_secure: bool = False) -> None:
        """
        Initialize seed context.

        Args:
            seed: Optional seed for the context.
            crypto_secure: If True, use crypto-secure generation.
        """
        self._seed = seed
        self._crypto_secure = crypto_secure
        self._manager: SeedManager | None = None

    def __enter__(self) -> SeedManager:
        """Enter the context and return the seed manager."""
        self._manager = SeedManager(seed=self._seed, crypto_secure=self._crypto_secure)
        return self._manager

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Exit the context and clean up."""
        self._manager = None
