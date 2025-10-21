#!/usr/bin/env python3
"""
TheAgentCompany Green Agent for AgentBeats
===========================================

This green agent orchestrates the evaluation of TheAgentCompany benchmark
by loading pre-computed evaluation results and reporting them via AgentBeats.

Architecture:
- No live white agents needed (results are pre-computed)
- Loads eval_*.json files for checkpoint scores
- Parses traj_*.json.gz for metadata (steps, tokens, costs)
- Reports aggregated results to AgentBeats backend via A2A protocol
"""

import json
import gzip
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

# AgentBeats SDK imports (will be installed via pip)
try:
    from agentbeats.agent import Agent
    from agentbeats.a2a import A2AMessage, MessageType
except ImportError:
    # Fallback for development without SDK
    logging.warning("AgentBeats SDK not found. Install with: pip install agentbeats-sdk")
    Agent = object
    A2AMessage = dict
    MessageType = object


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CheckpointScore:
    """Individual checkpoint score"""
    total: int
    result: int
    
    @property
    def passed(self) -> bool:
        return self.result == self.total
    
    @property
    def score(self) -> float:
        return self.result / self.total if self.total > 0 else 0.0


@dataclass
class TaskEvaluation:
    """Evaluation results for a single task"""
    task_name: str
    checkpoints: List[CheckpointScore]
    final_total: int
    final_result: int
    steps: Optional[int] = None
    cost_usd: Optional[float] = None
    
    @property
    def score(self) -> float:
        """Calculate score (0-1) using TAC formula"""
        if self.final_total == 0:
            return 0.0
        # TAC formula: (result/total * 0.5) + (perfect_completion * 0.5)
        completion_ratio = self.final_result / self.final_total
        perfect = 1.0 if self.final_result == self.final_total else 0.0
        return (completion_ratio * 0.5) + (perfect * 0.5)
    
    @property
    def perfect(self) -> bool:
        return self.final_result == self.final_total
    
    @property
    def category(self) -> str:
        """Extract category from task name (sde, pm, ds, admin, hr, finance)"""
        prefix = self.task_name.split('-')[0].lower()
        if prefix in ['sde', 'pm', 'ds', 'admin', 'hr', 'finance']:
            return prefix
        return 'other'


