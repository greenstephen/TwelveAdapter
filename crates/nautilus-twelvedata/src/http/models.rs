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

//! TwelveData API request and response models.

use serde::{Deserialize, Serialize};

/// TwelveData API response for time series data
#[derive(Debug, Deserialize, Serialize)]
pub struct TwelveDataTimeSeriesResponse {
    /// Metadata about the request
    pub meta: TimeSeriesMeta,
    /// Array of bar data points
    pub values: Vec<BarData>,
    /// API status
    pub status: String,
}

/// Metadata for time series request
#[derive(Debug, Deserialize, Serialize)]
pub struct TimeSeriesMeta {
    /// Symbol requested
    pub symbol: String,
    /// Interval used
    pub interval: String,
    /// Currency of the instrument
    pub currency: String,
    /// Exchange timezone
    pub exchange_timezone: String,
    /// Exchange name
    pub exchange: String,
    /// Instrument type
    #[serde(rename = "type")]
    pub instrument_type: String,
}

/// Individual bar data point from TwelveData
#[derive(Debug, Deserialize, Serialize)]
pub struct BarData {
    /// Datetime string (e.g., "2024-01-15 10:00:00")
    #[serde(rename = "datetime")]
    pub datetime_str: String,
    /// Open price (as string in API response)
    #[serde(deserialize_with = "parse_float")]
    pub open: f64,
    /// High price (as string in API response)
    #[serde(deserialize_with = "parse_float")]
    pub high: f64,
    /// Low price (as string in API response)
    #[serde(deserialize_with = "parse_float")]
    pub low: f64,
    /// Close price (as string in API response)
    #[serde(deserialize_with = "parse_float")]
    pub close: f64,
    /// Volume (as string in API response)
    #[serde(deserialize_with = "parse_u64")]
    pub volume: u64,
}

/// Helper function to deserialize string or number as f64
fn parse_float<'de, D>(deserializer: D) -> Result<f64, D::Error>
where
    D: serde::Deserializer<'de>,
{
    use serde::de::Error;
    let s = String::deserialize(deserializer)?;
    s.parse::<f64>()
        .map_err(|e| Error::custom(format!("Failed to parse float: {}", e)))
}

/// Helper function to deserialize string or number as u64
fn parse_u64<'de, D>(deserializer: D) -> Result<u64, D::Error>
where
    D: serde::Deserializer<'de>,
{
    use serde::de::Error;
    let s = String::deserialize(deserializer)?;
    s.parse::<u64>()
        .map_err(|e| Error::custom(format!("Failed to parse u64: {}", e)))
}

/// Query parameters for time series request
#[derive(Debug, Serialize)]
pub struct TimeSeriesQuery {
    /// Stock symbol (e.g., AAPL)
    pub symbol: String,
    /// Bar interval (e.g., 1hour, 1min, 1day)
    pub interval: String,
    /// Number of data points (max 1000 for free tier)
    #[serde(skip_serializing_if = "Option::is_none")]
    pub outputsize: Option<usize>,
    /// API key for authentication
    pub apikey: String,
}

impl TimeSeriesQuery {
    /// Create a new time series query
    pub fn new(symbol: &str, interval: &str, api_key: &str) -> Self {
        Self {
            symbol: symbol.to_string(),
            interval: interval.to_string(),
            outputsize: None,
            apikey: api_key.to_string(),
        }
    }

    /// Set the output size (number of data points)
    pub fn with_outputsize(mut self, size: usize) -> Self {
        self.outputsize = Some(size);
        self
    }
}

/// Error response from TwelveData API
#[derive(Debug, Deserialize)]
pub struct ApiErrorResponse {
    /// Error message
    pub message: String,
    /// Error status
    pub status: String,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_deserialize_time_series_response() {
        let json = r#"{
            "meta": {
                "symbol": "AAPL",
                "interval": "1hour",
                "currency": "USD",
                "exchange_timezone": "America/New_York",
                "exchange": "NASDAQ",
                "type": "Common Stock"
            },
            "values": [
                {
                    "datetime": "2024-01-15 10:00:00",
                    "open": "150.50000",
                    "high": "151.20000",
                    "low": "149.80000",
                    "close": "150.90000",
                    "volume": "1234567"
                }
            ],
            "status": "ok"
        }"#;

        let response: TwelveDataTimeSeriesResponse = serde_json::from_str(json).unwrap();
        assert_eq!(response.meta.symbol, "AAPL");
        assert_eq!(response.meta.interval, "1hour");
        assert_eq!(response.values.len(), 1);
        assert_eq!(response.values[0].open, 150.5);
    }

    #[test]
    fn test_time_series_query() {
        let query = TimeSeriesQuery::new("AAPL", "1hour", "test_key")
            .with_outputsize(100);

        assert_eq!(query.symbol, "AAPL");
        assert_eq!(query.interval, "1hour");
        assert_eq!(query.outputsize, Some(100));
    }
}
