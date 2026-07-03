"""
Main script to run NautilusTrader with TwelveData adapter.

This script ties together the configuration and strategy.
"""

import asyncio
import os
import sys

from example_config import create_backtest_config
from example_strategy import SimpleMovingAverageCrossStrategy
from example_strategy import SimpleMovingAverageCrossStrategyConfig


def run_backtest(api_key: str):
    """
    Run a backtest with TwelveData data.

    Parameters
    ----------
    api_key : str
        Your TwelveData API key.
    """
    from nautilus_trader.backtest.engine import BacktestEngine
    from nautilus_trader.backtest.models import BacktestRunConfig

    print("=== Running TwelveData Backtest ===\n")

    # Create configuration
    config = create_backtest_config(api_key)

    # Create backtest engine
    engine = BacktestEngine(config=config)

    # Add strategy
    strategy_config = SimpleMovingAverageCrossStrategyConfig(
        instrument_id="AAPL.NASDAQ.TWELVEDATA",
        short_period=10,
        long_period=20,
    )

    # Initialize and add strategy
    # Note: This is a simplified example - full implementation requires
    # proper NautilusTrader backtest setup with instruments and data

    print("Backtest configuration created!")
    print(f"Data client: TwelveData")
    print(f"Strategy: SimpleMovingAverageCrossStrategy")
    print(f"Instrument: AAPL.NASDAQ.TWELVEDATA")
    print("\nNote: Full backtest requires additional setup for instruments and data loading.")
    print("See NautilusTrader documentation for complete backtest examples.")


def run_live(api_key: str):
    """
    Run live trading with TwelveData.

    Parameters
    ----------
    api_key : str
        Your TwelveData API key.
    """
    from nautilus_trader.live import TradingNode
    from example_config import create_live_config

    print("=== Running TwelveData Live Trading ===\n")

    # Create configuration
    config = create_live_config(api_key)

    # Create trading node
    node = TradingNode(config=config)

    # Add strategy
    strategy_config = SimpleMovingAverageCrossStrategyConfig(
        instrument_id="AAPL.NASDAQ.TWELVEDATA",
    )

    # Configure node with strategy
    # node.add_strategy(SimpleMovingAverageCrossStrategy, config=strategy_config)

    print("Live trading configuration created!")
    print(f"Data client: TwelveData")
    print(f"Strategy: SimpleMovingAverageCrossStrategy")
    print(f"Instrument: AAPL.NASDAQ.TWELVEDATA")
    print("\nNote: Full live trading requires additional setup.")
    print("See NautilusTrader documentation for complete live trading examples.")


def main():
    """Main entry point."""
    # Get API key
    api_key = os.environ.get("TWELVEDATA_API_KEY")
    
    if not api_key:
        print("Error: TWELVEDATA_API_KEY environment variable not set")
        print("Usage: export TWELVEDATA_API_KEY=your_key")
        sys.exit(1)

    print("=" * 60)
    print("NautilusTrader with TwelveData Adapter")
    print("=" * 60)
    print()
    print("Choose mode:")
    print("1. Backtest")
    print("2. Live Trading")
    print()

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        run_backtest(api_key)
    elif choice == "2":
        run_live(api_key)
    else:
        print("Invalid choice")
        sys.exit(1)


if __name__ == "__main__":
    main()
