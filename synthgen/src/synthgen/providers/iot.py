"""IoT & Sensor Data Provider."""

from __future__ import annotations
from typing import Any
from synthgen.core.base import BaseProvider
from synthgen.core.seed_manager import SeedManager


class IoTProvider(BaseProvider):
    """Provider for IoT and sensor data."""

    def __init__(self, seed_manager: SeedManager | None = None) -> None:
        super().__init__(seed_manager)
        self._sm = seed_manager

    def _get_sm(self) -> SeedManager:
        if self._sm is None:
            raise RuntimeError("SeedManager not initialized")
        return self._sm

    def temperature(self, min_c: float = -20.0, max_c: float = 50.0) -> dict[str, Any]:
        """Generate temperature reading."""
        sm = self._get_sm()
        celsius = sm.random_float(min_c, max_c)
        fahrenheit = (celsius * 9/5) + 32
        return {"celsius": round(celsius, 2), "fahrenheit": round(fahrenheit, 2)}

    def humidity(self, min_pct: float = 0.0, max_pct: float = 100.0) -> float:
        """Generate humidity percentage."""
        sm = self._get_sm()
        return round(sm.random_float(min_pct, max_pct), 2)

    def pressure(self, min_hpa: float = 950.0, max_hpa: float = 1050.0) -> float:
        """Generate atmospheric pressure in hPa."""
        sm = self._get_sm()
        return round(sm.random_float(min_hpa, max_hpa), 2)

    def motion_detected(self, probability: float = 0.3) -> bool:
        """Generate motion detection event."""
        sm = self._get_sm()
        return sm.random_bool(probability)

    def battery_level(self, min_pct: float = 0.0, max_pct: float = 100.0) -> dict[str, Any]:
        """Generate battery level."""
        sm = self._get_sm()
        level = sm.random_float(min_pct, max_pct)
        status = "critical" if level < 10 else "low" if level < 30 else "normal" if level < 80 else "full"
        return {"level": round(level, 1), "status": status}

    def generate(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Generate complete IoT sensor profile."""
        return {
            "temperature": self.temperature(),
            "humidity": self.humidity(),
            "pressure": self.pressure(),
            "motion": self.motion_detected(),
            "battery": self.battery_level(),
        }
