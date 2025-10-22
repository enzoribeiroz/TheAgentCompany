# Quick Reference - AgentBeats Integration

## 🚀 Start Agent (Easiest Way)

```bash
cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration
./start_agent.sh
```

---

## 📋 Manual Start Commands

### Start Agent Server
```bash
cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration/green_agent
../../.venv/bin/python main_http.py > ../agent.log 2>&1 &
```

### Start ngrok
```bash
cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration
ngrok http 8080 --log=stdout > ngrok.log 2>&1 &
```

---

## 🔍 Check Status

### Is Agent Running?
```bash
curl http://localhost:8080/health
```

### Get ngrok URL
```bash
curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['tunnels'][0]['public_url'])"
```

### Check Agent Card
```bash
curl https://ruby-nondoctrinaire-cohen.ngrok-free.dev/.well-known/agent-card.json | python3 -m json.tool
```

---

## 📝 View Logs

### Agent Logs
```bash
tail -f /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration/agent.log
```

### ngrok Logs
```bash
tail -f /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration/ngrok.log
```

---

## 🔄 Restart

### Restart Everything
```bash
pkill -9 -f "main_http.py"
pkill ngrok
sleep 2
cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration
./start_agent.sh
```

### Restart Only Agent
```bash
pkill -9 -f "main_http.py"
cd /Users/joe2690812044/Desktop/cs\ 195/TheAgentCompany/agentbeats_integration/green_agent
../../.venv/bin/python main_http.py > ../agent.log 2>&1 &
```

---

## 🌐 URLs

- **Local Agent**: http://localhost:8080
- **Public Agent**: https://ruby-nondoctrinaire-cohen.ngrok-free.dev
- **Agent Card**: https://ruby-nondoctrinaire-cohen.ngrok-free.dev/.well-known/agent-card.json
- **AgentBeats**: https://agentbeats.org

---

## 📋 Registration Info

**Use these values when registering at https://agentbeats.org:**

- **Agent URL**: `https://ruby-nondoctrinaire-cohen.ngrok-free.dev`
- **Launcher URL**: `https://ruby-nondoctrinaire-cohen.ngrok-free.dev`
- **Green**: ✓ (checked)
- **Task Index**: `0`
- **Battle Timeout**: `300`
- **Participant Requirements**: (leave empty)

---

## ⚠️ Current Issue

**Registration fails** with: `"Failed to fetch agent card from agent_url"`

**But everything is working:**
- ✅ Agent responding
- ✅ ngrok tunnel active
- ✅ Agent card accessible (returns 200 OK)
- ✅ AgentBeats CAN fetch the card (confirmed in logs)

**Root Cause**: Backend validation issue on AgentBeats' side

**Next Step**: Contact AgentBeats support with `REGISTRATION_ISSUE_SUMMARY.md`

---

## 📁 Important Files

- **Startup Script**: `start_agent.sh`
- **Agent Code**: `green_agent/main_http.py`
- **Complete Log**: `AGENT_STARTUP_AND_ISSUE_LOG.md`
- **Issue Summary**: `REGISTRATION_ISSUE_SUMMARY.md`
- **Agent Logs**: `agent.log`
- **ngrok Logs**: `ngrok.log`

