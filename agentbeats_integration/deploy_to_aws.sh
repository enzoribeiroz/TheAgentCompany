#!/bin/bash

# Quick AWS EC2 Deployment Script for TheAgentCompany Agent

echo "╔═════════════════════════════════════════════════╗"
echo "║   AWS EC2 Deployment Instructions              ║"
echo "╚═════════════════════════════════════════════════╝"
echo ""

cat << 'EOF'
This script helps you deploy your agent to AWS EC2.

PREREQUISITES:
1. AWS Account (sign up at aws.amazon.com)
2. AWS EC2 instance launched (t2.micro for free tier)
3. SSH key pair downloaded (.pem file)
4. Security group allowing ports: 22, 80, 443, 8080

STEPS TO DEPLOY:

Step 1: Launch EC2 Instance
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Go to: https://console.aws.amazon.com/ec2/
2. Click "Launch Instance"
3. Choose:
   - Name: agentbeats-agent
   - AMI: Ubuntu Server 22.04 LTS
   - Instance type: t2.micro (Free tier)
   - Create or select key pair
   - Allow ports: 22, 80, 443, 8080
4. Launch and note your Public IP

Step 2: Connect to EC2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run these commands from your Mac:

EOF

echo "# Make key readable"
echo "chmod 400 ~/Downloads/your-key.pem"
echo ""
echo "# Connect to EC2 (replace with your IP and key)"
echo "ssh -i ~/Downloads/your-key.pem ubuntu@YOUR_EC2_IP"
echo ""

cat << 'EOF'

Step 3: On EC2, Install Dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run these on your EC2 instance:

EOF

cat << 'SETUP_SCRIPT'
sudo apt update
sudo apt install -y python3-pip python3-venv git
pip3 install httpx fastapi uvicorn
SETUP_SCRIPT

echo ""

cat << 'EOF'

Step 4: Copy Your Agent to EC2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
From your Mac, run:

EOF

EC2_IP="YOUR_EC2_IP"
KEY_PATH="~/Downloads/your-key.pem"
AGENT_PATH="/Users/joe2690812044/Desktop/cs 195/TheAgentCompany/agentbeats_integration"

echo "# Create directory on EC2"
echo "ssh -i $KEY_PATH ubuntu@$EC2_IP 'mkdir -p ~/agent'"
echo ""
echo "# Copy agent code"
echo "scp -i $KEY_PATH -r $AGENT_PATH/green_agent ubuntu@$EC2_IP:~/agent/"
echo ""
echo "# Copy experiments data"
echo "scp -i $KEY_PATH -r /Users/joe2690812044/Desktop/cs\\ 195/TheAgentCompany/experiments ubuntu@$EC2_IP:~/agent/"
echo ""

cat << 'EOF'

Step 5: Start Agent on EC2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Back on your EC2 instance, run:

EOF

cat << 'RUN_SCRIPT'
cd ~/agent/green_agent

# Set environment variables
export EXPERIMENTS_PATH="/home/ubuntu/agent/experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro"
export AGENTBEATS_BACKEND_URL="https://agentbeats.org"

# Run agent in background
nohup python3 main_http.py > agent.log 2>&1 &

# Check it's running
sleep 3
curl http://localhost:8080/health
RUN_SCRIPT

echo ""

cat << 'EOF'

Step 6: Test From Your Mac
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF

echo "curl http://$EC2_IP:8080/health"
echo ""

cat << 'EOF'

Step 7: Register on AgentBeats
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your permanent agent URL is:

EOF

echo "http://$EC2_IP:8080"
echo ""
echo "Or use the DNS name:"
echo "http://ec2-XX-XX-XX-XX.compute-1.amazonaws.com:8080"
echo ""

cat << 'EOF'

Use this URL to register on https://agentbeats.org

BONUS: Make Agent Auto-Start on Reboot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
On EC2, create a systemd service:

EOF

cat << 'SERVICE'
sudo tee /etc/systemd/system/agentbeats.service << 'SERVICEEOF'
[Unit]
Description=AgentBeats Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/agent/green_agent
Environment="EXPERIMENTS_PATH=/home/ubuntu/agent/experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro"
Environment="AGENTBEATS_BACKEND_URL=https://agentbeats.org"
ExecStart=/usr/bin/python3 /home/ubuntu/agent/green_agent/main_http.py
Restart=always

[Install]
WantedBy=multi-user.target
SERVICEEOF

sudo systemctl daemon-reload
sudo systemctl enable agentbeats
sudo systemctl start agentbeats
sudo systemctl status agentbeats
SERVICE

echo ""
echo "╔═════════════════════════════════════════════════╗"
echo "║   After deployment, your agent will have:      ║"
echo "║   ✅ Permanent URL                              ║"
echo "║   ✅ No expiration                              ║"
echo "║   ✅ No browser warnings                        ║"
echo "║   ✅ 24/7 availability                          ║"
echo "╚═════════════════════════════════════════════════╝"
