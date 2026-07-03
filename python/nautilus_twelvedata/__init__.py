"""
NautilusTrader TwelveData Adapter
High-performance market data adapter for TwelveData
"""

import os
from datetime import datetime
from typing import List, Dict, Optional

# Import the CFFI-based Rust extension
from .ffi import ffi
import os as _os

_lib = ffi.dlopen(_os.path.join(_os.path.dirname(__file__), 'libnautilus_twelvedata.so'))


class TwelveDataHttpClientPy:
    """
    TwelveData HTTP client wrapped from Rust extension.
    
    This is a Python wrapper around the Rust implementation.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the TwelveData HTTP client.
        
        Args:
            api_key: TwelveData API key
        """
        # For now, this is a placeholder - the actual Rust bindings
        # need to be properly exposed through PyO3
        self._api_key = api_key
        self._base_url = "https://api.twelvedata.com"
        self._default_interval = "1hour"
    
    @property
    def base_url(self) -> str:
        """Get the configured base URL."""
        return self._base_url
    
    @property
    def default_interval(self) -> str:
        """Get the default interval."""
        return self._default_interval
    
    @property
    def api_key(self) -> str:
        """Get the masked API key."""
        if len(self._api_key) > 4:
            return f"{self._api_key[:4]}****"
        return "****"
    
    def fetch_time_series(
        self,
        symbol: str,
        interval: str,
        outputsize: Optional[int] = None,
    ) -> List[Dict]:
        """
        Fetch time series data.
        
        Args:
            symbol: Trading symbol
            interval: Bar interval
            outputsize: Number of bars to fetch
        
        Returns:
            List of OHLCV bar dictionaries
        """
        # This would call the Rust implementation
        # For now, return empty list
        return []


__version__ = "0.1.1"
__all__ = ["TwelveDataHttpClientPy"]
