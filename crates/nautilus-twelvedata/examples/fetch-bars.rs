// -------------------------------------------------------------------------------------------------
//  Copyright (C) 2015-2026 Nautech Systems Pty Ltd. All rights reserved.
//  https://nautechsystems.io
//
//  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
//  You may not use this file except in compliance with the License.
//  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
// -------------------------------------------------------------------------------------------------

//! Example demonstrating how to fetch historical bar data from TwelveData.
//!
//! Run with:
//! ```bash
//! export TWELVEDATA_API_KEY="your_api_key_here"
//! cargo run --example fetch-bars
//! ```

use nautilus_twelvedata::{
    config::TwelveDataConfig,
    common::symbol::{format_instrument_id, normalize_symbol},
    data::{parse_bars, map_interval_to_bar_type},
    http::client::TwelveDataHttpClient,
};
use chrono::{Duration, Utc};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Get API key from environment variable
    let api_key = std::env::var("TWELVEDATA_API_KEY")
        .expect("TWELVEDATA_API_KEY environment variable not set");

    println!("=== TwelveData Adapter Example ===\n");

    // Create configuration
    let config = TwelveDataConfig::builder()
        .api_key(api_key)
        .http_timeout_secs(30)
        .default_interval("1hour".to_string())
        .build();

    // Create HTTP client
    let client = TwelveDataHttpClient::new(config)?;

    // Define symbol and exchange
    let symbol = "AAPL";
    let exchange = "NASDAQ";
    let instrument_id = format_instrument_id(symbol, exchange);

    println!("Symbol: {}", symbol);
    println!("Exchange: {}", exchange);
    println!("Instrument ID: {}", instrument_id);
    println!();

    // Fetch last 30 days of 1-hour bars
    let end = Utc::now();
    let start = end - Duration::days(30);
    let interval = "1h";  // TwelveData uses "1h" not "1hour"

    println!("Fetching {}-hour bars from {} to {}", interval, start, end);
    println!();

    // Fetch data
    let response = client
        .fetch_time_series_range(symbol, interval, start, end)
        .await?;

    println!("Fetched {} bars", response.values.len());
    println!();

    // Print metadata
    println!("Metadata:");
    println!("  Symbol: {}", response.meta.symbol);
    println!("  Interval: {}", response.meta.interval);
    println!("  Currency: {}", response.meta.currency);
    println!("  Exchange: {}", response.meta.exchange);
    println!("  Type: {}", response.meta.instrument_type);
    println!();

    // Parse bars
    let bars = parse_bars(&response, &instrument_id)?;
    println!("Parsed {} bars", bars.len());
    println!();

    // Print first few bars
    println!("First 5 bars:");
    for (i, bar) in bars.iter().take(5).enumerate() {
        println!(
            "  {}: {} - O:{:.2} H:{:.2} L:{:.2} C:{:.2} V:{}",
            i,
            bar.datetime,
            bar.open,
            bar.high,
            bar.low,
            bar.close,
            bar.volume
        );
    }
    println!();

    // Print last bar
    if let Some(last_bar) = bars.last() {
        println!("Last bar:");
        println!(
            "  {} - O:{:.2} H:{:.2} L:{:.2} C:{:.2} V:{}",
            last_bar.datetime,
            last_bar.open,
            last_bar.high,
            last_bar.low,
            last_bar.close,
            last_bar.volume
        );
    }
    println!();

    // Test different intervals
    println!("Testing different intervals:");
    let intervals = vec!["1min", "5min", "15min", "1hour", "1day"];
    for interval in intervals {
        let bar_type = map_interval_to_bar_type(interval);
        println!("  {} -> {}", interval, bar_type);
    }
    println!();

    // Test symbol normalization
    println!("Symbol normalization:");
    let test_symbols = vec!["aapl", "AAPL", "Msft", "tsla"];
    for sym in test_symbols {
        let normalized = normalize_symbol(sym);
        println!("  {} -> {}", sym, normalized);
    }

    Ok(())
}
