# Deploy Your Agent to AWS - Step by Step Guide

## Why AWS?

✅ **Permanent URL** - No expiration like ngrok/cloudflared  
✅ **No browser warnings** - Direct access  
✅ **Professional** - Real production deployment  
✅ **Free tier available** - First 12 months free for new accounts  

---

## AWS Deployment Options

### OPTION 1: AWS Lambda + API Gateway (Serverless) ⭐ EASIEST

**Cost**: FREE (within free tier limits)  
**Setup Time**: 15-30 minutes  
**Pros**: Scales automatically, pay per request  
**Cons**: Cold start delays  

### OPTION 2: AWS EC2 (Virtual Machine)

**Cost**: FREE t2.micro or t3.micro for 12 months  
**Setup Time**: 30-45 minutes  
**Pros**: Full control, always running  
**Cons**: Need to manage server  

### OPTION 3: AWS App Runner (Container) ⭐ RECOMMENDED

**Cost**: ~$5-10/month (no free tier)  
**Setup Time**: 10-15 minutes  
**Pros**: Easiest deployment, automatic HTTPS  
**Cons**: Not free  

### OPTION 4: AWS Lightsail (Simple VPS)

**Cost**: $3.50/month minimum  
**Setup Time**: 20 minutes  
**Pros**: Very simple, predictable pricing  
**Cons**: Not free  

---

## RECOMMENDED: AWS EC2 (Free Tier)

This gives you a permanent URL for FREE for 12 months!

### Step 1: Launch EC2 Instance

1. **Go to AWS Console**: https://console.aws.amazon.com/ec2/

2. **Launch Instance**:
   - Click "Launch Instance"
   - **Name**: `agentbeats-agent`
   - **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance Type**: t2.micro (Free tier eligible)
   - **Key pair**: Create new or use existing
   - **Network Settings**:
     - ✅ Allow SSH (port 22)
     - ✅ Allow HTTP (port 80)
     - ✅ Allow HTTPS (port 443)
     - ✅ Allow Custom TCP (port 8080)

3. **Launch** and wait ~2 minutes

### Step 2: Get Your Public IP

After launch, you'll see:
- **Public IPv4 address**: e.g., `54.123.45.67`
- **Public IPv4 DNS**: e.g., `ec2-54-123-45-67.compute-1.amazonaws.com`

### Step 3: Connect to Your Instance

```bash
# From your Mac terminal
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@54.123.45.67
```

### Step 4: Install Dependencies on EC2

```bash
# Update system
sudo apt update
sudo apt install -y python3-pip python3-venv git

# Create directory
mkdir -p ~/agent
cd ~/agent
```

### Step 5: Copy Your Agent Code

**From your Mac**:
```bash
# Copy the entire green_agent directory
scp -i your-key.pem -r \
  /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration/green_agent \
  ubuntu@54.123.45.67:~/agent/

# Copy the experiments data
scp -i your-key.pem -r \
  /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/experiments \
  ubuntu@54.123.45.67:~/agent/
```

### Step 6: Run Agent on EC2

**On EC2 instance**:
```bash
cd ~/agent/green_agent

# Install dependencies
pip3 install httpx fastapi uvicorn

# Set environment variable
export EXPERIMENTS_PATH="/home/ubuntu/agent/experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro"
export AGENTBEATS_BACKEND_URL="https://agentbeats.org"

# Run agent
nohup python3 main_http.py > agent.log 2>&1 &
```

### Step 7: Test Your Agent

```bash
# From your Mac
curl http://54.123.45.67:8080/health
# Should return: {"status":"healthy","agent":"TheAgentCompany Green Agent"}
```

### Step 8: Register with AgentBeats

Your agent URL is now:
```
http://ec2-54-123-45-67.compute-1.amazonaws.com:8080
```

Or use the IP:
```
http://54.123.45.67:8080
```

Register on AgentBeats with this URL!

---

## EASIER: AWS App Runner (If you can pay $5-10/month)

### Step 1: Prepare Your Agent

1. Create a `Dockerfile` in your `green_agent` directory:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements
RUN pip install httpx fastapi uvicorn

# Copy agent code
COPY main_http.py /app/
COPY agent_card.toml /app/

# Set environment variables
ENV PORT=8080
ENV AGENTBEATS_BACKEND_URL=https://agentbeats.org

EXPOSE 8080

CMD ["python", "main_http.py"]
```

2. **Push to GitHub** (if not already):
```bash
cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany
git add .
git commit -m "Add agent deployment files"
git push
```

### Step 2: Deploy to App Runner

1. Go to: https://console.aws.amazon.com/apprunner/
2. Click "Create service"
3. **Source**: 
   - Repository type: GitHub
   - Connect your GitHub account
   - Select your repository
4. **Build settings**:
   - Runtime: Python 3
   - Build command: (leave empty)
   - Start command: `python main_http.py`
5. **Service settings**:
   - Port: 8080
6. **Create & Deploy**

App Runner gives you a URL like:
```
https://abc123.us-east-1.awsapprunner.com
```

---

## ALTERNATIVE: Deploy with AWS Amplify (For containerized apps)

Or use **AWS Elastic Beanstalk** for a managed Python application.

---

## What I Recommend

### If you have AWS account:

**FREE Option**: Use **EC2 t2.micro** (free for 12 months)
- Permanent IP address
- Full control
- Can run 24/7

**Paid Option ($5/month)**: Use **App Runner**
- Easiest setup
- Auto-scaling
- Automatic HTTPS
- Just push code and deploy

### Quick Start Script

Would you like me to create a script that:
1. Sets up the EC2 instance automatically
2. Deploys your agent
3. Gets you the permanent URL

Or create a Dockerfile + deployment guide?

---

## Your Agent URL After AWS Deployment

Instead of:
```
https://ruby-nondoctrinaire-cohen.ngrok-free.dev  ❌ (expires, has warning)
```

You'll have:
```
http://ec2-54-123-45-67.compute-1.amazonaws.com:8080  ✅ (permanent, no warning)
```

Or with App Runner:
```
https://abc123.us-east-1.awsapprunner.com  ✅ (permanent, HTTPS, no warning)
```

---

## Next Steps

Let me know which option you prefer and I can:
1. Create the necessary configuration files
2. Generate deployment scripts
3. Walk you through the AWS setup

AWS will give you a **permanent, professional URL** that AgentBeats can access without any issues! 🚀
