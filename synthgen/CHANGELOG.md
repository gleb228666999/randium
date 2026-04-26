# SynthGen Changelog

## [1.0.0] - 2024-01-01

### Added
- Initial release with comprehensive data generation capabilities
- Core modules: registry, seed manager, base provider, config
- Providers for 10 major categories:
  - Personal & Demographic (names, emails, phones, addresses, IDs)
  - Financial & Commerce (credit cards, IBAN, transactions, crypto)
  - Geographic & Spatial (coordinates, countries, IPs, MACs)
  - Temporal & Scheduling (dates, times, durations, events)
  - Technical & Network (URLs, UUIDs, JWTs, API keys)
  - Scientific & Mathematical (distributions, vectors, matrices)
  - Linguistic & Content (words, sentences, reviews, SEO)
  - IoT & Sensor (temperature, humidity, pressure, battery)
  - Gaming & Entertainment (dice, cards, NPCs, loot)
  - Custom & Extensible (regex, constraints, weighted choices)
- Generation engines: batch, stream, async
- Output formatters: JSON, CSV, YAML, SQL
- Schema validation support
- CLI tool for command-line usage
- Comprehensive documentation and examples

### Features
- Reproducible generation with seed control
- Thread-safe operations
- Plugin architecture for custom providers
- Memory-efficient streaming
- Async/await support
- Type hints throughout
