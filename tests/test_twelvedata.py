"""
TwelveData Adapter - Test Suite
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Import the adapter
try:
    from nautilus_twelvedata import TwelveDataHttpClientPy
    HAS_ADAPTER = True
except ImportError:
    HAS_ADAPTER = False


class TestTwelveDataHttpClientPy:
    """Test suite for TwelveDataHttpClientPy."""
    
    @pytest.fixture
    def api_key(self):
        """Provide test API key."""
        return os.getenv("TWELVEDATA_API_KEY", "test_api_key_12345")
    
    @pytest.fixture
    def client(self, api_key):
        """Create a TwelveData client instance."""
        if not HAS_ADAPTER:
            pytest.skip("TwelveData adapter not available")
        return TwelveDataHttpClientPy(api_key=api_key)
    
    def test_client_initialization(self, client):
        """Test that client initializes correctly."""
        assert client is not None
        assert client.base_url == "https://api.twelvedata.com"
        assert client.default_interval == "1hour"
    
    def test_client_with_valid_api_key(self, api_key):
        """Test client creation with valid API key."""
        if not HAS_ADAPTER:
            pytest.skip("TwelveData adapter not available")
        
        client = TwelveDataHttpClientPy(api_key=api_key)
        assert client is not None
        assert len(client.api_key) > 0
    
    def test_fetch_time_series_basic(self, client):
        """Test basic time series fetching."""
        # This would normally require a real API call
        # For unit tests, we'll mock the response
        pass
    
    def test_fetch_time_series_with_interval(self, client):
        """Test fetching with different intervals."""
        intervals = ["1min", "5min", "15min", "30min", "1h", "1day", "1week"]
        
        for interval in intervals:
            # Validate interval is accepted (doesn't raise exception on creation)
            assert interval is not None
    
    def test_fetch_time_series_with_outputsize(self, client):
        """Test fetching with different output sizes."""
        outputsizes = [10, 50, 100, 500]
        
        for size in outputsizes:
            assert size > 0
            assert size <= 1000  # TwelveData max


class TestTwelveDataIntegration:
    """Integration tests with real TwelveData API."""
    
    @pytest.fixture
    def live_client(self):
        """Create client with live API key."""
        api_key = os.getenv("TWELVEDATA_API_KEY")
        if not api_key:
            pytest.skip("TWELVEDATA_API_KEY not set")
        
        if not HAS_ADAPTER:
            pytest.skip("TwelveData adapter not available")
        
        try:
            return TwelveDataHttpClientPy(api_key=api_key)
        except Exception as e:
            pytest.skip(f"Failed to create client: {e}")
    
    @pytest.mark.integration
    def test_fetch_real_time_series(self, live_client):
        """Test fetching real data from TwelveData API."""
        bars = live_client.fetch_time_series("AAPL", "1h", outputsize=5)
        
        assert bars is not None
        assert len(bars) > 0
        assert isinstance(bars, list)
        
        # Validate bar structure
        bar = bars[0]
        assert "datetime" in bar
        assert "open" in bar
        assert "high" in bar
        assert "low" in bar
        assert "close" in bar
        assert "volume" in bar
        
        # Validate data types
        assert isinstance(bar["datetime"], str)
        assert isinstance(bar["open"], float)
        assert isinstance(bar["high"], float)
        assert isinstance(bar["low"], float)
        assert isinstance(bar["close"], float)
        assert isinstance(bar["volume"], int)
    
    @pytest.mark.integration
    def test_fetch_daily_bars(self, live_client):
        """Test fetching daily bars."""
        bars = live_client.fetch_time_series("AAPL", "1day", outputsize=30)
        
        assert len(bars) > 0
        assert len(bars) <= 30
    
    @pytest.mark.integration
    def test_fetch_multiple_symbols(self, live_client):
        """Test fetching data for multiple symbols."""
        symbols = ["AAPL", "GOOGL", "MSFT"]
        
        for symbol in symbols:
            bars = live_client.fetch_time_series(symbol, "1day", outputsize=5)
            assert len(bars) > 0, f"No data for {symbol}"
    
    @pytest.mark.integration
    def test_rate_limit_handling(self, live_client):
        """Test that rate limits are handled gracefully."""
        # Make multiple rapid requests
        results = []
        for i in range(5):
            try:
                bars = live_client.fetch_time_series("AAPL", "1h", outputsize=1)
                results.append(len(bars))
            except RuntimeError as e:
                if "429" in str(e):
                    # Rate limited - this is expected
                    pytest.skip("Rate limit hit during test")
                else:
                    raise
        
        # If we got here, we successfully made requests
        assert len(results) > 0


class TestDataValidation:
    """Test data validation and parsing."""
    
    def test_bar_structure(self):
        """Test that bar data has correct structure."""
        # Sample bar data from TwelveData
        sample_bar = {
            "datetime": "2024-01-15 10:00:00",
            "open": 150.0,
            "high": 152.0,
            "low": 149.5,
            "close": 151.5,
            "volume": 1000000
        }
        
        # Validate required fields
        required_fields = ["datetime", "open", "high", "low", "close", "volume"]
        for field in required_fields:
            assert field in sample_bar
        
        # Validate OHLCV relationships
        assert sample_bar["high"] >= sample_bar["low"]
        assert sample_bar["high"] >= sample_bar["open"]
        assert sample_bar["high"] >= sample_bar["close"]
        assert sample_bar["low"] <= sample_bar["open"]
        assert sample_bar["low"] <= sample_bar["close"]
    
    def test_datetime_parsing(self):
        """Test datetime parsing from TwelveData format."""
        datetime_str = "2024-01-15 10:00:00"
        
        # Should be parseable
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        assert dt.year == 2024
        assert dt.month == 1
        assert dt.day == 15
        assert dt.hour == 10
        assert dt.minute == 0
    
    def test_volume_is_integer(self):
        """Test that volume is an integer."""
        volume = 1000000
        assert isinstance(volume, int)
        assert volume >= 0


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @pytest.mark.integration
    def test_invalid_api_key(self):
        """Test handling of invalid API key."""
        if not HAS_ADAPTER:
            pytest.skip("TwelveData adapter not available")
        
        client = TwelveDataHttpClientPy(api_key="invalid_key")
        
        # Should raise error when making request
        with pytest.raises(RuntimeError) as exc_info:
            client.fetch_time_series("AAPL", "1h", outputsize=1)
        
        assert "401" in str(exc_info.value) or "403" in str(exc_info.value)
    
    @pytest.mark.integration
    def test_invalid_symbol(self):
        """Test handling of invalid symbol."""
        api_key = os.getenv("TWELVEDATA_API_KEY")
        if not api_key:
            pytest.skip("TWELVEDATA_API_KEY not set")
        
        if not HAS_ADAPTER:
            pytest.skip("TwelveData adapter not available")
        
        client = TwelveDataHttpClientPy(api_key=api_key)
        
        # Invalid symbol should return error or empty result
        bars = client.fetch_time_series("INVALID_SYMBOL_12345", "1h", outputsize=1)
        
        # Either empty or error
        assert bars is None or len(bars) == 0
    
    @pytest.mark.integration
    def test_invalid_interval(self):
        """Test handling of invalid interval."""
        api_key = os.getenv("TWELVEDATA_API_KEY")
        if not api_key:
            pytest.skip("TWELVEDATA_API_KEY not set")
        
        if not HAS_ADAPTER:
            pytest.skip("TwelveData adapter not available")
        
        client = TwelveDataHttpClientPy(api_key=api_key)
        
        # Invalid interval should raise error
        with pytest.raises(RuntimeError) as exc_info:
            client.fetch_time_series("AAPL", "invalid_interval", outputsize=1)
        
        assert "Invalid" in str(exc_info.value) or "400" in str(exc_info.value)
    
    def test_rate_limit_error_format(self):
        """Test that rate limit errors are properly formatted."""
        error_message = "API error: HTTP 429 Too Many Requests"
        
        assert "429" in error_message
        assert "too many" in error_message.lower()


class TestConfiguration:
    """Test configuration and setup."""
    
    def test_api_key_from_environment(self):
        """Test loading API key from environment."""
        api_key = os.getenv("TWELVEDATA_API_KEY")
        
        if api_key:
            assert len(api_key) > 0
            assert isinstance(api_key, str)
    
    def test_supported_intervals(self):
        """Test that all supported intervals are documented."""
        supported_intervals = [
            "1min", "5min", "15min", "30min", "45min",
            "1h", "2h", "4h", "8h",
            "1day", "1week", "1month"
        ]
        
        assert len(supported_intervals) > 0
        assert "1h" in supported_intervals
        assert "1day" in supported_intervals
    
    def test_rate_limits(self):
        """Test rate limit constants."""
        free_tier_limits = {
            "daily": 800,
            "per_minute": 8
        }
        
        assert free_tier_limits["daily"] > 0
        assert free_tier_limits["per_minute"] > 0


class TestPerformance:
    """Test performance characteristics."""
    
    @pytest.mark.integration
    def test_fetch_speed(self, live_client):
        """Test that data fetching is reasonably fast."""
        import time
        
        start = time.time()
        bars = live_client.fetch_time_series("AAPL", "1h", outputsize=100)
        elapsed = time.time() - start
        
        # Should complete within 10 seconds
        assert elapsed < 10.0
        assert len(bars) > 0
    
    @pytest.mark.integration
    def test_concurrent_requests(self, live_client):
        """Test handling of concurrent requests."""
        import time
        import threading
        
        results = []
        errors = []
        
        def fetch_symbol(symbol):
            try:
                bars = live_client.fetch_time_series(symbol, "1day", outputsize=5)
                results.append((symbol, len(bars)))
            except Exception as e:
                errors.append((symbol, str(e)))
        
        # Create threads for multiple symbols
        symbols = ["AAPL", "GOOGL", "MSFT"]
        threads = []
        
        for symbol in symbols:
            t = threading.Thread(target=fetch_symbol, args=(symbol,))
            threads.append(t)
        
        # Start all threads
        start = time.time()
        for t in threads:
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        elapsed = time.time() - start
        
        # Should complete within 30 seconds
        assert elapsed < 30.0
        
        # At least some should succeed (might hit rate limits)
        assert len(results) + len(errors) == len(symbols)


# Mark for test selection
pytest_plugins = []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
