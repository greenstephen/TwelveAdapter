# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2026 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

"""TwelveData data client implementation."""

import asyncio
from datetime import datetime
from datetime import timezone
from typing import Optional

from nautilus_trader.common.component import LiveComponent
from nautilus_trader.common.component import MessageBus
from nautilus_trader.common.component import SignalGenerator
from nautilus_trader.common.component import Timer
from nautilus_trader.common.component import TimerName
from nautilus_trader.common.component import TimerNamespace
from nautilus_trader.common.factories import LiveDataClientFactory
from nautilus_trader.core.correctness import PyCondition
from nautilus_trader.core.rust.model import BarType
from nautilus_trader.data.client import LiveDataClient
from nautilus_trader.data.messages import DataRequest
from nautilus_trader.data.messages import DataResponse
from nautilus_trader.data.messages import BarsBulkRequest
from nautilus_trader.identifiers import ClientId
from nautilus_trader.model.data import Bar
from nautilus_trader.model.data import BarSpecification
from nautilus_trader.model.data import BarType as NautilusBarType
from nautilus_trader.model.data import QuoteTick
from nautilus_trader.model.data import TradeTick
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import Venue

from .config import TwelveDataDataClientConfig
from .constants import TWELVEDATA
from .constants import TWELVEDATA_CLIENT_ID


class TwelveDataDataClient(LiveDataClient):
    """
    A TwelveData data client for NautilusTrader.

    This client provides access to TwelveData market data including historical
    OHLCV bar data for US stocks.

    Parameters
    ----------
    client_id : ClientId
        The client ID.
    config : TwelveDataDataClientConfig
        The configuration for the client.
    msgbus : MessageBus
        The message bus for the client.
    cache : Cache
        The cache.
    timer : Timer
        The timer.
    signal_gen : SignalGenerator, optional
        The signal generator.
    assess_liveness : bool, optional
        If True, the client will assess its own liveness.
    loop : asyncio.AbstractEventLoop, optional
        The event loop.

    Raises
    ------
    ValueError
        If `client_id` is None.
    """

    def __init__(
        self,
        client_id: ClientId,
        config: TwelveDataDataClientConfig,
        msgbus: MessageBus,
        cache,
        timer: Timer,
        signal_gen: Optional[SignalGenerator] = None,
        assess_liveness: bool = True,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        super().__init__(
            client_id=client_id,
            msgbus=msgbus,
            cache=cache,
            timer=timer,
            signal_gen=signal_gen,
            assess_liveness=assess_liveness,
            loop=loop,
        )

        PyCondition.not_none(client_id, "client_id")
        PyCondition.not_none(config, "config")
        PyCondition.not_none(msgbus, "msgbus")
        PyCondition.not_none(cache, "cache")
        PyCondition.not_none(timer, "timer")

        self._config = config
        self._client = None  # Will be initialized in connect()

    async def connect(self) -> None:
        """Connect to the TwelveData API."""
        if self.is_connected:
            return

        # Initialize the Rust client
        from nautilus_twelvedata import TwelveDataHttpClientPy

        self._client = TwelveDataHttpClientPy(api_key=self._config.api_key)

        self._set_connected()

    async def disconnect(self) -> None:
        """Disconnect from the TwelveData API."""
        if not self.is_connected:
            return

        self._client = None
        self._set_disconnected()

    def reset(self) -> None:
        """Reset the client state."""
        super().reset()

    async def _request_bars(
        self,
        bar_type: NautilusBarType,
        start: datetime,
        end: datetime,
        aggregation_source: bool = False,
    ) -> None:
        """
        Request historical bar data.

        Parameters
        ----------
        bar_type : BarType
            The bar type.
        start : datetime
            The start time (UTC).
        end : datetime
            The end time (UTC).
        aggregation_source : bool, optional
            If True, request from aggregation source.
        """
        if not self._client:
            raise RuntimeError("Client is not connected")

        # Extract symbol from bar_type
        instrument_id = bar_type.instrument_id
        symbol = instrument_id.symbol.value

        # Convert interval from bar_type to TwelveData format
        interval = self._interval_from_bar_type(bar_type)

        # Convert timestamps to nanoseconds
        start_ns = int(start.timestamp() * 1e9)
        end_ns = int(end.timestamp() * 1e9)

        # Fetch data from Rust client
        try:
            bars = await self._client.fetch_time_series_range(
                symbol=symbol,
                interval=interval,
                start_ns=start_ns,
                end_ns=end_ns,
            )

            # Convert and emit bars
            for bar_data in bars:
                bar = self._create_bar(bar_data, bar_type)
                self._handle_data(bar)

        except Exception as e:
            self._log.error(f"Failed to fetch bars: {e}")

    def _interval_from_bar_type(self, bar_type: NautilusBarType) -> str:
        """Convert Nautilus BarType to TwelveData interval."""
        spec = bar_type.specification
        interval_map = {
            "1MIN": "1min",
            "5MIN": "5min",
            "15MIN": "15min",
            "30MIN": "30min",
            "1HR": "1h",
            "2HR": "2h",
            "4HR": "4h",
            "8HR": "8h",
            "1DAY": "1day",
            "1WEEK": "1week",
            "1MONTH": "1month",
        }

        return interval_map.get(str(spec.step), "1h")

    def _create_bar(self, bar_data: dict, bar_type: NautilusBarType) -> Bar:
        """Create a Nautilus Bar from TwelveData data."""
        from nautilus_trader.core.rust.model import Bar
        from nautilus_trader.core.rust.time import nanos_now

        # Parse datetime
        dt = datetime.fromisoformat(bar_data["datetime"])
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        ts_event = int(dt.timestamp() * 1e9)
        ts_init = nanos_now()

        # Create bar using Nautilus Bar constructor
        # Note: This is a simplified version - in production you'd use the proper Bar factory
        bar = Bar(
            bar_type=bar_type,
            open=bar_data["open"],
            high=bar_data["high"],
            low=bar_data["low"],
            close=bar_data["close"],
            volume=bar_data["volume"],
            ts_event=ts_event,
            ts_init=ts_init,
        )

        return bar


# Register the factory
LiveDataClientFactory.register(TWELVEDATA, TwelveDataDataClient)
