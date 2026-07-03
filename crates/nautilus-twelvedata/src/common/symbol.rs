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

//! Symbol mapping and normalization utilities.

use crate::common::consts::TWELVEDATA;
use ustr::Ustr;

/// Normalize a stock symbol to uppercase
pub fn normalize_symbol(symbol: &str) -> Ustr {
    Ustr::from(symbol.to_uppercase().as_str())
}

/// Format an instrument ID for TwelveData
/// 
/// # Arguments
/// * `symbol` - The stock symbol (will be normalized to uppercase)
/// * `exchange` - The exchange (e.g., "NASDAQ", "NYSE")
/// 
/// # Returns
/// A formatted instrument ID string in the format: `{SYMBOL}.{EXCHANGE}.{VENUE}`
/// 
/// # Examples
/// ```
/// use nautilus_twelvedata::common::symbol::format_instrument_id;
/// let id = format_instrument_id("aapl", "NASDAQ");
/// assert_eq!(id, "AAPL.NASDAQ.TWELVEDATA");
/// ```
pub fn format_instrument_id(symbol: &str, exchange: &str) -> String {
    let normalized = normalize_symbol(symbol);
    format!("{}.{}.{}", normalized, exchange.to_uppercase(), TWELVEDATA)
}

/// Parse an instrument ID to extract symbol and exchange
/// 
/// # Arguments
/// * `instrument_id` - The full instrument ID string
/// 
/// # Returns
/// A tuple of (symbol, exchange) if parsing succeeds
/// 
/// # Examples
/// ```
/// use nautilus_twelvedata::common::symbol::parse_instrument_id;
/// let (symbol, exchange) = parse_instrument_id("AAPL.NASDAQ.TWELVEDATA").unwrap();
/// assert_eq!(symbol, "AAPL");
/// assert_eq!(exchange, "NASDAQ");
/// ```
pub fn parse_instrument_id(instrument_id: &str) -> Option<(String, String)> {
    let parts: Vec<&str> = instrument_id.split('.').collect();
    
    if parts.len() >= 3 && parts[2] == TWELVEDATA {
        Some((parts[0].to_string(), parts[1].to_string()))
    } else {
        None
    }
}

/// Validate if a symbol is a valid US stock symbol
/// 
/// US stock symbols are typically 1-5 uppercase letters
pub fn is_valid_us_symbol(symbol: &str) -> bool {
    let normalized = symbol.to_uppercase();
    normalized.len() >= 1 && normalized.len() <= 5 && normalized.chars().all(|c| c.is_ascii_alphabetic())
}

/// Validate if an exchange is a valid US exchange
pub fn is_valid_us_exchange(exchange: &str) -> bool {
    matches!(
        exchange.to_uppercase().as_str(),
        "NASDAQ" | "NYSE" | "AMEX" | "BATS" | "ARCA"
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_normalize_symbol() {
        assert_eq!(normalize_symbol("aapl"), "AAPL");
        assert_eq!(normalize_symbol("MSFT"), "MSFT");
        assert_eq!(normalize_symbol("tsla"), "TSLA");
    }

    #[test]
    fn test_format_instrument_id() {
        assert_eq!(format_instrument_id("aapl", "NASDAQ"), "AAPL.NASDAQ.TWELVEDATA");
        assert_eq!(format_instrument_id("MSFT", "NYSE"), "MSFT.NYSE.TWELVEDATA");
    }

    #[test]
    fn test_parse_instrument_id() {
        let result = parse_instrument_id("AAPL.NASDAQ.TWELVEDATA");
        assert!(result.is_some());
        let (symbol, exchange) = result.unwrap();
        assert_eq!(symbol, "AAPL");
        assert_eq!(exchange, "NASDAQ");
    }

    #[test]
    fn test_parse_instrument_id_invalid() {
        assert!(parse_instrument_id("AAPL.NASDAQ").is_none());
        assert!(parse_instrument_id("AAPL.NASDAQ.BINANCE").is_none());
    }

    #[test]
    fn test_valid_us_symbol() {
        assert!(is_valid_us_symbol("AAPL"));
        assert!(is_valid_us_symbol("aapl"));
        assert!(is_valid_us_symbol("ABC"));
        assert!(!is_valid_us_symbol("AAPL123"));
        assert!(!is_valid_us_symbol(""));
    }

    #[test]
    fn test_valid_us_exchange() {
        assert!(is_valid_us_exchange("NASDAQ"));
        assert!(is_valid_us_exchange("NYSE"));
        assert!(is_valid_us_exchange("nasdaq"));
        assert!(!is_valid_us_exchange("BINANCE"));
    }
}
