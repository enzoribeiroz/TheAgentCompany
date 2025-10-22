#!/bin/bash

# AWS EC2 Deployment - Command Generator
# This script generates personalized commands for your deployment

echo "╔═══════════════════════════════════════════════════════╗"
echo "║   AWS EC2 Deployment - Command Generator             ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Get EC2 IP from user
read -p "Enter your EC2 Public IP address (e.g., 54.123.45.67): " EC2_IP

if [ -z "$EC2_IP" ]; then
    echo "❌ Error: EC2 IP is required"
    exit 1
fi

echo ""
echo "✅ Great! Generating personalized commands for IP: $EC2_IP"
echo ""
echo "═══════════════════════════════════════════════════════"
echo ""

# Generate commands file
COMMANDS_FILE="/Users/joe2690812044/Desktop/cs 195/TheAgentCompany/agentbeats_integration/MY_AWS_COMMANDS.sh"

cat > "$COMMANDS_FILE" << EOF
#!/bin/bash

# Personalized AWS Deployment Commands
# EC2 IP: $EC2_IP
# Generated: $(date)

# ═══════════════════════════════════════════════════════
# STEP 1: Setup SSH Key
# ═══════════════════════════════════════════════════════

echo "Setting up SSH key..."
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# If you downloaded the key to Downloads folder:
if [ -f ~/Downloads/agentbeats-key.pem ]; then
    mv ~/Downloads/agentbeats-key.pem ~/.ssh/
    echo "✅ Key moved to ~/.ssh/"
fi

chmod 400 ~/.ssh/agentbeats-key.pem
echo "✅ Key permissions set"

# ═══════════════════════════════════════════════════════
# STEP 2: Test Connection
# ═══════════════════════════════════════════════════════

echo ""
echo "Testing SSH connection..."
ssh -i ~/.ssh/agentbeats-key.pem -o StrictHostKeyChecking=no ubuntu@$EC2_IP 'echo "✅ SSH connection successful!"'

# ═══════════════════════════════════════════════════════
# STEP 3: Copy Files to EC2
# ═══════════════════════════════════════════════════════

echo ""
echo "Creating remote directory..."
ssh -i ~/.ssh/agentbeats-key.pem ubuntu@$EC2_IP 'mkdir -p ~/agent'

echo ""
echo "Copying agent code..."
scp -i ~/.ssh/agentbeats-key.pem -r \
  "/Users/joe2690812044/Desktop/cs 195/TheAgentCompany/agentbeats_integration/green_agent" \
  ubuntu@$EC2_IP:~/agent/

echo ""
echo "Copying experiments data (this may take a few minutes)..."
scp -i ~/.ssh/agentbeats-key.pem -r \
  "/Users/joe2690812044/Desktop/cs 195/TheAgentCompany/experiments" \
  ubuntu@$EC2_IP:~/agent/

echo ""
echo "✅ All files copied!"

# ═══════════════════════════════════════════════════════
# STEP 4: Install Dependencies and Start Agent
# ═══════════════════════════════════════════════════════

echo ""
echo "Installing dependencies and starting agent on EC2..."

ssh -i ~/.ssh/agentbeats-key.pem ubuntu@$EC2_IP << 'REMOTE_COMMANDS'
# Update system
echo "Updating system..."
sudo apt update -y

# Install Python
echo "Installing Python and dependencies..."
sudo apt install -y python3-pip python3-venv git

# Install Python packages
pip3 install httpx==0.28.1 fastapi==0.119.1 uvicorn==0.38.0

# Go to agent directory
cd ~/agent/green_agent

# Set environment variables
export EXPERIMENTS_PATH="/home/ubuntu/agent/experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro"
export AGENTBEATS_BACKEND_URL="https://agentbeats.org"

# Start agent
echo "Starting agent..."
nohup python3 main_http.py > agent.log 2>&1 &

# Wait for startup
sleep 5

# Test locally
echo ""
echo "Testing agent locally on EC2..."
curl -s http://localhost:8080/health

echo ""
echo "✅ Agent started successfully!"
REMOTE_COMMANDS

# ═══════════════════════════════════════════════════════
# STEP 5: Test Public Access
# ═══════════════════════════════════════════════════════

echo ""
echo "Testing public access from your Mac..."
sleep 2

curl -s http://$EC2_IP:8080/health
echo ""

curl -s http://$EC2_IP:8080/status
echo ""

# ═══════════════════════════════════════════════════════
# SUCCESS!
# ═══════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║              🎉 DEPLOYMENT SUCCESSFUL! 🎉             ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "Your Agent URL:"
echo "  http://$EC2_IP:8080"
echo ""
echo "Test it:"
echo "  curl http://$EC2_IP:8080/health"
echo "  curl http://$EC2_IP:8080/.well-known/agent-card.json"
echo ""
echo "Register on AgentBeats:"
echo "  1. Go to: https://agentbeats.org"
echo "  2. Login and find 'Register Agent'"
echo "  3. Enter URL: http://$EC2_IP:8080"
echo ""
echo "SSH to your EC2 instance anytime:"
echo "  ssh -i ~/.ssh/agentbeats-key.pem ubuntu@$EC2_IP"
echo ""
EOF

chmod +x "$COMMANDS_FILE"

echo "═══════════════════════════════════════════════════════"
echo ""
echo "✅ Personalized commands saved to:"
echo "   $COMMANDS_FILE"
echo ""
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Quick Commands:"
echo ""
echo "1. Connect to EC2:"
echo "   ssh -i ~/.ssh/agentbeats-key.pem ubuntu@$EC2_IP"
echo ""
echo "2. Test agent:"
echo "   curl http://$EC2_IP:8080/health"
echo ""
echo "3. Run full deployment:"
echo "   bash $COMMANDS_FILE"
echo ""
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📋 Next Steps:"
echo ""
echo "After launching your EC2 instance:"
echo "1. Run: bash $COMMANDS_FILE"
echo "2. Wait for completion (~5-10 minutes)"
echo "3. Your agent will be live at: http://$EC2_IP:8080"
echo "4. Register on https://agentbeats.org"
echo ""
echo "🎯 Your Agent URL: http://$EC2_IP:8080"
echo ""
