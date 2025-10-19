# Adding an Evaluator Agent to TheAgentCompany

This guide explains how to add an evaluator agent to assess other agents' performance in TheAgentCompany benchmark.

## Types of Evaluator Agents

### 1. LLM-Based Evaluator Agent

LLM-based evaluators use language models to assess agent performance by analyzing trajectories, outputs, and intermediate results.

#### Implementation Steps:

**Step 1: Create the Evaluator Function**

```python
# In your task's evaluator.py
from scoring import Result, Checkpoint
from common import grader
import openai  # or your preferred LLM client

@grader
def grade_llm_evaluator_checkpoint(trajectory=""):
    """
    Use an LLM to evaluate agent performance based on trajectory and outputs
    """
    # Prepare evaluation prompt
    evaluation_prompt = f"""
    You are an expert evaluator assessing an AI agent's performance on a professional task.
    
    Task Context: [Your task description]
    Expected Outcomes: [What the agent should accomplish]
    
    Agent Trajectory:
    {trajectory}
    
    Please evaluate the agent's performance on the following criteria:
    1. Task Completion: Did the agent complete the required task?
    2. Process Quality: Was the approach logical and efficient?
    3. Communication: Did the agent communicate effectively with NPCs?
    4. Technical Accuracy: Were the technical implementations correct?
    
    Rate each criterion on a scale of 0-1 and provide an overall score.
    Return your evaluation in JSON format:
    {{
        "task_completion": 0.0-1.0,
        "process_quality": 0.0-1.0,
        "communication": 0.0-1.0,
        "technical_accuracy": 0.0-1.0,
        "overall_score": 0.0-1.0,
        "reasoning": "Brief explanation of the evaluation"
    }}
    """
    
    try:
        # Call your LLM
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or your preferred model
            messages=[{"role": "user", "content": evaluation_prompt}],
            temperature=0.1
        )
        
        evaluation = json.loads(response.choices[0].message.content)
        return evaluation["overall_score"] >= 0.7  # Pass if score >= 70%
        
    except Exception as e:
        print(f"LLM evaluation failed: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints = []
    
    # Add LLM-based evaluation checkpoint
    llm_result = grade_llm_evaluator_checkpoint(trajectory)
    checkpoints.append(Checkpoint(1, int(llm_result)))
    
    # Add other checkpoints as needed
    # ... other evaluation logic
    
    return Result(checkpoints)
```

**Step 2: Environment Configuration**

Set up your LLM credentials in the evaluation environment:

```bash
# When running evaluation
LITELLM_API_KEY=<your_llm_api_key> \
LITELLM_BASE_URL=<your_llm_base_url> \
LITELLM_MODEL=<your_model_name> \
python /utils/eval.py --trajectory_path <path> --output_path <path>
```

### 2. NPC-Based Evaluator Agent

Create an NPC that acts as an evaluator, providing feedback and scoring during task execution.

#### Implementation Steps:

**Step 1: Create Evaluator NPC Profile**

Add to `npc_definition.json`:

```json
{
  "first_name": "Dr. Evaluator",
  "last_name": "Smith",
  "age": 45,
  "occupation": "Senior Performance Analyst",
  "profile_picture": "https://example.com/evaluator.jpg",
  "gender": "Non-binary",
  "gender_pronoun": "They/Them",
  "public_info": "Dr. Smith is a senior performance analyst with expertise in evaluating AI agent capabilities. They assess task completion quality, communication effectiveness, and technical accuracy.",
  "personality_and_values": "Dr. Smith is methodical, fair, and thorough in their evaluations. They value clear communication, logical reasoning, and attention to detail.",
  "decision_making_style": "Analytical and evidence-based, Dr. Smith makes decisions based on clear criteria and objective assessment.",
  "secret": "Dr. Smith has a background in cognitive science and understands both human and AI decision-making processes.",
  "model_id": "evaluator-001",
  "mbti": "INTJ"
}
```

