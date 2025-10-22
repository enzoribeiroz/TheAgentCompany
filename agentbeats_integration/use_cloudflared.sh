#!/bin/bash
# Use cloudflared instead of ngrok (no interstitial page!)

echo "============================================================"
echo "Starting Cloudflared Tunnel (No Interstitial Page!)"
echo "============================================================"
echo ""

# Check if cloudflared exists
if [ ! -f "/tmp/cloudflared" ]; then
    echo "Downloading cloudflared..."
    curl -Lo /tmp/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64
    chmod +x /tmp/cloudflared
    echo "✅ Downloaded to /tmp/cloudflared"
    echo ""
fi

echo "Starting tunnel to port 8080..."
echo "This will give you a public URL with NO interstitial page"
echo ""
echo "Press Ctrl+C to stop when done"
echo "============================================================"
echo ""

/tmp/cloudflared tunnel --url http://localhost:8080
