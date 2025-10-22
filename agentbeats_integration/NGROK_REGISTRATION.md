# AgentBeats Registration with Ngrok

## Current Setup

**Ngrok URL**: `https://ruby-nondoctrinaire-cohen.ngrok-free.dev`  
**Local Agent**: Running on `localhost:8080`  
**Status**: ✅ All endpoints working

## Tested Endpoints

```bash
# Root endpoint
curl -H "ngrok-skip-browser-warning: true" https://ruby-nondoctrinaire-cohen.ngrok-free.dev/
# ✅ Returns: {"status":"healthy","agent":"TheAgentCompany Green Agent","version":"1.0.0","is_green":true}

# Health endpoint
curl -H "ngrok-skip-browser-warning: true" https://ruby-nondoctrinaire-cohen.ngrok-free.dev/health
# ✅ Returns: {"status":"healthy","agent":"TheAgentCompany Green Agent"}

# Agent card
curl -H "ngrok-skip-browser-warning: true" https://ruby-nondoctrinaire-cohen.ngrok-free.dev/.well-known/agent-card.json
# ✅ Returns valid agent card JSON
```

## ⚠️ Ngrok Free Tier Warning Page Issue

The problem with ngrok free tier is that it shows an interstitial warning page for first-time visitors:
- When AgentBeats backend tries to access the URL without the bypass header
- It gets HTML instead of JSON
- Registration fails

## Registration Options

### Option 1: Register with Ngrok URL (May Fail)

Go to https://agentbeats.org and register:

```
agent_url: https://ruby-nondoctrinaire-cohen.ngrok-free.dev
launcher_url: https://ruby-nondoctrinaire-cohen.ngrok-free.dev
is_green: ✓ (checked)
participant_requirements: [] (empty)
```

**Expected issue**: AgentBeats backend will likely get the warning page instead of agent card.

### Option 2: Try API Registration with Custom Headers

If AgentBeats API supports custom headers:

```bash
curl -X POST https://agentbeats.org/api/agents \
  -H "Content-Type: application/json" \
  -H "ngrok-skip-browser-warning: true" \
  -v \
  -d '{
    "agent_url": "https://ruby-nondoctrinaire-cohen.ngrok-free.dev",
    "launcher_url": "https://ruby-nondoctrinaire-cohen.ngrok-free.dev",
    "is_green": true,
    "participant_requirements": []
  }'
```

### Option 3: Use AWS EC2 URL (Recommended)

The EC2 deployment is more reliable:

```
agent_url: http://50.18.84.152:8080
launcher_url: http://50.18.84.152:8080
is_green: ✓ (checked)
participant_requirements: [] (empty)
```

**Advantages**:
- No interstitial warning page
- Permanent URL
- No tunnel service limitations
- More professional setup

### Option 4: Upgrade Ngrok (Paid Plan)

Ngrok paid plans remove the warning page:
- Go to https://ngrok.com/pricing
- Starting at $8/month
- No interstitial warning
- Custom domains available

## Current Services Running

```bash
# Check agent status
ps aux | grep main_http.py

# Check ngrok status
curl -s http://localhost:4040/api/tunnels | python3 -m json.tool

# Test agent locally
curl http://localhost:8080/health

# Test through ngrok (with bypass)
curl -H "ngrok-skip-browser-warning: true" https://ruby-nondoctrinaire-cohen.ngrok-free.dev/health
```

## Stopping Services

```bash
# Stop agent
pkill -f main_http.py

# Stop ngrok
pkill ngrok

# Or find and kill specific process
lsof -ti:8080 | xargs kill -9
```

## Recommendation

**Use the AWS EC2 deployment** for registration:
- More reliable
- No warning page issues
- Already deployed and working
- URL: `http://50.18.84.152:8080`

The ngrok setup is good for local development and testing, but EC2 is better for production registration with AgentBeats.

---

**Next Step**: Try registering with EC2 URL first. If that still fails, we need to:
1. Get the exact error message from AgentBeats
2. Check if HTTPS is required
3. Check if there are specific schema requirements
