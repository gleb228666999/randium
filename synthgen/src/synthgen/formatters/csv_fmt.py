"""CSV Formatter."""

from __future__ import annotations
import csv
import io
from typing import Any


class CSVFormatter:
    """Format data as CSV."""

    def format(self, data: list[dict[str, Any]], delimiter: str = ",") -> str:
        """Convert list of dicts to CSV string."""
        if not data:
            return ""
        
        output = io.StringIO()
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        for row in data:
            writer.writerow({k: str(v) if not isinstance(v, str) else v for k, v in row.items()})
        return output.getvalue()

    def to_file(self, data: list[dict[str, Any]], filepath: str, delimiter: str = ",") -> None:
        """Write data to CSV file."""
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            if data:
                fieldnames = list(data[0].keys())
                writer.writerow(fieldnames)
                for row in data:
                    writer.writerow([str(v) if not isinstance(v, (str, int, float)) else v for v in row.values()])
