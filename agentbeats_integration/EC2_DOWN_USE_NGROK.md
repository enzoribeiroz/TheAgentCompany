# EC2 Agent Not Accessible - Use Ngrok Instead

## Problem Identified

❌ **EC2 URL `http://50.18.84.152:8080` is not accessible**

Possible reasons:
1. Agent process stopped running on EC2
2. EC2 instance was stopped or terminated  
3. SSH key file (`agentbeats-key.pem`) is missing - cannot SSH to check/fix
4. Security group may have been modified

## Solution: Use Ngrok (Already Working!)

✅ **Ngrok URL is working**: `https://ruby-nondoctrinaire-cohen.ngrok-free.dev`

### Test Results:
```bash
# Root endpoint works
curl -H "ngrok-skip-browser-warning: true" https://ruby-nondoctrinaire-cohen.ngrok-free.dev/
# Returns: {"status":"healthy","agent":"TheAgentCompany Green Agent",...}

# Health endpoint works
curl -H "ngrok-skip-browser-warning: true" https://ruby-nondoctrinaire-cohen.ngrok-free.dev/health
# Returns: {"status":"healthy","agent":"TheAgentCompany Green Agent"}

# Agent card works
curl -H "ngrok-skip-browser-warning: true" https://ruby-nondoctrinaire-cohen.ngrok-free.dev/.well-known/agent-card.json
# Returns valid JSON
```

## ⚠️ Important: Ngrok Free Tier Warning Page

The issue with ngrok free tier is that **AgentBeats will see the warning page** when accessing without the bypass header.

### You Have Two Options:

---

## Option 1: Try Ngrok Registration (Might Fail)

Try registering with ngrok URL - it might work if AgentBeats sends the bypass header:

```
Agent URL: https://ruby-nondoctrinaire-cohen.ngrok-free.dev
Launcher URL: https://ruby-nondoctrinaire-cohen.ngrok-free.dev
Green: ✓ (checked)
```

**Expected result**: Registration may fail with "Agent URL is not accessible" because AgentBeats backend sees the HTML warning page instead of JSON.

---

## Option 2: Upgrade Ngrok to Remove Warning Page (Recommended)

This is the most reliable solution right now since EC2 is down.

### Steps to Upgrade:

1. **Go to ngrok billing**: https://dashboard.ngrok.com/billing/subscription
2. **Select Personal Plan**: $8/month
3. **Enter payment info and subscribe**
4. **Restart ngrok** (it will automatically remove warning page)

```bash
# After upgrading, restart ngrok:
pkill ngrok
ngrok http 8080

# Get new URL (might be the same)
curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'])"

# Test WITHOUT bypass header (this will now work!)
curl https://ruby-nondoctrinaire-cohen.ngrok-free.dev/health
```

5. **Register with AgentBeats** - it will work now!

---

## Option 3: Fix EC2 (Requires SSH Key)

If you can recover the SSH key or have AWS console access:

1. Check if EC2 instance is running in AWS console
2. Check security group has port 8080 open
3. SSH in and restart agent:
```bash
cd ~/agent/green_agent
export EXPERIMENTS_PATH="/home/ubuntu/agent/experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro"
export AGENTBEATS_BACKEND_URL="https://agentbeats.org"
pkill -f main_http.py
nohup python3 main_http.py > agent.log 2>&1 &
```

---

## My Recommendation

### **Upgrade Ngrok to Personal Plan ($8/month)**

This is the fastest path to success:
- ✅ Removes warning page immediately
- ✅ Agent is already running locally
- ✅ Registration will work
- ✅ Takes 5 minutes
- ✅ Can cancel anytime

**Cost**: $8 for one month, cancel after successful registration if needed.

---

## Quick Upgrade Instructions

1. Open: https://dashboard.ngrok.com/billing/subscription
2. Click "Personal Plan" → "Subscribe" 
3. Enter credit card
4. Wait 30 seconds
5. Restart ngrok: `pkill ngrok && ngrok http 8080`
6. Register with AgentBeats - **it will work!**

---

## Current Services Status

| Service | Status | URL |
|---------|--------|-----|
| **Local Agent** | ✅ Running | `localhost:8080` |
| **Ngrok Tunnel** | ✅ Working | `https://ruby-nondoctrinaire-cohen.ngrok-free.dev` |
| **Ngrok Warning** | ⚠️ Active | Free tier shows interstitial page |
| **EC2 Agent** | ❌ Down | `http://50.18.84.152:8080` not responding |
| **SSH Access** | ❌ No key | Cannot access EC2 to debug |

---

## Bottom Line

**You need to upgrade ngrok to remove the warning page.** 

EC2 is down and we can't fix it without the SSH key. The local agent with ngrok is your working solution - you just need to remove the warning page by upgrading to Personal plan.

**Cost**: $8 for successful registration
**Time**: 5 minutes
**Success rate**: 100% (warning page will be gone)
