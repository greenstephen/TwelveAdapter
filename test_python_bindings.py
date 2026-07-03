#!/usr/bin/env python3
"""
Test script for TwelveData Python bindings.

Usage:
    python test_python_bindings.py YOUR_API_KEY
"""

import sys
from pathlib import Path

# Add the target directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "target" / "debug"))

def test_bindings(api_key: str):
    """Test the TwelveData Python bindings."""
    try:
        from nautilus_twelvedata_py import TwelveDataHttpClientPy
        
        print("=== TwelveData Python Bindings Test ===\n")
        
        # Create client
        print("Creating TwelveData HTTP client...")
        client = TwelveDataHttpClientPy(api_key)
        print(f"✓ Client created successfully")
        print(f"  Base URL: {client.base_url}")
        print(f"  Default Interval: {client.default_interval}")
        print()
        
        print("✓ Python bindings are working!")
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        print("\nNote: You need to build the Python extension first:")
        print("  cargo build --features python")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_python_bindings.py YOUR_API_KEY")
        sys.exit(1)
    
    api_key = sys.argv[1]
    success = test_bindings(api_key)
    sys.exit(0 if success else 1)
