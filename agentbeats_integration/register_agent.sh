#!/bin/bash
# Script to register the agent with AgentBeats backend

if [ -z "$1" ]; then
    echo "Usage: ./register_agent.sh <NGROK_URL>"
    echo ""
    echo "Example: ./register_agent.sh https://abc123.ngrok-free.app"
    echo ""
    echo "Get your ngrok URL from the terminal running ./start_tunnel.sh"
    echo "Look for a line like: Forwarding https://....ngrok-free.app -> http://localhost:8080"
    exit 1
fi

NGROK_URL="$1"
BACKEND_URL="https://agentbeats.org"

echo "============================================================"
echo "Registering Agent with AgentBeats Backend"
echo "============================================================"
echo "Backend URL: $BACKEND_URL"
echo "Agent URL: $NGROK_URL"
echo "============================================================"
echo ""

curl -X POST "$BACKEND_URL/api/agents" \
  -H "Content-Type: application/json" \
  -d '{
    "alias": "TheAgentCompany Benchmark Reporter",
    "agent_url": "'"$NGROK_URL"'",
    "launcher_url": "'"$NGROK_URL"'",
    "is_green": true,
    "participant_requirements": [],
    "battle_timeout": 600
  }' | python3 -m json.tool

echo ""
echo "============================================================"
echo "Registration complete!"
echo ""
echo "Next steps:"
echo "1. Go to http://nuggets.puppy9.com:9000/ (or :5173) in your browser"
echo "2. Find 'TheAgentCompany Benchmark Reporter' in the agent list"
echo "3. Create a battle and select this agent"
echo "4. Start the battle"
echo "5. Watch your agent terminal for the battle_start message!"
echo "============================================================"
