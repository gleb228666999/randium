"""Constraint-based Validation."""

from __future__ import annotations
from typing import Any


class ConstraintValidator:
    """Validates data against constraints."""

    def __init__(self, constraints: dict[str, Any]) -> None:
        self._constraints = constraints

    def validate(self, value: Any, field_name: str = "") -> tuple[bool, list[str]]:
        """Validate a value against constraints."""
        errors = []
        
        if "type" in self._constraints:
            expected_type = self._constraints["type"]
            type_map = {"int": int, "float": (int, float), "str": str, "bool": bool, "list": list, "dict": dict}
            if expected_type in type_map and not isinstance(value, type_map[expected_type]):
                errors.append(f"{field_name}: Expected {expected_type}, got {type(value).__name__}")
        
        if "min" in self._constraints and isinstance(value, (int, float)):
            if value < self._constraints["min"]:
                errors.append(f"{field_name}: Value {value} below minimum {self._constraints['min']}")
        
        if "max" in self._constraints and isinstance(value, (int, float)):
            if value > self._constraints["max"]:
                errors.append(f"{field_name}: Value {value} above maximum {self._constraints['max']}")
        
        if "min_length" in self._constraints and isinstance(value, (str, list)):
            if len(value) < self._constraints["min_length"]:
                errors.append(f"{field_name}: Length {len(value)} below minimum {self._constraints['min_length']}")
        
        if "max_length" in self._constraints and isinstance(value, (str, list)):
            if len(value) > self._constraints["max_length"]:
                errors.append(f"{field_name}: Length {len(value)} above maximum {self._constraints['max_length']}")
        
        if "pattern" in self._constraints and isinstance(value, str):
            import re
            if not re.match(self._constraints["pattern"], value):
                errors.append(f"{field_name}: Value does not match pattern {self._constraints['pattern']}")
        
        if "enum" in self._constraints and value not in self._constraints["enum"]:
            errors.append(f"{field_name}: Value {value} not in allowed values {self._constraints['enum']}")
        
        return len(errors) == 0, errors
