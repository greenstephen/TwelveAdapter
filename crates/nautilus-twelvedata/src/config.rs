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

//! TwelveData adapter configuration.

use crate::common::error::{Result, TwelveDataError};

/// Configuration for TwelveData HTTP client
#[derive(Clone, Debug, bon::Builder)]
#[builder(builder_type = TwelveDataConfigBuilder)]
pub struct TwelveDataConfig {
    /// API key for TwelveData authentication
    pub api_key: Option<String>,

    /// Base URL for TwelveData API (optional, uses default if not provided)
    #[builder(default = "https://api.twelvedata.com".to_string())]
    pub base_url: String,

    /// HTTP request timeout in seconds
    #[builder(default = 30)]
    pub http_timeout_secs: u64,

    /// Default interval for bar data requests
    #[builder(default = "1hour".to_string())]
    pub default_interval: String,

    /// Enable high-precision mode (128-bit values)
    #[builder(default = true)]
    pub high_precision: bool,
}

impl TwelveDataConfig {
    /// Validate the configuration
    pub fn validate(&self) -> Result<()> {
        if self.api_key.is_none() || self.api_key.as_ref().unwrap().is_empty() {
            return Err(TwelveDataError::Configuration {
                message: "API key cannot be empty".to_string(),
            });
        }

        if self.http_timeout_secs == 0 {
            return Err(TwelveDataError::Configuration {
                message: "HTTP timeout must be greater than 0".to_string(),
            });
        }

        Ok(())
    }
}

impl Default for TwelveDataConfig {
    fn default() -> Self {
        Self::builder().build()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::consts::{DEFAULT_HTTP_TIMEOUT_SECS, TWELVEDATA_BASE_URL};

    #[test]
    fn test_config_builder() {
        let config = TwelveDataConfig::builder()
            .api_key("test_key".to_string())
            .build();

        assert_eq!(config.api_key, Some("test_key".to_string()));
        assert_eq!(config.base_url, TWELVEDATA_BASE_URL);
        assert_eq!(config.http_timeout_secs, DEFAULT_HTTP_TIMEOUT_SECS);
    }

    #[test]
    fn test_config_validation() {
        let config = TwelveDataConfig::builder()
            .api_key("".to_string())
            .build();

        assert!(config.validate().is_err());
    }
}
