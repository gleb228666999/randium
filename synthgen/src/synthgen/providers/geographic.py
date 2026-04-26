"""
Geographic & Spatial Data Provider.

Generates geographic data including:
- Coordinates (lat/lon)
- Countries, cities, regions
- ZIP/postal codes
- Timezones
- IP addresses
- MAC addresses
- GPS traces
"""

from __future__ import annotations

from typing import Any

from synthgen.core.base import BaseProvider
from synthgen.core.seed_manager import SeedManager


COUNTRIES = [
    {"name": "United States", "code": "US", "capital": "Washington D.C.", "continent": "North America"},
    {"name": "Canada", "code": "CA", "capital": "Ottawa", "continent": "North America"},
    {"name": "United Kingdom", "code": "GB", "capital": "London", "continent": "Europe"},
    {"name": "Germany", "code": "DE", "capital": "Berlin", "continent": "Europe"},
    {"name": "France", "code": "FR", "capital": "Paris", "continent": "Europe"},
    {"name": "Japan", "code": "JP", "capital": "Tokyo", "continent": "Asia"},
    {"name": "China", "code": "CN", "capital": "Beijing", "continent": "Asia"},
    {"name": "India", "code": "IN", "capital": "New Delhi", "continent": "Asia"},
    {"name": "Australia", "code": "AU", "capital": "Canberra", "continent": "Oceania"},
    {"name": "Brazil", "code": "BR", "capital": "Brasilia", "continent": "South America"},
    {"name": "Mexico", "code": "MX", "capital": "Mexico City", "continent": "North America"},
    {"name": "Italy", "code": "IT", "capital": "Rome", "continent": "Europe"},
    {"name": "Spain", "code": "ES", "capital": "Madrid", "continent": "Europe"},
    {"name": "South Korea", "code": "KR", "capital": "Seoul", "continent": "Asia"},
    {"name": "Russia", "code": "RU", "capital": "Moscow", "continent": "Europe"},
]

TIMEZONES = [
    "UTC", "America/New_York", "America/Los_Angeles", "America/Chicago",
    "Europe/London", "Europe/Paris", "Europe/Berlin", "Asia/Tokyo",
    "Asia/Shanghai", "Asia/Kolkata", "Australia/Sydney", "Pacific/Auckland"
]


class GeographicProvider(BaseProvider):
    """Provider for geographic and spatial data."""

    def __init__(self, seed_manager: SeedManager | None = None) -> None:
        super().__init__(seed_manager)
        self._sm = seed_manager

    def _get_sm(self) -> SeedManager:
        if self._sm is None:
            raise RuntimeError("SeedManager not initialized")
        return self._sm

    def coordinates(
        self,
        lat_range: tuple[float, float] = (-90.0, 90.0),
        lon_range: tuple[float, float] = (-180.0, 180.0),
    ) -> dict[str, float]:
        """Generate random coordinates."""
        sm = self._get_sm()
        lat = sm.random_float(lat_range[0], lat_range[1])
        lon = sm.random_float(lon_range[0], lon_range[1])
        return {"latitude": round(lat, 6), "longitude": round(lon, 6)}

    def country(self) -> dict[str, str]:
        """Generate country information."""
        sm = self._get_sm()
        return sm.random_choice(COUNTRIES)

    def city(self) -> str:
        """Generate a city name."""
        sm = self._get_sm()
        cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "London", "Berlin", "Paris", "Tokyo", "Beijing", "Mumbai",
            "Sydney", "Toronto", "Mexico City", "Sao Paulo"
        ]
        return sm.random_choice(cities)

    def timezone(self) -> str:
        """Generate a timezone."""
        sm = self._get_sm()
        return sm.random_choice(TIMEZONES)

    def ip_address(self, version: str = "v4") -> str:
        """Generate an IP address."""
        sm = self._get_sm()
        if version.lower() == "v4":
            return ".".join(str(sm.random_int(0, 255)) for _ in range(4))
        else:
            # IPv6
            groups = ["".join(str(sm.random_int(0, 15)) for _ in range(4)) for _ in range(8)]
            return ":".join(groups)

    def mac_address(self) -> str:
        """Generate a MAC address."""
        sm = self._get_sm()
        octets = [f"{sm.random_int(0, 255):02x}" for _ in range(6)]
        return ":".join(octets)

    def generate(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Generate complete geographic profile."""
        return {
            "coordinates": self.coordinates(),
            "country": self.country(),
            "city": self.city(),
            "timezone": self.timezone(),
            "ip_address": self.ip_address(),
            "mac_address": self.mac_address(),
        }
