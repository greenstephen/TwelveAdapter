# nautilus-twelvedata

[![PyPI version](https://badge.fury.io/py/nautilus-twelvedata.svg)](https://badge.fury.io/py/nautilus-twelvedata)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.13-blue.svg)](https://www.python.org)
[![NautilusTrader](https://img.shields.io/badge/nautilus_trader-1.230.0-purple.svg)](https://nautilustrader.io)
[![License](https://img.shields.io/badge/license-LGPL%20v3.0-green.svg)](LICENSE)

## Installation

### Install from PyPI (Recommended)

```bash
pip install nautilus-twelvedata
```

### Install from Source

```bash
git clone https://github.com/yourusername/nautilus-twelvedata.git
cd nautilus-twelvedata
pip install maturin
maturin develop --release
```

## Features

- ⚡ **Rust Performance** - Built with PyO3 for maximum speed
- 📊 **OHLCV Data** - Fetch historical bars with multiple intervals
- 🔄 **Rate Limiting** - Built-in handling of TwelveData API limits
- 🛡️ **Error Handling** - Robust error handling and retry logic
- 🔧 **NautilusTrader Native** - Full integration with NautilusTrader framework

## Requirements

- Python 3.10, 3.11, 3.12, or 3.13
- NautilusTrader 1.230.0+
- TwelveData API key (free tier available)

- Python 3.10, 3.11, 3.12, or 3.13
- Rust toolchain (latest stable)
- NautilusTrader 1.230.0+
- TwelveData API key (free tier available)

## Quick Start

### 1. Get Your TwelveData API Key

Sign up at [TwelveData](https://twelvedata.com/) to get your free API key.

### 2. Basic Usage

```python
from nautilus_twelvedata import TwelveDataHttpClientPy

# Initialize the client
client = TwelveDataHttpClientPy(api_key="your_api_key")

# Fetch 1-hour bars
bars = client.fetch_time_series("AAPL", "1h", outputsize=100)

# Access the data
for bar in bars:
    print(f"{bar['datetime']}: O={bar['open']} H={bar['high']} "
          f"L={bar['low']} C={bar['close']} V={bar['volume']}")
```

### 3. Using with NautilusTrader

```python
from nautilus_trader.adapters.twelvedata import TwelveDataHttpClientPy
from nautilus_trader.config import NautilusConfig

class TwelveDataConfig(NautilusConfig):
    """TwelveData configuration."""
    api_key: str
    base_url: str = "https://api.twelvedata.com"
    default_interval: str = "1h"

# Create adapter
config = TwelveDataConfig(api_key="your_api_key")
client = TwelveDataHttpClientPy(config.api_key)

# Fetch data for trading strategy
bars = client.fetch_time_series("AAPL", "1h", outputsize=100)
```

## Supported Intervals

TwelveData supports the following intervals:

| Interval | Description |
|----------|-------------|
| `1min`   | 1-minute bars |
| `5min`   | 5-minute bars |
| `15min`  | 15-minute bars |
| `30min`  | 30-minute bars |
| `45min`  | 45-minute bars |
| `1h`     | 1-hour bars |
| `2h`     | 2-hour bars |
| `4h`     | 4-hour bars |
| `8h`     | 8-hour bars |
| `1day`   | Daily bars |
| `1week`  | Weekly bars |
| `1month` | Monthly bars |

## Configuration

### Environment Variables

```bash
# TwelveData API Key
export TWELVEDATA_API_KEY="your_api_key_here"

# Optional: Custom base URL
export TWELVEDATA_BASE_URL="https://api.twelvedata.com"
```

### Python Configuration

```python
import os
from nautilus_twelvedata import TwelveDataHttpClientPy

# From environment
api_key = os.getenv("TWELVEDATA_API_KEY")
client = TwelveDataHttpClientPy(api_key=api_key)

# Or directly
client = TwelveDataHttpClientPy(
    api_key="your_api_key",
    interval="1h"  # Default interval
)
```

## Advanced Usage

### Fetching Time Series with Date Range

```python
from datetime import datetime

# Fetch bars for specific date range
start = datetime(2024, 1, 1)
end = datetime(2024, 1, 31)

# Convert to nanoseconds for Rust adapter
start_ns = int(start.timestamp() * 1e9)
end_ns = int(end.timestamp() * 1e9)

bars = client.fetch_time_series_range(
    symbol="AAPL",
    interval="1h",
    start_ns=start_ns,
    end_ns=end_ns
)
```

### Error Handling

```python
from nautilus_twelvedata import TwelveDataHttpClientPy

client = TwelveDataHttpClientPy(api_key="your_api_key")

try:
    bars = client.fetch_time_series("AAPL", "1h", outputsize=100)
    print(f"Fetched {len(bars)} bars")
except Exception as e:
    if "429" in str(e):
        print("Rate limit exceeded - wait before retrying")
    elif "401" in str(e):
        print("Invalid API key")
    else:
        print(f"Error: {e}")
```

### Rate Limiting

TwelveData free tier limits:
- **800 requests per day**
- **8 requests per minute**

The adapter handles errors gracefully, but you should implement your own rate limiting:

```python
import time

def fetch_with_rate_limit(client, symbol, interval, max_requests_per_minute=8):
    """Fetch bars with rate limiting."""
    delay = 60 / max_requests_per_minute
    
    for i in range(10):  # Fetch 10 times
        bars = client.fetch_time_series(symbol, interval, outputsize=100)
        print(f"Fetch {i+1}: {len(bars)} bars")
        time.sleep(delay)  # Respect rate limits
```

## Building from Source

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Python dependencies
pip install maturin nautilus-trader
```

### Build Commands

```bash
# Development build (faster, includes debug info)
maturin develop

# Release build (optimized, smaller)
maturin develop --release

# Build wheel for distribution
maturin build --release
```

## Testing

```bash
# Run tests
pytest tests/ -v

# Test with coverage
pytest tests/ -v --cov=nautilus_twelvedata

# Run specific test
pytest tests/test_client.py::test_fetch_time_series -v
```

## Examples

### Example 1: Fetch and Analyze Data

```python
from nautilus_twelvedata import TwelveDataHttpClientPy
import pandas as pd

client = TwelveDataHttpClientPy(api_key="your_api_key")

# Fetch data
bars = client.fetch_time_series("AAPL", "1h", outputsize=100)

# Convert to DataFrame
df = pd.DataFrame(bars)
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)

# Calculate simple moving average
df['SMA_20'] = df['close'].rolling(window=20).mean()

# Plot
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['close'], label='Close')
plt.plot(df.index, df['SMA_20'], label='SMA 20')
plt.legend()
plt.show()
```

### Example 2: Multiple Symbols

```python
symbols = ["AAPL", "GOOGL", "MSFT"]
client = TwelveDataHttpClientPy(api_key="your_api_key")

for symbol in symbols:
    bars = client.fetch_time_series(symbol, "1day", outputsize=30)
    latest = bars[-1] if bars else None
    if latest:
        print(f"{symbol}: ${latest['close']:.2f}")
```

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'nautilus_twelvedata'`
- **Solution**: Ensure you've built the adapter with `maturin develop`

**Issue**: `API error: HTTP 429`
- **Solution**: You've exceeded rate limits. Wait 1 minute or upgrade your TwelveData plan

**Issue**: `API error: HTTP 401`
- **Solution**: Check your API key is correct

**Issue**: `Invalid interval provided`
- **Solution**: Use supported intervals (see table above)

### Getting Help

- [GitHub Issues](https://github.com/yourusername/nautilus-twelvedata/issues)
- [NautilusTrader Discord](https://discord.gg/nautilustrader)
- [TwelveData Documentation](https://twelvedata.com/docs)

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/nautilus-twelvedata.git
cd nautilus-twelvedata
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install maturin pytest pytest-cov black flake8

# Build in development mode
maturin develop
```

## License

This project is licensed under the GNU Lesser General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [NautilusTrader](https://nautilustrader.io) - High-performance trading framework
- [TwelveData](https://twelvedata.com) - Market data API
- [PyO3](https://pyo3.rs) - Rust bindings for Python

## Roadmap

### v1.1 (Planned)
- [ ] WebSocket support for real-time data
- [ ] Additional data types (forex, crypto)
- [ ] Built-in caching layer
- [ ] More example strategies

### v1.2 (Future)
- [ ] Technical indicators integration
- [ ] Multiple venue support
- [ ] Docker containerization

---

**Happy Trading!** 📈
