#!/usr/bin/env python3
"""
Test script for TwelveData Python adapter structure.

This test verifies the adapter structure without requiring NautilusTrader to be installed.
"""

import sys
from pathlib import Path

def test_structure():
    """Test the adapter structure."""
    print("=== TwelveData Python Adapter Structure Test ===\n")

    adapter_path = Path(__file__).parent / "nautilus_trader" / "adapters" / "twelvedata"

    # Check files exist
    required_files = [
        "__init__.py",
        "config.py",
        "constants.py",
        "factories.py",
        "data.py",
        "providers.py",
    ]

    print("Checking required files...")
    all_exist = True
    for filename in required_files:
        filepath = adapter_path / filename
        if filepath.exists():
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} MISSING")
            all_exist = False

    print()

    if not all_exist:
        print("✗ Some files are missing")
        return False

    # Try to import constants directly (no NautilusTrader dependency for this file)
    print("Testing constants module...")
    try:
        # Import constants directly without going through __init__.py
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "constants",
            adapter_path / "constants.py"
        )
        constants = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(constants)

        print(f"  ✓ TWELVEDATA = {constants.TWELVEDATA}")
        print(f"  ✓ TWELVEDATA_CLIENT_ID = {constants.TWELVEDATA_CLIENT_ID}")
        print(f"  ✓ DEFAULT_INTERVAL = {constants.DEFAULT_INTERVAL}")
        print(f"  ✓ SUPPORTED_INTERVALS = {len(constants.SUPPORTED_INTERVALS)} intervals")
        print()

    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False

    # Test Rust client integration
    print("Testing Rust client integration...")
    try:
        from nautilus_twelvedata import TwelveDataHttpClientPy

        client = TwelveDataHttpClientPy("test_key")
        print(f"  ✓ Rust client created")
        print(f"    Base URL: {client.base_url}")
        print(f"    Default Interval: {client.default_interval}")
        print()

    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False

    print("✓ All structure tests passed!")
    print("\nPhase 3 Complete: Python Integration Layer")
    print("  - File structure: ✓")
    print("  - Constants module: ✓")
    print("  - Rust client integration: ✓")
    print("  - Ready for NautilusTrader integration")
    return True


if __name__ == "__main__":
    success = test_structure()
    sys.exit(0 if success else 1)
