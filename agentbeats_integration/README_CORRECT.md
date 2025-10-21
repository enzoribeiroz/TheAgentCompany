# TheAgentCompany - AgentBeats Integration

## 🎯 Quick Start (The Correct Way)

Based on the AgentBeats OpenAPI specification, here's the **actual workflow**:

```bash
# Create a venv by doing 
python3 -m venv .venv

# enter the venv
source .venv/bin/activate (on linux based systems)

# 1. Install dependencies
pip install httpx fastapi uvicorn

# 2. Start your green agent
cd agentbeats_integration/green_agent
python main_http.py

# 3. Agent runs at http://localhost:8080 and connects to http://nuggets.puppy9.com:9000

# 4. Go to AgentBeats UI and start a battle
# 5. Select "TheAgentCompany Benchmark Reporter" as participant
# 6. Results appear automatically in the UI
```

## Architecture: HTTP-Based Communication

```
┌──────────────────────────────────────────────────────────────┐
│         AgentBeats Backend (Official Deployment)              │
│              http://nuggets.puppy9.com:9000                   │
│                                                                │
│  ┌──────────────┐         ┌─────────────┐                    │
│  │   REST API   │         │  Battle     │                    │
│  │  /agents     │◄────────│  Manager    │                    │
│  │  /battles    │         │             │                    │
│  └──────┬───────┘         └──────┬──────┘                    │
│         │                        │                            │
└─────────┼────────────────────────┼────────────────────────────┘
          │                        │
          │ 1. POST /agents        │ 2. A2A: battle_start
          │    (registration)      │    (with battle_id)
          │                        │
          ▼                        ▼
   ┌──────────────────────────────────────────┐
   │  Your Green Agent (Local)                │
   │  http://localhost:8080                   │
   │                                           │
   │  ┌────────────────┐   ┌────────────────┐│
   │  │  FastAPI       │   │  Log Parser    ││
   │  │  Server        │───│  & Aggregator  ││
   │  │  (A2A Handler) │   │                ││
   │  └────────────────┘   └────────────────┘│
   └────────────┬──────────────────────────────┘
                │
                │ 3. POST /battles/{battleId}
                │    (final results)
                │
                ▼
         [Backend stores & displays results]
```

## The Three-Step Dance

### Step 1: Register Your Agent

**Your agent makes:** `POST http://nuggets.puppy9.com:9000/agents`

```json
{
  "alias": "TheAgentCompany Benchmark Reporter",
  "agent_url": "http://YOUR_IP:8080",
  "launcher_url": "http://YOUR_IP:8080",
  "is_green": true,
  "participant_requirements": [],
  "battle_timeout": 600
}
```

**Backend responds with:** `{ "agent_id": "abc123..." }`

### Step 2: Receive Battle Start

**Backend sends to your agent:** `POST http://YOUR_IP:8080/a2a`

```json
{
  "type": "battle_start",
  "battle_id": "battle_xyz789",
  "timestamp": "2025-10-20T10:00:00Z"
}
```

Your agent receives this, extracts `battle_id`, and starts processing.

### Step 3: Report Results

**Your agent makes:** `POST http://nuggets.puppy9.com:9000/battles/battle_xyz789`

```json
{
  "is_result": true,
  "timestamp": "2025-10-20T10:05:00Z",
  "message": "TheAgentCompany benchmark results successfully aggregated.",
  "winner": "N/A",
  "reported_by": "TheAgentCompany Green Agent",
  "detail": {
    "overall_pass_rate": 0.3029,
    "total_tasks": 175,
    "perfect_tasks": 53,
    "categories": {
      "sde": { "pass_rate": 0.3768, "avg_steps": 25.5 },
      "pm": { "pass_rate": 0.28, "avg_steps": 30.2 },
      "ds": { "pass_rate": 0.35, "avg_steps": 22.1 },
      "admin": { "pass_rate": 0.25, "avg_steps": 18.5 },
      "hr": { "pass_rate": 0.32, "avg_steps": 20.8 },
      "finance": { "pass_rate": 0.29, "avg_steps": 24.3 }
    }
  },
  "markdown_content": "# TheAgentCompany Benchmark Results\n\n..."
}
```

## File Structure

