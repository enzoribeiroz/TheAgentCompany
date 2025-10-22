#!/bin/bash
# Quick status check and info display

echo "============================================================"
echo "🎯 AgentBeats Integration - Current Status"
echo "============================================================"
echo ""

# Check agent
echo "1. Agent Server:"
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "   ✅ Running on http://localhost:8080"
    curl -s http://localhost:8080/health | python3 -m json.tool 2>/dev/null | head -5
else
    echo "   ❌ Not running"
    echo "      Start with: nohup ./run_agent.sh > agent.log 2>&1 &"
fi
echo ""

# Check ngrok
echo "2. Ngrok Tunnel:"
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels 2>/dev/null | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data.get('tunnels') else '')" 2>/dev/null)

if [ -n "$NGROK_URL" ]; then
    echo "   ✅ Running"
    echo "   📍 Public URL: $NGROK_URL"
    echo "   🌐 Dashboard: http://127.0.0.1:4040"
else
    echo "   ❌ Not running"
    echo "      Start with: nohup ngrok http 8080 > ngrok.log 2>&1 &"
fi
echo ""

# Check backend
echo "3. AgentBeats Backend:"
if curl -s -m 5 https://agentbeats.org/api/health > /dev/null 2>&1; then
    echo "   ✅ Accessible at https://agentbeats.org"
else
    echo "   ⚠️  Cannot connect to https://agentbeats.org"
fi
echo ""

echo "============================================================"
echo "📋 Next Steps:"
echo "============================================================"
echo ""

if [ -n "$NGROK_URL" ] && curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Everything is running! Ready to register."
    echo ""
    echo "📖 Registration Instructions:"
    echo ""
    echo "1. Open your browser: https://agentbeats.org"
    echo ""
    echo "2. Register your agent with these details:"
    echo "   • Alias: TheAgentCompany Benchmark Reporter"
    echo "   • Agent URL: $NGROK_URL"
    echo "   • Launcher URL: $NGROK_URL"
    echo "   • Type: Green Agent"
    echo "   • Timeout: 600 seconds"
    echo ""
    echo "3. Test your agent card:"
    echo "   Open in browser: $NGROK_URL/card"
    echo "   (Click through ngrok interstitial if it appears)"
    echo ""
    echo "4. Create and start a battle in the UI"
    echo ""
    echo "5. Monitor logs:"
    echo "   tail -f agent.log"
    echo ""
    echo "📚 Full guide: UI_REGISTRATION_GUIDE.md"
else
    if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "⚠️  Agent not running. Start it:"
        echo "   cd /Users/joe2690812044/Desktop/cs\\ 195/TheAgentCompany/agentbeats_integration"
        echo "   nohup ./run_agent.sh > agent.log 2>&1 &"
        echo ""
    fi
    
    if [ -z "$NGROK_URL" ]; then
        echo "⚠️  Ngrok not running. Start it:"
        echo "   nohup ngrok http 8080 > ngrok.log 2>&1 &"
        echo ""
    fi
fi

echo "============================================================"
