# 🚀 Deploy Your Agent to AWS EC2 - Complete Checklist

## ✅ Step-by-Step Guide (Copy and Follow)

### PART 1: Launch EC2 Instance (5-10 minutes)

#### 1. Go to AWS Console
- Open: https://console.aws.amazon.com/
- Login or create free account (12 months free tier!)

#### 2. Navigate to EC2
- In search bar, type "EC2"
- Click "EC2" service
- Or go directly to: https://console.aws.amazon.com/ec2/

#### 3. Launch Instance
Click the orange "Launch Instance" button

#### 4. Configure Instance

**Name and tags:**
```
Name: agentbeats-agent
```

**Application and OS Images (AMI):**
```
✅ Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
   - Free tier eligible
   - 64-bit (x86)
```

**Instance type:**
```
✅ t2.micro (Free tier eligible)
   - 1 vCPU, 1 GB RAM
```

**Key pair (login):**
```
Click "Create new key pair"
   - Key pair name: agentbeats-key
   - Key pair type: RSA
   - Private key format: .pem
   - Click "Create key pair"
   
📥 Your browser will download: agentbeats-key.pem
   Save it to: ~/Downloads/agentbeats-key.pem
```

**Network settings:**
Click "Edit" and configure:
```
✅ Auto-assign public IP: Enable

✅ Firewall (security groups): Create security group
   Security group name: agentbeats-sg
   Description: Security group for AgentBeats agent
   
   Add these rules:
   ✅ SSH (port 22) - Source: My IP
   ✅ HTTP (port 80) - Source: Anywhere (0.0.0.0/0)
   ✅ HTTPS (port 443) - Source: Anywhere (0.0.0.0/0)
   ✅ Custom TCP (port 8080) - Source: Anywhere (0.0.0.0/0)
```

**Configure storage:**
```
✅ 8 GB gp3 (default is fine, free tier eligible)
```

#### 5. Launch!
- Review everything
- Click "Launch instance"
- Wait ~2 minutes for it to start

#### 6. Get Your Instance Details
- Click "View all instances"
- Find your instance: agentbeats-agent
- Note these details:
  ```
  Public IPv4 address: _____________ (e.g., 54.123.45.67)
  Public IPv4 DNS: _____________ (e.g., ec2-54-123-45-67.compute-1.amazonaws.com)
  ```

---

### PART 2: Connect and Setup (10-15 minutes)

#### 7. Prepare SSH Key on Your Mac

Open Terminal on your Mac and run:

```bash
# Move key to safe location
mkdir -p ~/.ssh
mv ~/Downloads/agentbeats-key.pem ~/.ssh/

# Set proper permissions
chmod 400 ~/.ssh/agentbeats-key.pem
```

#### 8. Connect to EC2

Replace `YOUR_EC2_IP` with your actual IP:

```bash
ssh -i ~/.ssh/agentbeats-key.pem ubuntu@YOUR_EC2_IP
```

You should see:
```
Welcome to Ubuntu 22.04...
ubuntu@ip-xxx:~$
```

#### 9. Install Dependencies (On EC2)

Copy and paste these commands:

```bash
# Update system
sudo apt update

# Install Python and tools
sudo apt install -y python3-pip python3-venv git

# Install Python packages
pip3 install httpx==0.28.1 fastapi==0.119.1 uvicorn==0.38.0

# Create directory
mkdir -p ~/agent
```

---

### PART 3: Copy Your Agent Files (5 minutes)

#### 10. Open NEW Terminal on Your Mac (Keep EC2 connection open)

In a **new terminal window** on your Mac, run these commands:

**Replace `YOUR_EC2_IP` with your actual IP!**

```bash
# Set variables (EDIT THESE!)
EC2_IP="YOUR_EC2_IP"  # <- CHANGE THIS!
KEY="~/.ssh/agentbeats-key.pem"

# Create remote directory
ssh -i $KEY ubuntu@$EC2_IP 'mkdir -p ~/agent'

# Copy agent code
echo "Copying agent code..."
scp -i $KEY -r \
  "/Users/joe2690812044/Desktop/cs 195/TheAgentCompany/agentbeats_integration/green_agent" \
  ubuntu@$EC2_IP:~/agent/

# Copy experiments data
echo "Copying experiments data (this may take a few minutes)..."
scp -i $KEY -r \
  "/Users/joe2690812044/Desktop/cs 195/TheAgentCompany/experiments" \
  ubuntu@$EC2_IP:~/agent/

echo "✅ Files copied!"
```

