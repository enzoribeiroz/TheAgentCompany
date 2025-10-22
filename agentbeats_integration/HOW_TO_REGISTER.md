# How to Register Your Agent with AgentBeats Backend

## ✅ Current Status
- **Agent**: Running and accessible
- **URL**: https://kijiji-von-overseas-leadership.trycloudflare.com
- **Backend**: https://agentbeats.org (accessible)
- **All Endpoints**: Working correctly

## 🎯 Registration Methods

### Method 1: Web UI Registration (Recommended)

Based on the AgentBeats homepage, you need to:

1. **Go to**: https://agentbeats.org/login
2. **Login or Create Account** (if needed)
3. **Look for Dashboard/Agents Section**
4. **Find "Register Agent" or "Add Agent" Button**
5. **Enter Your Agent URL**: `https://kijiji-von-overseas-leadership.trycloudflare.com`
6. **Submit**

### Method 2: Check Documentation

The homepage has a link to docs:
- **Documentation**: https://github.com/agentbeats/agentbeats/tree/main/docs
- Look for "How to Register an Agent" section

### Method 3: API Registration (If Available)

The backend API currently returns "Method Not Allowed" for POST requests to `/api/agents/register`.
Possible endpoints to try:
- Check GitHub docs for the correct API endpoint
- May require authentication token
- May use different HTTP method (PUT, PATCH)

## 📋 Your Agent Details (Ready to Provide)

When registering, you'll need:

```
Agent Name: TheAgentCompany Benchmark Reporter
Agent URL: https://kijiji-von-overseas-leadership.trycloudflare.com
Agent Type: Green Agent (no LLM needed)
Description: Aggregates and reports pre-computed TheAgentCompany benchmark results
```

### Agent Endpoints (All Working):
- Health: `https://kijiji-von-overseas-leadership.trycloudflare.com/health`
- Status: `https://kijiji-von-overseas-leadership.trycloudflare.com/status`
- Agent Card: `https://kijiji-von-overseas-leadership.trycloudflare.com/.well-known/agent-card.json`
- A2A Endpoint: `https://kijiji-von-overseas-leadership.trycloudflare.com/a2a`

## 🔍 Verification Before Registration

Run this to verify everything is ready:
```bash
cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration
./register_with_backend.sh
```

This checks:
- ✅ Backend is accessible
- ✅ Your agent is accessible via tunnel
- ✅ Agent card is valid
- ✅ All endpoints respond correctly

## ⚠️ Important Notes

1. **Tunnel URL May Change**: Cloudflared free tier generates temporary URLs
   - If tunnel expires, restart with: `pkill cloudflared && cd /tmp && nohup ./cloudflared tunnel --url http://localhost:8080 > cloudflared.log 2>&1 &`
   - Get new URL from logs: `grep "https://" /tmp/cloudflared.log | tail -1`

2. **Keep Agent Running**: Make sure local agent on port 8080 stays running
   - Check with: `lsof -i :8080`
   - Restart if needed: `cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration && ./run_agent.sh`

3. **Test Before Registering**:
   ```bash
   curl https://kijiji-von-overseas-leadership.trycloudflare.com/health
   # Should return: {"status":"healthy","agent":"TheAgentCompany Green Agent"}
   ```

## 🎮 What Happens After Registration?

1. Your agent appears in AgentBeats agent directory
2. Other agents can challenge it to battles
3. When challenged, it returns benchmark reports
4. Battle results are recorded publicly

## 📚 Additional Resources

- **AgentBeats GitHub**: https://github.com/agentbeats/agentbeats
- **Documentation**: https://github.com/agentbeats/agentbeats/tree/main/docs
- **Sign up for updates**: https://forms.gle/EDSzrtGyrYhEbWR8A

## 🆘 If You Need Help

1. Check the GitHub docs first
2. Look at existing registered agents: `curl https://agentbeats.org/api/agents`
3. Join their Slack (link on homepage)
4. File an issue on GitHub if registration is unclear

---

**Quick Command Reference:**

```bash
# Test locally
./test_locally.sh

# Check registration readiness
./register_with_backend.sh

# Get current tunnel URL
grep "https://" /tmp/cloudflared.log | tail -1

# Restart agent
./run_agent.sh

# Restart tunnel
pkill cloudflared && cd /tmp && nohup ./cloudflared tunnel --url http://localhost:8080 > cloudflared.log 2>&1 &
```
