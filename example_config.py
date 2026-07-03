"""
Example NautilusTrader configuration with TwelveData adapter.

This file sets up the data client configuration for TwelveData.
"""

from nautilus_trader.adapters.twelvedata import TwelveDataDataClientConfig
from nautilus_trader.config import BacktestEngineConfig
from nautilus_trader.config import BacktestVenueConfig
from nautilus_trader.config import LoggingConfig


def create_backtest_config(api_key: str) -> BacktestEngineConfig:
    """
    Create a backtest configuration with TwelveData data client.

    Parameters
    ----------
    api_key : str
        Your TwelveData API key.

    Returns
    -------
    BacktestEngineConfig
        The configured backtest engine.
    """
    config = BacktestEngineConfig(
        # Data client configuration
        data_clients=[
            TwelveDataDataClientConfig(
                api_key=api_key,
                default_interval="1h",
                base_url="https://api.twelvedata.com",
            )
        ],
        # Venue configuration
        venues=[
            BacktestVenueConfig(
                name="TWELVEDATA",
                base_currency="USD",
                starting_balance=100_000.0,
            )
        ],
        # Logging
        logging=LoggingConfig(
            log_level="INFO",
        ),
    )
    
    return config


def create_live_config(api_key: str):
    """
    Create a live trading configuration with TwelveData data client.

    Parameters
    ----------
    api_key : str
        Your TwelveData API key.

    Returns
    -------
    TradingNodeConfig
        The configured trading node.
    """
    from nautilus_trader.config import TradingNodeConfig
    from nautilus_trader.config import LiveDataEngineConfig
    from nautilus_trader.config import LiveExecEngineConfig

    config = TradingNodeConfig(
        # Data engine
        data_engine=LiveDataEngineConfig(),
        # Execution engine (if you add execution)
        exec_engine=LiveExecEngineConfig(),
        # Data clients
        data_clients=[
            TwelveDataDataClientConfig(
                api_key=api_key,
                default_interval="1h",
            )
        ],
        # Logging
        logging=LoggingConfig(
            log_level="INFO",
        ),
    )
    
    return config


if __name__ == "__main__":
    # Example: Create and print config
    api_key = "your_api_key_here"
    config = create_backtest_config(api_key)
    print("Configuration created successfully!")
    print(f"Data clients: {len(config.data_clients)}")
    print(f"Venues: {len(config.venues)}")
