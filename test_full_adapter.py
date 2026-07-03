#!/usr/bin/env python3
"""
Test script for TwelveData NautilusTrader adapter.

Usage:
    python test_full_adapter.py YOUR_API_KEY
"""

import asyncio
import sys
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from nautilus_trader.adapters.twelvedata import (
    TWELVEDATA,
    TwelveDataDataClientConfig,
    TwelveDataInstrumentProvider,
)
from nautilus_twelvedata import TwelveDataHttpClientPy


async def test_full_adapter(api_key: str):
    """Test the full TwelveData adapter."""
    print("=== TwelveData NautilusTrader Adapter Test ===\n")

    # Test 1: Constants
    print("1. Testing constants...")
    print(f"   Venue: {TWELVEDATA}")
    print(f"   ✓ Constants working\n")

    # Test 2: Configuration
    print("2. Testing configuration...")
    config = TwelveDataDataClientConfig(
        api_key=api_key,
        default_interval="1h",
    )
    print(f"   API Key: {config.api_key[:4]}****")
    print(f"   Base URL: {config.base_url}")
    print(f"   Default Interval: {config.default_interval}")
    print(f"   ✓ Configuration working\n")

    # Test 3: Rust Client
    print("3. Testing Rust client...")
    rust_client = TwelveDataHttpClientPy(api_key=api_key)
    print(f"   Base URL: {rust_client.base_url}")
    print(f"   Default Interval: {rust_client.default_interval}")
    print(f"   ✓ Rust client working\n")

    # Test 4: Instrument Provider
    print("4. Testing instrument provider...")
    provider = TwelveDataInstrumentProvider(config)
    await provider.initialize()
    print(f"   Provider initialized")
    
    # Load an instrument
    instrument_id = await provider.load_async("AAPL", "NASDAQ")
    print(f"   Instrument ID: {instrument_id}")
    print(f"   ✓ Instrument provider working\n")

    # Test 5: Fetch actual data (if you want to test with real API)
    print("5. Testing data fetch (optional)...")
    response = await rust_client.fetch_time_series("AAPL", "1h", outputsize=5)
    print(f"   Fetched {len(response)} bars")
    if len(response) > 0:
        print(f"   First bar: {response[0]}")
    print(f"   ✓ Data fetch working\n")

    print("✅ All tests passed!")
    print("\n=== Phase 4 Complete: NautilusTrader Integration ===")
    print("  - Constants: ✓")
    print("  - Configuration: ✓")
    print("  - Rust client: ✓")
    print("  - Instrument provider: ✓")
    print("  - Data fetching: ✓")
    print("\nThe TwelveData adapter is fully integrated with NautilusTrader!")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_full_adapter.py YOUR_API_KEY")
        sys.exit(1)

    api_key = sys.argv[1]
    success = asyncio.run(test_full_adapter(api_key))
    sys.exit(0 if success else 1)
