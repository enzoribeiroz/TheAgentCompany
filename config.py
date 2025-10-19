#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TheAgentCompany Green Agent Configuration

This module contains configuration settings for the green agent.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GreenAgentConfig:
    """Configuration class for the green agent."""
    
    # Agent configuration
    AGENT_NAME = "TheAgentCompany Green Evaluator - License Change Task"
    AGENT_HOST = os.getenv("GREEN_AGENT_HOST", "0.0.0.0")
    AGENT_PORT = int(os.getenv("GREEN_AGENT_PORT", "9041"))
    LAUNCHER_PORT = int(os.getenv("GREEN_AGENT_LAUNCHER_PORT", "9040"))
    
    # API keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # AgentBeats configuration
    AGENTBEATS_BACKEND_URL = os.getenv("AGENTBEATS_BACKEND_URL", "http://localhost:9000")
    AGENTBEATS_MCP_SERVER_URL = os.getenv("AGENTBEATS_MCP_SERVER_URL", "http://localhost:9001/sse")
    
    # Battle configuration
    BATTLE_TIMEOUT = int(os.getenv("BATTLE_TIMEOUT", "300"))  # 5 minutes
    MAX_RETRIES = 3
    
    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Task configuration
    TASK_CONFIG = {
        "name": "sde-change-license-easy",
        "description": "Change the license of the JanusGraph repository by keeping APACHE-2.0 and removing CC-BY-4.0",
        "repository_url": "http://the-agent-company.com:8929/root/janusgraph",
        "workspace_path": "/workspace",
        "checkpoints": [
            {
                "number": 1,
                "description": "Get the correct codebase and go to the license to edit it",
                "points": 1,
                "timeout": 60
            },
            {
                "number": 2,
                "description": "Clone the repository locally",
                "points": 1,
                "timeout": 120
            },
            {
                "number": 3,
                "description": "Check the license of the repository",
                "points": 2,
                "timeout": 180
            }
        ]
    }
    
    # Evaluation criteria
    EVALUATION_CRITERIA = {
        "repository_exists": 1,
        "license_file_found": 1,
        "apache_license_present": 1,
        "cc_by_license_removed": 1,
        "max_score": 4
    }
    
    # Agent URLs (will be provided during battle)
    RED_AGENT_URL = None
    BLUE_AGENT_URL = None
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate the configuration."""
        errors = []
        
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            errors.append("Either OPENAI_API_KEY or ANTHROPIC_API_KEY is required")
        
        if cls.AGENT_PORT == cls.LAUNCHER_PORT:
            errors.append("AGENT_PORT and LAUNCHER_PORT must be different")
        
        if not cls.AGENTBEATS_BACKEND_URL:
            errors.append("AGENTBEATS_BACKEND_URL is required")
        
        if errors:
            print("❌ Configuration validation failed:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    @classmethod
    def get_agent_url(cls) -> str:
        """Get the full agent URL."""
        return f"http://{cls.AGENT_HOST}:{cls.AGENT_PORT}"
    
    @classmethod
    def get_launcher_url(cls) -> str:
        """Get the full launcher URL."""
        return f"http://{cls.AGENT_HOST}:{cls.LAUNCHER_PORT}"
    
    @classmethod
    def print_config(cls):
        """Print the current configuration."""
        print("🌱 TheAgentCompany Green Agent Configuration:")
        print(f"  Agent Name: {cls.AGENT_NAME}")
        print(f"  Agent URL: {cls.get_agent_url()}")
        print(f"  Launcher URL: {cls.get_launcher_url()}")
        print(f"  Backend URL: {cls.AGENTBEATS_BACKEND_URL}")
        print(f"  MCP Server URL: {cls.AGENTBEATS_MCP_SERVER_URL}")
        print(f"  Battle Timeout: {cls.BATTLE_TIMEOUT}s")
        print(f"  Log Level: {cls.LOG_LEVEL}")
        print(f"  Task: {cls.TASK_CONFIG['name']}")

# Global configuration instance
config = GreenAgentConfig()

if __name__ == "__main__":
    # Print configuration when run directly
    config.print_config()
    
    # Validate configuration
    if config.validate_config():
        print("✅ Configuration is valid")
    else:
        print("❌ Configuration validation failed")
        exit(1)
