# nautilus-twelvedata

[![build](https://github.com/yourusername/TwelveAdapter/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/yourusername/TwelveAdapter/actions/workflows/build.yml)
[![crates.io version](https://img.shields.io/crates/v/nautilus-twelvedata.svg)](https://crates.io/crates/nautilus-twelvedata)
![license](https://img.shields.io/github/license/yourusername/TwelveAdapter?color=blue)

[NautilusTrader](https://nautilustrader.io) adapter for [TwelveData](https://twelvedata.com).

The `nautilus-twelvedata` crate provides a integration with the TwelveData API for accessing historical market data for US stocks.

## NautilusTrader

[NautilusTrader](https://nautilustrader.io) is an open-source, production-grade, Rust-native engine for multi-asset, multi-venue trading systems.

## Features

- Fetch historical OHLCV bar data from TwelveData
- Support for multiple intervals (1min, 5min, 15min, 1hour, 4hour, 1day)
- Parse data into NautilusTrader Bar objects
- Python bindings via PyO3
- High-precision mode support (128-bit values)

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
nautilus-twelvedata = "0.1.0"
```

## Usage

### Rust

```rust
use nautilus_twelvedata::{
    config::TwelveDataConfig,
    http::client::TwelveDataHttpClient,
};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = TwelveDataConfig::builder()
        .api_key("your_api_key")
        .build();
    
    let client = TwelveDataHttpClient::new(config)?;
    
    let response = client
        .fetch_time_series("AAPL", "1hour", Some(100))
        .await?;
    
    println!("Fetched {} bars", response.values.len());
    
    Ok(())
}
```

### Python

```python
from nautilus_trader.core.nautilus_pyo3 import TwelveDataHttpClient

client = TwelveDataHttpClient(api_key="your_api_key")
bars = await client.fetch_time_series("AAPL", "1hour", start_ns, end_ns)
print(f"Fetched {len(bars)} bars")
```

## Feature flags

- `python`: Enables Python bindings from [PyO3](https://pyo3.rs).
- `high-precision`: Enables high-precision mode (128-bit value types).

## Limitations

- Free tier: 800 API calls per day, 8 calls per minute
- No WebSocket support on free tier
- Historical data only (no real-time streaming)

## License

The source code for NautilusTrader is available on GitHub under the [GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html).

---

NautilusTrader™ is developed and maintained by Nautech Systems.
TwelveData adapter is a community contribution.

Use of this software is subject to the [Disclaimer](https://nautilustrader.io/legal/disclaimer/).
