# Registration Troubleshooting Guide

## Current Situation

You can open the URLs in browser and see valid JSON responses, but AgentBeats registration still fails with "Agent URL is not accessible".

## What to Check

### 1. Check Browser Console (MOST IMPORTANT!)

When you try to register in the AgentBeats UI:

1. **Open Developer Tools**: Press `F12` or `Cmd+Option+I` (Mac)
2. **Go to Console tab**: Look for any red error messages
3. **Go to Network tab**: 
   - Clear it (trash icon)
   - Try registration again
   - Find the request that failed (look for red ones)
   - Click on it
   - Check "Response" tab to see exact error message

This will tell us EXACTLY why it's failing!

### 2. Possible Issues

#### Issue A: CORS (Cross-Origin) Error
If browser console shows CORS error, we need to add CORS middleware to the agent.

**Solution**: Add to `main_http.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

# In __init__ after creating self.app:
self.app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Issue B: Missing Required Fields
AgentBeats might require additional fields we don't know about.

**To check**: Look at the API response or browser console for messages like "Missing field: X"

#### Issue C: Authentication Required
AgentBeats might require you to be logged in or have an API key.

**To check**: Are you logged into AgentBeats? Do you need to generate an API key first?

#### Issue D: Agent Card Schema Mismatch
The agent card might need specific fields in a specific format.

**To verify**: Compare with a working agent example on AgentBeats

#### Issue E: Network/DNS Issues
AgentBeats backend might not be able to resolve or reach ngrok URLs.

**To test**: Try with a different tunnel service or the EC2 URL (if we can get it working)

### 3. Debug Steps to Try

#### Step 1: Open Browser Console
```
1. Open AgentBeats registration page
2. Press F12 (or Cmd+Option+I on Mac)
3. Click "Console" tab
4. Try registration
5. Screenshot any red errors
```

#### Step 2: Check Network Tab
```
1. In Developer Tools, click "Network" tab
2. Click trash icon to clear
3. Try registration
4. Look for red/failed requests
5. Click on the failed request
6. Screenshot the "Response" tab
```

#### Step 3: Try Manual API Call
```bash
# In terminal, run this and copy the full output:
curl -X POST https://agentbeats.org/api/agents \
  -H "Content-Type: application/json" \
  -v \
  -d '{
    "alias": "TheAgentCompany Benchmark Reporter",
    "agent_url": "https://ruby-nondoctrinaire-cohen.ngrok-free.dev",
    "launcher_url": "https://ruby-nondoctrinaire-cohen.ngrok-free.dev",
    "is_green": true,
    "roles": []
  }' 2>&1
```

#### Step 4: Check If Agent Is Green-Enabled
Some platforms require agents to be explicitly enabled as "green" agents in settings.

**To check**: Look for agent settings or configuration in AgentBeats dashboard

#### Step 5: Look for Documentation
Check if AgentBeats has:
- Registration documentation
- API documentation  
- Example agents
- Support forum/Discord/Slack

---

## Quick Tests to Run Now

### Test 1: Verify All Endpoints Work
```bash
# Run these commands and verify all return JSON (not HTML):
curl https://ruby-nondoctrinaire-cohen.ngrok-free.dev/
curl https://ruby-nondoctrinaire-cohen.ngrok-free.dev/health
curl https://ruby-nondoctrinaire-cohen.ngrok-free.dev/status
curl https://ruby-nondoctrinaire-cohen.ngrok-free.dev/.well-known/agent-card.json
```

All should return JSON, not HTML or error pages.

### Test 2: Check Response Headers
```bash
curl -I https://ruby-nondoctrinaire-cohen.ngrok-free.dev/.well-known/agent-card.json
```

Should show:
```
HTTP/2 200
content-type: application/json
```

### Test 3: Test from Different Network
Try accessing the URLs from:
- Your phone (disconnect from WiFi, use cellular)
- A different computer
- An online service like https://reqbin.com/ or https://httpie.io/app

This checks if there's a network-level block.

---

## What Information to Gather

Please provide:

1. **Screenshot of browser console** when registration fails
2. **Screenshot of network tab** showing the failed request
3. **Output of this command**:
   ```bash
   curl -X POST https://agentbeats.org/api/agents \
     -H "Content-Type: application/json" \
     -v \
     -d '{"alias":"TheAgentCompany Benchmark Reporter","agent_url":"https://ruby-nondoctrinaire-cohen.ngrok-free.dev","launcher_url":"https://ruby-nondoctrinaire-cohen.ngrok-free.dev","is_green":true,"roles":[]}'
   ```
4. **Any error message** shown in AgentBeats UI
5. **Your AgentBeats account status** - are there any verification steps needed?

---

## Most Likely Culprits

Based on experience with similar platforms:

1. **CORS issue** (most common with web UIs)
2. **Missing authentication** (need to generate API key first)
3. **Account not verified** (need email verification or approval)
4. **Missing required field** in registration
5. **Rate limiting** (tried too many times)

---

## Next Step

**Please check the browser console** and share what error you see. That will tell us exactly what's wrong!
