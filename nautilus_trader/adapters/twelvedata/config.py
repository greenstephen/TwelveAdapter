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

"""TwelveData adapter configuration."""

import msgspec
from typing import Optional

from .constants import DEFAULT_INTERVAL
from .constants import TWELVEDATA_BASE_URL


class TwelveDataDataClientConfig(msgspec.Struct, frozen=True, kw_only=True):
    """
    Configuration for TwelveData data client.

    Parameters
    ----------
    api_key : str
        The TwelveData API key.
    base_url : str, optional
        The base URL for the TwelveData API.
    default_interval : str, optional
        The default interval for bar data requests.
    http_timeout_secs : int, optional
        The HTTP request timeout in seconds.
    """

    type_name: str = "TwelveDataDataClientConfig"
    api_key: str
    base_url: str = TWELVEDATA_BASE_URL
    default_interval: str = DEFAULT_INTERVAL
    http_timeout_secs: int = 30
