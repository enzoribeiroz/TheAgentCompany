#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TheAgentCompany Green Agent - Setup Test Script

This script tests the basic setup and imports to ensure everything is working correctly.
"""

import sys
import os

def test_imports():
    """Test all required imports."""
    print("🧪 Testing imports...")
    
    try:
        import agentbeats as ab
        print("✅ AgentBeats import successful")
    except ImportError as e:
        print(f"❌ AgentBeats import failed: {e}")
        return False
    
    try:
        from a2a.client import A2AClient
        print("✅ A2A client import successful")
    except ImportError as e:
        print(f"❌ A2A client import failed: {e}")
        return False
    
    try:
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
        print("✅ Tools import successful")
    except ImportError as e:
        print(f"❌ Tools import failed: {e}")
        return False
    
    try:
        from config import config
        print("✅ Config import successful")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration validation."""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import config
        
        # Print configuration
        config.print_config()
        
        # Validate configuration
        if config.validate_config():
            print("✅ Configuration validation passed")
            return True
        else:
            print("❌ Configuration validation failed")
            return False
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_agent_card():
    """Test agent card loading."""
    print("\n📋 Testing agent card...")
    
    try:
        import tomllib
        
        # Check if agent card exists
        if not os.path.exists("green_agent_card.toml"):
            print("❌ green_agent_card.toml not found")
            return False
        
        # Try to parse the agent card
        with open("green_agent_card.toml", "rb") as f:
            agent_card = tomllib.load(f)
        
        # Check required fields
        required_fields = ["name", "description", "url", "version"]
        for field in required_fields:
            if field not in agent_card:
                print(f"❌ Required field '{field}' missing from agent card")
                return False
        
        print("✅ Agent card validation passed")
        print(f"  Agent name: {agent_card['name']}")
        print(f"  Agent URL: {agent_card['url']}")
        print(f"  Version: {agent_card['version']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent card test failed: {e}")
        return False

def test_tools():
    """Test tool functions."""
    print("\n🛠️ Testing tools...")
    
    try:
        from tools import get_task_description, create_task_prompt_for_agent
        
        # Test task description
        task_desc = get_task_description()
        if not task_desc or len(task_desc) < 100:
            print("❌ Task description seems incomplete")
            return False
        
        print("✅ Task description generated successfully")
        
        # Test task prompt
        task_prompt = create_task_prompt_for_agent()
        if not task_prompt or len(task_prompt) < 100:
            print("❌ Task prompt seems incomplete")
            return False
        
        print("✅ Task prompt generated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Tools test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🌱 TheAgentCompany Green Agent - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_configuration),
        ("Agent Card Test", test_agent_card),
        ("Tools Test", test_tools)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} passed")
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! TheAgentCompany Green Agent is ready to go!")
        return True
    else:
        print("❌ Some tests failed. Please check the setup and try again.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
