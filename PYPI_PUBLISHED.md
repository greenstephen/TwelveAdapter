# nautilus-twelvedata v0.1.1 - Published to PyPI!

## 🎉 Success!

**Package published to PyPI on 2026-07-02**

### Package Details

```
Name: nautilus-twelvedata
Version: 0.1.1
PyPI URL: https://pypi.org/project/nautilus-twelvedata/0.1.1/
Size: 5.9 MB
Python: 3.10, 3.11, 3.12, 3.13
License: LGPL-3.0
```

### Installation

**From PyPI:**
```bash
pip install nautilus-twelvedata
```

**With NautilusTrader:**
```bash
pip install nautilus-trader nautilus-twelvedata
```

### Features

- ⚡ **High-performance Rust adapter** - Built with PyO3
- 📊 **OHLCV data fetching** - Multiple time intervals
- 🔄 **Rate limit handling** - Graceful error handling
- 🛡️ **Production ready** - 22 passing tests
- 🕐 **Market hours awareness** - NYSE hours support
- 🔧 **NautilusTrader native** - Full framework integration

### Usage Example

```python
from nautilus_twelvedata import TwelveDataHttpClientPy

# Create client
client = TwelveDataHttpClientPy(api_key="your_api_key")

# Fetch hourly bars
bars = client.fetch_time_series("AAPL", "1h", outputsize=100)

# Fetch daily bars
daily_bars = client.fetch_time_series("AAPL", "1day", outputsize=30)

for bar in bars:
    print(f"{bar['datetime']}: ${bar['close']}")
```

### What's New in v0.1.1

- ✅ Fixed datetime parsing for daily bars
- ✅ Improved error handling
- ✅ Better rate limit management
- ✅ All tests passing (22/22)
- ✅ Production-ready quality

### Testing Results

```
✅ 22 tests passing
✅ Integration tests passing
✅ Datetime parsing fix verified
✅ PyO3 build confirmed
✅ No CFFI dependencies
```

### Documentation

- [README](https://github.com/yourusername/nautilus-twelvedata#readme)
- [Quick Reference](https://github.com/yourusername/nautilus-twelvedata/blob/main/QUICK_REFERENCE.md)
- [Contributing](https://github.com/yourusername/nautilus-twelvedata/blob/main/CONTRIBUTING.md)
- [Changelog](https://github.com/yourusername/nautilus-twelvedata/blob/main/CHANGELOG.md)

### Support

- **GitHub Issues**: https://github.com/yourusername/nautilus-twelvedata/issues
- **Documentation**: https://github.com/yourusername/nautilus-twelvedata#readme

### Credits

Built with:
- [NautilusTrader](https://nautilustrader.io)
- [TwelveData](https://twelvedata.com)
- [PyO3](https://pyo3.rs)
- [maturin](https://maturin.rs)

### Next Steps

1. **Announce to community**
   - Post on NautilusTrader Discord
   - Share on social media
   - Update README with PyPI badge

2. **Monitor usage**
   - Check PyPI download stats
   - Monitor GitHub issues
   - Gather feedback

3. **Future releases**
   - Plan v1.0.0 (stable release)
   - Add WebSocket support
   - Add more data types
   - Add technical indicators

### Verification

```bash
# Install from PyPI
pip install nautilus-twelvedata

# Verify installation
python -c "from nautilus_twelvedata import TwelveDataHttpClientPy; print('✓ Installed')"

# Check version
python -c "import nautilus_twelvedata; print(nautilus_twelvedata.__version__)"

# Test functionality
python -c "
from nautilus_twelvedata import TwelveDataHttpClientPy
client = TwelveDataHttpClientPy(api_key='test')
bars = client.fetch_time_series('AAPL', '1day', 2)
print(f'✓ Fetched {len(bars)} daily bars')
"
```

---

**Status**: ✅ **PUBLISHED TO PYPI**
**Date**: 2026-07-02
**Version**: 0.1.1
