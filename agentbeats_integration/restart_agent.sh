#!/bin/bash

# Kill any existing agent processes
pkill -9 -f "main_http.py" 2>/dev/null

# Wait a moment for cleanup
sleep 1

# Change to the green_agent directory
cd "$(dirname "$0")/green_agent"

# Activate virtual environment and start the agent
../../.venv/bin/python main_http.py

