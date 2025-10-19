#!/bin/bash
# TheAgentCompany Green Agent - Environment Setup Script

set -e  # Exit on any error

echo "🌱 Setting up TheAgentCompany Green Agent environment..."

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python $required_version or higher is required. Found: $python_version"
    echo "Please upgrade Python and try again."
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Install AgentBeats SDK from local path (if available)
if [ -d "../GreenAgent/agentbeats" ]; then
    echo "🔧 Installing AgentBeats SDK from local path..."
    pip install -e ../GreenAgent/agentbeats/
    echo "✅ AgentBeats SDK installed from local path"
else
    echo "⚠️  AgentBeats SDK not found in local path, will use PyPI version"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p workspace
mkdir -p config

# Set up environment variables
echo "🔧 Setting up environment variables..."
cat > .env << EOF
# TheAgentCompany Green Agent Configuration
OPENAI_API_KEY=your_openai_api_key_here
AGENTBEATS_BACKEND_URL=http://localhost:9000
AGENTBEATS_MCP_SERVER_URL=http://localhost:9001/sse
GREEN_AGENT_HOST=0.0.0.0
GREEN_AGENT_PORT=9041
GREEN_AGENT_LAUNCHER_PORT=9040
BATTLE_TIMEOUT=300
LOG_LEVEL=INFO
EOF

echo "✅ Environment variables file created (.env)"

# Test imports
echo "🧪 Testing imports..."
python3 -c "
try:
    import agentbeats as ab
    print('✅ AgentBeats import successful')
except ImportError as e:
    print(f'❌ AgentBeats import failed: {e}')
    exit(1)

try:
    from a2a.client import A2AClient
    print('✅ A2A client import successful')
except ImportError as e:
    print(f'❌ A2A client import failed: {e}')
    exit(1)

try:
    from tools import setup_license_change_task
    print('✅ Tools import successful')
except ImportError as e:
    print(f'❌ Tools import failed: {e}')
    exit(1)

print('🎉 All imports successful!')
"

echo ""
echo "🎉 Environment setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Update .env file with your API keys and configuration"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the green agent: python main.py"
echo ""
echo "🔧 To activate the environment in the future:"
echo "   source venv/bin/activate"
echo ""
echo "🌱 TheAgentCompany Green Agent is ready for deployment!"
