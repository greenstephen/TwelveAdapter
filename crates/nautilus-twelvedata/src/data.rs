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

//! Data parsing utilities for converting TwelveData responses.

use crate::common::error::{Result, TwelveDataError};
use crate::http::models::{BarData, TwelveDataTimeSeriesResponse};
use chrono::{DateTime, Utc};

/// Simple bar structure for MVP (will be replaced with Nautilus Bar when integrated)
#[derive(Debug, Clone)]
pub struct Bar {
    pub instrument_id: String,
    pub datetime: DateTime<Utc>,
    pub open: f64,
    pub high: f64,
    pub low: f64,
    pub close: f64,
    pub volume: u64,
    pub ts_event: u64,
}

/// Parse a TwelveData BarData into a simple Bar
pub fn parse_bar(
    bar_data: &BarData,
    instrument_id: &str,
) -> Result<Bar> {
    let datetime = crate::http::client::TwelveDataHttpClient::parse_datetime(&bar_data.datetime_str)?;
    let ts_event = datetime.timestamp_nanos_opt()
        .ok_or_else(|| TwelveDataError::TimestampParsing {
            message: format!("Invalid timestamp for bar at {}", bar_data.datetime_str),
        })? as u64;
    
    Ok(Bar {
        instrument_id: instrument_id.to_string(),
        datetime,
        open: bar_data.open,
        high: bar_data.high,
        low: bar_data.low,
        close: bar_data.close,
        volume: bar_data.volume,
        ts_event,
    })
}

/// Parse all bars from a TwelveData response
pub fn parse_bars(
    response: &TwelveDataTimeSeriesResponse,
    instrument_id: &str,
) -> Result<Vec<Bar>> {
    let mut bars = Vec::with_capacity(response.values.len());
    
    for bar_data in &response.values {
        let bar = parse_bar(bar_data, instrument_id)?;
        bars.push(bar);
    }
    
    Ok(bars)
}

/// Map TwelveData interval to Nautilus BarType string
pub fn map_interval_to_bar_type(interval: &str) -> String {
    match interval.to_lowercase().as_str() {
        "1min" | "1m" => "1MIN".to_string(),
        "5min" | "5m" => "5MIN".to_string(),
        "15min" | "15m" => "15MIN".to_string(),
        "30min" | "30m" => "30MIN".to_string(),
        "45min" | "45m" => "45MIN".to_string(),
        "1h" | "1hour" => "1HR".to_string(),
        "2h" | "2hour" => "2HR".to_string(),
        "4h" | "4hour" => "4HR".to_string(),
        "8h" | "8hour" => "8HR".to_string(),
        "1day" | "1d" => "1DAY".to_string(),
        "1week" | "1w" => "1WEEK".to_string(),
        "1month" | "1mo" => "1MONTH".to_string(),
        _ => format!("{}BAR", interval.to_uppercase()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_map_interval_to_bar_type() {
        assert_eq!(map_interval_to_bar_type("1hour"), "1HR");
        assert_eq!(map_interval_to_bar_type("1min"), "1MIN");
        assert_eq!(map_interval_to_bar_type("5m"), "5MIN");
        assert_eq!(map_interval_to_bar_type("1day"), "1DAY");
        assert_eq!(map_interval_to_bar_type("invalid"), "INVALIDBAR");
    }

    #[test]
    fn test_parse_bar() {
        let bar_data = BarData {
            datetime_str: "2024-01-15 10:00:00".to_string(),
            open: 150.5,
            high: 151.2,
            low: 149.8,
            close: 150.9,
            volume: 1234567,
        };
        
        let bar = parse_bar(&bar_data, "AAPL.NASDAQ.TWELVEDATA").unwrap();
        assert_eq!(bar.instrument_id, "AAPL.NASDAQ.TWELVEDATA");
        assert_eq!(bar.open, 150.5);
        assert_eq!(bar.volume, 1234567);
    }
}
