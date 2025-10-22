#!/bin/bash

# Register with AgentBeats using the correct API endpoint

BACKEND_URL="https://agentbeats.org"
AGENT_URL="https://kijiji-von-overseas-leadership.trycloudflare.com"

echo "╔═════════════════════════════════════════════════╗"
echo "║   Registering Agent with AgentBeats             ║"
echo "╚═════════════════════════════════════════════════╝"
echo ""

# Check connectivity
echo "1️⃣  Checking connectivity..."
curl -s --max-time 5 "$AGENT_URL/health" > /dev/null
if [ $? -ne 0 ]; then
    echo "   ❌ Agent not accessible. Tunnel may have expired."
    echo "   Run: pkill cloudflared && cd /tmp && nohup ./cloudflared tunnel --url http://localhost:8080 > cloudflared.log 2>&1 &"
    exit 1
fi
echo "   ✅ Agent is accessible"
echo ""

# Register using the correct API endpoint
echo "2️⃣  Registering with backend..."
echo "   Endpoint: POST $BACKEND_URL/agents"
echo ""

RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$BACKEND_URL/agents" \
  -H "Content-Type: application/json" \
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

echo "   HTTP Status: $HTTP_CODE"
echo ""

if [ "$HTTP_CODE" = "201" ]; then
    echo "╔═════════════════════════════════════════════════╗"
    echo "║   ✅ Registration Successful!                   ║"
    echo "╚═════════════════════════════════════════════════╝"
    echo ""
    echo "📋 Agent Details:"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
    echo ""
    echo "🎮 Your agent is now registered and ready for battles!"
    echo ""
    echo "🌐 View on AgentBeats:"
    echo "   • https://agentbeats.org"
    echo "   • Check the agents list to see your agent"
    echo ""
elif [ "$HTTP_CODE" = "400" ] || [ "$HTTP_CODE" = "422" ]; then
    echo "⚠️  Registration failed - validation error"
    echo ""
    echo "Response:"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
    echo ""
    echo "💡 Common issues:"
    echo "   • Agent card may not be accessible"
    echo "   • Agent URL format incorrect"
    echo "   • Agent card format doesn't match requirements"
    echo ""
    echo "🔍 Test agent card:"
    echo "   curl $AGENT_URL/.well-known/agent-card.json"
elif [ "$HTTP_CODE" = "409" ]; then
    echo "⚠️  Agent may already be registered"
    echo ""
    echo "Response:"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
    echo ""
    echo "🔍 Check existing agents:"
    echo "   curl $BACKEND_URL/agents"
else
    echo "❌ Registration failed"
    echo ""
    echo "Response:"
    echo "$BODY"
    echo ""
    echo "💡 Try:"
    echo "   1. Check if backend is accessible: curl $BACKEND_URL/api/health"
    echo "   2. Check if agent is accessible: curl $AGENT_URL/health"
    echo "   3. View API docs: https://github.com/agentbeats/agentbeats/blob/main/docs/backend_openapi.yaml"
fi
