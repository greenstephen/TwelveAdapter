#!/usr/bin/env python3
"""
Advanced Usage Example - Data analysis with pandas
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from nautilus_twelvedata import TwelveDataHttpClientPy

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    HAS_PANDAS = True
except ImportError:
    print("Note: pandas/matplotlib not installed - skipping analysis")
    HAS_PANDAS = False


def main():
    """Fetch and analyze market data."""
    # Get API key from environment
    api_key = os.getenv("TWELVEDATA_API_KEY")
    
    if not api_key:
        print("Error: TWELVEDATA_API_KEY not set")
        sys.exit(1)
    
    print("=" * 70)
    print("TwelveData Adapter - Advanced Analysis Example")
    print("=" * 70)
    
    # Initialize client
    print("\nInitializing TwelveData client...")
    client = TwelveDataHttpClientPy(api_key=api_key)
    
    # Fetch daily bars
    print("\nFetching 90 days of daily bars for AAPL...")
    bars = client.fetch_time_series("AAPL", "1day", outputsize=90)
    
    if not bars:
        print("✗ No data returned")
        return
    
    print(f"✓ Fetched {len(bars)} bars")
    
    if HAS_PANDAS:
        # Convert to DataFrame
        print("\nConverting to DataFrame...")
        df = pd.DataFrame(bars)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        
        # Calculate indicators
        print("Calculating technical indicators...")
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['SMA_50'] = df['close'].rolling(window=50).mean()
        df['ROC'] = df['close'].pct_change(periods=10) * 100
        
        # Display summary
        print("\n" + "-" * 70)
        print("Data Summary:")
        print("-" * 70)
        print(f"Date Range: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")
        print(f"Total Bars: {len(df)}")
        print(f"\nPrice Statistics:")
        print(f"  Current:    ${df['close'].iloc[-1]:.2f}")
        print(f"  High:       ${df['close'].max():.2f}")
        print(f"  Low:        ${df['close'].min():.2f}")
        print(f"  Avg:        ${df['close'].mean():.2f}")
        print(f"\nMoving Averages:")
        print(f"  SMA 20:     ${df['SMA_20'].iloc[-1]:.2f}")
        print(f"  SMA 50:     ${df['SMA_50'].iloc[-1]:.2f}")
        print(f"\nMomentum (10-day ROC):")
        print(f"  {df['ROC'].iloc[-1]:.2f}%")
        
        # Check position vs SMA
        current = df['close'].iloc[-1]
        sma_20 = df['SMA_20'].iloc[-1]
        sma_50 = df['SMA_50'].iloc[-1]
        
        print("\n" + "-" * 70)
        print("Technical Analysis:")
        print("-" * 70)
        
        if current > sma_20 > sma_50:
            print("✓ Bullish: Price > SMA 20 > SMA 50")
        elif current < sma_20 < sma_50:
            print("✗ Bearish: Price < SMA 20 < SMA 50")
        else:
            print("➡ Neutral: Mixed signals")
        
        # Plot if requested
        if len(sys.argv) > 1 and sys.argv[1] == "--plot":
            print("\nGenerating plot...")
            fig, ax = plt.subplots(figsize=(12, 6))
            
            ax.plot(df.index, df['close'], label='Close', linewidth=2)
            ax.plot(df.index, df['SMA_20'], label='SMA 20', linestyle='--')
            ax.plot(df.index, df['SMA_50'], label='SMA 50', linestyle='--')
            
            ax.set_title('AAPL Price with Moving Averages')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price ($)')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('aapl_analysis.png', dpi=150)
            print("✓ Plot saved to aapl_analysis.png")
    
    # Fetch multiple symbols
    print("\n" + "=" * 70)
    print("Fetching data for multiple symbols...")
    print("-" * 70)
    
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
    
    for symbol in symbols:
        bars = client.fetch_time_series(symbol, "1day", outputsize=5)
        if bars:
            latest = bars[-1]
            print(f"{symbol:6s}: ${latest['close']:7.2f}  Volume: {latest['volume']:>12,}")
    
    print("\n" + "=" * 70)
    print("Example complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
