# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of TwelveData adapter for NautilusTrader
- Rust-based implementation using PyO3
- Support for multiple time intervals
- Rate limit error handling
- Comprehensive error handling and logging

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [1.0.0] - 2026-07-02

### Added
- Initial stable release
- Core functionality:
  - `fetch_time_series()` for OHLCV data
  - `fetch_time_series_range()` for date range queries
  - Multiple interval support (1min to 1month)
- Rust performance optimization
- TwelveData API integration
- NautilusTrader compatibility
- Example usage documentation
- Error handling for rate limits (429)
- Authentication error handling (401)
- Basic test suite

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- API key validation
- Input sanitization

---

## Version History

| Version | Release Date | Status |
|---------|--------------|--------|
| 1.0.0   | 2026-07-02   | Stable |

## Upcoming Features

### Planned for v1.1
- WebSocket support for real-time data
- Built-in caching layer
- Additional data types (forex, crypto)
- More comprehensive test coverage

### Planned for v1.2
- Technical indicators integration
- Multiple venue support
- Docker containerization
- PyPI package distribution

---

[Unreleased]: https://github.com/yourusername/nautilus-twelvedata/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/nautilus-twelvedata/releases/tag/v1.0.0
