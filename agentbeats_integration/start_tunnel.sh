#!/bin/bash
# Script to start ngrok tunnel

echo "============================================================"
echo "Starting ngrok tunnel to port 8080"
echo "============================================================"
echo ""
echo "Your agent must be running on port 8080!"
echo "If not, run ./run_agent.sh in another terminal first."
echo ""
echo "Press Ctrl+C to stop the tunnel when done."
echo ""

ngrok http 8080
