# Quick Reference Guide

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/nautilus-twelvedata.git
cd nautilus-twelvedata

# Setup environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install nautilus-trader maturin

# Build and install
maturin develop --release
```

## Basic Usage

```python
from nautilus_twelvedata import TwelveDataHttpClientPy

# Initialize
client = TwelveDataHttpClientPy(api_key="your_key")

# Fetch bars
bars = client.fetch_time_series("AAPL", "1h", outputsize=100)

# Access data
for bar in bars:
    print(f"{bar['datetime']}: ${bar['close']}")
```

## Supported Intervals

| Interval | Description      |
|----------|------------------|
| `1min`   | 1-minute bars    |
| `5min`   | 5-minute bars    |
| `15min`  | 15-minute bars   |
| `30min`  | 30-minute bars   |
| `1h`     | 1-hour bars      |
| `1day`   | Daily bars       |
| `1week`  | Weekly bars      |
| `1month` | Monthly bars     |

## API Rate Limits

- **Free Tier**: 800 requests/day, 8 requests/minute
- **Starter**: 8,000 requests/day, 80 requests/minute
- **Standard**: 80,000 requests/day, 800 requests/minute

## Common Operations

### Fetch Multiple Symbols
```python
symbols = ["AAPL", "GOOGL", "MSFT"]
for symbol in symbols:
    bars = client.fetch_time_series(symbol, "1day", outputsize=30)
    print(f"{symbol}: ${bars[-1]['close']:.2f}")
```

### Date Range Query
```python
from datetime import datetime

start = datetime(2024, 1, 1)
end = datetime(2024, 1, 31)

bars = client.fetch_time_series_range(
    "AAPL", "1day",
    start_ns=int(start.timestamp() * 1e9),
    end_ns=int(end.timestamp() * 1e9)
)
```

### Error Handling
```python
try:
    bars = client.fetch_time_series("AAPL", "1h")
except Exception as e:
    if "429" in str(e):
        print("Rate limit exceeded")
    elif "401" in str(e):
        print("Invalid API key")
    else:
        print(f"Error: {e}")
```

## Environment Variables

```bash
export TWELVEDATA_API_KEY="your_api_key"
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=nautilus_twelvedata

# Specific test
pytest tests/test_client.py -v
```

## Examples

```bash
# Basic usage
python examples/basic_usage.py

# Advanced analysis (requires pandas/matplotlib)
python examples/advanced_analysis.py --plot
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | Run `maturin develop` |
| Rate limit (429) | Wait 1 minute or upgrade plan |
| Invalid key (401) | Check your API key |
| Invalid interval | Use supported intervals (see table) |

## Support

- [GitHub Issues](https://github.com/yourusername/nautilus-twelvedata/issues)
- [Documentation](https://github.com/yourusername/nautilus-twelvedata#readme)
- [Changelog](https://github.com/yourusername/nautilus-twelvedata/blob/main/CHANGELOG.md)
