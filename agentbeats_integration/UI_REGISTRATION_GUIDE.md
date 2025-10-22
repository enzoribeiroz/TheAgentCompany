# 🎯 How to Register Your Agent via AgentBeats UI

## Current Setup Status

✅ **Agent Running**: `http://localhost:8080`  
✅ **Ngrok Tunnel**: `https://ruby-nondoctrinaire-cohen.ngrok-free.dev`  
✅ **Backend**: `https://agentbeats.org`  

---

## Step-by-Step UI Registration

### Step 1: Open AgentBeats Web Interface

Open your browser and go to:

```
https://agentbeats.org
```

**Common URLs to try if the above doesn't work:**
- https://agentbeats.org/
- https://agentbeats.org/app
- https://agentbeats.org/dashboard
- https://agentbeats.org/agents

### Step 2: Find the Agent Registration Section

Look for one of these options in the UI:
- "Register Agent" button
- "Add Agent" button
- "New Agent" link
- "My Agents" section with a "+" or "Add" button
- Navigation menu with "Agents" → "Register"

### Step 3: Fill in the Agent Details

When you find the registration form, enter these details:

**Required Fields:**

| Field | Value |
|-------|-------|
| **Alias/Name** | `TheAgentCompany Benchmark Reporter` |
| **Agent URL** | `https://ruby-nondoctrinaire-cohen.ngrok-free.dev` |
| **Launcher URL** | `https://ruby-nondoctrinaire-cohen.ngrok-free.dev` |
| **Agent Type** | Select "Green Agent" or check "Is Green" |
| **Battle Timeout** | `600` (seconds) or `10` (minutes) |

**Optional Fields (if present):**
- **Description**: "Aggregates and reports pre-computed TheAgentCompany benchmark results"
- **Version**: `1.0.0`
- **Participant Requirements**: Leave empty or set to `[]`

### Step 4: Handle the Ngrok Interstitial Page

When the UI tries to fetch your agent card from the ngrok URL, you might see:

1. **First visit to ngrok URL**: You'll see an ngrok interstitial page with a button saying "Visit Site"
2. **Click "Visit Site"** - this tells ngrok to allow traffic
3. **The registration should then succeed**

**Alternative**: Open the ngrok URL in a new tab first:
```
https://ruby-nondoctrinaire-cohen.ngrok-free.dev/card
```
Click through the ngrok interstitial page, then go back and register.

### Step 5: Verify Registration

After registration, you should see:
- ✅ Your agent listed in the agents page
- ✅ Agent status showing as "Online" or "Active"
- ✅ Agent card information displayed

---

## Testing Your Agent Card Manually

You can verify your agent card is accessible:

1. **Open in browser**: https://ruby-nondoctrinaire-cohen.ngrok-free.dev/card
2. **Click through ngrok page** if it appears
3. **You should see** JSON data like:
   ```json
   {
     "alias": "TheAgentCompany Benchmark Reporter",
     "is_green": true,
     "description": "Aggregates and reports pre-computed TheAgentCompany benchmark results (175 tasks across 6 categories)",
     "participant_requirements": [],
     "battle_timeout": 600,
     "capabilities": [
       "Load 175 pre-computed task evaluations",
       "Aggregate results by category (SDE, PM, DS, Admin, HR, Finance)",
       "Generate detailed markdown reports",
       "Report 30.29% overall pass rate"
     ],
     "version": "1.0.0"
   }
   ```

---

## Starting a Battle

Once your agent is registered:

### Option A: Via UI

1. **Navigate to Battles/Matches** section
2. **Click "New Battle"** or "Create Battle"
3. **Select your agent**: "TheAgentCompany Benchmark Reporter"
4. **Configure battle** (if needed):
   - Battle type: Single agent / Green agent battle
   - Timeout: 600 seconds
5. **Click "Start Battle"**

### Option B: Via API (if UI doesn't work)

If the UI is having issues, you can start a battle via API:

```bash
# First, get your agent_id from the UI or API
curl -s https://agentbeats.org/api/agents/my

# Then create a battle (replace AGENT_ID)
curl -X POST https://agentbeats.org/api/battles \
  -H "Content-Type: application/json" \
  -d '{
    "green_agent_id": "YOUR_AGENT_ID",
    "white_agents": [],
    "battle_config": {
      "timeout": 600
    }
  }'
```

---

## What Happens When Battle Starts

1. **Backend sends** `POST https://ruby-nondoctrinaire-cohen.ngrok-free.dev/a2a` with:
   ```json
   {
     "type": "battle_start",
     "battle_id": "battle_xyz123"
   }
   ```

2. **Your agent**:
   - Receives the message
   - Loads 175 task evaluations
   - Generates summary report
   - Posts results back to backend

3. **Watch your agent logs**:
   ```bash
   tail -f /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration/agent.log
   ```

4. **Results appear in UI** with:
   - Overall pass rate: 30.29%
   - 175 tasks analyzed
   - Category breakdown
   - Detailed markdown report

---

## Troubleshooting

### "Cannot find registration page"

The UI might be at a different route. Check:
- Browser console (F12) for any error messages
- Look for a "Sign In" or "Login" button (you might need an account)
- Check the documentation at https://agentbeats.org/docs

### "Agent registration failed"

1. **Check agent is running**:
   ```bash
   curl http://localhost:8080/health
   ```

2. **Check ngrok is running**:
   ```bash
   curl -s http://127.0.0.1:4040/api/tunnels
   ```

3. **Test the card endpoint**:
   ```bash
   curl http://localhost:8080/card
   ```

### "Agent shows as offline"

The backend might be trying to ping your agent. The ngrok interstitial can cause this. Solutions:
1. Click through the ngrok page once
2. Upgrade to ngrok paid ($8/mo removes interstitial)
3. Use alternative tunnel (cloudflared or localtunnel)

### "Battle starts but no results"

Check the agent logs:
```bash
tail -f agent.log
```

Look for:
- "Battle started: battle_xyz"
- "Loaded 175 task evaluations"
- "Results reported successfully"

---

## Alternative: Manual Battle Simulation

If the UI gives you trouble, you can test locally:

```bash
# Simulate battle start message
curl -X POST http://localhost:8080/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "type": "battle_start",
    "battle_id": "test_battle_123"
  }'

# Watch the logs to see it process
tail -20 agent.log
```

This will trigger your agent to load data and attempt to report results (though it will fail since the backend won't recognize the test battle ID).

---

## Quick Reference

**Your Agent URLs:**
- Local: `http://localhost:8080`
- Public: `https://ruby-nondoctrinaire-cohen.ngrok-free.dev`
- Health: `https://ruby-nondoctrinaire-cohen.ngrok-free.dev/health`
- Card: `https://ruby-nondoctrinaire-cohen.ngrok-free.dev/card`
- A2A: `https://ruby-nondoctrinaire-cohen.ngrok-free.dev/a2a`

**AgentBeats URLs:**
- Main: `https://agentbeats.org`
- API: `https://agentbeats.org/api`
- Docs: `https://agentbeats.org/api/docs`

**Monitoring:**
- Ngrok Dashboard: `http://127.0.0.1:4040`
- Agent Logs: `tail -f agent.log`

---

## Need Help?

If you're still stuck:

1. **Check agent logs**: `tail -50 agent.log`
2. **Check ngrok logs**: `tail -50 ngrok.log`
3. **Test endpoints manually** using the curl commands above
4. **Look for UI screenshots** in AgentBeats documentation
5. **Ask your instructor** for the exact registration flow

**Your agent is fully functional and ready to go!** The only step remaining is the UI registration process. 🚀
