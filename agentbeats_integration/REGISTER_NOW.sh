#!/bin/bash

# Simple script to keep trying registration until it works

AGENT_URL="https://ruby-nondoctrinaire-cohen.ngrok-free.dev"
BACKEND="https://agentbeats.org/api/agents"

echo "╔═════════════════════════════════════════════════╗"
echo "║   AgentBeats Registration Helper                ║"
echo "╚═════════════════════════════════════════════════╝"
echo ""
echo "Your Agent Details:"
echo "  URL: $AGENT_URL"
echo "  Name: TheAgentCompany Benchmark Reporter"
echo "  Type: Green Agent"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "OPTION 1: Manual Registration via Web UI"
echo ""
echo "  1. Open in browser: https://agentbeats.org"
echo "  2. Login or create account"
echo "  3. Find 'Register Agent' or 'Add Agent'"
echo "  4. Enter this URL: $AGENT_URL"
echo "  5. Submit"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "OPTION 2: Try API Registration (may fail)"
echo ""
read -p "Press Enter to try API registration, or Ctrl+C to use web UI... "

echo ""
echo "Attempting API registration..."
echo ""

RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$BACKEND" \
  -H "Content-Type: application/json" \
  -H "User-Agent: AgentBeats-Registration/1.0" \
  -d '{
    "alias": "TheAgentCompany Benchmark Reporter",
    "agent_url": "'"$AGENT_URL"'",
    "launcher_url": "'"$AGENT_URL"'",
    "is_green": true,
    "participant_requirements": [],
    "battle_timeout": 600
  }')

HTTP_CODE=$(echo "$RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_CODE:/d')

echo "Response Code: $HTTP_CODE"
echo ""

if [ "$HTTP_CODE" = "201" ]; then
    echo "✅ SUCCESS! Agent registered!"
    echo ""
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
    echo ""
    echo "🎮 Your agent is now live on AgentBeats!"
    echo "   Visit: https://agentbeats.org to see it"
else
    echo "❌ API Registration Failed"
    echo ""
    echo "Response:"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📋 Please use MANUAL REGISTRATION via Web UI:"
    echo ""
    echo "  1. Go to: https://agentbeats.org"
    echo "  2. Login/Signup"
    echo "  3. Look for 'Register Agent' or dashboard"
    echo "  4. Paste URL: $AGENT_URL"
    echo ""
    echo "✅ Your agent is READY and WORKING at:"
    echo "   $AGENT_URL"
    echo ""
    echo "Test it yourself:"
    echo "   curl $AGENT_URL/health"
    echo "   curl $AGENT_URL/.well-known/agent-card.json"
fi
