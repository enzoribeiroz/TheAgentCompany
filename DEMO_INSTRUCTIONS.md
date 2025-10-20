# 🎬 TheAgentCompany Green Agent Demo Instructions

This document provides step-by-step instructions for demonstrating the green agent in a video.

## 🎯 Demo Overview

The demo showcases how the green agent evaluates white agents on the `sde-change-license-easy` task from TheAgentCompany.

## 📋 Pre-Demo Setup

1. **Navigate to the project directory:**
   ```bash
   cd /home/enzoribeiroz/VSCode/berkeley/agent-company/TheAgentCompany
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

## 🎬 Demo Sequence

### Step 1: Show Project Structure
```bash
ls -la
```
**Say:** "Here's our green agent project with all the necessary files."

### Step 2: Show Configuration
```bash
cat .env
```
**Say:** "This is our configuration file where we can add the Claude API key."

### Step 3: Run Setup Test
```bash
python test_setup.py
```
**Say:** "Let's verify everything is working correctly."

### Step 4: Show Task Description
```bash
python -c "from tools import get_task_description; print(get_task_description())"
```
**Say:** "This is the task that white agents will be evaluated on - changing the license of the JanusGraph repository."

### Step 5: Show Task Prompt
```bash
python -c "from tools import create_task_prompt_for_agent; print(create_task_prompt_for_agent())"
```
**Say:** "This is the prompt that will be sent to white agents."

### Step 6: Test Individual Tools
```bash
python -c "
from tools import setup_license_change_task, talk_to_agent, monitor_checkpoint_progress
print('=== Testing Green Agent Tools ===')
print('1. Setup Task Environment:')
result1 = setup_license_change_task('demo-battle-123')
print(f'   {result1}')
print()
print('2. Agent Communication:')
result2 = talk_to_agent('Please complete the license change task', 'http://localhost:9000/red_agent')
print(f'   {result2}')
print()
print('3. Checkpoint Monitoring:')
result3 = monitor_checkpoint_progress('I found the janusgraph repository and cloned it locally. Now I need to check the license file.', 2)
print(f'   {result3}')
"
```
**Say:** "Let's test the individual tools that the green agent uses."

### Step 7: Run Complete Battle Simulation
```bash
python -c "
from main import TheAgentCompanyGreenEvaluator
print('=== Running Complete Battle Simulation ===')
evaluator = TheAgentCompanyGreenEvaluator()
evaluator.initialize_battle('demo-battle-456', 'http://localhost:9000/red_agent', 'http://localhost:9000/blue_agent')
print('Running complete battle workflow...')
battle_result = evaluator.run_battle()
print(f'Battle Result: {battle_result}')
"
```
**Say:** "Now let's run a complete battle simulation to see the green agent in action."

### Step 8: Run Full Demo Script
```bash
python demo_script.py
```
**Say:** "Finally, let's run the complete demo script that shows all the green agent's capabilities."

### Step 9: Show Results
```bash
echo "Demo completed! The green agent successfully:"
echo "✅ Orchestrated a battle between white agents"
echo "✅ Evaluated their performance on the license change task"
echo "✅ Monitored progress through checkpoints"
echo "✅ Determined a winner based on objective criteria"
echo "✅ Reported detailed results"
```
**Say:** "The green agent successfully demonstrated all its capabilities."

## 🎥 Video Script Suggestions

### Introduction (30 seconds)
- "Today I'm demonstrating the TheAgentCompany Green Agent"
- "This is an AI agent that evaluates other AI agents on real-world tasks"
- "Specifically, it evaluates white agents on the sde-change-license-easy task"

### Technical Overview (1 minute)
- "The green agent is built on the AgentBeats framework"
- "It uses Claude 3.5 Sonnet for AI capabilities"
- "It orchestrates battles between white agents and evaluates their performance"

### Demo Execution (3-4 minutes)
- Follow the demo sequence above
- Explain what's happening at each step
- Highlight the key features and capabilities

### Conclusion (30 seconds)
- "The green agent is ready for production use"
- "It successfully demonstrates the ability to evaluate AI agents on real-world tasks"
- "This is a prototype that can be extended to evaluate other tasks from TheAgentCompany"

## 🎯 Key Points to Emphasize

1. **Real-world task evaluation**: The agent evaluates on actual professional tasks
2. **Automated orchestration**: No human intervention needed during battles
3. **Objective evaluation**: Uses checkpoints and scoring criteria
4. **AgentBeats integration**: Built on a robust framework for agent evaluation
5. **Production ready**: Ready for deployment with proper API keys

## 📊 Expected Results

The demo should show:
- ✅ All tests passing
- ✅ Tools working correctly
- ✅ Complete battle simulation
- ✅ Detailed evaluation results
- ✅ Winner determination
- ✅ Comprehensive reporting

## 🚀 Next Steps

After the demo, mention:
- Add Claude API key for full functionality
- Deploy to AgentBeats platform
- Extend to other TheAgentCompany tasks
- Scale to multiple white agents
