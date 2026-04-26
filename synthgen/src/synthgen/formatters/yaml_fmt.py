"""YAML Formatter."""

from __future__ import annotations
from typing import Any


class YAMLFormatter:
    """Format data as YAML (simple implementation without external deps)."""

    def format(self, data: Any, indent: int = 0) -> str:
        """Convert data to YAML string."""
        return self._to_yaml(data, indent)

    def _to_yaml(self, data: Any, indent: int) -> str:
        """Recursive YAML conversion."""
        prefix = "  " * indent
        
        if isinstance(data, dict):
            if not data:
                return "{}"
            lines = []
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{prefix}{key}:")
                    lines.append(self._to_yaml(value, indent + 1))
                else:
                    lines.append(f"{prefix}{key}: {self._format_value(value)}")
            return "\n".join(lines)
        
        elif isinstance(data, list):
            if not data:
                return "[]"
            lines = []
            for item in data:
                if isinstance(item, (dict, list)):
                    lines.append(f"{prefix}-")
                    lines.append(self._to_yaml(item, indent + 1))
                else:
                    lines.append(f"{prefix}- {self._format_value(item)}")
            return "\n".join(lines)
        
        else:
            return f"{prefix}{self._format_value(data)}"

    def _format_value(self, value: Any) -> str:
        """Format a scalar value."""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, str):
            if any(c in value for c in ":#{}[]&*?|>'\"\n"):
                return f'"{value}"'
            return value
        else:
            return str(value)

    def to_file(self, data: Any, filepath: str) -> None:
        """Write data to YAML file."""
        with open(filepath, 'w') as f:
            f.write(self.format(data))
