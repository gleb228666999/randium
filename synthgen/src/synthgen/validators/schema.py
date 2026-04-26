"""Schema-based Data Validation and Generation."""

from __future__ import annotations
from typing import Any


class SchemaValidator:
    """Validates and generates data based on JSON Schema."""

    def __init__(self, schema: dict[str, Any]) -> None:
        self._schema = schema

    def validate(self, data: Any) -> tuple[bool, list[str]]:
        """Validate data against schema. Returns (is_valid, errors)."""
        errors = []
        self._validate_recursive(data, self._schema, "", errors)
        return len(errors) == 0, errors

    def _validate_recursive(
        self, data: Any, schema: dict, path: str, errors: list[str]
    ) -> None:
        """Recursively validate data."""
        schema_type = schema.get("type")
        
        if schema_type == "object" and isinstance(data, dict):
            props = schema.get("properties", {})
            required = schema.get("required", [])
            
            for req in required:
                if req not in data:
                    errors.append(f"Missing required field: {path}.{req}")
            
            for key, prop_schema in props.items():
                if key in data:
                    self._validate_recursive(data[key], prop_schema, f"{path}.{key}", errors)
        
        elif schema_type == "array" and isinstance(data, list):
            items_schema = schema.get("items", {})
            for i, item in enumerate(data):
                self._validate_recursive(item, items_schema, f"{path}[{i}]", errors)
        
        elif schema_type == "string" and not isinstance(data, str):
            errors.append(f"Expected string at {path}, got {type(data).__name__}")
        
        elif schema_type == "number" and not isinstance(data, (int, float)):
            errors.append(f"Expected number at {path}, got {type(data).__name__}")
        
        elif schema_type == "integer" and not isinstance(data, int):
            errors.append(f"Expected integer at {path}, got {type(data).__name__}")
        
        elif schema_type == "boolean" and not isinstance(data, bool):
            errors.append(f"Expected boolean at {path}, got {type(data).__name__}")

    def generate(self, count: int, generator: Any) -> list[dict[str, Any]]:
        """Generate data matching the schema."""
        results = []
        for _ in range(count):
            record = self._generate_from_schema(self._schema, generator)
            results.append(record)
        return results

    def _generate_from_schema(self, schema: dict, gen: Any) -> Any:
        """Generate a value from schema definition."""
        schema_type = schema.get("type", "string")
        
        if schema_type == "object":
            result = {}
            props = schema.get("properties", {})
            for key, prop_schema in props.items():
                result[key] = self._generate_from_schema(prop_schema, gen)
            return result
        
        elif schema_type == "array":
            items_schema = schema.get("items", {"type": "string"})
            length = schema.get("minItems", schema.get("maxItems", 5))
            return [self._generate_from_schema(items_schema, gen) for _ in range(length)]
        
        elif schema_type == "string":
            if "enum" in schema:
                return gen.personal.first_name()  # Simplified
            return gen.linguistic.word()
        
        elif schema_type == "number":
            return gen.scientific.uniform_distribution(
                schema.get("minimum", 0), schema.get("maximum", 100)
            )
        
        elif schema_type == "integer":
            return gen.custom.constrained_value(
                "int",
                min_val=schema.get("minimum"),
                max_val=schema.get("maximum"),
            )
        
        elif schema_type == "boolean":
            return gen.custom.constrained_value("bool")
        
        return None
