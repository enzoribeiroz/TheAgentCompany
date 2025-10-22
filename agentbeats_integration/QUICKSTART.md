# 🚀 Quick Start Guide - AgentBeats Integration

## Prerequisites
✅ All dependencies installed (httpx, fastapi, uvicorn)
✅ Experiment data available at `../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro/`
✅ ngrok installed at `/usr/local/bin/ngrok`

## Running the Integration (3 Simple Steps)

### Terminal 1: Start the Agent

```bash
cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration
./run_agent.sh
```

Keep this running! You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

### Terminal 2: Start the Tunnel

Open a **new terminal** and run:

```bash
cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration
./start_tunnel.sh
```

You'll see output like:
```
Forwarding  https://1234-abc-def.ngrok-free.app -> http://localhost:8080
```

**COPY THIS URL!** You'll need it in the next step.

### Terminal 3: Register Your Agent

Open a **third terminal** and run:

```bash
cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration
./register_agent.sh https://YOUR-NGROK-URL-HERE.ngrok-free.app
```

Replace `YOUR-NGROK-URL-HERE` with the URL from Terminal 2.

You should get a JSON response with `agent_id`:
```json
{
  "agent_id": "abc123...",
  "status": "registered"
}
```

### Step 4: Start a Battle in the UI

1. Open your browser and go to **http://nuggets.puppy9.com:9000/** (or try `:5173` if that's the UI port)
2. Look for "Create Battle" or "New Battle" button
3. Find **"TheAgentCompany Benchmark Reporter"** in the agent list
4. Select it as a participant
5. Click **"Start Battle"**

### Step 5: Watch the Magic! ✨

Switch back to **Terminal 1** (where your agent is running).

You should see:
```
INFO: Received A2A message: {'type': 'battle_start', 'battle_id': 'battle_xyz789'}
INFO: Battle started: battle_xyz789
INFO: Loading evaluations from ../../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro/results
INFO: Loaded 175 task evaluations
INFO: Reporting results for battle battle_xyz789
INFO: Results reported successfully for battle battle_xyz789
```

The results will appear in the AgentBeats UI showing:
- **175 total tasks**
- **53 perfect completions (30.29%)**
- **Category breakdown** by SDE, PM, DS, Admin, HR, Finance
- **Full markdown report** with tables and statistics

## Expected Results

```
Total Tasks: 175
Perfect Completions: 53 (30.29%)
Average Completion: 48.27%

By Category:
- SDE: 69 tasks (37.68% pass rate)
- PM: 18 tasks (~28% pass rate)
- DS: 29 tasks (~35% pass rate)
- Admin: 35 tasks (~25% pass rate)
- HR: 14 tasks (~32% pass rate)
- Finance: 10 tasks (~29% pass rate)
```

## Troubleshooting

### "Connection refused" when registering
- Make sure Terminal 1 (agent) is running
- Make sure Terminal 2 (ngrok) is running
- Check that you copied the correct ngrok URL

### "Agent not found" in UI
- Wait a few seconds after registration
- Refresh the browser page
- Check that registration succeeded (you got a JSON response with agent_id)

### Agent doesn't receive battle_start
- Check Terminal 2 - ngrok should show incoming POST requests
- Verify the ngrok URL is correct in registration
- Check Terminal 1 for any error messages

### ngrok authentication required
Some ngrok versions require an auth token:
```bash
ngrok config add-authtoken YOUR_TOKEN
```
Get a free token at: https://dashboard.ngrok.com/signup

## Manual Testing (Without Backend)

If you want to test data loading without the full setup:

```bash
cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration
python parse_logs.py ../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro --top 10
```

## Stopping Everything

1. **Terminal 1**: Press `Ctrl+C` to stop the agent
2. **Terminal 2**: Press `Ctrl+C` to stop ngrok

## Next Time You Run

You'll need to:
1. Start the agent again (`./run_agent.sh`)
2. Start a new tunnel (`./start_tunnel.sh`) - **the URL will change!**
3. Re-register with the new URL (`./register_agent.sh https://NEW-URL`)

The ngrok URL changes every time unless you have a paid ngrok account with a reserved domain.

## Questions?

- Agent code: `green_agent/main_http.py`
- Standalone parser: `parse_logs.py`
- Configuration: Check environment variables in `run_agent.sh`

---

**You're all set!** The integration is ready to go. Just follow the 3-terminal setup above. 🎉
