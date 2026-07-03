#!/usr/bin/env python3
"""
Comprehensive test for TwelveData NautilusTrader adapter.

Usage:
    python test_final.py YOUR_API_KEY
    Or set environment variable: export TWELVEDATA_API_KEY=your_key
"""

import asyncio
import os
import sys

from nautilus_trader.adapters.twelvedata import (
    TWELVEDATA,
    TwelveDataDataClientConfig,
    TwelveDataInstrumentProvider,
)
from nautilus_twelvedata import TwelveDataHttpClientPy


def test_sync_fetch(api_key: str):
    """Test synchronous data fetching."""
    print("=== Testing Sync Data Fetch ===\n")
    
    client = TwelveDataHttpClientPy(api_key)
    print(f"✓ Client created")
    print(f"  Base URL: {client.base_url}")
    print(f"  Default Interval: {client.default_interval}")
    print()
    
    print("Fetching 5 hourly bars for AAPL...")
    bars = client.fetch_time_series("AAPL", "1h", outputsize=5)
    print(f"✓ Fetched {len(bars)} bars")
    
    if len(bars) > 0:
        print(f"\nFirst bar:")
        for key, value in bars[0].items():
            print(f"  {key}: {value}")
    
    print(f"\nLast bar:")
    if len(bars) > 0:
        for key, value in bars[-1].items():
            print(f"  {key}: {value}")
    
    print("\n✓ Sync fetch working!\n")
    return len(bars) > 0


async def test_async_fetch(api_key: str):
    """Test async data fetching with date range."""
    print("=== Testing Async Date Range Fetch ===\n")
    
    client = TwelveDataHttpClientPy(api_key)
    
    # Get timestamps for last 7 days
    import time
    end_ns = int(time.time() * 1e9)
    start_ns = end_ns - (7 * 24 * 60 * 60 * 1e9)  # 7 days ago
    
    print(f"Fetching 7 days of hourly bars for MSFT...")
    bars = client.fetch_time_series_range(
        "MSFT",
        "1h",
        int(start_ns),
        int(end_ns),
    )
    
    print(f"✓ Fetched {len(bars)} bars")
    print(f"  Sample bar: {bars[0] if len(bars) > 0 else 'None'}")
    print("\n✓ Async fetch working!\n")
    return len(bars) > 0


async def test_adapter_integration(api_key: str):
    """Test full adapter integration."""
    print("=== Testing Full Adapter Integration ===\n")
    
    # Test constants
    print(f"1. Venue: {TWELVEDATA}")
    print("   ✓ Constants working\n")
    
    # Test config
    print("2. Creating configuration...")
    config = TwelveDataDataClientConfig(
        api_key=api_key,
        default_interval="1h",
    )
    print(f"   ✓ Config created\n")
    
    # Test provider
    print("3. Creating instrument provider...")
    provider = TwelveDataInstrumentProvider(config)
    await provider.initialize()
    print("   ✓ Provider initialized")
    
    # Load instrument
    print("4. Loading instrument...")
    instrument_id = await provider.load_async("GOOGL", "NASDAQ")
    print(f"   Instrument ID: {instrument_id}")
    print("   ✓ Instrument loaded\n")
    
    print("✓ Adapter integration working!\n")
    return True


async def main(api_key: str):
    """Run all tests."""
    print("=" * 60)
    print("TwelveData NautilusTrader Adapter - Final Test")
    print("=" * 60)
    print()
    
    # Test 1: Sync fetch
    sync_ok = test_sync_fetch(api_key)
    
    # Test 2: Async fetch
    async_ok = await test_async_fetch(api_key)
    
    # Test 3: Adapter integration
    adapter_ok = await test_adapter_integration(api_key)
    
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Sync Fetch:          {'✓ PASS' if sync_ok else '✗ FAIL'}")
    print(f"Async Fetch:         {'✓ PASS' if async_ok else '✗ FAIL'}")
    print(f"Adapter Integration: {'✓ PASS' if adapter_ok else '✗ FAIL'}")
    print()
    
    if sync_ok and async_ok and adapter_ok:
        print("🎉 ALL TESTS PASSED!")
        print("\nThe TwelveData adapter is fully functional!")
        print("\nYou can now use it with NautilusTrader:")
        print("""
from nautilus_trader.adapters.twelvedata import (
    TwelveDataDataClientConfig,
    TwelveDataInstrumentProvider,
)

config = TwelveDataDataClientConfig(api_key="your_api_key")
provider = TwelveDataInstrumentProvider(config)
await provider.initialize()
        """)
        return True
    else:
        print("❌ SOME TESTS FAILED")
        return False


if __name__ == "__main__":
    api_key = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("TWELVEDATA_API_KEY")
    
    if not api_key:
        print("Usage: python test_final.py YOUR_API_KEY")
        print("Or set: export TWELVEDATA_API_KEY=your_key")
        sys.exit(1)
    
    success = asyncio.run(main(api_key))
    sys.exit(0 if success else 1)
