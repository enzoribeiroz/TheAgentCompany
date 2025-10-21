# TheAgentCompany - AgentBeats Integration

This integration allows you to run TheAgentCompany benchmark evaluations on the AgentBeats platform using pre-computed results from experiment logs.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AgentBeats Platform                       │
│  ┌──────────────┐                                           │
│  │   Backend    │◄──── HTTP API (OpenAPI)                   │
│  │   (Port 9000)│                                            │
│  └──────┬───────┘                                            │
│         │                                                     │
│         │ A2A Protocol (Agent-to-Agent)                      │
│         │                                                     │
│         ▼                                                     │
│  ┌──────────────────────────────────────┐                   │
│  │  Green Agent (Results Aggregator)    │                   │
│  │  - Loads eval_*.json files           │                   │
│  │  - Parses traj_*.json.gz             │                   │
│  │  - Generates reports                 │                   │
│  │  - Reports via A2A                   │                   │
│  └──────────────────────────────────────┘                   │
│         ▲                                                     │
│         │                                                     │
│         │ Reads from disk                                    │
│         │                                                     │
└─────────┼─────────────────────────────────────────────────────┘
          │
          ▼
   ┌──────────────────────────────────────┐
   │  Experiment Logs (Local Filesystem)  │
   │  ├── results/                        │
   │  │   ├── eval_task1.json             │
   │  │   └── eval_task2.json             │
   │  └── trajectories/                   │
   │      ├── traj_task1.json.gz          │
   │      └── traj_task2.json.gz          │
   └──────────────────────────────────────┘
```

## Key Features

- ✅ **No Live Agents Required**: Evaluates pre-computed results from logs
- ✅ **175 Tasks**: Complete benchmark coverage
- ✅ **Category Breakdown**: Performance analysis by SDE, PM, DS, Admin, HR, Finance
- ✅ **Detailed Metrics**: Steps, costs, checkpoint scores
- ✅ **Markdown Reports**: Rich visualizations in AgentBeats UI

## Prerequisites

1. **AgentBeats package** installed
   ```bash
   pip install agentbeats
   ```

2. **AgentBeats Backend** running locally or accessible remotely
   ```bash
   # Deploy from AgentBeats repository in dev mode
   cd /path/to/agentbeats
   agentbeats deploy --deploy_mode dev --launch_mode tmux
   ```

3. **Experiment Logs**: Download or clone experiments repository
   ```bash
   git clone https://github.com/TheAgentCompany/experiments.git
   ```

## Setup

### 1. Install Dependencies

```bash
cd agentbeats_integration
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy template
cp .env.template .env

# Edit .env and add your OpenAI API key
nano .env
```

### 3. Verify Experiment Logs

Ensure you have the experiment logs in the correct location:

```bash
ls ../../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro/
# Should show: results/ trajectories/ screenshots/ README.md
```

## Usage

### Option 1: Run via AgentBeats CLI (Recommended)

```bash
# From AgentBeats repository directory
cd /path/to/agentbeats

# Load the scenario (prepares everything but doesn't start)
agentbeats load_scenario /path/to/TheAgentCompany_Original/agentbeats_integration/scenarios/theagentcompany_eval/

# Run the scenario (starts battle and opens in browser)
agentbeats run_scenario scenarios/theagentcompany_eval/

