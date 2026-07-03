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

"""TwelveData adapter for NautilusTrader.

This adapter provides integration with TwelveData for accessing historical
market data for US stocks.
"""

from .config import TwelveDataDataClientConfig
from .constants import DEFAULT_INTERVAL
from .constants import RATE_LIMIT_CALLS_PER_DAY
from .constants import RATE_LIMIT_CALLS_PER_MINUTE
from .constants import SUPPORTED_INTERVALS
from .constants import TWELVEDATA
from .constants import TWELVEDATA_BASE_URL
from .constants import TWELVEDATA_CLIENT_ID
from .factories import create_twelvedata_data_client
from .factories import get_cached_twelvedata_http_client
from .providers import TwelveDataInstrumentProvider

__all__ = [
    "TwelveDataDataClientConfig",
    "TwelveDataInstrumentProvider",
    "create_twelvedata_data_client",
    "get_cached_twelvedata_http_client",
    "TWELVEDATA",
    "TWELVEDATA_CLIENT_ID",
    "TWELVEDATA_BASE_URL",
    "DEFAULT_INTERVAL",
    "SUPPORTED_INTERVALS",
    "RATE_LIMIT_CALLS_PER_DAY",
    "RATE_LIMIT_CALLS_PER_MINUTE",
]
