"""JSON Formatter."""

from __future__ import annotations
import json
from typing import Any


class JSONFormatter:
    """Format data as JSON."""

    def format(self, data: Any, indent: int = 2) -> str:
        """Convert data to JSON string."""
        return json.dumps(data, indent=indent, default=str)

    def to_file(self, data: Any, filepath: str, indent: int = 2) -> None:
        """Write data to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=indent, default=str)
