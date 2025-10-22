#!/bin/bash
# Get the current tunnel URL

echo "============================================================"
echo "🔍 Finding Current Tunnel URL"
echo "============================================================"
echo ""

# Check if cloudflared is running
if ! ps aux | grep -v grep | grep cloudflared > /dev/null 2>&1; then
    echo "❌ Cloudflared is NOT running"
    echo ""
    echo "Start it with:"
    echo "   cd /tmp && nohup ./cloudflared tunnel --url http://localhost:8080 > cloudflared.log 2>&1 &"
    exit 1
fi

# Get URL from logs
URL=$(grep -oE "https://[a-z-]+\.trycloudflare\.com" /tmp/cloudflared.log 2>/dev/null | tail -1)

if [ -z "$URL" ]; then
    echo "❌ Could not find URL in logs"
    exit 1
fi

echo "✅ Cloudflared is running"
echo ""
echo "📍 Current URL:"
echo "   $URL"
echo ""

# Test if it works
echo "🧪 Testing URL..."
if curl -s "$URL/health" > /dev/null 2>&1; then
    echo "   ✅ URL is working!"
    curl -s "$URL/health"
else
    echo "   ⚠️  URL is not responding"
    echo "   Try restarting cloudflared"
fi

echo ""
echo "============================================================"
echo "📋 Registration Info (Copy These):"
echo "============================================================"
echo ""
echo "Alias:        TheAgentCompany Benchmark Reporter"
echo "Agent URL:    $URL"
echo "Launcher URL: $URL"
echo "Type:         Green Agent"
echo "Timeout:      600"
echo ""
echo "============================================================"
echo "🌐 Test in Browser:"
echo "============================================================"
echo ""
echo "Health:      $URL/health"
echo "Agent Card:  $URL/.well-known/agent-card.json"
echo "Status:      $URL/status"
echo ""
echo "============================================================"
