#!/bin/bash

# TheAgentCompany Green Agent Demo Runner
# This script provides a step-by-step demo of the green agent

echo "🌱 TheAgentCompany Green Agent Demo Runner"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup_environment.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if demo script exists
if [ ! -f "demo_script.py" ]; then
    echo "❌ Demo script not found."
    exit 1
fi

echo "✅ Environment ready!"
echo ""

# Run the demo
echo "🚀 Starting Green Agent Demo..."
echo "Press Ctrl+C to stop at any time."
echo ""

python demo_script.py

echo ""
echo "🎉 Demo completed successfully!"
echo "The green agent is ready for production use."
