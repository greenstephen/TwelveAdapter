"""
Pytest configuration and fixtures for TwelveData adapter tests
"""

import pytest
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Check if adapter is available
try:
    from nautilus_twelvedata import TwelveDataHttpClientPy
    HAS_ADAPTER = True
except ImportError:
    HAS_ADAPTER = False


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test requiring live API"
    )


def pytest_collection_modifyitems(config, items):
    """Skip integration tests by default unless explicitly requested."""
    if config.getoption("--integration"):
        return
    
    # Skip all integration tests
    skip_integration = pytest.mark.skip(
        reason="Need --integration option to run integration tests"
    )
    
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


def pytest_addoption(parser):
    """Add command-line options."""
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Run integration tests with live API"
    )


@pytest.fixture(scope="session")
def test_api_key():
    """Provide test API key from environment."""
    return os.getenv("TWELVEDATA_API_KEY", "test_key")


@pytest.fixture(scope="function")
def temp_test_dir(tmp_path):
    """Provide temporary directory for test files."""
    return tmp_path


@pytest.fixture(scope="function")
def sample_bar_data():
    """Provide sample bar data for testing."""
    return {
        "datetime": "2024-01-15 10:00:00",
        "open": 150.0,
        "high": 152.0,
        "low": 149.5,
        "close": 151.5,
        "volume": 1000000
    }


@pytest.fixture(scope="function")
def sample_bars_data(sample_bar_data):
    """Provide sample bars data for testing."""
    return [sample_bar_data] * 10


@pytest.fixture(scope="session")
def data_dir():
    """Provide path to test data directory."""
    return Path(__file__).parent / "data"
