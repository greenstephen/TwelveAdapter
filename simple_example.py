#!/usr/bin/env python3
"""
Simple complete example: Fetch data and use in a basic strategy.

This shows the full flow without requiring full NautilusTrader setup.
"""

import os
import sys
from datetime import datetime

from nautilus_twelvedata import TwelveDataHttpClientPy


def fetch_and_analyze(api_key: str, symbol: str = "AAPL"):
    """
    Fetch recent data and perform basic analysis.

    This is a simplified example showing how to use the data.
    """
    print(f"=== Fetching {symbol} Data ===\n")

    # Create client
    client = TwelveDataHttpClientPy(api_key=api_key)

    # Fetch last 20 hourly bars
    bars = client.fetch_time_series(symbol, "1h", outputsize=20)

    print(f"Fetched {len(bars)} bars\n")

    # Calculate simple moving averages
    closes = [bar['close'] for bar in bars]
    
    if len(closes) >= 10:
        short_ma = sum(closes[-5:]) / 5
        long_ma = sum(closes[-10:]) / 10
        
        print(f"5-period MA:  {short_ma:.2f}")
        print(f"10-period MA: {long_ma:.2f}")
        
        # Simple signal
        if short_ma > long_ma:
            print("Signal: BULLISH (short MA > long MA)")
        else:
            print("Signal: BEARISH (short MA < long MA)")
    
    print("\nRecent bars:")
    for i, bar in enumerate(bars[-5:]):
        dt = datetime.fromisoformat(bar['datetime'])
        print(f"  {dt.strftime('%H:%M')}: O={bar['open']:.2f} "
              f"H={bar['high']:.2f} L={bar['low']:.2f} "
              f"C={bar['close']:.2f} V={bar['volume']:,}")

    return bars


def main():
    """Main entry point."""
    api_key = os.environ.get("TWELVEDATA_API_KEY")
    
    if not api_key:
        print("Error: TWELVEDATA_API_KEY not set")
        print("Run: export TWELVEDATA_API_KEY=your_key")
        sys.exit(1)

    # Fetch and analyze AAPL
    bars = fetch_and_analyze(api_key, "AAPL")
    
    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Add this logic to your NautilusTrader strategy")
    print("2. Use on_bar() callback to receive real-time bars")
    print("3. Implement your trading rules")
    print("4. Submit orders using self.submit_market_order()")
    print()
    print("See example_strategy.py for a complete NautilusTrader strategy")
    print("See README_USAGE.md for file organization guidance")


if __name__ == "__main__":
    main()
