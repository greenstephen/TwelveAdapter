# Contributing to NautilusTrader TwelveData Adapter

Thank you for your interest in contributing! This document provides guidelines and instructions.

## How Can I Contribute?

### 🐛 Report Bugs

Found a bug? Please report it by opening an issue with:

- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)

### ✨ Suggest Features

Have an idea? Open an issue with:

- Feature description
- Use case/example
- Why it's useful

### 🔧 Submit Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a PR

## Development Setup

### Prerequisites

```bash
# Python 3.10+
python --version

# Rust toolchain
rustc --version

# Required packages
pip install maturin pytest pytest-cov black flake8
```

### Clone and Setup

```bash
git clone https://github.com/yourusername/nautilus-twelvedata.git
cd nautilus-twelvedata
python -m venv venv
source venv/bin/activate
maturin develop
```

## Code Style

### Python

We use:
- **Black** for formatting
- **Flake8** for linting
- **isort** for imports

```bash
# Format code
black .

# Lint code
flake8 .

# Sort imports
isort .
```

### Rust

We use standard Rust conventions:
- `cargo fmt` for formatting
- `cargo clippy` for linting

```bash
# Format Rust code
cargo fmt

# Run clippy
cargo clippy
```

## Testing

### Run Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=nautilus_twelvedata

# Specific test file
pytest tests/test_client.py -v
```

### Write Tests

All new features must include tests:

```python
# tests/test_client.py
import pytest
from nautilus_twelvedata import TwelveDataHttpClientPy

def test_fetch_time_series():
    client = TwelveDataHttpClientPy(api_key="test")
    bars = client.fetch_time_series("AAPL", "1h", outputsize=10)
    assert len(bars) > 0
    assert 'datetime' in bars[0]
    assert 'close' in bars[0]
```

## Documentation

### Update README

If you add a feature, update the README:

- Add to features list
- Include usage example
- Update API reference

### Add Docstrings

All public functions must have docstrings:

```python
def fetch_time_series(
    self,
    symbol: str,
    interval: str,
    outputsize: int = 100,
) -> List[Dict]:
    """
    Fetch time series data for a symbol.
    
    Args:
        symbol: Trading symbol (e.g., "AAPL")
        interval: Bar interval (e.g., "1h", "1day")
        outputsize: Number of bars to fetch (max 1000)
    
    Returns:
        List of OHLCV bar dictionaries
    
    Raises:
        RuntimeError: If API request fails
    """
```

## Pull Request Process

1. **Title**: Clear, descriptive title
2. **Description**: 
   - What changes?
   - Why these changes?
   - How to test?
3. **Checklist**:
   - [ ] Code follows style guidelines
   - [ ] Tests added and passing
   - [ ] Documentation updated
   - [ ] No new warnings
   - [ ] Changelog entry added

## Code Review

- Be respectful and constructive
- Review within 48 hours when possible
- Address feedback promptly

## Questions?

Join our [Discord](https://discord.gg/nautilustrader) or open a discussion issue.

---

Thank you for contributing! 🙏