# Or run headless for CI/CD
agentbeats run_e2e scenarios/theagentcompany_eval/
```

### Option 2: Run Green Agent Standalone

```bash
# Run the green agent directly (for testing)
cd green_agent
python main.py ../../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro
```

## Understanding the Results

### Evaluation Files Structure

Each task has two files:

1. **`eval_<task>-image.json`**: Checkpoint scores
   ```json
   {
       "checkpoints": [
           {"total": 1, "result": 1},  // Pass
           {"total": 2, "result": 1}   // Partial
       ],
       "final_score": {
           "total": 3,
           "result": 2
       }
   }
   ```

2. **`traj_<task>-image.json.gz`**: Full execution trace
   - Agent actions and observations
   - Model calls and token usage
   - Browser screenshots (if applicable)

### Scoring Formula

TheAgentCompany uses a hybrid scoring formula:

```python
score = (result / total * 0.5) + (perfect_completion * 0.5)
```

Where:
- **Completion ratio** (0-0.5): Partial credit for incomplete tasks
- **Perfect bonus** (0 or 0.5): Full credit if task is 100% complete

### Report Categories

- **Overall Score**: Aggregate across all 175 tasks
- **By Category**: SDE, PM, DS, Admin, HR, Finance
- **By Service**: GitLab, Plane, RocketChat, OwnCloud
- **Top Performers**: Best-scoring tasks

## Project Structure

```
agentbeats_integration/
├── green_agent/
│   ├── main.py              # Green agent implementation
│   └── agent_card.toml      # Agent configuration
├── scenarios/
│   └── theagentcompany_eval/
│       └── scenario.toml    # Scenario definition
├── .env.template            # Environment variable template
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Extending the Integration

### Adding New Experiment Logs

1. Place new experiment folder in `experiments/evaluation/1.0.0/`
2. Update `EXPERIMENTS_PATH` in `.env`
3. Re-run the scenario

### Custom Reporting

Modify `generate_markdown_report()` in `main.py` to customize the output:

```python
def generate_markdown_report(self) -> str:
    # Add custom charts, tables, or analysis
    pass
```

### Filtering Tasks

To evaluate only specific tasks (e.g., SDE category):

```python
# In main.py, add filtering logic
def load_evaluations(self):
    for eval_file in self.results_dir.glob("eval_sde-*.json"):
        # Only load SDE tasks
        ...
```

## Troubleshooting

### Issue: "Experiments path not found"

**Solution**: Verify the path in `.env` matches your actual directory structure:

```bash
ls $EXPERIMENTS_PATH/results/
# Should list eval_*.json files
```

### Issue: "AgentBeats SDK not found"

**Solution**: Install the package:

```bash
pip install agentbeats
```

### Issue: "No evaluations loaded"

**Solution**: Check that results directory contains eval_*.json files:

```bash
find ../../experiments -name "eval_*.json" | head -5
```

### Issue: Import errors in main.py

**Solution**: This is expected during development. The AgentBeats imports are mocked with a fallback. Install the package to resolve:

```bash
pip install agentbeats
```

### Issue: "MCP server not found" when deploying

**Solution**: The `agentbeats deploy` command must be run from within the AgentBeats repository directory, not from your integration directory:

```bash
cd /path/to/agentbeats  # The cloned AgentBeats repo
agentbeats deploy --deploy_mode dev --launch_mode tmux
```

## Performance Notes

- **Load Time**: ~10-30 seconds to load 175 task evaluations
- **Memory**: ~500MB for full trajectory parsing
- **Network**: Minimal (only API calls to AgentBeats backend)

## Known Limitations

1. **Live Environment State Not Available**: 
   - Cannot re-run evaluators that check file contents, API responses, or database state
   - Only pre-computed checkpoint scores are available

2. **Trajectory Size**: 
   - Some trajectory files are large (>10MB compressed)
   - Parsing all 175 files may take time

3. **No White Agent Simulation**:
   - Does not instantiate the 13 personas as live agents
   - Persona information is implicit in task assignments

## Future Enhancements

- [ ] Interactive task filtering (by category, score, etc.)
- [ ] Trajectory replay visualization
- [ ] Comparison across multiple experiment runs
- [ ] Export results to CSV/Excel
- [ ] Integration with CI/CD for automated benchmarking

## References

- [TheAgentCompany Paper](https://arxiv.org/abs/2412.14161)
- [TheAgentCompany GitHub](https://github.com/TheAgentCompany/TheAgentCompany)
- [AgentBeats Documentation](https://agentbeats.dev/)

## License

Same as TheAgentCompany (MIT License)
