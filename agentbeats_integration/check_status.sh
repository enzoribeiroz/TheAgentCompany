#!/bin/bash
# Check the status of all components

echo "============================================================"
echo "AgentBeats Integration Status Check"
echo "============================================================"
echo ""

# Check if agent is running
echo "1. Agent Status (port 8080):"
if lsof -i :8080 | grep LISTEN > /dev/null 2>&1; then
    echo "   ✅ Agent is RUNNING on port 8080"
    lsof -i :8080 | grep LISTEN
else
    echo "   ❌ Agent is NOT running"
    echo "      Run: ./run_agent.sh"
fi
echo ""

# Check if ngrok is installed
echo "2. ngrok Installation:"
if command -v ngrok > /dev/null 2>&1; then
    echo "   ✅ ngrok is installed"
    ngrok version
else
    echo "   ❌ ngrok is NOT installed"
fi
echo ""

# Check if experiment data exists
echo "3. Experiment Data:"
EXPERIMENTS_PATH="../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro"
if [ -d "$EXPERIMENTS_PATH/results" ]; then
    EVAL_COUNT=$(ls -1 "$EXPERIMENTS_PATH/results"/eval_*-image.json 2>/dev/null | wc -l)
    echo "   ✅ Experiment data found"
    echo "      Path: $EXPERIMENTS_PATH"
    echo "      Evaluation files: $EVAL_COUNT"
else
    echo "   ❌ Experiment data NOT found"
    echo "      Expected path: $EXPERIMENTS_PATH"
fi
echo ""

# Check dependencies
echo "4. Python Dependencies:"
if ../../.venv/bin/python -c "import httpx, fastapi, uvicorn" 2>/dev/null; then
    echo "   ✅ All dependencies installed (httpx, fastapi, uvicorn)"
else
    echo "   ❌ Some dependencies missing"
    echo "      Run: ../../.venv/bin/pip install httpx fastapi uvicorn"
fi
echo ""

# Quick test
echo "5. Quick Test:"
if lsof -i :8080 | grep LISTEN > /dev/null 2>&1; then
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "   ✅ Agent is responding to health checks"
        curl -s http://localhost:8080/health | python3 -m json.tool 2>/dev/null || echo "      (Could not parse response)"
    else
        echo "   ⚠️  Agent port is open but not responding"
    fi
else
    echo "   ⏸️  Agent not running - cannot test"
fi
echo ""

echo "============================================================"
echo "Next Steps:"
echo "============================================================"
if ! lsof -i :8080 | grep LISTEN > /dev/null 2>&1; then
    echo "1. Start the agent: ./run_agent.sh"
    echo "2. Start the tunnel: ./start_tunnel.sh"
    echo "3. Register: ./register_agent.sh <NGROK_URL>"
else
    echo "1. ✅ Agent is running"
    echo "2. Start the tunnel: ./start_tunnel.sh"
    echo "3. Register: ./register_agent.sh <NGROK_URL>"
fi
echo ""
echo "See QUICKSTART.md for detailed instructions."
echo "============================================================"
