"""TwelveData instrument provider."""

from typing import Optional

from nautilus_trader.model.identifiers import InstrumentId

from .config import TwelveDataDataClientConfig
from .constants import TWELVEDATA


class TwelveDataInstrumentProvider:
    """
    Provides instrument definitions for TwelveData.

    This provider loads instrument definitions from TwelveData's API and caches
    them for use by the data client.

    Parameters
    ----------
    config : TwelveDataDataClientConfig
        The configuration for the client.
    """

    def __init__(
        self,
        config: TwelveDataDataClientConfig,
    ) -> None:
        self._config = config
        self._client = None
        self._instruments = {}

    async def initialize(self) -> None:
        """Initialize the provider."""
        from nautilus_twelvedata import TwelveDataHttpClientPy

        self._client = TwelveDataHttpClientPy(api_key=self._config.api_key)

    async def load_all_async(self, filters: Optional[dict] = None) -> None:
        """
        Load all instruments asynchronously.

        Parameters
        ----------
        filters : dict, optional
            Filters to apply when loading instruments.
        """
        # For MVP, we'll create instruments on-demand
        # In a full implementation, this would fetch from TwelveData's symbol search API
        pass

    async def load_async(
        self,
        symbol: str,
        exchange: str = "NASDAQ",
    ) -> Optional[InstrumentId]:
        """
        Load a specific instrument.

        Parameters
        ----------
        symbol : str
            The stock symbol.
        exchange : str, optional
            The exchange. Defaults to "NASDAQ".

        Returns
        -------
        InstrumentId or None
            The instrument ID if found.
        """
        symbol = symbol.upper()

        # Check cache first
        instrument_id = self._format_instrument_id(symbol, exchange)
        if instrument_id in self._instruments:
            return self._instruments[instrument_id]

        # Create instrument ID
        instrument_id = InstrumentId.from_str(f"{symbol}.{exchange}.{TWELVEDATA}")

        # Cache the instrument ID
        self._instruments[instrument_id] = instrument_id

        return instrument_id

    def _format_instrument_id(self, symbol: str, exchange: str) -> InstrumentId:
        """Format an instrument ID."""
        return InstrumentId.from_str(f"{symbol.upper()}.{exchange.upper()}.{TWELVEDATA}")
