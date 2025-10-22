# ✅ Registration Complete Guide

## Current Status

**Agent Running**: ✅ On port 8080  
**Tunnel Active**: ✅ https://bridges-chef-hansen-displayed.trycloudflare.com  
**Backend**: ✅ https://agentbeats.org  

## How to Register with Backend

### ✅ CORRECT API Endpoint

```bash
POST https://agentbeats.org/api/agents
```

### Required Request Body

```json
{
  "alias": "TheAgentCompany Benchmark Reporter",
  "agent_url": "https://bridges-chef-hansen-displayed.trycloudflare.com",
  "launcher_url": "https://bridges-chef-hansen-displayed.trycloudflare.com",
  "is_green": true,
  "participant_requirements": [],
  "battle_timeout": 600
}
```

### Quick Registration Command

```bash
# Get current tunnel URL
AGENT_URL=$(grep -oE "https://[^[:space:]]+" /tmp/cloudflared.log | tail -1)

# Register
curl -X POST https://agentbeats.org/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "alias": "TheAgentCompany Benchmark Reporter",
    "agent_url": "'"$AGENT_URL"'",
    "launcher_url": "'"$AGENT_URL"'",
    "is_green": true,
    "participant_requirements": [],
    "battle_timeout": 600
  }'
```

## ⚠️ Current Issue

**Problem**: Backend returns `"Failed to get agent card from agent_url"`

**Possible Causes**:
1. Backend might be checking a different URL path for the agent card
2. Cloudflared tunnel might have CORS or SSL issues
3. Backend might timeout before cloudflared establishes connection
4. Backend might be checking `/card` instead of `/.well-known/agent-card.json`

## 🔧 Troubleshooting Steps

### 1. Verify Your Agent Card is Accessible

```bash
# Get current URL
URL=$(grep -oE "https://[^[:space:]]+" /tmp/cloudflared.log | tail -1)

# Test all card endpoints
echo "Testing: $URL/.well-known/agent-card.json"
curl -v "$URL/.well-known/agent-card.json"

echo "Testing: $URL/card"
curl -v "$URL/card"
```

### 2. Check What Backend is Requesting

Look at your agent logs to see what URL path the backend is trying to fetch.

### 3. Restart Everything

```bash
# 1. Stop old processes
pkill cloudflared
lsof -ti:8080 | xargs kill -9 2>/dev/null

# 2. Start agent
cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration
./run_agent.sh &

# 3. Wait for agent to start
sleep 5

# 4. Start tunnel
cd /tmp
nohup ./cloudflared tunnel --url http://localhost:8080 > cloudflared.log 2>&1 &

# 5. Wait and get URL
sleep 8
grep -oE "https://[^[:space:]]+" cloudflared.log | tail -1
```

## 🎯 Alternative: Use AgentBeats CLI

Instead of manual registration, you can use the AgentBeats CLI if you have it installed:

```bash
# Install agentbeats
pip install agentbeats

# Create a scenario.toml file
# Then run
ab load_scenario /path/to/scenario
```

## 📝 What We Know Works

✅ **Local Agent**: Fully functional on http://localhost:8080  
✅ **All Endpoints**: /health, /status, /card, /.well-known/agent-card.json, /a2a  
✅ **Data Loading**: 175 tasks load correctly  
✅ **Tunnel Setup**: Cloudflared runs and creates public URLs  
✅ **Agent Card**: Valid JSON returned  

❌ **Registration**: Backend can't fetch agent card (reason unclear)

## 🌐 Current Tunnel URL

**Latest**: https://bridges-chef-hansen-displayed.trycloudflare.com

**Note**: This URL will expire. To get the current URL:
```bash
grep -oE "https://[^[:space:]]+" /tmp/cloudflared.log | tail -1
```

## 💡 Recommendation

The registration issue might be:
1. A backend-side configuration
2. Cloudflared tunnel compatibility issue
3. SSL/TLS verification problem

**Best approach**: 
- Check the AgentBeats GitHub issues for similar problems
- Ask in their Slack channel
- Try using a more stable tunnel service (like ngrok paid tier, or actual domain/server)

---

**Last Updated**: Just now  
**Agent Status**: Running  
**Tunnel Status**: Active but registration fails
