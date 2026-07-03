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

//! TwelveData adapter error types.

use thiserror::Error;

/// TwelveData adapter error type
#[derive(Debug, Error)]
pub enum TwelveDataError {
    #[error("HTTP error: {0}")]
    Http(#[from] reqwest::Error),

    #[error("JSON parsing error: {0}")]
    Json(#[from] serde_json::Error),

    #[error("Invalid configuration: {message}")]
    Configuration { message: String },

    #[error("Invalid symbol: {message}")]
    InvalidSymbol { message: String },

    #[error("Invalid interval: {message}")]
    InvalidInterval { message: String },

    #[error("API error: {message}")]
    Api { message: String },

    #[error("Rate limit exceeded: {message}")]
    RateLimit { message: String },

    #[error("Data parsing error: {message}")]
    DataParsing { message: String },

    #[error("Timestamp parsing error: {message}")]
    TimestampParsing { message: String },

    #[error("Not found: {message}")]
    NotFound { message: String },

    #[error("Unknown error: {message}")]
    Unknown { message: String },
}

/// Result type for TwelveData operations
pub type Result<T> = std::result::Result<T, TwelveDataError>;
