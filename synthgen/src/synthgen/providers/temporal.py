"""
Temporal & Scheduling Data Provider.

Generates temporal data including:
- Dates and times
- Durations
- Recurring events
- Holidays
- Time series
- Business hours
"""

from __future__ import annotations

from typing import Any, Iterator
from datetime import date, datetime, time, timedelta
import calendar

from synthgen.core.base import BaseProvider
from synthgen.core.seed_manager import SeedManager


HOLIDAYS_US = {
    "New Year's Day": (1, 1),
    "Independence Day": (7, 4),
    "Christmas": (12, 25),
    "Thanksgiving": (11, -4),  # 4th Thursday of November
    "Labor Day": (9, -1),  # 1st Monday of September
}


class TemporalProvider(BaseProvider):
    """Provider for temporal and scheduling data."""

    def __init__(self, seed_manager: SeedManager | None = None) -> None:
        super().__init__(seed_manager)
        self._sm = seed_manager

    def _get_sm(self) -> SeedManager:
        if self._sm is None:
            raise RuntimeError("SeedManager not initialized")
        return self._sm

    def date(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> date:
        """Generate a random date."""
        sm = self._get_sm()
        if start_date is None:
            start_date = date(2020, 1, 1)
        if end_date is None:
            end_date = date.today()
        
        delta_days = (end_date - start_date).days
        random_days = sm.random_int(0, max(0, delta_days))
        return start_date + timedelta(days=random_days)

    def datetime(
        self,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> datetime:
        """Generate a random datetime."""
        sm = self._get_sm()
        d = self.date(
            start_datetime.date() if start_datetime else None,
            end_datetime.date() if end_datetime else None,
        )
        return datetime.combine(d, self.time())

    def time(self) -> time:
        """Generate a random time."""
        sm = self._get_sm()
        hour = sm.random_int(0, 23)
        minute = sm.random_int(0, 59)
        second = sm.random_int(0, 59)
        return time(hour, minute, second)

    def duration(self, min_seconds: int = 1, max_seconds: int = 86400) -> timedelta:
        """Generate a random duration."""
        sm = self._get_sm()
        seconds = sm.random_int(min_seconds, max_seconds)
        return timedelta(seconds=seconds)

    def timestamp(self, min_ts: int = 0, max_ts: int | None = None) -> int:
        """Generate a Unix timestamp."""
        sm = self._get_sm()
        if max_ts is None:
            max_ts = int(datetime.now().timestamp())
        return sm.random_int(min_ts, max_ts)

    def recurring_event(
        self,
        interval: str = "daily",
        count: int = 10,
        start_date: date | None = None,
    ) -> list[date]:
        """Generate recurring event dates."""
        sm = self._get_sm()
        if start_date is None:
            start_date = date.today()
        
        dates = [start_date]
        current = start_date
        
        for _ in range(count - 1):
            if interval == "daily":
                current += timedelta(days=1)
            elif interval == "weekly":
                current += timedelta(weeks=1)
            elif interval == "monthly":
                # Add ~30 days
                current += timedelta(days=sm.random_int(28, 31))
            elif interval == "yearly":
                try:
                    current = current.replace(year=current.year + 1)
                except ValueError:
                    current += timedelta(days=365)
            dates.append(current)
        
        return dates

    def business_hours(self) -> dict[str, time]:
        """Generate business hours."""
        sm = self._get_sm()
        open_hour = sm.random_int(8, 10)
        close_hour = sm.random_int(17, 21)
        return {
            "open": time(open_hour, 0),
            "close": time(close_hour, 0),
        }

    def generate(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Generate complete temporal profile."""
        return {
            "date": self.date().isoformat(),
            "datetime": self.datetime().isoformat(),
            "time": self.time().isoformat(),
            "duration_seconds": self.duration().total_seconds(),
            "timestamp": self.timestamp(),
            "business_hours": {
                "open": self.business_hours()["open"].isoformat(),
                "close": self.business_hours()["close"].isoformat(),
            },
        }