**Step 2: Define Evaluator NPC Context**

In your task's `scenarios.json`:

```json
{
  "Dr. Evaluator": {
    "extra_info": "You are evaluating an AI agent's performance on a professional task. You will observe their work and provide feedback. You have access to evaluation criteria and can score the agent's performance on different dimensions.",
    "strategy_hint": "Act as a fair and thorough evaluator. Ask clarifying questions if needed, provide constructive feedback, and give scores based on clear criteria. Be encouraging but objective in your assessment."
  }
}
```

**Step 3: Create Evaluation Checkpoints**

```python
@grader
def grade_npc_evaluator_feedback():
    """
    Evaluate based on NPC evaluator's feedback and scoring
    """
    chat_history = get_rocketchat_personal_chat_history(rocket, "Dr. Evaluator")
    
    # Look for evaluation scores in the conversation
    for message in chat_history:
        if "score:" in message.lower() or "rating:" in message.lower():
            # Extract score and evaluate
            # Implementation depends on your NPC's response format
            pass
    
    return len(chat_history) > 0  # Basic check for interaction

@grader
def grade_npc_specific_criteria():
    """
    Evaluate specific criteria mentioned by the NPC evaluator
    """
    chat_history = get_rocketchat_personal_chat_history(rocket, "Dr. Evaluator")
    
    criteria_met = 0
    total_criteria = 4  # Adjust based on your criteria
    
    for message in chat_history:
        if "task completion" in message.lower() and "excellent" in message.lower():
            criteria_met += 1
        if "communication" in message.lower() and "clear" in message.lower():
            criteria_met += 1
        # Add more criteria checks
    
    return criteria_met >= (total_criteria * 0.75)  # Pass if 75% of criteria met
```

### 3. Hybrid Evaluator Agent

Combine multiple evaluation approaches for comprehensive assessment.

#### Implementation:

```python
def grade_checkpoints(trajectory="") -> Result:
    checkpoints = []
    
    # Automated checks
    auto_result = grade_automated_checks(trajectory)
    checkpoints.append(Checkpoint(1, int(auto_result)))
    
    # LLM-based evaluation
    llm_result = grade_llm_evaluator_checkpoint(trajectory)
    checkpoints.append(Checkpoint(2, int(llm_result)))
    
    # NPC interaction evaluation
    npc_result = grade_npc_evaluator_feedback()
    checkpoints.append(Checkpoint(1, int(npc_result)))
    
    # Final comprehensive evaluation
    final_result = grade_comprehensive_evaluation(trajectory)
    checkpoints.append(Checkpoint(3, 3 * int(final_result)))
    
    return Result(checkpoints, bonus_for_completing_final)
```

## Best Practices for Evaluator Agents

### 1. Robust Error Handling

```python
@grader
def robust_evaluator_checkpoint(trajectory=""):
    try:
        # Your evaluation logic
        return evaluate_performance(trajectory)
    except Exception as e:
        logging.error(f"Evaluation failed: {e}")
        return False  # Fail gracefully
```

### 2. Partial Credit System

```python
def grade_with_partial_credit(trajectory=""):
    score = 0
    max_score = 5
    
    # Check different aspects and award partial credit
    if check_basic_requirements(trajectory):
        score += 1
    if check_advanced_features(trajectory):
        score += 2
    if check_quality_indicators(trajectory):
        score += 2
    
    return Checkpoint(max_score, score)
```

### 3. Multi-Dimensional Evaluation

```python
def grade_multidimensional_evaluation(trajectory=""):
    dimensions = {
        "task_completion": evaluate_task_completion(trajectory),
        "process_quality": evaluate_process_quality(trajectory),
        "communication": evaluate_communication(trajectory),
        "technical_accuracy": evaluate_technical_accuracy(trajectory),
        "efficiency": evaluate_efficiency(trajectory)
    }
    
    # Weight different dimensions
    weights = {
        "task_completion": 0.3,
        "process_quality": 0.2,
        "communication": 0.15,
        "technical_accuracy": 0.25,
        "efficiency": 0.1
    }
    
    weighted_score = sum(dimensions[dim] * weights[dim] for dim in dimensions)
    return weighted_score >= 0.7
```

