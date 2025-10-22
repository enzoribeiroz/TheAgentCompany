#!/bin/bash

# Register TheAgentCompany Agent with AgentBeats Backend

echo "╔═════════════════════════════════════════════════╗"
echo "║   Register Agent with AgentBeats Backend       ║"
echo "╚═════════════════════════════════════════════════╝"
echo ""

# Configuration
BACKEND_URL="https://agentbeats.org"
AGENT_URL="https://kijiji-von-overseas-leadership.trycloudflare.com"

echo "📋 Configuration:"
echo "   Backend: $BACKEND_URL"
echo "   Agent URL: $AGENT_URL"
echo ""

# Step 1: Check backend is accessible
echo "1️⃣  Checking backend connectivity..."
BACKEND_HEALTH=$(curl -s --max-time 5 "$BACKEND_URL/api/health")
if [[ $BACKEND_HEALTH == *"ok"* ]]; then
    echo "   ✅ Backend is accessible"
else
    echo "   ❌ Backend is not accessible"
    exit 1
fi
echo ""

# Step 2: Check agent is accessible
echo "2️⃣  Checking agent connectivity..."
AGENT_HEALTH=$(curl -s --max-time 5 "$AGENT_URL/health")
if [[ $AGENT_HEALTH == *"healthy"* ]]; then
    echo "   ✅ Agent is accessible at $AGENT_URL"
else
    echo "   ❌ Agent is not accessible. Tunnel may have expired."
    echo "   💡 Restart tunnel with: pkill cloudflared && cd /tmp && nohup ./cloudflared tunnel --url http://localhost:8080 &"
    exit 1
fi
echo ""

# Step 3: Check agent card
echo "3️⃣  Verifying agent card..."
AGENT_CARD=$(curl -s --max-time 5 "$AGENT_URL/.well-known/agent-card.json")
if [[ $AGENT_CARD == *"alias"* ]]; then
    echo "   ✅ Agent card is valid"
    echo "   Agent: $(echo $AGENT_CARD | grep -o '"alias":"[^"]*"' | cut -d'"' -f4)"
else
    echo "   ❌ Agent card is invalid"
    exit 1
fi
echo ""

# Step 4: Register via API
echo "4️⃣  Attempting to register via API..."
REGISTER_RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/agents/register" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"$AGENT_URL\"}")

echo "   Response: $REGISTER_RESPONSE"
echo ""

# Check if registration succeeded
if [[ $REGISTER_RESPONSE == *"success"* ]] || [[ $REGISTER_RESPONSE == *"registered"* ]]; then
    echo "╔═════════════════════════════════════════════════╗"
    echo "║   ✅ Registration Successful!                   ║"
    echo "╚═════════════════════════════════════════════════╝"
else
    echo "╔═════════════════════════════════════════════════╗"
    echo "║   ⚠️  API Registration May Have Failed          ║"
    echo "╚═════════════════════════════════════════════════╝"
    echo ""
    echo "📝 Alternative: Register via Web UI"
    echo ""
    echo "   1. Open: $BACKEND_URL"
    echo "   2. Look for 'Register Agent' or 'Add Agent' button"
    echo "   3. Enter URL: $AGENT_URL"
    echo "   4. Submit"
    echo ""
    echo "🔍 Or try these common endpoints:"
    echo "   • $BACKEND_URL/register"
    echo "   • $BACKEND_URL/agents/register"
    echo "   • $BACKEND_URL/dashboard"
    echo ""
fi

echo "🌐 Your Agent Details:"
echo "   • URL: $AGENT_URL"
echo "   • Health: $AGENT_URL/health"
echo "   • Card: $AGENT_URL/.well-known/agent-card.json"
echo "   • Status: $AGENT_URL/status"
echo ""
