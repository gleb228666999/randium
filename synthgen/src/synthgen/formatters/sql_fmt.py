"""SQL Formatter."""

from __future__ import annotations
from typing import Any


class SQLFormatter:
    """Format data as SQL INSERT statements."""

    def __init__(self, table_name: str = "data") -> None:
        self._table_name = table_name

    def format(self, data: list[dict[str, Any]]) -> str:
        """Convert list of dicts to SQL INSERT statements."""
        if not data:
            return ""
        
        statements = []
        for record in data:
            columns = list(record.keys())
            values = [self._escape_value(record[col]) for col in columns]
            cols_str = ", ".join(columns)
            vals_str = ", ".join(values)
            statements.append(f"INSERT INTO {self._table_name} ({cols_str}) VALUES ({vals_str});")
        
        return "\n".join(statements)

    def _escape_value(self, value: Any) -> str:
        """Escape a value for SQL."""
        if value is None:
            return "NULL"
        elif isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        else:
            return f"'{str(value)}'"

    def to_file(self, data: list[dict[str, Any]], filepath: str) -> None:
        """Write SQL statements to file."""
        with open(filepath, 'w') as f:
            f.write(self.format(data))