class TheAgentCompanyGreenAgent(Agent):
    """Green agent that aggregates TheAgentCompany benchmark results"""
    
    def __init__(self, experiments_path: str):
        """
        Initialize green agent
        
        Args:
            experiments_path: Path to experiments folder 
                             (e.g., experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro/)
        """
        super().__init__()
        self.experiments_path = Path(experiments_path)
        self.results_dir = self.experiments_path / "results"
        self.trajectories_dir = self.experiments_path / "trajectories"
        self.evaluations: Dict[str, TaskEvaluation] = {}
        
    def load_evaluations(self):
        """Load all pre-computed evaluation results"""
        logger.info(f"Loading evaluations from {self.results_dir}")
        
        for eval_file in self.results_dir.glob("eval_*.json"):
            task_name = eval_file.stem.replace("eval_", "").replace("-image", "")
            
            with open(eval_file, 'r') as f:
                data = json.load(f)
            
            checkpoints = [
                CheckpointScore(**cp) for cp in data['checkpoints']
            ]
            
            final_score = data['final_score']
            
            # Try to load trajectory metadata (steps, cost)
            traj_file = self.trajectories_dir / f"traj_{task_name}-image.json.gz"
            steps, cost = None, None
            
            if traj_file.exists():
                try:
                    steps, cost = self._parse_trajectory_metadata(traj_file)
                except Exception as e:
                    logger.warning(f"Failed to parse trajectory for {task_name}: {e}")
            
            evaluation = TaskEvaluation(
                task_name=task_name,
                checkpoints=checkpoints,
                final_total=final_score['total'],
                final_result=final_score['result'],
                steps=steps,
                cost_usd=cost
            )
            
            self.evaluations[task_name] = evaluation
        
        logger.info(f"Loaded {len(self.evaluations)} task evaluations")
    
    def _parse_trajectory_metadata(self, traj_file: Path) -> tuple[Optional[int], Optional[float]]:
        """
        Extract step count and cost from trajectory file
        
        Returns:
            (steps, cost_usd)
        """
        steps = 0
        total_cost = 0.0
        
        try:
            with gzip.open(traj_file, 'rt') as f:
                trajectory = json.load(f)
            
            # Trajectory is a list of action events
            if isinstance(trajectory, list):
                steps = len(trajectory)
                # Cost data not available in basic trajectory format
                total_cost = 0.0
            else:
                # Legacy dict format support
                response_ids = set()
                
                for event in trajectory:
                    if event.get("tool_call_metadata") and "model_response" in event["tool_call_metadata"]:
                        response = event["tool_call_metadata"]["model_response"]
                        response_id = response.get("id")
                        
                        # Avoid counting same response multiple times
                        if response_id and response_id not in response_ids:
                            response_ids.add(response_id)
                            steps += 1
                            
                            # Calculate cost
                            usage = response.get("usage", {})
                            model = response.get("model", "")
                            prompt_tokens = usage.get("prompt_tokens", 0)
                            completion_tokens = usage.get("completion_tokens", 0)
                            
                            total_cost += self._calculate_cost(model, prompt_tokens, completion_tokens)
        except Exception as e:
            logger.warning(f"Could not parse trajectory {traj_file.name}: {e}")
            return 0, 0.0
        
        return steps, total_cost
    
    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost based on model pricing"""
        model_lower = model.lower()
        
        # Pricing as of experiment date (May 2025)
        if "gemini-2.5-pro" in model_lower:
            # Context window dependent pricing
            cost = (0.00000125 if prompt_tokens <= 200000 else 0.0000025) * prompt_tokens
            cost += (0.00001 if prompt_tokens <= 200000 else 0.000015) * completion_tokens
            return cost
        elif "gemini-2.0-flash" in model_lower:
            return 0.0000001 * prompt_tokens + 0.0000004 * completion_tokens
        elif "claude-3.5-sonnet" in model_lower or "claude-3-5-sonnet" in model_lower:
            return 0.000003 * prompt_tokens + 0.000015 * completion_tokens
        elif "gpt-4o" in model_lower:
            return 0.0000025 * prompt_tokens + 0.00001 * completion_tokens
        else:
            logger.warning(f"Unknown model for cost calculation: {model}")
            return 0.0
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate comprehensive summary statistics"""
        if not self.evaluations:
            return {"error": "No evaluations loaded"}
        
        total_tasks = len(self.evaluations)
        perfect_count = sum(1 for e in self.evaluations.values() if e.perfect)
        overall_score = sum(e.score for e in self.evaluations.values()) / total_tasks
        avg_steps = sum(e.steps for e in self.evaluations.values() if e.steps) / total_tasks
        avg_cost = sum(e.cost_usd for e in self.evaluations.values() if e.cost_usd) / total_tasks
        
        # Category breakdown
        categories = {}
        for eval in self.evaluations.values():
            cat = eval.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(eval)
        
        category_stats = {}
        for cat, evals in categories.items():
            perfect = sum(1 for e in evals if e.perfect)
            avg_score = sum(e.score for e in evals) / len(evals)
            category_stats[cat] = {
                "tasks": len(evals),
                "perfect_completions": perfect,
                "perfect_rate": perfect / len(evals),
                "average_score": avg_score
            }
        
        return {
            "summary": {
                "total_tasks": total_tasks,
                "perfect_completions": perfect_count,
                "perfect_rate": perfect_count / total_tasks,
                "overall_score": overall_score,
                "average_steps": avg_steps,
                "average_cost_usd": avg_cost
            },
            "by_category": category_stats,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_markdown_report(self) -> str:
        """Generate markdown-formatted report for AgentBeats UI"""
        summary = self.generate_summary_report()
        
        if "error" in summary:
            return f"# Error\n\n{summary['error']}"
        
        md = "# TheAgentCompany Benchmark Results\n\n"
        md += f"**Evaluation Date:** {summary['timestamp']}\n\n"
        
        # Overall stats
        md += "## Summary\n\n"
        s = summary['summary']
        md += f"- **Total Tasks:** {s['total_tasks']}\n"
        md += f"- **Perfect Completions:** {s['perfect_completions']} ({s['perfect_rate']:.1%})\n"
        md += f"- **Overall Score:** {s['overall_score']:.1%}\n"
        md += f"- **Average Steps:** {s['average_steps']:.1f}\n"
        md += f"- **Average Cost:** ${s['average_cost_usd']:.2f}\n\n"
        
        # Category breakdown
        md += "## Performance by Category\n\n"
        md += "| Category | Tasks | Perfect | Perfect Rate | Avg Score |\n"
        md += "|----------|-------|---------|--------------|----------|\n"
        
        for cat, stats in sorted(summary['by_category'].items()):
            md += f"| {cat.upper()} | {stats['tasks']} | {stats['perfect_completions']} | "
            md += f"{stats['perfect_rate']:.1%} | {stats['average_score']:.1%} |\n"
        
        # Top performers
        md += "\n## Top 10 Tasks (by score)\n\n"
        top_tasks = sorted(self.evaluations.values(), key=lambda e: e.score, reverse=True)[:10]
        md += "| Rank | Task | Score | Perfect |\n"
        md += "|------|------|-------|--------|\n"
        for i, task in enumerate(top_tasks, 1):
            perfect_mark = "⭐" if task.perfect else ""
            md += f"| {i} | {task.task_name} | {task.score:.1%} | {perfect_mark} |\n"
        
        return md
    
    async def on_battle_start(self, battle_info: Dict[str, Any]):
        """
        Called when battle starts. Load evaluations and report results.
        
        Args:
            battle_info: Information about the battle from AgentBeats backend
        """
        logger.info(f"Battle started: {battle_info.get('battle_id')}")
        
        # Load evaluations
        self.load_evaluations()
        
        # Generate report
        report = self.generate_summary_report()
        markdown = self.generate_markdown_report()
        
        # Send initial status update
        await self.send_battle_log(
            message="TheAgentCompany evaluation loaded",
            detail={"tasks_loaded": len(self.evaluations)},
            markdown_content=f"## Status\n\nLoaded {len(self.evaluations)} task evaluations."
        )
        
        # Send final result
        await self.send_battle_result(
            winner="benchmark_complete",  # No winner in benchmarks
            message=f"Evaluation complete: {report['summary']['overall_score']:.1%} overall score",
            detail=report,
            markdown_content=markdown
        )
        
        logger.info("Battle completed successfully")


def main():
    """Entry point for the green agent"""
    import os
    import sys
    
    # Get experiments path from environment or command line
    experiments_path = os.getenv(
        "EXPERIMENTS_PATH",
        "experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro"
    )
    
    if len(sys.argv) > 1:
        experiments_path = sys.argv[1]
    
    # Validate path
    if not Path(experiments_path).exists():
        logger.error(f"Experiments path not found: {experiments_path}")
        sys.exit(1)
    
    # Create and run agent
    agent = TheAgentCompanyGreenAgent(experiments_path)
    
    # Run as AgentBeats A2A service
    agent.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
