#!/bin/bash
# Alternative to ngrok - use Cloudflare Tunnel (free, no warning page, more reliable)

echo "Installing cloudflared..."
brew install cloudflare/cloudflare/cloudflared || echo "Install manually from: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"

echo ""
echo "Starting Cloudflare Tunnel..."
echo "This will give you a public URL that works with AgentBeats"
echo ""

# Start tunnel
cloudflared tunnel --url http://localhost:8080

