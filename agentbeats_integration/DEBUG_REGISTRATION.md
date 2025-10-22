# AgentBeats Registration Debug Guide

## Quick Test Commands

### 1. Verify All Endpoints Work
```bash
# Root endpoint (must return 200 with JSON)
curl -v http://50.18.84.152:8080/

# Expected: HTTP/1.1 200 OK
# Expected Body: {"status":"healthy","agent":"TheAgentCompany Green Agent",...}

# Agent card (AgentBeats will check this)
curl -v http://50.18.84.152:8080/.well-known/agent-card.json

# Expected: HTTP/1.1 200 OK
# Expected Body: {"alias":"TheAgentCompany Benchmark Reporter","is_green":true,...}
```

### 2. Test What AgentBeats Backend Sees
```bash
# Simulate what AgentBeats validator does
curl -v -H "User-Agent: AgentBeats/1.0" http://50.18.84.152:8080/
curl -v -H "User-Agent: AgentBeats/1.0" http://50.18.84.152:8080/.well-known/agent-card.json
```

### 3. Try API Registration Directly
```bash
# Instead of using UI, try API endpoint
curl -X POST https://agentbeats.org/api/agents \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -v \
  -d '{
    "agent_url": "http://50.18.84.152:8080",
    "launcher_url": "http://50.18.84.152:8080",
    "is_green": true,
    "participant_requirements": []
  }'
```

## Common Issues to Check

### Issue 1: HTTPS Required
**Symptom**: Registration fails silently or shows "insecure connection" error  
**Solution**: Set up HTTPS with Let's Encrypt
```bash
# Install certbot and nginx
sudo apt update
sudo apt install -y nginx certbot python3-certbot-nginx

# Get a domain name first, then:
sudo certbot --nginx -d yourdomain.com
```

### Issue 2: Agent Card Schema Mismatch
**Symptom**: "Invalid agent card" error  
**Check**: Compare your agent card with the official schema
```bash
# View current agent card
curl http://50.18.84.152:8080/.well-known/agent-card.json | python3 -m json.tool

# Required fields (verify these exist):
# - alias (string)
# - is_green (boolean)
# - description (string)
# - participant_requirements (array)
# - capabilities (array)
# - version (string)
```

### Issue 3: Timeout Issues
**Symptom**: Registration takes long then fails  
**Check**: Response time
```bash
time curl http://50.18.84.152:8080/
# Should be < 5 seconds

# Check agent logs for errors
ssh -i agentbeats-key.pem ubuntu@50.18.84.152 "tail -50 ~/agent/green_agent/agent.log"
```

### Issue 4: IP Blocking / Geo-Restrictions
**Symptom**: Works in browser but registration fails  
**Test**: Try from different network
```bash
# Try registration from a VPN or different location
# Or use a proxy to test
```

### Issue 5: Port Issues
**Symptom**: "Cannot reach agent" error despite curl working  
**Check**: Try standard ports
```bash
# Some platforms only accept 80/443
# You might need Nginx proxy:
# External: http://50.18.84.152:80 -> Internal: localhost:8080
```

## What to Capture When Reporting Issues

1. **Exact error message from AgentBeats UI**
   - Screenshot the error
   - Copy any error text
   - Note the error code if shown

2. **Browser console logs**
   - Open Developer Tools (F12)
   - Go to Console tab
   - Copy any red error messages
   - Note any failed network requests

3. **Network tab in browser**
   - Open Developer Tools (F12)
   - Go to Network tab
   - Try registration
   - Find the failed request
   - Copy request/response headers and body

4. **Agent logs from EC2**
   ```bash
   ssh -i agentbeats-key.pem ubuntu@50.18.84.152
   tail -100 ~/agent/green_agent/agent.log
   ```

5. **AgentBeats API response**
   ```bash
   curl -X POST https://agentbeats.org/api/agents \
     -H "Content-Type: application/json" \
     -v \
     -d '{
       "agent_url": "http://50.18.84.152:8080",
       "launcher_url": "http://50.18.84.152:8080",
       "is_green": true,
       "participant_requirements": []
     }' 2>&1 | tee registration_debug.log
   ```

## Alternative Registration Methods

### Method 1: Use EC2 DNS Name
Instead of IP, try the DNS name:
```
agent_url: http://ec2-50-18-84-152.us-west-1.compute.amazonaws.com:8080
launcher_url: http://ec2-50-18-84-152.us-west-1.compute.amazonaws.com:8080
```

### Method 2: Use ngrok/cloudflare Tunnel (Temporary)
If AgentBeats requires HTTPS:
```bash
# On your local machine
ngrok http 50.18.84.152:8080

# Or use cloudflare tunnel
# Then register with the https:// URL provided
```

### Method 3: Contact AgentBeats Support
If all technical aspects check out:
- Look for AgentBeats Discord/Slack
- Check GitHub issues
- Email support if available
- Provide this debug log

## Validation Checklist

Before asking for help, verify:

- [ ] `curl http://50.18.84.152:8080/` returns 200 with JSON
- [ ] `curl http://50.18.84.152:8080/.well-known/agent-card.json` returns valid JSON
- [ ] Agent is running: `ssh ubuntu@50.18.84.152 "ps aux | grep main_http"`
- [ ] Port 8080 is open in security group
- [ ] Agent listening on 0.0.0.0:8080, not 127.0.0.1
- [ ] All JSON responses are valid (use jsonlint or python -m json.tool)
- [ ] Response times are fast (< 5 seconds)
- [ ] No error logs in agent.log
- [ ] Tried registration via API (not just UI)
- [ ] Captured exact error message from AgentBeats

## Quick Recovery Commands

If agent stops or needs restart:
```bash
# SSH into EC2
ssh -i agentbeats-key.pem ubuntu@50.18.84.152

# Restart agent
cd ~/agent/green_agent
export EXPERIMENTS_PATH="/home/ubuntu/agent/experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro"
export AGENTBEATS_BACKEND_URL="https://agentbeats.org"
pkill -f main_http.py
nohup python3 main_http.py > agent.log 2>&1 &

# Verify it started
sleep 3
curl http://localhost:8080/health

# Exit and test externally
exit
curl http://50.18.84.152:8080/health
```

---

**Status**: All technical requirements met. Registration failure is likely:
1. AgentBeats platform issue
2. HTTPS requirement
3. Schema validation we're missing
4. Account/permission issue on AgentBeats

**Next Step**: Need exact error message from AgentBeats to proceed.
