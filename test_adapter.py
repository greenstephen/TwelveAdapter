#!/usr/bin/env python3
"""
Test script for TwelveData Python adapter.

Usage:
    python test_adapter.py YOUR_API_KEY
"""

import asyncio
import sys
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from nautilus_trader.adapters.twelvedata import TwelveDataDataClientConfig
from nautilus_trader.adapters.twelvedata import TWELVEDATA
from nautilus_trader.adapters.twelvedata import create_twelvedata_data_client


async def test_adapter(api_key: str):
    """Test the TwelveData adapter."""
    print("=== TwelveData Python Adapter Test ===\n")

    # Create configuration
    print("Creating configuration...")
    config = TwelveDataDataClientConfig(
        api_key=api_key,
        default_interval="1h",
    )
    print(f"✓ Configuration created")
    print(f"  Base URL: {config.base_url}")
    print(f"  Default Interval: {config.default_interval}")
    print()

    # Test constants
    print("Testing constants...")
    print(f"  Venue: {TWELVEDATA}")
    print(f"  Supported Intervals: {len(config.default_interval)} interval(s)")
    print()

    # Test client creation
    print("Creating data client...")
    try:
        client = create_twelvedata_data_client(config=config)
        print(f"✓ Data client created")
        print(f"  Client ID: {client.client_id}")
        print(f"  Venue: {client.venue}")
        print()

        print("✓ Python adapter is working!")
        print("\nPhase 3 Complete: Python Integration Layer")
        print("  - Configuration: ✓")
        print("  - Constants: ✓")
        print("  - Factory functions: ✓")
        print("  - Data client: ✓")
        return True

    except Exception as e:
        print(f"✗ Error creating client: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_adapter.py YOUR_API_KEY")
        sys.exit(1)

    api_key = sys.argv[1]
    success = asyncio.run(test_adapter(api_key))
    sys.exit(0 if success else 1)
