#!/bin/bash
# Test script for TwelveData adapter
# Usage: ./test-api.sh YOUR_API_KEY

if [ -z "$1" ]; then
    echo "Usage: ./test-api.sh YOUR_API_KEY"
    echo "Example: ./test-api.sh abc123xyz"
    exit 1
fi

export TWELVEDATA_API_KEY="$1"

echo "Testing TwelveData API with symbol AAPL..."
echo ""

cargo run --example fetch-bars 2>&1 | grep -v "warning:"
