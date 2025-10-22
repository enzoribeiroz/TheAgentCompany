#!/bin/bash
# Script to run the TheAgentCompany Green Agent

cd "$(dirname "$0")/green_agent"

export AGENTBEATS_BACKEND_URL=https://agentbeats.org
export EXPERIMENTS_PATH=../../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro

echo "============================================================"
echo "Starting TheAgentCompany Green Agent"
echo "============================================================"
echo "Backend: $AGENTBEATS_BACKEND_URL"
echo "Experiments: $EXPERIMENTS_PATH"
echo "Agent will listen on: http://0.0.0.0:8080"
echo "============================================================"
echo ""
echo "Keep this terminal running!"
echo "In another terminal, run: ./start_tunnel.sh"
echo ""

../../.venv/bin/python main_http.py
