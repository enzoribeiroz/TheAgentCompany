#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TheAgentCompany Green Agent - Main Implementation

This is the main implementation for the green agent that evaluates white agents
on the "sde-change-license-easy" task from TheAgentCompany.
"""

import agentbeats as ab
import os
import json
import time
from typing import Dict, Any, List
from tools import (
    setup_license_change_task,
    talk_to_agent,
    monitor_checkpoint_progress,
    evaluate_license_change,
    update_battle_process,
    report_on_battle_end,
    create_task_prompt_for_agent,
    get_task_description
)

# Initialize the AgentBeats agent with required parameters
ab_agent = ab.BeatsAgent(
    name="TheAgentCompanyGreenEvaluator",
    agent_host="0.0.0.0",
    agent_port=9041,
    model_type="anthropic",
    model_name="claude-3-5-sonnet-20241022"
)

class TheAgentCompanyGreenEvaluator:
    """
    TheAgentCompany Green Agent that evaluates white agents on the license change task.
    """
    
    def __init__(self):
        self.battle_id = None
        self.red_agent_url = None
        self.blue_agent_url = None
        self.task_completed = False
        self.evaluation_results = {}
        
    def initialize_battle(self, battle_id: str, red_agent_url: str, blue_agent_url: str):
        """Initialize the battle with agent URLs and battle ID."""
        self.battle_id = battle_id
        self.red_agent_url = red_agent_url
        self.blue_agent_url = blue_agent_url
        
        # Log battle initialization
        update_battle_process(
            battle_id=self.battle_id,
            message="Battle initialized for license change task evaluation",
            reported_by="green_agent",
            detail={
                "red_agent_url": self.red_agent_url,
                "blue_agent_url": self.blue_agent_url,
                "task": "sde-change-license-easy"
            }
        )
        
    def run_battle(self):
        """Execute the complete battle workflow."""
        try:
            # Stage 0: Initialize task environment
            self.setup_task_environment()
            
            # Stage 1: Provide task to red agent
            red_response = self.provide_task_to_red_agent()
            
            # Stage 2: Provide task to blue agent
            blue_response = self.provide_task_to_blue_agent()
            
            # Stage 3: Monitor progress through checkpoints
            self.monitor_agent_progress(red_response, blue_response)
            
            # Stage 4: Collect final responses
            final_red_response = self.collect_final_response("red")
            final_blue_response = self.collect_final_response("blue")
            
            # Stage 5: Evaluate license changes
            red_evaluation = self.evaluate_agent_performance(final_red_response, "red")
            blue_evaluation = self.evaluate_agent_performance(final_blue_response, "blue")
            
            # Stage 6: Log evaluation results
            self.log_evaluation_results(red_evaluation, blue_evaluation)
            
            # Stage 7: Determine winner
            winner = self.determine_winner(red_evaluation, blue_evaluation)
            
            # Stage 8: Report final battle result
            self.report_battle_end(winner, red_evaluation, blue_evaluation)
            
            return f"Battle completed successfully. Winner: {winner}"
            
        except Exception as e:
            error_msg = f"Battle execution failed: {str(e)}"
            update_battle_process(
                battle_id=self.battle_id,
                message=error_msg,
                reported_by="green_agent",
                detail={"error": str(e)}
            )
            return error_msg
    
    def setup_task_environment(self):
        """Stage 0: Initialize the license change task environment."""
        result = setup_license_change_task(self.battle_id)
        update_battle_process(
            battle_id=self.battle_id,
            message="Task environment setup completed",
            reported_by="green_agent",
            detail={"setup_result": result}
        )
    
    def provide_task_to_red_agent(self):
        """Stage 1: Provide the license change task to the red agent."""
        task_prompt = create_task_prompt_for_agent()
        
        update_battle_process(
            battle_id=self.battle_id,
            message="Providing license change task to red agent",
            reported_by="green_agent",
            detail={"task_prompt": task_prompt[:200] + "..."}  # Truncate for logging
        )
        
        red_response = talk_to_agent(task_prompt, self.red_agent_url)
        
        update_battle_process(
            battle_id=self.battle_id,
            message="Red agent received task and responded",
            reported_by="red_agent",
            detail={"response": red_response[:200] + "..."}  # Truncate for logging
        )
        
        return red_response
    
    def provide_task_to_blue_agent(self):
        """Stage 2: Provide the license change task to the blue agent."""
        task_prompt = create_task_prompt_for_agent()
        
        update_battle_process(
            battle_id=self.battle_id,
            message="Providing license change task to blue agent",
            reported_by="green_agent",
            detail={"task_prompt": task_prompt[:200] + "..."}  # Truncate for logging
        )
        
        blue_response = talk_to_agent(task_prompt, self.blue_agent_url)
        
        update_battle_process(
            battle_id=self.battle_id,
            message="Blue agent received task and responded",
            reported_by="blue_agent",
            detail={"response": blue_response[:200] + "..."}  # Truncate for logging
        )
        
        return blue_response
    
    def monitor_agent_progress(self, red_response: str, blue_response: str):
        """Stage 3: Monitor progress through checkpoints."""
        # Monitor red agent progress
        for checkpoint_num in [1, 2, 3]:
            red_progress = monitor_checkpoint_progress(red_response, checkpoint_num)
            update_battle_process(
                battle_id=self.battle_id,
                message=f"Red agent checkpoint {checkpoint_num} progress",
                reported_by="green_agent",
                detail={"checkpoint": checkpoint_num, "progress": red_progress}
            )
        
        # Monitor blue agent progress
        for checkpoint_num in [1, 2, 3]:
            blue_progress = monitor_checkpoint_progress(blue_response, checkpoint_num)
            update_battle_process(
                battle_id=self.battle_id,
                message=f"Blue agent checkpoint {checkpoint_num} progress",
                reported_by="green_agent",
                detail={"checkpoint": checkpoint_num, "progress": blue_progress}
            )
    
    def collect_final_response(self, agent_type: str):
        """Stage 4: Collect final responses from agents."""
        agent_url = self.red_agent_url if agent_type == "red" else self.blue_agent_url
        
        # Request final status from agent
        final_prompt = f"Please provide your final status and results for the license change task. Include details about what you accomplished."
        
        final_response = talk_to_agent(final_prompt, agent_url)
        
        update_battle_process(
            battle_id=self.battle_id,
            message=f"Collected final response from {agent_type} agent",
            reported_by=f"{agent_type}_agent",
            detail={"final_response": final_response[:300] + "..."}  # Truncate for logging
        )
        
        return final_response
    
    def evaluate_agent_performance(self, agent_response: str, agent_type: str):
        """Stage 5: Evaluate agent performance on the license change task."""
        evaluation_result = evaluate_license_change(agent_response)
        
        # Parse evaluation result to extract score
        try:
            if "Score" in evaluation_result:
                score_part = evaluation_result.split("Score")[1].split("/")[0].strip()
                score = int(score_part)
            else:
                score = 0
        except:
            score = 0
        
        evaluation_data = {
            "agent_type": agent_type,
            "evaluation_result": evaluation_result,
            "score": score,
            "timestamp": time.time()
        }
        
        self.evaluation_results[agent_type] = evaluation_data
        
        update_battle_process(
            battle_id=self.battle_id,
            message=f"Performance evaluation completed for {agent_type} agent",
            reported_by="green_agent",
            detail=evaluation_data
        )
        
        return evaluation_data
    
    def log_evaluation_results(self, red_evaluation: Dict, blue_evaluation: Dict):
        """Stage 6: Log comprehensive evaluation results."""
        update_battle_process(
            battle_id=self.battle_id,
            message="Comprehensive evaluation results logged",
            reported_by="green_agent",
            detail={
                "red_agent_score": red_evaluation.get("score", 0),
                "blue_agent_score": blue_evaluation.get("score", 0),
                "red_evaluation": red_evaluation.get("evaluation_result", ""),
                "blue_evaluation": blue_evaluation.get("evaluation_result", "")
            }
        )
    
    def determine_winner(self, red_evaluation: Dict, blue_evaluation: Dict):
        """Stage 7: Determine the winner based on evaluation results."""
        red_score = red_evaluation.get("score", 0)
        blue_score = blue_evaluation.get("score", 0)
        
        if red_score > blue_score:
            winner = "red"
        elif blue_score > red_score:
            winner = "blue"
        else:
            winner = "draw"
        
        update_battle_process(
            battle_id=self.battle_id,
            message=f"Winner determined: {winner}",
            reported_by="green_agent",
            detail={
                "red_score": red_score,
                "blue_score": blue_score,
                "winner": winner
            }
        )
        
        return winner
    
    def report_battle_end(self, winner: str, red_evaluation: Dict, blue_evaluation: Dict):
        """Stage 8: Report the final battle result."""
        battle_summary = {
            "winner": winner,
            "red_agent_performance": red_evaluation,
            "blue_agent_performance": blue_evaluation,
            "task": "sde-change-license-easy",
            "total_checkpoints": 3,
            "battle_duration": time.time() - self.evaluation_results.get("red", {}).get("timestamp", time.time())
        }
        
        result = report_on_battle_end(
            battle_id=self.battle_id,
            winner=winner,
            detail=battle_summary
        )
        
        update_battle_process(
            battle_id=self.battle_id,
            message="Final battle result reported",
            reported_by="green_agent",
            detail=battle_summary
        )
        
        return result

# Global evaluator instance
evaluator = TheAgentCompanyGreenEvaluator()

@ab_agent.tool()
def start_license_change_evaluation(battle_id: str, red_agent_url: str, blue_agent_url: str) -> str:
    """
    Start the license change task evaluation battle between red and blue agents.
    
    Args:
        battle_id: The unique battle session identifier
        red_agent_url: URL of the red agent (first white agent)
        blue_agent_url: URL of the blue agent (second white agent)
        
    Returns:
        str: Battle execution result
    """
    try:
        # Initialize the battle
        evaluator.initialize_battle(battle_id, red_agent_url, blue_agent_url)
        
        # Run the complete battle workflow
        result = evaluator.run_battle()
        
        return result
        
    except Exception as e:
        error_msg = f"Failed to start license change evaluation: {str(e)}"
        update_battle_process(
            battle_id=battle_id,
            message=error_msg,
            reported_by="green_agent",
            detail={"error": str(e)}
        )
        return error_msg

@ab_agent.tool()
def get_task_info() -> str:
    """
    Get information about the license change task.
    
    Returns:
        str: Task information and description
    """
    return get_task_description()

@ab_agent.tool()
def check_battle_status(battle_id: str) -> str:
    """
    Check the current status of a battle.
    
    Args:
        battle_id: The unique battle session identifier
        
    Returns:
        str: Current battle status
    """
    if evaluator.battle_id == battle_id:
        return f"Battle {battle_id} is active. Red agent: {evaluator.red_agent_url}, Blue agent: {evaluator.blue_agent_url}"
    else:
        return f"No active battle found with ID: {battle_id}"

def main():
    """Main entry point for the green agent."""
    try:
        # Load the agent card
        ab_agent.load_agent_card("green_agent_card.toml")
        
        # Add MCP server for logging and reporting
        ab_agent.add_mcp_server("http://localhost:9001/sse")
        
        # Run the agent
        ab_agent.run()
        
    except Exception as e:
        print(f"Failed to start green agent: {str(e)}")
        raise

if __name__ == "__main__":
    main()
