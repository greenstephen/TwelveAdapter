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

"""TwelveData adapter constants."""

from nautilus_trader.model.identifiers import Venue

TWELVEDATA = Venue("TWELVEDATA")
TWELVEDATA_CLIENT_ID = "twelvedata_client"
TWELVEDATA_BASE_URL = "https://api.twelvedata.com"

# Rate limits for free tier
RATE_LIMIT_CALLS_PER_DAY = 800
RATE_LIMIT_CALLS_PER_MINUTE = 8

# Default interval
DEFAULT_INTERVAL = "1h"

# Supported intervals
SUPPORTED_INTERVALS = [
    "1min",
    "5min",
    "15min",
    "30min",
    "45min",
    "1h",
    "2h",
    "4h",
    "8h",
    "1day",
    "1week",
    "1month",
]
