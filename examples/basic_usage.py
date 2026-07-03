#!/usr/bin/env python3
"""
Basic Usage Example - Fetch and display market data
"""

import os
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from nautilus_twelvedata import TwelveDataHttpClientPy


def main():
    """Fetch and display market data."""
    # Get API key from environment
    api_key = os.getenv("TWELVEDATA_API_KEY")
    
    if not api_key:
        print("Error: TWELVEDATA_API_KEY not set")
        print("Set it with: export TWELVEDATA_API_KEY='your_key'")
        sys.exit(1)
    
    print("=" * 70)
    print("TwelveData Adapter - Basic Usage Example")
    print("=" * 70)
    
    # Initialize client
    print("\nInitializing TwelveData client...")
    client = TwelveDataHttpClientPy(api_key=api_key)
    print(f"✓ Client initialized")
    print(f"  Base URL: {client.base_url}")
    print(f"  Default Interval: {client.default_interval}")
    
    # Fetch 1-hour bars
    print("\nFetching 1-hour bars for AAPL...")
    bars = client.fetch_time_series("AAPL", "1h", outputsize=10)
    
    if not bars:
        print("✗ No data returned")
        return
    
    print(f"✓ Fetched {len(bars)} bars")
    print("\n" + "-" * 70)
    print("Latest 5 bars:")
    print("-" * 70)
    
    # Display bars
    for i, bar in enumerate(bars[-5:]):
        print(f"\nBar {i+1}:")
        print(f"  DateTime: {bar['datetime']}")
        print(f"  Open:     ${bar['open']:.2f}")
        print(f"  High:     ${bar['high']:.2f}")
        print(f"  Low:      ${bar['low']:.2f}")
        print(f"  Close:    ${bar['close']:.2f}")
        print(f"  Volume:   {bar['volume']:,}")
    
    # Fetch daily bars
    print("\n" + "=" * 70)
    print("Fetching daily bars for AAPL...")
    daily_bars = client.fetch_time_series("AAPL", "1day", outputsize=30)
    
    if daily_bars:
        print(f"✓ Fetched {len(daily_bars)} daily bars")
        latest = daily_bars[-1]
        print(f"\nLatest daily bar:")
        print(f"  Date: {latest['datetime'][:10]}")
        print(f"  Close: ${latest['close']:.2f}")
        print(f"  Volume: {latest['volume']:,}")
    
    print("\n" + "=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
