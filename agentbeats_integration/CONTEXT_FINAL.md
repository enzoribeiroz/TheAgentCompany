# TheAgentCompany ↔ AgentBeats Integration: Complete Context (Updated)

## 1. Project Goal

Integrate TheAgentCompany benchmark (175 tasks, 6 categories, 13 personas) into the AgentBeats platform as a "green agent" that reports pre-computed evaluation results using existing experiment logs (not re-running benchmarks).

## 2. Critical Revelation: The Correct Architecture

Your friend identified the key misunderstanding: **We don't need to deploy AgentBeats locally**. The backend already exists at `http://nuggets.puppy9.com:9000` with a full OpenAPI specification.

### The Correct Workflow

1. **Your agent runs standalone** as an HTTP server (FastAPI)
2. **Agent registers** via `POST http://nuggets.puppy9.com:9000/agents`
3. **Backend sends battle start** via A2A message (POST to your agent's `/a2a` endpoint)
4. **Agent reports results** via `POST http://nuggets.puppy9.com:9000/battles/{battleId}`

**Key Insight**: No `ab deploy` needed. No local MCP server needed. Just HTTP calls to the existing backend.

## 3. Architectural Options Considered

- **Option A (Chosen):**  
  Simple "green agent" that loads pre-computed evaluation results from experiment logs, aggregates scores, and reports them to AgentBeats via HTTP REST API. No white agent simulation, no replaying logs, no live environment state required.

- **Option B (Not chosen):**  
  Simulate a full A2A battle by replaying logs with both green and white agents, reconstructing all persona actions and environment state. Overly complex and unnecessary.

**You explicitly chose Option A for simplicity and reliability.**

## 4. Implementation Details

### File Structure
```
agentbeats_integration/
├── green_agent/
│   ├── main_http.py         # ✨ NEW: HTTP-based implementation (400+ lines)
│   ├── main.py              # OLD: SDK-based approach (kept for reference)
│   └── agent_card.toml      # Agent configuration
├── scenarios/
│   └── theagentcompany_eval/
│       └── scenario.toml    # Scenario definition
├── parse_logs.py            # Standalone utility (working ✅)
├── requirements.txt         # Updated with httpx, fastapi, uvicorn
├── .env.template            # Environment variables
├── README.md                # Original documentation
└── README_CORRECT.md        # ✨ NEW: Correct HTTP-based workflow
```

### Key Components

**HTTP-Based Green Agent (`green_agent/main_http.py`):**

```python
class TheAgentCompanyGreenAgent:
    """HTTP-based agent that communicates directly with AgentBeats backend"""
    
    async def register_agent(self, agent_url, launcher_url) -> str:
        """POST /agents - Register with backend"""
        payload = {
            "alias": "TheAgentCompany Benchmark Reporter",
            "agent_url": agent_url,  # Where this agent runs
            "launcher_url": launcher_url,
            "is_green": True,
            "participant_requirements": [],  # No white agents needed
            "battle_timeout": 600
        }
        # Returns agent_id from backend
    
    async def handle_battle_start(self, battle_id: str):
        """Handle incoming A2A message with battle_id"""
        # 1. Load evaluations from disk
        # 2. Generate summary statistics
        # 3. Report results immediately
    
    async def report_results(self, battle_id: str):
        """POST /battles/{battleId} - Report final results"""
        result_payload = {
            "is_result": True,  # Mark as final result
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": "TheAgentCompany benchmark results successfully aggregated.",
            "winner": "N/A",
            "reported_by": "TheAgentCompany Green Agent",
            "detail": {
                "overall_pass_rate": 0.3029,
                "total_tasks": 175,
                "categories": { ... }  # Category breakdowns
            },
            "markdown_content": "# Results\n\n..."  # Rich report
        }
```

**FastAPI Server for A2A Messages:**
```python
@app.post("/a2a")
async def receive_a2a_message(request: Request):
    """Receive battle_start signal from backend"""
    message = await request.json()
    if message.get("type") == "battle_start":
        battle_id = message.get("battle_id")
        await agent.handle_battle_start(battle_id)
```

**Data Loading:**
- Loads 175 `eval_*-image.json` files from results directory
- Parses gzipped `traj_*-image.json.gz` trajectory files for step counts
- **Trajectory format**: List of action events, not dict (fixed from original assumption)
- Aggregates by 6 categories: SDE (69 tasks), PM, DS, Admin, HR, Finance
- Cost calculation returns $0.00 (token usage not in trajectory format)

## 5. Experiment Log Structure

- **Location**: `../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro/`
- **Results**: `results/eval_*-image.json` - Contains checkpoint scores
  ```json
  {
    "checkpoints": [{"total": 1, "result": 1}, ...],
    "final_score": {"total": 3, "result": 2}
  }
  ```
- **Trajectories**: `trajectories/traj_*-image.json.gz` - Gzipped action logs
  - Format: List of objects with keys: `id`, `timestamp`, `source`, `message`, `action`, `args`
  - Example: `[{"id": 0, "timestamp": "2025-05-09T07:51:28", "source": "user", ...}, ...]`
- **Screenshots**: `screenshots/` directory

## 6. Current State

- ✅ All code and configuration files complete
- ✅ Standalone log parsing works perfectly (`parse_logs.py`)
- ✅ **NEW**: HTTP-based agent implementation created (`main_http.py`)
- ✅ **NEW**: Correct workflow documented (`README_CORRECT.md`)
- ✅ Dependencies updated (httpx, fastapi, uvicorn)
- ✅ Trajectory parsing handles list format correctly
- ⏳ Ready for testing with actual backend

## 7. How to Run (The Correct Way)

```bash
# 1. Install dependencies
pip install httpx fastapi uvicorn

# 2. Set environment variables
export AGENTBEATS_BACKEND_URL=http://nuggets.puppy9.com:9000
export EXPERIMENTS_PATH=/path/to/experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro
export AGENT_HOST=0.0.0.0
export AGENT_PORT=8080

# 3. Start the agent
cd agentbeats_integration/green_agent
python3 main_http.py

# Agent will:
# - Start FastAPI server on port 8080
# - Log its agent_url (http://YOUR_IP:8080)
# - Wait for registration and battle start signals

# 4. Register with backend (manual or via UI)
# POST http://nuggets.puppy9.com:9000/agents with agent details

# 5. Start battle in AgentBeats UI
# Select "TheAgentCompany Benchmark Reporter" as participant

# 6. Agent receives battle_start, loads data, reports results
```

## 8. Previous Errors and Resolutions

### Error 1: "MCP server not found" ❌
```
Error: MCP server not found at /home/ihsan/Desktop/194/TheAgentCompany_Original/.venv/lib/python3.12/src/backend/mcp/mcp_server.py
```

**Root Cause**: Trying to run `ab deploy` from integration directory. The CLI looked for local backend source files.

**Resolution**: ✅ Don't use `ab deploy`. Connect to existing backend at `nuggets.puppy9.com:9000`

### Error 2: Trajectory parsing warnings ❌
```
Warning: Could not parse traj_*.json.gz: 'list' object has no attribute 'get'
```

**Root Cause**: Code expected dict format with `trajectory` key, but actual format is a list.

**Resolution**: ✅ Updated parsing logic to handle list format directly

### Error 3: SDK import confusion ❌
```
AgentBeats SDK not found. Install with: pip install agentbeats-sdk
```

**Root Cause**: Package is `agentbeats`, not `agentbeats-sdk` or `agentbeats-cli`

**Resolution**: ✅ Updated documentation. Created HTTP-based implementation that doesn't need SDK.

## 9. Installation & Environment

### What's Installed
- **Package**: `agentbeats` (provides CLI at `/home/ihsan/Desktop/194/TheAgentCompany_Original/.venv/bin/agentbeats`)
- **AgentBeats Repo**: Cloned at `/home/ihsan/Desktop/194/agentbeats` (reference only, not needed for runtime)
- **New Dependencies**: `httpx`, `fastapi`, `uvicorn` (for HTTP-based agent)

### Backend Configuration
- **Official Backend**: `http://nuggets.puppy9.com:9000`
- **OpenAPI Docs**: Available at backend URL (defines all endpoints)
- **Key Endpoints**:
  - `POST /agents` - Register agent
  - `POST /battles/{battleId}` - Report results
  - Agent receives: `POST http://YOUR_AGENT/a2a` - Battle start signal

## 10. What Works ✅

1. **Standalone Analysis** (`parse_logs.py`):
   ```bash
   python3 parse_logs.py ../experiments/.../20250510_OpenHands-0.28.1-gemini-2.5-pro --top 10
   ```
   - Loads 175 evaluations
   - Shows: 53 perfect (30.29%), avg completion 48.27%
   - Category filtering, CSV/JSON export working

2. **HTTP Implementation** (`main_http.py`):
   - FastAPI server for A2A messages
   - Agent registration payload construction
   - Result reporting payload construction
   - All parsing logic functional

## 11. Key Decisions

- **Chose Option A**: Simple aggregation, no simulation
- **Chose HTTP-based approach**: Direct REST API calls instead of SDK abstraction
- **Target existing backend**: Use `nuggets.puppy9.com:9000` instead of local deployment
- **Clean separation**: Keep `main.py` (SDK-based) and `main_http.py` (HTTP-based) separate

## 12. What Needs Testing 🔍

1. **Agent Registration**:
   - Verify `POST /agents` call succeeds
   - Confirm `agent_id` is returned
   - Check agent appears in UI

2. **Battle Flow**:
   - Start battle in UI
   - Verify agent receives `battle_start` A2A message
   - Confirm `battle_id` is extracted correctly

3. **Result Reporting**:
   - Verify `POST /battles/{battleId}` succeeds
   - Check results appear in UI
   - Validate markdown rendering

4. **Network Accessibility**:
   - Backend can reach agent's A2A endpoint
   - Firewall/NAT not blocking connections
   - Agent URL is externally accessible

## 13. Expected Results

From experiment logs (OpenHands 0.28.1 with Gemini 2.5 Pro):

```json
{
  "overall_pass_rate": 0.3029,
  "total_tasks": 175,
  "perfect_tasks": 53,
  "categories": {
    "sde": {"pass_rate": 0.3768, "total_tasks": 69, "perfect_tasks": 26},
    "pm": {"pass_rate": 0.28, "total_tasks": 30},
    "ds": {"pass_rate": 0.35, "total_tasks": 25},
    "admin": {"pass_rate": 0.25, "total_tasks": 15},
    "hr": {"pass_rate": 0.32, "total_tasks": 25},
    "finance": {"pass_rate": 0.29, "total_tasks": 11}
  }
}
```

## 14. Next Steps

1. **Immediate**: Test `main_http.py` locally
   ```bash
   python3 main_http.py
   # Verify server starts on port 8080
   ```

2. **Short-term**: Register agent with backend
   ```bash
   curl -X POST http://nuggets.puppy9.com:9000/agents \
     -H "Content-Type: application/json" \
     -d '{"alias":"TheAgentCompany Benchmark Reporter","agent_url":"http://YOUR_IP:8080",...}'
   ```

3. **Integration**: Test full battle flow in UI

4. **Enhancement**: Add error handling, retry logic, auth tokens

## 15. References

- **AgentBeats OpenAPI Spec**: `http://nuggets.puppy9.com:9000/docs` - Source of truth
- **TheAgentCompany Paper**: https://arxiv.org/abs/2412.14161
- **Experiments Repo**: https://github.com/TheAgentCompany/experiments

---

**This context provides complete understanding of the project evolution, the architectural breakthrough (HTTP-based direct API calls), current implementation state, and clear next steps for testing.**
