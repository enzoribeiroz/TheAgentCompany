# TheAgentCompany Green Agent - License Change Task Evaluator

A green agent for AgentBeats that evaluates white agents (SWEs) on the "sde-change-license-easy" task from TheAgentCompany.

## 🌱 Overview

This green agent serves as a battle orchestrator and evaluator that:
- Provides the license change task to white agents
- Monitors their progress through 3 checkpoints
- Evaluates their performance based on task completion
- Determines winners and reports results

## 📋 Task: sde-change-license-easy

**Description**: Change the license of the JanusGraph repository by keeping APACHE-2.0 and removing CC-BY-4.0

**Checkpoints**:
1. **Checkpoint 1 (1pt)**: Get the correct codebase and go to the license to edit it
2. **Checkpoint 2 (1pt)**: Clone the repository locally  
3. **Checkpoint 3 (2pt)**: Check the license of the repository

**Total Points**: 4 points

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Run the setup script
./setup_environment.sh

# Activate virtual environment
source venv/bin/activate
```

### 2. Configuration

Update the `.env` file with your configuration:

```bash
# Required: OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Customize URLs and ports
AGENTBEATS_BACKEND_URL=http://localhost:9000
GREEN_AGENT_PORT=9041
GREEN_AGENT_LAUNCHER_PORT=9040
```

### 3. Test Setup

```bash
# Run the test script to verify everything works
python test_setup.py
```

### 4. Run the Green Agent

```bash
# Start the green agent
python main.py
```

## 📁 Project Structure

```
TheAgentCompany/
├── green_agent_card.toml    # Agent configuration
├── main.py                  # Main agent implementation
├── tools.py                 # Evaluation tools
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── setup_environment.sh     # Environment setup script
├── test_setup.py           # Setup verification script
├── README_green_agent.md   # This file
├── .env                    # Environment variables (created by setup)
├── venv/                   # Virtual environment (created by setup)
├── logs/                   # Log files (created by setup)
└── workspace/              # Workspace directory (created by setup)
```

## 🛠️ Tools and Functions

### Core Tools

- **`setup_license_change_task()`**: Initialize task environment
- **`talk_to_agent()`**: Communicate with white agents
- **`monitor_checkpoint_progress()`**: Track checkpoint completion
- **`evaluate_license_change()`**: Evaluate final results
- **`update_battle_process()`**: Log battle progress
- **`report_on_battle_end()`**: Report final results

### Main Agent Functions

- **`start_license_change_evaluation()`**: Main battle entry point
- **`get_task_info()`**: Get task information
- **`check_battle_status()`**: Check battle status

## 🎯 Battle Workflow

1. **Setup**: Initialize task environment
2. **Task Distribution**: Provide task to red and blue agents
3. **Progress Monitoring**: Track checkpoint completion
4. **Evaluation**: Assess agent performance
5. **Reporting**: Determine winner and report results

## 📊 Evaluation Criteria

Agents are evaluated based on:
- Repository access and cloning (2 points)
- License file modification (2 points)
- Total possible score: 4 points

## 🔧 Configuration Options

### Environment Variables

- `OPENAI_API_KEY`: Required for OpenAI integration
- `GREEN_AGENT_PORT`: Port for agent communication (default: 9041)
- `GREEN_AGENT_LAUNCHER_PORT`: Port for launcher (default: 9040)
- `BATTLE_TIMEOUT`: Battle timeout in seconds (default: 300)
- `LOG_LEVEL`: Logging level (default: INFO)

### AgentBeats Integration

- `AGENTBEATS_BACKEND_URL`: Backend API URL
- `AGENTBEATS_MCP_SERVER_URL`: MCP server URL for logging

## 🧪 Testing

### Run Setup Tests

```bash
python test_setup.py
```

This will test:
- Import functionality
- Configuration validation
- Agent card parsing
- Tool functions

### Manual Testing

```bash
# Test configuration
python config.py

# Test individual tools
python -c "from tools import get_task_description; print(get_task_description())"
```

## 🚀 Deployment

### Local Deployment

```bash
# Start the agent
python main.py
```

### AgentBeats Integration

1. Register the agent on agentbeats.org
2. Set agent URL: `http://your-server:9041`
3. Set launcher URL: `http://your-server:9040`
4. Start battles with white agents

## 📝 Logging

Logs are written to:
- Console output (INFO level)
- `logs/` directory (if configured)

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Run `./setup_environment.sh` to install dependencies
2. **Configuration Errors**: Check `.env` file and run `python config.py`
3. **AgentBeats Connection**: Verify backend URL and MCP server URL
4. **OpenAI API**: Ensure valid API key is set

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python main.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of TheAgentCompany and follows the same MIT license.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Run the test script to verify setup
3. Check logs for error messages
4. Create an issue in the repository

---

**🌱 TheAgentCompany Green Agent - Ready to evaluate white agents on license change tasks!**
