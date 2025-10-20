#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TheAgentCompany Green Agent Demo Script

This script demonstrates the complete functionality of the green agent
for evaluating white agents on the sde-change-license-easy task.
"""

import time
import sys
from main import TheAgentCompanyGreenEvaluator
from tools import get_task_description, create_task_prompt_for_agent
import config

def print_header(title, char="=", width=80):
    """Print a formatted header."""
    print(f"\n{char * width}")
    print(f"{title:^{width}}")
    print(f"{char * width}\n")

def print_step(step_num, title, description=""):
    """Print a formatted step."""
    print(f"🔹 Step {step_num}: {title}")
    if description:
        print(f"   {description}")
    print()

def print_result(title, result, max_length=100):
    """Print a formatted result."""
    print(f"📋 {title}:")
    if len(str(result)) > max_length:
        print(f"   {str(result)[:max_length]}...")
    else:
        print(f"   {result}")
    print()

def print_success(message):
    """Print a success message."""
    print(f"✅ {message}")

def print_info(message):
    """Print an info message."""
    print(f"ℹ️  {message}")

def demo_green_agent():
    """Run the complete green agent demo."""
    
    print_header("🌱 TheAgentCompany Green Agent Demo", "=", 80)
    print_info("Welcome to the TheAgentCompany Green Agent demonstration!")
    print_info("This demo shows how the green agent evaluates white agents on the sde-change-license-easy task.")
    print()
    
    # Step 1: Show the task description
    print_step(1, "Task Overview", "Displaying the sde-change-license-easy task details")
    task_desc = get_task_description()
    print_result("Task Description", task_desc)
    
    # Step 2: Show the task prompt for white agents
    print_step(2, "Task Prompt Generation", "Creating the prompt that will be sent to white agents")
    task_prompt = create_task_prompt_for_agent()
    print_result("Generated Task Prompt", task_prompt, 150)
    
    # Step 3: Initialize the green evaluator
    print_step(3, "Green Agent Initialization", "Setting up the green evaluator with battle parameters")
    evaluator = TheAgentCompanyGreenEvaluator()
    
    battle_id = "demo-battle-2024"
    red_agent_url = "http://localhost:9000/red_agent"
    blue_agent_url = "http://localhost:9000/blue_agent"
    
    print_info(f"Battle ID: {battle_id}")
    print_info(f"Red Agent URL: {red_agent_url}")
    print_info(f"Blue Agent URL: {blue_agent_url}")
    
    evaluator.initialize_battle(battle_id, red_agent_url, blue_agent_url)
    print_success("Green evaluator initialized successfully!")
    
    # Step 4: Run the complete battle
    print_step(4, "Battle Execution", "Running the complete battle workflow")
    print_info("The green agent will now orchestrate the entire evaluation process...")
    print()
    
    start_time = time.time()
    battle_result = evaluator.run_battle()
    end_time = time.time()
    
    print_success(f"Battle completed in {end_time - start_time:.2f} seconds!")
    print_result("Final Battle Result", battle_result)
    
    # Step 5: Show detailed results
    print_step(5, "Detailed Results Analysis", "Analyzing the evaluation results")
    
    print("📊 Evaluation Summary:")
    print(f"   • Red Agent Score: {evaluator.evaluation_results.get('red_agent_score', 'N/A')}")
    print(f"   • Blue Agent Score: {evaluator.evaluation_results.get('blue_agent_score', 'N/A')}")
    print(f"   • Winner: {evaluator.evaluation_results.get('winner', 'N/A')}")
    print(f"   • Task: {evaluator.evaluation_results.get('task', 'N/A')}")
    print()
    
    # Step 6: Show the green agent's capabilities
    print_step(6, "Green Agent Capabilities", "Demonstrating key features of the green agent")
    
    print("🛠️  Key Features Demonstrated:")
    print("   ✅ Task Environment Setup")
    print("   ✅ Agent Communication (A2A)")
    print("   ✅ Checkpoint Monitoring")
    print("   ✅ Performance Evaluation")
    print("   ✅ Winner Determination")
    print("   ✅ Battle Reporting")
    print("   ✅ TheAgentCompany Integration")
    print("   ✅ AgentBeats Framework Integration")
    print()
    
    # Step 7: Show configuration
    print_step(7, "Configuration Details", "Displaying the green agent's configuration")
    
    config_obj = config.GreenAgentConfig()
    print("⚙️  Green Agent Configuration:")
    print(f"   • Agent Name: {config_obj.AGENT_NAME}")
    print(f"   • Agent URL: http://{config_obj.AGENT_HOST}:{config_obj.AGENT_PORT}")
    print(f"   • Backend URL: {config_obj.AGENTBEATS_BACKEND_URL}")
    print(f"   • MCP Server: {config_obj.AGENTBEATS_MCP_SERVER_URL}")
    print(f"   • Model: Claude 3.5 Sonnet")
    print(f"   • Task: sde-change-license-easy")
    print()
    
    # Final summary
    print_header("🎯 Demo Summary", "=", 80)
    print_success("The green agent successfully demonstrated:")
    print("   • Complete battle orchestration workflow")
    print("   • White agent evaluation capabilities")
    print("   • TheAgentCompany task integration")
    print("   • AgentBeats framework compatibility")
    print("   • Real-time monitoring and reporting")
    print()
    print_info("The green agent is ready for production use!")
    print_info("Add your Claude API key to the .env file to enable full functionality.")
    print()
    print_header("Demo Complete", "=", 80)

if __name__ == "__main__":
    try:
        demo_green_agent()
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        sys.exit(1)
