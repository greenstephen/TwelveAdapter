"""
Example trading strategy using TwelveData data.

This strategy demonstrates how to use bar data from TwelveData in a NautilusTrader strategy.
"""

from nautilus_trader.core.datetime import nanos_to_unix_nanos
from nautilus_trader.core.datetime import unix_nanos_to_nano
from nautilus_trader.model.data import Bar
from nautilus_trader.model.data import BarType
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import TraderId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Quantity
from nautilus_trader.model.objects import Price
from nautilus_trader.strategy.strategy import Strategy
from nautilus_trader.strategy.strategy import StrategyConfig


class SimpleMovingAverageCrossStrategy(Strategy):
    """
    A simple moving average crossover strategy.
    
    This strategy buys when the short MA crosses above the long MA,
    and sells when the short MA crosses below the long MA.
    """

    def __init__(
        self,
        instrument_id: InstrumentId,
        short_period: int = 10,
        long_period: int = 20,
        **kwargs,
    ):
        """
        Initialize the strategy.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument to trade.
        short_period : int
            The short moving average period.
        long_period : int
            The long moving average period.
        **kwargs
            Additional keyword arguments for Strategy.
        """
        super().__init__(**kwargs)

        self.instrument_id = instrument_id
        self.short_period = short_period
        self.long_period = long_period
        
        # Store bar data for calculating MAs
        self.close_prices = []
        
        # Track position
        self.in_position = False

    def on_start(self):
        """Called when the strategy starts."""
        self.log.info("Strategy started")
        
        # Subscribe to bar data
        bar_type = BarType.from_str(f"{self.instrument_id}-1HR-INTERNAL")
        self.subscribe_bars(bar_type)

    def on_stop(self):
        """Called when the strategy stops."""
        self.log.info("Strategy stopped")

    def on_reset(self):
        """Called when the strategy is reset."""
        self.close_prices.clear()
        self.in_position = False

    def on_bar(self, bar: Bar):
        """
        Called when a new bar is received.

        Parameters
        ----------
        bar : Bar
            The new bar data.
        """
        # Store the close price
        self.close_prices.append(bar.close.as_double())
        
        # Keep only the last N prices
        max_periods = max(self.short_period, self.long_period)
        if len(self.close_prices) > max_periods:
            self.close_prices = self.close_prices[-max_periods:]

        # Need enough data to calculate MAs
        if len(self.close_prices) < self.long_period:
            return

        # Calculate moving averages
        short_ma = sum(self.close_prices[-self.short_period:]) / self.short_period
        long_ma = sum(self.close_prices[-self.long_period:]) / self.long_period

        self.log.info(f"Short MA: {short_ma:.2f}, Long MA: {long_ma:.2f}")

        # Check for crossover
        if not self.in_position and short_ma > long_ma:
            # Buy signal
            self.log.info("Buy signal - Short MA crossed above Long MA")
            self._buy()
        elif self.in_position and short_ma < long_ma:
            # Sell signal
            self.log.info("Sell signal - Short MA crossed below Long MA")
            self._sell()

    def _buy(self):
        """Execute a buy order."""
        instrument = self.cache.instrument(self.instrument_id)
        if instrument is None:
            self.log.error(f"Instrument {self.instrument_id} not found")
            return

        # Calculate order quantity
        quantity = Quantity.from_int(10)  # Fixed quantity for example
        
        # Submit market order
        self.submit_market_order(
            quantity=quantity,
            instrument_id=self.instrument_id,
            side="BUY",
        )
        
        self.in_position = True

    def _sell(self):
        """Execute a sell order."""
        if not self.in_position:
            return

        instrument = self.cache.instrument(self.instrument_id)
        if instrument is None:
            self.log.error(f"Instrument {self.instrument_id} not found")
            return

        # Get current position
        position = self.cache.position(
            trader_id=TraderId("TRADER-001"),
            instrument_id=self.instrument_id,
        )
        
        if position is not None and position.is_closed:
            return

        # Submit market order to close
        quantity = Quantity.from_int(10)  # Close full position
        
        self.submit_market_order(
            quantity=quantity,
            instrument_id=self.instrument_id,
            side="SELL",
        )
        
        self.in_position = False


class SimpleMovingAverageCrossStrategyConfig(StrategyConfig):
    """Configuration for SimpleMovingAverageCrossStrategy."""

    instrument_id: str = "AAPL.NASDAQ.TWELVEDATA"
    short_period: int = 10
    long_period: int = 20