---

### PART 4: Start Your Agent (2 minutes)

#### 11. Back in EC2 Terminal

```bash
cd ~/agent/green_agent

# Set environment variables
export EXPERIMENTS_PATH="/home/ubuntu/agent/experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro"
export AGENTBEATS_BACKEND_URL="https://agentbeats.org"

# Start agent in background
nohup python3 main_http.py > agent.log 2>&1 &

# Wait a moment
sleep 3

# Test it
curl http://localhost:8080/health
```

You should see:
```json
{"status":"healthy","agent":"TheAgentCompany Green Agent"}
```

✅ **Your agent is running!**

---

### PART 5: Test from Your Mac (1 minute)

#### 12. Test Public Access

From your **Mac terminal**:

```bash
# Replace with your EC2 IP
curl http://YOUR_EC2_IP:8080/health

# Test all endpoints
curl http://YOUR_EC2_IP:8080/status
curl http://YOUR_EC2_IP:8080/.well-known/agent-card.json
```

All should work! ✅

---

### PART 6: Register on AgentBeats (2 minutes)

#### 13. Your Permanent Agent URL

Your agent URL is one of these (both work):

**Option A (IP):**
```
http://YOUR_EC2_IP:8080
```

**Option B (DNS):**
```
http://ec2-XX-XX-XX-XX.compute-1.amazonaws.com:8080
```

#### 14. Register on AgentBeats

1. Go to: https://agentbeats.org
2. Login/Create account
3. Find "Register Agent" option
4. Enter your URL: `http://YOUR_EC2_IP:8080`
5. Fill in:
   - Name: TheAgentCompany Benchmark Reporter
   - Type: Green Agent
   - Description: Reports TheAgentCompany benchmark results
6. Submit!

---

### BONUS: Make Agent Auto-Start on Reboot

#### 15. Create Systemd Service (On EC2)

```bash
sudo tee /etc/systemd/system/agentbeats.service << 'EOF'
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
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable agentbeats
sudo systemctl start agentbeats

# Check status
sudo systemctl status agentbeats
```

Now your agent will automatically start when EC2 reboots! 🎉

---

## 📝 Quick Reference Commands

### On Your Mac:
```bash
# Connect to EC2
ssh -i ~/.ssh/agentbeats-key.pem ubuntu@YOUR_EC2_IP

# Test agent
curl http://YOUR_EC2_IP:8080/health
```

### On EC2:
```bash
# Check if agent is running
ps aux | grep main_http.py

# View logs
tail -f ~/agent/green_agent/agent.log

# Restart agent (if needed)
pkill python3
cd ~/agent/green_agent && nohup python3 main_http.py > agent.log 2>&1 &

# Check with systemd (if you set it up)
sudo systemctl status agentbeats
sudo systemctl restart agentbeats
```

---

## ✅ Final Checklist

- [ ] AWS account created
- [ ] EC2 instance launched (t2.micro)
- [ ] Security group configured (ports 22, 80, 443, 8080)
- [ ] SSH key downloaded and permissions set
- [ ] Connected to EC2
- [ ] Dependencies installed
- [ ] Agent files copied
- [ ] Agent started
- [ ] Tested locally on EC2
- [ ] Tested from Mac
- [ ] Registered on AgentBeats ✅

---

## 🎉 Success!

Your agent now has:
- ✅ Permanent URL (doesn't expire)
- ✅ No browser warnings
- ✅ 24/7 availability
- ✅ FREE (with AWS free tier for 12 months)

**Your Agent URL:**
```
http://YOUR_EC2_IP:8080
```

Use this to register on AgentBeats! 🚀

---

## 💰 Cost

- **First 12 months**: FREE (750 hours/month of t2.micro)
- **After 12 months**: ~$8/month
- **Data transfer**: First 15 GB/month free

---

## 🆘 Troubleshooting

**Can't connect via SSH?**
- Check security group has port 22 open for your IP
- Verify key permissions: `chmod 400 ~/.ssh/agentbeats-key.pem`

**Can't access agent from outside?**
- Check security group has port 8080 open
- Verify agent is running: `curl http://localhost:8080/health` on EC2

**Agent not starting?**
- Check logs: `tail -f ~/agent/green_agent/agent.log`
- Verify environment variables are set

**Need help?**
- AWS Support: https://console.aws.amazon.com/support/
- Check AWS documentation: https://docs.aws.amazon.com/ec2/

---

Ready to start? Let's go! 🚀
