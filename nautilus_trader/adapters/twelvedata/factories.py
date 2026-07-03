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

"""TwelveData adapter factories."""

from typing import Optional

from .config import TwelveDataDataClientConfig
from .constants import TWELVEDATA_CLIENT_ID


def get_cached_twelvedata_http_client(
    config: TwelveDataDataClientConfig,
) -> "TwelveDataHttpClientPy":
    """
    Create or return cached TwelveData HTTP client.

    Parameters
    ----------
    config : TwelveDataDataClientConfig
        The configuration for the client.

    Returns
    -------
    TwelveDataHttpClientPy
        The TwelveData HTTP client instance.
    """
    from nautilus_twelvedata import TwelveDataHttpClientPy

    return TwelveDataHttpClientPy(api_key=config.api_key)


def create_twelvedata_data_client(
    config: TwelveDataDataClientConfig,
    client_id: Optional[str] = None,
) -> "TwelveDataDataClient":
    """
    Create a TwelveData data client.

    Parameters
    ----------
    config : TwelveDataDataClientConfig
        The configuration for the client.
    client_id : str, optional
        The client ID. Defaults to TWELVEDATA_CLIENT_ID.

    Returns
    -------
    TwelveDataDataClient
        The TwelveData data client instance.
    """
    from .data import TwelveDataDataClient

    client_id = client_id or TWELVEDATA_CLIENT_ID
    return TwelveDataDataClient(
        client_id=client_id,
        config=config,
    )
