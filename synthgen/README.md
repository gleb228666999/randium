# SynthGen - Production-Ready Random Data Generation Library

## Project Structure

```
synthgen/
├── src/
│   └── synthgen/
│       ├── __init__.py              # Package initialization, public API
│       ├── core/
│       │   ├── __init__.py
│       │   ├── registry.py          # Provider registry with lazy loading
│       │   ├── seed_manager.py      # Reproducible seed control
│       │   ├── base.py              # Base generator classes
│       │   └── config.py            # Configuration & constants
│       ├── providers/
│       │   ├── __init__.py
│       │   ├── personal.py          # Names, emails, phones, addresses
│       │   ├── financial.py         # Credit cards, IBAN, transactions
│       │   ├── geographic.py        # Coordinates, countries, IPs
│       │   ├── temporal.py          # Dates, times, schedules
│       │   ├── technical.py         # URLs, UUIDs, tokens
│       │   ├── scientific.py        # Distributions, vectors, matrices
│       │   ├── linguistic.py        # Words, sentences, content
│       │   ├── iot.py               # Sensor data, telemetry
│       │   ├── gaming.py            # Dice, cards, NPC stats
│       │   └── custom.py            # Regex, constraints, ML features
│       ├── engines/
│       │   ├── __init__.py
│       │   ├── batch.py             # Vectorized batch generation
│       │   ├── stream.py            # Memory-efficient streaming
│       │   └── async_engine.py      # Async support
│       ├── validators/
│       │   ├── __init__.py
│       │   ├── schema.py            # Pydantic/JSON Schema validation
│       │   └── constraints.py       # Range & distribution constraints
│       ├── formatters/
│       │   ├── __init__.py
│       │   ├── json_fmt.py          # JSON output
│       │   ├── csv_fmt.py           # CSV output
│       │   ├── yaml_fmt.py          # YAML output
│       │   ├── parquet_fmt.py       # Parquet output
│       │   └── sql_fmt.py           # SQL INSERT statements
│       └── utils/
│           ├── __init__.py
│           ├── helpers.py           # Utility functions
│           └── safety.py            # Safety markers & warnings
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_registry.py
│   ├── test_seed_manager.py
│   ├── test_providers/
│   │   ├── test_personal.py
│   │   ├── test_financial.py
│   │   └── ...
│   ├── test_engines/
│   │   ├── test_batch.py
│   │   └── test_stream.py
│   └── test_property_based.py       # Hypothesis tests
├── docs/
│   ├── index.md
│   ├── api_reference.md
│   ├── extension_guide.md
│   └── examples.md
├── examples/
│   ├── basic_usage.py
│   ├── cli_examples.py
│   ├── schema_driven.py
│   └── custom_provider.py
├── pyproject.toml                   # Build configuration
├── README.md
├── CHANGELOG.md
├── LICENSE
└── setup.cfg
```
