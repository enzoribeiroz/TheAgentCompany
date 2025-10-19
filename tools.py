# -*- coding: utf-8 -*-
"""
TheAgentCompany Green Agent Tools for License Change Task Evaluation

This module provides tools for the green agent to evaluate white agents
on the "sde-change-license-easy" task from TheAgentCompany.
"""

import os
import json
import subprocess
import agentbeats as ab
from typing import Dict, Any, List
import requests
import time
import os
from anthropic import Anthropic

# Task configuration
LICENSE_CHANGE_TASK = {
    "name": "sde-change-license-easy",
    "description": "Change the license of the JanusGraph repository by keeping APACHE-2.0 and removing CC-BY-4.0",
    "repository_url": "http://the-agent-company.com:8929/root/janusgraph",
    "checkpoints": [
        {
            "number": 1,
            "description": "Get the correct codebase and go to the license to edit it",
            "points": 1
        },
        {
            "number": 2,
            "description": "Clone the repository locally",
            "points": 1
        },
        {
            "number": 3,
            "description": "Check the license of the repository",
            "points": 2
        }
    ]
}

@ab.tool
def setup_license_change_task(battle_id: str) -> str:
    """
    Initialize the license change task environment for the battle.
    
    Args:
        battle_id: The unique battle session identifier
        
    Returns:
        str: Setup status message
    """
    try:
        # Log the task setup
        ab.record_battle_event(
            battle_id=battle_id,
            event_type="task_setup",
            message="Setting up license change task environment",
            detail={
                "task_name": LICENSE_CHANGE_TASK["name"],
                "repository_url": LICENSE_CHANGE_TASK["repository_url"],
                "total_checkpoints": len(LICENSE_CHANGE_TASK["checkpoints"])
            }
        )
        
        return f"License change task environment initialized for battle {battle_id}. Task: {LICENSE_CHANGE_TASK['description']}"
        
    except Exception as e:
        error_msg = f"Failed to setup license change task: {str(e)}"
        ab.record_battle_event(
            battle_id=battle_id,
            message=error_msg,
            reported_by="green_agent",
            detail={"error": str(e)}
        )
        return error_msg

@ab.tool
def talk_to_agent(query: str, target_url: str) -> str:
    """
    Communicate with white agents to provide the license change task and collect responses.
    
    Args:
        query: The message to send to the agent
        target_url: The URL of the target agent
        
    Returns:
        str: The agent's response
    """
    try:
        # Use AgentBeats A2A communication
        response = ab.send_message_to_agent(
            target_url=target_url,
            message=query
        )
        
        return response
        
    except Exception as e:
        return f"Failed to communicate with agent at {target_url}: {str(e)}"

@ab.tool
def monitor_checkpoint_progress(agent_output: str, checkpoint_number: int) -> str:
    """
    Monitor white agent progress through the license change task checkpoints.
    
    Args:
        agent_output: The agent's output/response
        checkpoint_number: The checkpoint number being evaluated
        
    Returns:
        str: Progress assessment
    """
    try:
        battle_id = ab.get_battle_id()
        
        # Define checkpoint success criteria
        checkpoint_criteria = {
            1: ["janusgraph", "license", "apache", "cc-by"],
            2: ["clone", "repository", "local", "git clone"],
            3: ["license", "file", "apache", "cc-by", "modified", "changed"]
        }
        
        criteria = checkpoint_criteria.get(checkpoint_number, [])
        success_indicators = []
        
        # Check for success indicators in agent output
        for criterion in criteria:
            if criterion.lower() in agent_output.lower():
                success_indicators.append(criterion)
        
        # Determine if checkpoint is passed
        checkpoint_passed = len(success_indicators) >= len(criteria) // 2
        
        # Log progress
        ab.record_battle_event(
            battle_id=battle_id,
            message=f"Checkpoint {checkpoint_number} progress evaluation",
            reported_by="green_agent",
            detail={
                "checkpoint_number": checkpoint_number,
                "checkpoint_passed": checkpoint_passed,
                "success_indicators_found": success_indicators,
                "total_criteria": len(criteria)
            }
        )
        
        status = "PASSED" if checkpoint_passed else "FAILED"
        return f"Checkpoint {checkpoint_number}: {status}. Found indicators: {success_indicators}"
        
    except Exception as e:
        return f"Failed to monitor checkpoint progress: {str(e)}"

