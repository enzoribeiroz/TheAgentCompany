#!/bin/bash
# Use localtunnel instead of ngrok (no interstitial page!)

echo "============================================================"
echo "Starting Localtunnel (No Interstitial Page!)"
echo "============================================================"
echo ""

# Check if localtunnel is installed
if ! command -v lt &> /dev/null && ! command -v npx &> /dev/null; then
    echo "❌ Neither 'lt' nor 'npx' found."
    echo ""
    echo "Install Node.js/npm first, then either:"
    echo "  npm install -g localtunnel"
    echo "  OR"
    echo "  Use npx (comes with npm): npx localtunnel --port 8080"
    echo ""
    exit 1
fi

echo "Starting tunnel to port 8080..."
echo "This will give you a public URL with NO interstitial page"
echo ""
echo "Press Ctrl+C to stop when done"
echo "============================================================"
echo ""

# Try to use localtunnel
if command -v lt &> /dev/null; then
    lt --port 8080
else
    echo "Using npx localtunnel..."
    npx localtunnel --port 8080
fi
