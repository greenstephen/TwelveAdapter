#!/usr/bin/env python3
"""
Test runner for TwelveData adapter
"""

import sys
import subprocess
from pathlib import Path


def run_tests(args=None):
    """Run pytest with given arguments."""
    pytest_args = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short"
    ]
    
    if args:
        pytest_args.extend(args)
    
    print("=" * 70)
    print("Running TwelveData Adapter Tests")
    print("=" * 70)
    print(f"Command: {' '.join(pytest_args)}")
    print("=" * 70)
    
    result = subprocess.run(pytest_args)
    
    print("=" * 70)
    
    return result.returncode


def run_unit_tests():
    """Run only unit tests (no API calls)."""
    return run_tests(["-m", "not integration"])


def run_integration_tests():
    """Run integration tests (requires API key)."""
    return run_tests(["--integration", "-m", "integration"])


def run_with_coverage():
    """Run tests with coverage report."""
    return run_tests([
        "--cov=nautilus_twelvedata",
        "--cov-report=html",
        "--cov-report=term-missing"
    ])


def run_quick():
    """Run quick test suite."""
    return run_tests(["-v", "-x"])


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run TwelveData adapter tests")
    parser.add_argument(
        "--unit",
        action="store_true",
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration",
        action="store_true",
        help="Run integration tests"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run with coverage report"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick test suite"
    )
    parser.add_argument(
        "additional_args",
        nargs="*",
        help="Additional pytest arguments"
    )
    
    args = parser.parse_args()
    
    if args.unit:
        return run_unit_tests()
    elif args.integration:
        return run_integration_tests()
    elif args.coverage:
        return run_with_coverage()
    elif args.quick:
        return run_quick()
    else:
        return run_tests(args.additional_args)


if __name__ == "__main__":
    sys.exit(main())