```
agentbeats_integration/
├── green_agent/
│   ├── main_http.py         # NEW: HTTP-based implementation ✨
│   ├── main.py              # OLD: A2A SDK-based (legacy)
│   └── agent_card.toml      # Agent configuration
├── scenarios/
│   └── theagentcompany_eval/
│       └── scenario.toml    # Scenario definition
├── parse_logs.py            # Standalone utility
├── requirements.txt         # Updated with httpx, fastapi, uvicorn
├── .env.template            # Environment variables
└── README_CORRECT.md        # This file
```

## Environment Variables

```bash
# .env file
AGENTBEATS_BACKEND_URL=http://nuggets.puppy9.com:9000
EXPERIMENTS_PATH=../../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro
AGENT_HOST=0.0.0.0
AGENT_PORT=8080
```

## Running Your Agent

### Option 1: Direct Python (Simplest)

```bash
cd agentbeats_integration/green_agent

# Set environment variables
export AGENTBEATS_BACKEND_URL=http://nuggets.puppy9.com:9000
export EXPERIMENTS_PATH=../../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro

# Run the agent
python3 main_http.py
```

### Option 2: With .env file

```bash
# Copy and edit environment template
cp .env.template .env
nano .env  # Edit your paths

# Run with environment loaded
python3 -c "from dotenv import load_dotenv; load_dotenv(); exec(open('green_agent/main_http.py').read())"
```

### Option 3: Via AgentBeats CLI (if applicable)

```bash
# From agentbeats repository
cd /path/to/agentbeats
agentbeats run /path/to/agentbeats_integration/green_agent/agent_card.toml
```

## Testing Standalone (Without Backend)

Use the standalone log parser to verify your data loads correctly:

```bash
cd agentbeats_integration

# View top 10 tasks
python3 parse_logs.py ../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro --top 10

# Filter by category
python3 parse_logs.py ../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro --category sde

# Export to CSV
python3 parse_logs.py ../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro --format csv --output results.csv
```

## Expected Results

From the experiment logs (OpenHands 0.28.1 with Gemini 2.5 Pro):

- **Total Tasks**: 175
- **Perfect Completions**: 53 (30.29%)
- **Average Completion Rate**: 48.27%
- **By Category**:
  - SDE: 69 tasks, 26 perfect (37.68%)
  - PM, DS, Admin, HR, Finance: Various completion rates

## Troubleshooting

### "Connection refused to nuggets.puppy9.com:9000"

**Check:** Is the backend actually running and accessible?

```bash
curl http://nuggets.puppy9.com:9000/health
```

If this fails, you may need to deploy your own backend or get access credentials.

### "Import httpx could not be resolved"

**Solution:**
```bash
pip install httpx fastapi uvicorn
```

### "Experiments path not found"

**Solution:** Update `EXPERIMENTS_PATH` in your `.env` or environment to point to the correct location:

```bash
export EXPERIMENTS_PATH=/absolute/path/to/experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro
```

### "Agent not receiving battle_start signal"

**Check:**
1. Is your agent accessible from the backend? (firewall, NAT issues)
2. Did you register with the correct `agent_url`?
3. Check agent logs for incoming requests

## Key Differences from Previous Approach

| Old Approach | New Approach (Correct) |
|--------------|------------------------|
| Tried to use `ab deploy` | No deployment needed |
| Expected SDK to handle everything | Direct HTTP calls to API |
| Looked for MCP server locally | Uses remote backend at nuggets.puppy9.com |
| Complex A2A SDK integration | Simple FastAPI server for A2A messages |
| Unclear registration flow | Explicit POST /agents registration |

## Next Steps After Getting It Working

1. **Add Authentication**: Backend may require API keys or tokens
2. **Handle Registration Errors**: Retry logic, validation
3. **Persist Agent ID**: Save agent_id to avoid re-registering
4. **Rich Reporting**: Add charts, graphs, detailed breakdowns
5. **Multiple Experiments**: Support comparing different model runs
6. **Real-time Updates**: Stream progress instead of waiting for completion

## References

- [AgentBeats OpenAPI Spec](http://nuggets.puppy9.com:9000/docs) - The source of truth
- [TheAgentCompany Paper](https://arxiv.org/abs/2412.14161)
- [TheAgentCompany GitHub](https://github.com/TheAgentCompany/TheAgentCompany)

## License

Same as TheAgentCompany (MIT License)
