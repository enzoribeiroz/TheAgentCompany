# TheAgentCompany ↔ AgentBeats Integration: Project Context

**Status:** Implementation complete, agent running, ready for external registration  
**Current Blocker:** Need to expose agent externally (ngrok failed with Exit Code 1)

---

## 1. Project Goal

Integrate TheAgentCompany benchmark (175 tasks, 6 categories, 13 personas) into AgentBeats as a "green agent" that reports pre-computed evaluation results from existing experiment logs. No re-running benchmarks.

---

## 2. Architectural Decisions

### The Critical Insight
Your friend analyzed the AgentBeats OpenAPI spec and revealed:
- Backend already exists at `http://nuggets.puppy9.com:9000`
- No local deployment needed
- Three simple HTTP calls: register → receive signal → report results
- OpenAPI spec is the contract

### Options Considered

**Option A (CHOSEN):**
- Load pre-computed results from experiment logs
- Aggregate scores by category
- Report to AgentBeats via HTTP REST API
- No white agents, no log replay, no environment reconstruction

**Option B (REJECTED):**
- Full A2A battle simulation with log replay
- Reconstruct all 13 persona actions
- Rebuild environment state
- **Why rejected:** Unnecessary complexity, results already computed

**Key Decisions:**
- HTTP-based direct API calls (no SDK abstraction)
- FastAPI server for A2A messages
- Standalone agent (no AgentBeats deployment)

---

## 3. Implementation: The HTTP Workflow

### Three-Step Communication Pattern

**Step 1: Register Agent**
```bash
POST http://nuggets.puppy9.com:9000/agents
{
  "alias": "TheAgentCompany Benchmark Reporter",
  "agent_url": "http://YOUR_EXTERNAL_URL:8080",
  "is_green": true,
  "participant_requirements": [],
  "battle_timeout": 600
}
→ Returns: {"agent_id": "uuid"}
```

**Step 2: Receive Battle Start (Incoming A2A)**
```bash
POST http://YOUR_EXTERNAL_URL:8080/a2a
{
  "type": "battle_start",
  "battle_id": "battle_xyz789"
}
→ Agent loads evaluations and prepares report
```

**Step 3: Report Results**
```bash
POST http://nuggets.puppy9.com:9000/battles/battle_xyz789
{
  "is_result": true,
  "detail": {
    "overall_pass_rate": 0.3029,
    "total_tasks": 175,
    "categories": {...}
  },
  "markdown_content": "# Results..."
}
```

---

## 4. Implementation Files

```
green_agent/
├── main_http.py         ⭐ PRIMARY: HTTP-based (400+ lines)
├── main.py              📦 LEGACY: SDK-based (reference)
└── agent_card.toml      

parse_logs.py            ✅ Standalone utility (tested, working)
requirements.txt         httpx, fastapi, uvicorn
README_CORRECT.md        HTTP workflow documentation
```

**Key Class:** `TheAgentCompanyGreenAgent`
- FastAPI server for A2A endpoint (`/a2a`, `/health`)
- Loads 175 task evaluations from `eval_*-image.json` files
- Parses gzipped trajectories for step counts
- Aggregates by 6 categories: SDE (69), PM, DS, Admin, HR, Finance
- Generates markdown reports with tables

**Trajectory Discovery:** Format is a **list of action events**, not a dict with `trajectory` key. Fixed parsing logic to handle this.

---

## 5. Current Status

### ✅ Working
- Standalone parser: `python3 parse_logs.py ...` loads 175 tasks, shows 30.29% pass rate
- Agent server: Running on `http://0.0.0.0:8080`
  ```
  INFO: Uvicorn running on http://0.0.0.0:8080
  INFO: Backend URL: http://nuggets.puppy9.com:9000
  ```

### ⚠️ Active Blocker
**Need external access for A2A messages:**
- Agent runs on localhost:8080
- Backend at nuggets.puppy9.com needs to POST to agent
- Attempted: `ngrok http 8080` (Exit Code 1 - failed)

**Solutions:**
1. Fix ngrok authentication: `ngrok config add-authtoken TOKEN`
2. Use alternative: `cloudflared tunnel --url http://localhost:8080`
3. Deploy agent on cloud VM with public IP

---

## 6. Expected Results (OpenHands 0.28.1 + Gemini 2.5 Pro)

- **Total Tasks:** 175
- **Perfect Completions:** 53 (30.29%)
- **Average Completion:** 48.27%
- **By Category:** SDE 37.68%, PM ~28%, DS ~35%, Admin ~25%, HR ~32%, Finance ~29%

---

## 7. Next Steps

1. **Establish tunnel:** Get ngrok/cloudflared working → `https://abc123.tunnel.app`
2. **Register agent:**
   ```bash
   curl -X POST http://nuggets.puppy9.com:9000/agents \
     -H "Content-Type: application/json" \
     -d '{"alias":"TheAgentCompany Benchmark Reporter","agent_url":"https://abc123.tunnel.app",...}'
   ```
3. **Access UI:** Navigate to `http://nuggets.puppy9.com:9000/` or `:5173/`
4. **Start battle:** Select agent in UI, click "Start Battle"
5. **Verify:** Watch agent logs for `POST /a2a`, confirm results appear in UI

---

## 8. Key Technical Details

**Dependencies:**
```bash
pip install httpx fastapi uvicorn
```

**Environment:**
```bash
AGENTBEATS_BACKEND_URL=http://nuggets.puppy9.com:9000
EXPERIMENTS_PATH=../../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro
```

**Data Structure:**
- Results: `results/eval_*-image.json` (checkpoint scores)
- Trajectories: `trajectories/traj_*-image.json.gz` (action lists, not dicts)

**Past Errors Resolved:**
- "MCP server not found" → Don't use `ab deploy`, connect directly to backend
- Trajectory parsing errors → Handle list format, not dict
- Package confusion → Use `agentbeats` (not `-cli` or `-sdk`)

---

## References
- **Backend API:** `http://nuggets.puppy9.com:9000`
- **TheAgentCompany Paper:** https://arxiv.org/abs/2412.14161
- **Primary Implementation:** `green_agent/main_http.py`
- **Workflow Guide:** `README_CORRECT.md`
