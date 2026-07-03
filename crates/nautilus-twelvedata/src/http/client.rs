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

//! TwelveData HTTP client implementation.

use crate::common::consts::MAX_OUTPUTSIZE;
use crate::common::error::{Result, TwelveDataError};
use crate::config::TwelveDataConfig;
use crate::http::models::{
    BarData, TimeSeriesMeta, TimeSeriesQuery, TwelveDataTimeSeriesResponse,
};
use chrono::{DateTime, NaiveDate, NaiveDateTime, Utc};
use reqwest::Client;

/// HTTP client for TwelveData API
#[derive(Debug)]
pub struct TwelveDataHttpClient {
    pub(crate) config: TwelveDataConfig,
    client: Client,
}

impl TwelveDataHttpClient {
    /// Create a new TwelveData HTTP client
    pub fn new(config: TwelveDataConfig) -> Result<Self> {
        config.validate()?;

        let client = Client::builder()
            .timeout(std::time::Duration::from_secs(config.http_timeout_secs))
            .build()
            .map_err(|e| TwelveDataError::Http(e))?;

        Ok(Self { config, client })
    }

    /// Get the base URL for API requests
    fn get_base_url(&self) -> &str {
        &self.config.base_url
    }

    /// Build the time series endpoint URL
    fn build_time_series_url(&self) -> String {
        format!("{}/time_series", self.get_base_url())
    }

    /// Fetch time series data for a symbol
    pub async fn fetch_time_series(
        &self,
        symbol: &str,
        interval: &str,
        outputsize: Option<usize>,
    ) -> Result<TwelveDataTimeSeriesResponse> {
        let url = self.build_time_series_url();
        
        let api_key = self.config.api_key.as_ref().ok_or_else(|| TwelveDataError::Configuration {
            message: "API key not configured".to_string(),
        })?;
        
        let mut query = TimeSeriesQuery::new(symbol, interval, api_key);
        
        if let Some(size) = outputsize {
            query = query.with_outputsize(size.min(MAX_OUTPUTSIZE));
        }

        log::debug!("Fetching time series: symbol={}, interval={}", symbol, interval);

        let response = self
            .client
            .get(&url)
            .query(&query)
            .send()
            .await
            .map_err(|e| TwelveDataError::Http(e))?;

        // Check for HTTP errors
        if !response.status().is_success() {
            let status = response.status();
            let error_body = response.text().await.unwrap_or_default();
            return Err(TwelveDataError::Api {
                message: format!("HTTP {} - {}", status, error_body),
            });
        }

        // Parse response
        let data: TwelveDataTimeSeriesResponse = response
            .json()
            .await
            .map_err(|e| TwelveDataError::Http(e))?;

        // Check API status
        if data.status != "ok" {
            return Err(TwelveDataError::Api {
                message: format!("API error: {}", data.status),
            });
        }

        log::debug!(
            "Fetched {} bars for {} at interval {}",
            data.values.len(),
            symbol,
            interval
        );

        Ok(data)
    }

    /// Fetch time series data with date range
    pub async fn fetch_time_series_range(
        &self,
        symbol: &str,
        interval: &str,
        start: DateTime<Utc>,
        end: DateTime<Utc>,
    ) -> Result<TwelveDataTimeSeriesResponse> {
        // TwelveData doesn't support direct date range queries in time_series endpoint
        // We fetch with maximum outputsize and filter client-side
        // For MVP, we'll use outputsize parameter
        
        let outputsize = Some(1000); // Maximum for free tier
        let mut response = self.fetch_time_series(symbol, interval, outputsize).await?;
        
        // Filter by date range
        response.values.retain(|bar| {
            if let Ok(datetime) = Self::parse_datetime(&bar.datetime_str) {
                datetime >= start && datetime <= end
            } else {
                false
            }
        });

        Ok(response)
    }

    /// Parse TwelveData datetime string to DateTime<Utc>
    /// Note: TwelveData returns exchange timezone, we treat as UTC for MVP
    pub fn parse_datetime(datetime_str: &str) -> Result<DateTime<Utc>> {
        // Trim whitespace
        let trimmed = datetime_str.trim();
        
        // Check if it contains time component
        let naive = if trimmed.contains(' ') && trimmed.contains(':') {
            // Full datetime: "2024-01-15 10:00:00"
            NaiveDateTime::parse_from_str(trimmed, "%Y-%m-%d %H:%M:%S")
                .map_err(|e| TwelveDataError::TimestampParsing {
                    message: format!("Failed to parse datetime with time '{}': {}", trimmed, e),
                })?
        } else if trimmed.len() == 10 && trimmed.contains('-') {
            // Date only: "2024-01-15" - parse manually
            let parts: Vec<&str> = trimmed.split('-').collect();
            if parts.len() == 3 {
                let year = parts[0].parse::<i32>()
                    .map_err(|e| TwelveDataError::TimestampParsing {
                        message: format!("Invalid year in '{}': {}", trimmed, e),
                    })?;
                let month = parts[1].parse::<u32>()
                    .map_err(|e| TwelveDataError::TimestampParsing {
                        message: format!("Invalid month in '{}': {}", trimmed, e),
                    })?;
                let day = parts[2].parse::<u32>()
                    .map_err(|e| TwelveDataError::TimestampParsing {
                        message: format!("Invalid day in '{}': {}", trimmed, e),
                    })?;
                
                NaiveDate::from_ymd_opt(year, month, day)
                    .and_then(|d| d.and_hms_opt(0, 0, 0))
                    .ok_or_else(|| TwelveDataError::TimestampParsing {
                        message: format!("Invalid date '{}'", trimmed),
                    })?
            } else {
                return Err(TwelveDataError::TimestampParsing {
                    message: format!("Invalid date format '{}'", trimmed),
                });
            }
        } else {
            return Err(TwelveDataError::TimestampParsing {
                message: format!("Unrecognized datetime format '{}'", trimmed),
            });
        };

        Ok(DateTime::from_naive_utc_and_offset(naive, Utc))
    }

    /// Get metadata from time series response
    pub fn get_metadata(response: &TwelveDataTimeSeriesResponse) -> &TimeSeriesMeta {
        &response.meta
    }

    /// Get bar data from response
    pub fn get_bars(response: &TwelveDataTimeSeriesResponse) -> &[BarData] {
        &response.values
    }

    /// Check if response contains an error
    pub fn is_error(response: &TwelveDataTimeSeriesResponse) -> bool {
        response.status != "ok"
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::{Datelike, Timelike};

    #[test]
    fn test_parse_datetime() {
        let datetime_str = "2024-01-15 10:00:00";
        let result = TwelveDataHttpClient::parse_datetime(datetime_str);
        assert!(result.is_ok());
        
        let dt = result.unwrap();
        assert_eq!(dt.year(), 2024);
        assert_eq!(dt.month(), 1);
        assert_eq!(dt.day(), 15);
        assert_eq!(dt.hour(), 10);
        assert_eq!(dt.minute(), 0);
    }

    #[test]
    fn test_parse_datetime_invalid() {
        let datetime_str = "invalid-date";
        let result = TwelveDataHttpClient::parse_datetime(datetime_str);
        assert!(result.is_err());
    }

    #[test]
    fn test_build_url() {
        let config = TwelveDataConfig::builder()
            .api_key("test_key".to_string())
            .build();
        
        let client = TwelveDataHttpClient::new(config).unwrap();
        let url = client.build_time_series_url();
        
        assert!(url.contains("api.twelvedata.com"));
        assert!(url.contains("time_series"));
    }
}
