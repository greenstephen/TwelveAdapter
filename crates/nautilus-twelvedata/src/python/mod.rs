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

//! Python bindings for TwelveData adapter.

use crate::config::TwelveDataConfig;
use crate::data::parse_bars;
use crate::http::client::TwelveDataHttpClient;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use std::sync::Arc;

/// Python-exposed TwelveData HTTP client
#[pyclass]
#[derive(Debug)]
pub struct TwelveDataHttpClientPy {
    inner: Arc<TwelveDataHttpClient>,
}

#[pymethods]
impl TwelveDataHttpClientPy {
    /// Create a new TwelveData HTTP client
    #[new]
    fn new(api_key: String) -> PyResult<Self> {
        let config = TwelveDataConfig::builder()
            .api_key(api_key)
            .build();
        
        let client = TwelveDataHttpClient::new(config)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
        
        Ok(Self {
            inner: Arc::new(client),
        })
    }

    /// Get the configured base URL
    #[getter]
    fn base_url(&self) -> String {
        self.inner.config.base_url.clone()
    }

    /// Get the default interval
    #[getter]
    fn default_interval(&self) -> String {
        self.inner.config.default_interval.clone()
    }

    /// Get the API key (masked)
    #[getter]
    fn api_key(&self) -> String {
        match &self.inner.config.api_key {
            Some(key) if key.len() > 4 => format!("{}****", &key[..4]),
            _ => "****".to_string(),
        }
    }

    /// Fetch time series data (synchronous wrapper)
    fn fetch_time_series(
        &self,
        symbol: String,
        interval: String,
        outputsize: Option<usize>,
    ) -> PyResult<Vec<PyObject>> {
        let rt = tokio::runtime::Runtime::new()
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
        
        let response = rt.block_on(async {
            self.inner
                .fetch_time_series(&symbol, &interval, outputsize)
                .await
        })
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

        let bars = parse_bars(&response, &format!("{}.NASDAQ.TWELVEDATA", symbol))
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

        // Convert bars to Python list of dicts
        Python::with_gil(|py| {
            let py_bars: Vec<PyObject> = bars
                .into_iter()
                .map(|bar| {
                    let dict = PyDict::new(py);
                    dict.set_item("datetime", bar.datetime.to_rfc3339())?;
                    dict.set_item("open", bar.open)?;
                    dict.set_item("high", bar.high)?;
                    dict.set_item("low", bar.low)?;
                    dict.set_item("close", bar.close)?;
                    dict.set_item("volume", bar.volume)?;
                    dict.set_item("ts_event", bar.ts_event)?;
                    Ok(dict.into())
                })
                .collect::<PyResult<_>>()?;

            Ok(py_bars)
        })
    }

    /// Fetch time series data with date range (synchronous wrapper)
    fn fetch_time_series_range(
        &self,
        symbol: String,
        interval: String,
        start_ns: u64,
        end_ns: u64,
    ) -> PyResult<Vec<PyObject>> {
        let rt = tokio::runtime::Runtime::new()
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
        
        let start = chrono::DateTime::from_timestamp(
            (start_ns / 1_000_000_000) as i64,
            (start_ns % 1_000_000_000) as u32,
        )
        .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid start timestamp"))?;
        
        let end = chrono::DateTime::from_timestamp(
            (end_ns / 1_000_000_000) as i64,
            (end_ns % 1_000_000_000) as u32,
        )
        .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid end timestamp"))?;

        let response = rt.block_on(async {
            self.inner
                .fetch_time_series_range(&symbol, &interval, start, end)
                .await
        })
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

        let bars = parse_bars(&response, &format!("{}.NASDAQ.TWELVEDATA", symbol))
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

        // Convert bars to Python list of dicts
        Python::with_gil(|py| {
            let py_bars: Vec<PyObject> = bars
                .into_iter()
                .map(|bar| {
                    let dict = PyDict::new(py);
                    dict.set_item("datetime", bar.datetime.to_rfc3339())?;
                    dict.set_item("open", bar.open)?;
                    dict.set_item("high", bar.high)?;
                    dict.set_item("low", bar.low)?;
                    dict.set_item("close", bar.close)?;
                    dict.set_item("volume", bar.volume)?;
                    dict.set_item("ts_event", bar.ts_event)?;
                    Ok(dict.into())
                })
                .collect::<PyResult<_>>()?;

            Ok(py_bars)
        })
    }
}

/// Python module entry point
#[pymodule]
fn nautilus_twelvedata(m: &Bound<PyModule>) -> PyResult<()> {
    m.add_class::<TwelveDataHttpClientPy>()?;
    Ok(())
}
