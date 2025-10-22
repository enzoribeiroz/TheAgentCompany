#!/bin/bash
# Direct API registration with ngrok bypass header

if [ -z "$1" ]; then
    echo "Usage: ./register_with_header.sh <NGROK_URL>"
    echo ""
    echo "Example: ./register_with_header.sh https://ruby-nondoctrinaire-cohen.ngrok-free.dev"
    exit 1
fi

NGROK_URL="$1"
BACKEND_URL="https://agentbeats.org"

echo "============================================================"
echo "Registering Agent with AgentBeats Backend"
echo "============================================================"
echo "Backend URL: $BACKEND_URL"
echo "Agent URL: $NGROK_URL"
echo ""
echo "Note: Including ngrok-skip-browser-warning header hint"
echo "============================================================"
echo ""

# First, let's test if the agent is accessible
echo "Testing agent accessibility..."
if curl -s -H "ngrok-skip-browser-warning: true" "$NGROK_URL/card" > /dev/null 2>&1; then
    echo "✅ Agent card is accessible with bypass header"
else
    echo "❌ Agent card not accessible"
    echo "   Make sure agent is running: curl http://localhost:8080/card"
    exit 1
fi
echo ""

# Try registration with additional headers
echo "Attempting registration..."
curl -X POST "$BACKEND_URL/api/agents" \
  -H "Content-Type: application/json" \
  -H "User-Agent: AgentBeats-Registration/1.0" \
  -d '{
    "alias": "TheAgentCompany Benchmark Reporter",
    "agent_url": "'"$NGROK_URL"'",
    "launcher_url": "'"$NGROK_URL"'",
    "is_green": true,
    "participant_requirements": [],
    "battle_timeout": 600,
    "headers": {
      "ngrok-skip-browser-warning": "true"
    }
  }' | python3 -m json.tool

echo ""
echo "============================================================"
echo "If registration failed due to ngrok interstitial:"
echo ""
echo "Option 1: Use localtunnel instead (no interstitial)"
echo "   npm install -g localtunnel"
echo "   lt --port 8080"
echo ""
echo "Option 2: Use cloudflared (Cloudflare tunnel)"
echo "   ./use_cloudflared.sh"
echo ""
echo "Option 3: Visit the URL in browser first to bypass:"
echo "   open $NGROK_URL/card"
echo "   Click 'Visit Site', then try registration again"
echo "============================================================"
