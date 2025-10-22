#!/bin/bash
# Quick Start Script for TheAgentCompany AgentBeats Integration
# Usage: ./start_agent.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "============================================================"
echo "Starting TheAgentCompany Green Agent"
echo "============================================================"
echo ""

# Kill any existing processes
echo "1. Cleaning up existing processes..."
pkill -9 -f "main_http.py" 2>/dev/null || true
sleep 1

# Start agent
echo "2. Starting agent server..."
cd "$SCRIPT_DIR/green_agent"
"$PROJECT_ROOT/.venv/bin/python" main_http.py > "$SCRIPT_DIR/agent.log" 2>&1 &
AGENT_PID=$!
echo "   Agent started (PID: $AGENT_PID)"
sleep 2

# Check if agent is running
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "   ✅ Agent is responding on http://localhost:8080"
else
    echo "   ❌ Agent failed to start"
    exit 1
fi

# Check ngrok
echo ""
echo "3. Checking ngrok tunnel..."
if curl -s http://localhost:4040/api/tunnels > /dev/null 2>&1; then
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data.get('tunnels') else '')" 2>/dev/null)
    
    if [ -n "$NGROK_URL" ]; then
        echo "   ✅ ngrok tunnel is active: $NGROK_URL"
        
        # Test agent through ngrok
        if curl -s "$NGROK_URL/health" > /dev/null 2>&1; then
            echo "   ✅ Agent accessible via ngrok"
        else
            echo "   ⚠️  ngrok tunnel exists but agent not responding"
        fi
    else
        echo "   ⚠️  ngrok is running but no tunnels found"
        echo "   Starting ngrok..."
        cd "$SCRIPT_DIR"
        ngrok http 8080 --log=stdout > ngrok.log 2>&1 &
        echo "   ngrok started (PID: $!)"
        sleep 3
        NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data.get('tunnels') else '')" 2>/dev/null)
        echo "   ✅ ngrok URL: $NGROK_URL"
    fi
else
    echo "   ⚠️  ngrok not running. Starting ngrok..."
    cd "$SCRIPT_DIR"
    ngrok http 8080 --log=stdout > ngrok.log 2>&1 &
    echo "   ngrok started (PID: $!)"
    sleep 3
    
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data.get('tunnels') else '')" 2>/dev/null)
    if [ -n "$NGROK_URL" ]; then
        echo "   ✅ ngrok URL: $NGROK_URL"
    else
        echo "   ❌ Failed to get ngrok URL"
    fi
fi

echo ""
echo "4. Testing agent card endpoint..."
if [ -n "$NGROK_URL" ]; then
    CARD_RESPONSE=$(curl -s "$NGROK_URL/.well-known/agent-card.json")
    if echo "$CARD_RESPONSE" | python3 -m json.tool > /dev/null 2>&1; then
        echo "   ✅ Agent card is valid JSON"
        echo ""
        echo "   Agent Card:"
        echo "$CARD_RESPONSE" | python3 -m json.tool | sed 's/^/   /'
    else
        echo "   ❌ Agent card is not valid JSON"
    fi
fi

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "Agent URL: $NGROK_URL"
echo "Agent Card: $NGROK_URL/.well-known/agent-card.json"
echo ""
echo "Logs:"
echo "  - Agent: $SCRIPT_DIR/agent.log"
echo "  - ngrok: $SCRIPT_DIR/ngrok.log"
echo ""
echo "Next Steps:"
echo "  1. Go to https://agentbeats.org"
echo "  2. Click 'Register Agent'"
echo "  3. Enter Agent URL: $NGROK_URL"
echo "  4. Enter Launcher URL: $NGROK_URL"
echo "  5. Check 'Green' toggle"
echo "  6. Click 'Register Agent'"
echo ""
echo "To view logs:"
echo "  tail -f $SCRIPT_DIR/agent.log"
echo ""
echo "============================================================"