@ab.tool
def evaluate_license_change(agent_output: str, repository_path: str = "/workspace/janusgraph") -> str:
    """
    Evaluate white agent's license file changes against the task requirements.
    
    Args:
        agent_output: The agent's output/response
        repository_path: Path to the repository (default: /workspace/janusgraph)
        
    Returns:
        str: Evaluation results
    """
    try:
        battle_id = ab.get_battle_id()
        
        # Check if repository exists and has been modified
        evaluation_results = {
            "repository_exists": False,
            "license_file_found": False,
            "apache_license_present": False,
            "cc_by_license_removed": False,
            "total_score": 0
        }
        
        # Check if repository exists
        if os.path.exists(repository_path):
            evaluation_results["repository_exists"] = True
            
            # Look for license file
            license_files = ["LICENSE", "LICENSE.txt", "LICENSE.md"]
            license_file_path = None
            
            for license_file in license_files:
                potential_path = os.path.join(repository_path, license_file)
                if os.path.exists(potential_path):
                    license_file_path = potential_path
                    evaluation_results["license_file_found"] = True
                    break
            
            # Check license content if file exists
            if license_file_path:
                try:
                    with open(license_file_path, 'r', encoding='utf-8') as f:
                        license_content = f.read().lower()
                        
                        # Check for Apache license
                        if "apache" in license_content and "2.0" in license_content:
                            evaluation_results["apache_license_present"] = True
                        
                        # Check if CC-BY license was removed
                        if "cc-by" not in license_content and "creative commons" not in license_content:
                            evaluation_results["cc_by_license_removed"] = True
                            
                except Exception as e:
                    pass
        
        # Calculate score
        if evaluation_results["repository_exists"]:
            evaluation_results["total_score"] += 1
        if evaluation_results["license_file_found"]:
            evaluation_results["total_score"] += 1
        if evaluation_results["apache_license_present"]:
            evaluation_results["total_score"] += 1
        if evaluation_results["cc_by_license_removed"]:
            evaluation_results["total_score"] += 1
        
        # Log evaluation results
        ab.record_battle_event(
            battle_id=battle_id,
            message="License change evaluation completed",
            reported_by="green_agent",
            detail=evaluation_results
        )
        
        return f"License change evaluation: Score {evaluation_results['total_score']}/4. Repository exists: {evaluation_results['repository_exists']}, License file found: {evaluation_results['license_file_found']}, Apache license present: {evaluation_results['apache_license_present']}, CC-BY license removed: {evaluation_results['cc_by_license_removed']}"
        
    except Exception as e:
        error_msg = f"Failed to evaluate license change: {str(e)}"
        ab.record_battle_event(
            battle_id=battle_id,
            message=error_msg,
            reported_by="green_agent",
            detail={"error": str(e)}
        )
        return error_msg

@ab.tool
def update_battle_process(battle_id: str, message: str, reported_by: str, detail: dict = None) -> str:
    """
    Log intermediate steps and evaluation results during the battle.
    
    Args:
        battle_id: The unique battle session identifier
        message: Description of what happened
        reported_by: The agent/role reporting this information
        detail: Optional structured data with specific event details
        
    Returns:
        str: Logging confirmation
    """
    try:
        # Use AgentBeats logging functionality
        ab.record_battle_event(
            battle_id=battle_id,
            message=message,
            reported_by=reported_by,
            detail=detail or {}
        )
        
        return f"Battle process updated: {message}"
        
    except Exception as e:
        return f"Failed to update battle process: {str(e)}"

@ab.tool
def report_on_battle_end(battle_id: str, winner: str, detail: dict = None) -> str:
    """
    Report the final battle result with winner and evaluation details.
    
    Args:
        battle_id: The unique battle session identifier
        winner: The winner of the battle ("red", "blue", or "draw")
        detail: Optional structured data with specific result details
        
    Returns:
        str: Reporting confirmation
    """
    try:
        # Use AgentBeats reporting functionality
        ab.report_on_battle_end(
            battle_id=battle_id,
            winner=winner,
            detail=detail or {}
        )
        
        return f"Battle end reported: Winner is {winner}"
        
    except Exception as e:
        return f"Failed to report battle end: {str(e)}"

# Additional utility functions for the green agent

def get_task_description() -> str:
    """Get the full task description for the license change task."""
    return f"""
Task: {LICENSE_CHANGE_TASK['name']}
Description: {LICENSE_CHANGE_TASK['description']}

Repository URL: {LICENSE_CHANGE_TASK['repository_url']}

Checkpoints:
{chr(10).join([f"{cp['number']}. {cp['description']} ({cp['points']}pt)" for cp in LICENSE_CHANGE_TASK['checkpoints']])}

Instructions:
1. Find the JanusGraph repository from wiki http://the-agent-company.com:8929/root/doc/-/wikis
2. Clone the repository to /workspace
3. Change the license by keeping APACHE-2.0 and removing CC-BY-4.0
4. Keep changes locally (no need to push to GitLab)
"""

def create_task_prompt_for_agent() -> str:
    """Create a formatted task prompt to send to white agents."""
    return f"""
You are a Software Engineer (SWE) participating in a TheAgentCompany evaluation.

{get_task_description()}

Please complete this task step by step and report your progress. The green agent will monitor your progress through the checkpoints and evaluate your final result.

Good luck!
"""
