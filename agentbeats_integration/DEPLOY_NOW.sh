#!/bin/bash

# AWS EC2 Deployment Script - Personalized for Your Instance
# EC2 IP: 50.18.84.152
# Instance ID: i-0c566aba209e1d1aa
# Generated: $(date)

set -e  # Exit on any error

EC2_IP="50.18.84.152"
KEY_PATH="/Users/joe2690812044/Desktop/cs 195/TheAgentCompany/agentbeats_integration/agentbeats-key.pem"
AGENT_PATH="/Users/joe2690812044/Desktop/cs 195/TheAgentCompany/agentbeats_integration"

echo "╔═══════════════════════════════════════════════════════╗"
echo "║   Deploying Your Agent to AWS EC2                    ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "EC2 IP: $EC2_IP"
echo "Key: $KEY_PATH"
echo ""

# ═══════════════════════════════════════════════════════
# STEP 1: Setup SSH Key
# ═══════════════════════════════════════════════════════

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Setting up SSH key..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if key exists
if [ ! -f "$KEY_PATH" ]; then
    echo "❌ Error: Key file not found at $KEY_PATH"
    echo "Please make sure the .pem file is in the agentbeats_integration folder"
    exit 1
fi

# Set proper permissions
chmod 400 "$KEY_PATH"
echo "✅ Key permissions set"

# ═══════════════════════════════════════════════════════
# STEP 2: Test Connection
# ═══════════════════════════════════════════════════════

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Testing SSH connection..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ssh -i "$KEY_PATH" -o StrictHostKeyChecking=no -o ConnectTimeout=10 ubuntu@$EC2_IP 'echo "Connection successful"' 2>/dev/null; then
    echo "✅ SSH connection working!"
else
    echo "❌ Cannot connect to EC2. Please check:"
    echo "   1. Instance is running (check AWS console)"
    echo "   2. Security group allows SSH (port 22)"
    echo "   3. IP address is correct: $EC2_IP"
    exit 1
fi

# ═══════════════════════════════════════════════════════
# STEP 3: Install Dependencies on EC2
# ═══════════════════════════════════════════════════════

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Installing dependencies on EC2..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ssh -i "$KEY_PATH" ubuntu@$EC2_IP << 'INSTALL_DEPS'
set -e
echo "Updating system..."
sudo apt update -y > /dev/null 2>&1

echo "Installing Python and tools..."
sudo apt install -y python3-pip python3-venv git > /dev/null 2>&1

echo "Installing Python packages..."
pip3 install httpx==0.28.1 fastapi==0.119.1 uvicorn==0.38.0 > /dev/null 2>&1

echo "Creating directories..."
mkdir -p ~/agent

echo "✅ Dependencies installed!"
INSTALL_DEPS

# ═══════════════════════════════════════════════════════
# STEP 4: Copy Files to EC2
# ═══════════════════════════════════════════════════════

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Copying agent files to EC2..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "Copying agent code..."
scp -i "$KEY_PATH" -r \
  "$AGENT_PATH/green_agent" \
  ubuntu@$EC2_IP:~/agent/ > /dev/null 2>&1

echo "✅ Agent code copied"

echo "Copying experiments data (this may take a minute)..."
scp -i "$KEY_PATH" -r \
  "/Users/joe2690812044/Desktop/cs 195/TheAgentCompany/experiments" \
  ubuntu@$EC2_IP:~/agent/ > /dev/null 2>&1

echo "✅ Experiments data copied"

# ═══════════════════════════════════════════════════════
# STEP 5: Start Agent on EC2
# ═══════════════════════════════════════════════════════

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5: Starting agent on EC2..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ssh -i "$KEY_PATH" ubuntu@$EC2_IP << 'START_AGENT'
set -e
cd ~/agent/green_agent

# Set environment variables
export EXPERIMENTS_PATH="/home/ubuntu/agent/experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro"
export AGENTBEATS_BACKEND_URL="https://agentbeats.org"

# Kill any existing agent
pkill -f main_http.py 2>/dev/null || true

# Start agent in background
nohup python3 main_http.py > agent.log 2>&1 &

echo "Agent started, waiting for it to be ready..."
sleep 5

# Test locally
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Agent is running!"
else
    echo "❌ Agent failed to start. Check logs:"
    tail -20 agent.log
    exit 1
fi
START_AGENT

# ═══════════════════════════════════════════════════════
# STEP 6: Test Public Access
# ═══════════════════════════════════════════════════════

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 6: Testing public access..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

sleep 3

echo "Testing /health endpoint:"
curl -s http://$EC2_IP:8080/health
echo ""

echo ""
echo "Testing /status endpoint:"
curl -s http://$EC2_IP:8080/status
echo ""

echo ""
echo "Testing agent card:"
curl -s http://$EC2_IP:8080/.well-known/agent-card.json | head -c 200
echo "..."

# ═══════════════════════════════════════════════════════
# SUCCESS!
# ═══════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║              🎉 DEPLOYMENT SUCCESSFUL! 🎉             ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Your Agent is LIVE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Your Permanent Agent URL:"
echo "   http://$EC2_IP:8080"
echo ""
echo "✅ Test it:"
echo "   curl http://$EC2_IP:8080/health"
echo "   curl http://$EC2_IP:8080/.well-known/agent-card.json"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Next Step: Register on AgentBeats"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Go to: https://agentbeats.org"
echo "2. Login and find 'Register Agent'"
echo "3. Enter your agent URL:"
echo ""
echo "   http://$EC2_IP:8080"
echo ""
echo "4. Fill in details:"
echo "   - Name: TheAgentCompany Benchmark Reporter"
echo "   - Type: Green Agent"
echo "   - Description: Reports TheAgentCompany benchmark results"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Useful Commands:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Connect to EC2:"
echo "  ssh -i \"$KEY_PATH\" ubuntu@$EC2_IP"
echo ""
echo "View agent logs:"
echo "  ssh -i \"$KEY_PATH\" ubuntu@$EC2_IP 'tail -f ~/agent/green_agent/agent.log'"
echo ""
echo "Restart agent:"
echo "  ssh -i \"$KEY_PATH\" ubuntu@$EC2_IP 'cd ~/agent/green_agent && pkill python3 && nohup python3 main_http.py > agent.log 2>&1 &'"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 You're all set! Your agent is running 24/7 on AWS!"
echo ""