## Integration with Existing System

### 1. Add to Task Configuration

Ensure your evaluator agent is properly configured in:
- `dependencies.yml` (if using external services)
- `scenarios.json` (if using NPCs)
- `evaluator.py` (main evaluation logic)

### 2. Environment Setup

Make sure your evaluator agent has access to:
- Required LLM APIs
- RocketChat credentials (for NPCs)
- Task-specific resources
- Evaluation criteria and rubrics

### 3. Testing and Validation

Test your evaluator agent with:
- Known good trajectories
- Known bad trajectories
- Edge cases and error conditions
- Different agent behaviors

## Example: Complete Evaluator Agent Implementation

Here's a complete example of an evaluator agent that combines multiple evaluation approaches:

```python
"""
Complete evaluator agent example
"""
import json
import requests
from scoring import Result, Checkpoint, bonus_for_completing_any
from common import grader, get_rocketchat_personal_chat_history, create_rocketchat_client

rocket = create_rocketchat_client()

@grader
def grade_llm_comprehensive_evaluation(trajectory=""):
    """Comprehensive LLM-based evaluation"""
    evaluation_prompt = f"""
    Evaluate this AI agent's performance comprehensively:
    
    Trajectory: {trajectory}
    
    Rate on 1-5 scale for each dimension:
    1. Task Completion (Did they complete the required task?)
    2. Process Quality (Was their approach logical?)
    3. Communication (Did they communicate well with NPCs?)
    4. Technical Accuracy (Were technical implementations correct?)
    5. Efficiency (Did they work efficiently?)
    
    Return JSON: {{"scores": [1,2,3,4,5], "overall": 3.5, "feedback": "..."}}
    """
    
    # Implement LLM call here
    # Return True if overall score >= 3.0
    return True  # Placeholder

@grader
def grade_npc_interaction_quality():
    """Evaluate quality of NPC interactions"""
    chat_history = get_rocketchat_personal_chat_history(rocket, "Dr. Evaluator")
    
    if not chat_history:
        return False
    
    # Check for positive feedback indicators
    positive_indicators = ["good", "excellent", "well done", "correct", "accurate"]
    negative_indicators = ["wrong", "incorrect", "poor", "failed", "mistake"]
    
    positive_count = sum(1 for msg in chat_history for indicator in positive_indicators 
                        if indicator in msg.lower())
    negative_count = sum(1 for msg in chat_history for indicator in negative_indicators 
                        if indicator in msg.lower())
    
    return positive_count > negative_count

@grader
def grade_final_output_quality():
    """Evaluate the final output quality"""
    # Check if required files exist and meet quality standards
    required_files = ["/workspace/output/report.pdf", "/workspace/output/data.json"]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            return False
        
        # Add file content validation here
        # ...
    
    return True

def grade_checkpoints(trajectory="") -> Result:
    """Main evaluation function"""
    checkpoints = []
    
    # Comprehensive evaluation (highest weight)
    comprehensive_result = grade_llm_comprehensive_evaluation(trajectory)
    checkpoints.append(Checkpoint(5, 5 * int(comprehensive_result)))
    
    # NPC interaction quality
    npc_result = grade_npc_interaction_quality()
    checkpoints.append(Checkpoint(2, 2 * int(npc_result)))
    
    # Final output quality
    output_result = grade_final_output_quality()
    checkpoints.append(Checkpoint(3, 3 * int(output_result)))
    
    return Result(checkpoints, bonus_for_completing_any)
```

This comprehensive guide should help you implement evaluator agents that can effectively assess other agents' performance in TheAgentCompany benchmark. Choose the approach that best fits your evaluation needs and integrate it with the existing system architecture.
