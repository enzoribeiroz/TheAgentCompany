#!/usr/bin/env python3
"""
TheAgentCompany Green Agent for AgentBeats Integration
=======================================================

HTTP-based implementation that communicates with AgentBeats backend
at http://nuggets.puppy9.com:9000

Workflow:
1. Agent starts up and registers via POST /agents
2. Backend sends battle start signal (A2A message) with battle_id
3. Agent loads pre-computed results from experiment logs
4. Agent posts final results via POST /battles/{battleId}
"""

import asyncio
import gzip
import json
import logging
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import httpx
from fastapi import FastAPI, Request
from uvicorn import Config, Server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configuration from environment
BACKEND_URL = os.getenv("AGENTBEATS_BACKEND_URL", "http://nuggets.puppy9.com:9000")
EXPERIMENTS_PATH = os.getenv("EXPERIMENTS_PATH", "../../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro")
AGENT_HOST = os.getenv("AGENT_HOST", "0.0.0.0")
AGENT_PORT = int(os.getenv("AGENT_PORT", "8080"))


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
    """Complete task evaluation"""
    task_id: str
    checkpoints: List[CheckpointScore]
    final_score: CheckpointScore
    total_steps: int = 0
    total_cost: float = 0.0
    
    @property
    def category(self) -> str:
        """Extract category from task ID (e.g., 'sde-add-wiki-page' -> 'sde')"""
        if '-' in self.task_id:
            return self.task_id.split('-')[0]
        return 'unknown'
    
    @property
    def completion_rate(self) -> float:
        """Task completion percentage"""
        return self.final_score.score
    
    @property
    def is_perfect(self) -> bool:
        """Whether task was completed perfectly"""
        return self.final_score.passed


class TheAgentCompanyGreenAgent:
    """
    Green agent that loads pre-computed TheAgentCompany benchmark results
    and reports them to AgentBeats backend via HTTP API.
    """
    
    def __init__(self, experiments_path: str):
        self.experiments_path = Path(experiments_path)
        self.results_dir = self.experiments_path / "results"
        self.trajectories_dir = self.experiments_path / "trajectories"
        
        # Runtime state
        self.agent_id: Optional[str] = None
        self.agent_url: Optional[str] = None
        self.evaluations: List[TaskEvaluation] = []
        
        # FastAPI app for receiving A2A messages
        self.app = FastAPI(title="TheAgentCompany Green Agent")
        self.setup_routes()
        
        if not self.results_dir.exists():
            raise ValueError(f"Results directory not found: {self.results_dir}")
        
        logger.info(f"Initialized agent with experiments path: {self.experiments_path}")
    
    def setup_routes(self):
        """Setup FastAPI routes for A2A message handling"""
        
        @self.app.post("/a2a")
        async def receive_a2a_message(request: Request):
            """Receive A2A messages from AgentBeats backend"""
            message = await request.json()
            logger.info(f"Received A2A message: {message}")
            
            # Handle battle start signal
            if message.get("type") == "battle_start" or message.get("event_type") == "battle_start":
                battle_id = message.get("battle_id")
                if battle_id:
                    await self.handle_battle_start(battle_id)
                    return {"status": "ok", "message": "Battle started"}
            
            return {"status": "ok"}
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy", "agent": "TheAgentCompany Green Agent"}
    
    async def register_agent(self, agent_url: str, launcher_url: str) -> str:
        """
        Register agent with AgentBeats backend
        
        Args:
            agent_url: URL where this agent is running (for A2A messages)
            launcher_url: Launcher URL from ab run
            
        Returns:
            agent_id assigned by backend
        """
        payload = {
            "alias": "TheAgentCompany Benchmark Reporter",
            "agent_url": agent_url,
            "launcher_url": launcher_url,
            "is_green": True,
            "participant_requirements": [],  # No white agents needed
            "battle_timeout": 600  # 10 minutes
        }
        
        logger.info(f"Registering agent with backend: {BACKEND_URL}/agents")
        logger.info(f"Payload: {payload}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/agents",
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            
        self.agent_id = result.get("agent_id")
        self.agent_url = agent_url
        
        logger.info(f"Agent registered successfully with ID: {self.agent_id}")
        return self.agent_id
    
    def load_evaluations(self) -> List[TaskEvaluation]:
        """Load all task evaluations from results directory"""
        evaluations = []
        
        logger.info(f"Loading evaluations from {self.results_dir}")
        
        for eval_file in sorted(self.results_dir.glob("eval_*-image.json")):
            task_id = eval_file.stem.replace("eval_", "").replace("-image", "")
            
            with open(eval_file) as f:
                data = json.load(f)
            
            # Parse checkpoints
            checkpoints = []
            if "checkpoints" in data:
                for cp in data["checkpoints"]:
                    checkpoints.append(CheckpointScore(
                        total=cp.get("total", 0),
                        result=cp.get("result", 0)
                    ))
            
            # Parse final score
            final_score = CheckpointScore(
                total=data.get("final_score", {}).get("total", 0),
                result=data.get("final_score", {}).get("result", 0)
            )
            
            # Parse trajectory for steps
            traj_file = self.trajectories_dir / f"traj_{task_id}-image.json.gz"
            steps = self._parse_trajectory_steps(traj_file)
            
            evaluations.append(TaskEvaluation(
                task_id=task_id,
                checkpoints=checkpoints,
                final_score=final_score,
                total_steps=steps,
                total_cost=0.0  # Cost data not available in trajectory format
            ))
        
        logger.info(f"Loaded {len(evaluations)} task evaluations")
        return evaluations
    
    def _parse_trajectory_steps(self, traj_file: Path) -> int:
        """Parse trajectory file to extract step count"""
        if not traj_file.exists():
            return 0
        
        try:
            with gzip.open(traj_file, 'rt') as f:
                traj_data = json.load(f)
            
            # Trajectory is a list of action events
            if isinstance(traj_data, list):
                return len(traj_data)
            
            return 0
        except Exception as e:
            logger.warning(f"Could not parse {traj_file.name}: {e}")
            return 0
    
    def generate_summary(self) -> Dict:
        """Generate summary statistics from evaluations"""
        if not self.evaluations:
            return {}
        
        # Aggregate by category
        by_category = {}
        for eval in self.evaluations:
            cat = eval.category
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(eval)
        
        # Calculate category stats
        category_stats = {}
        for cat, evals in by_category.items():
            total_tasks = len(evals)
            perfect_tasks = sum(1 for e in evals if e.is_perfect)
            avg_completion = sum(e.completion_rate for e in evals) / total_tasks
            avg_steps = sum(e.total_steps for e in evals) / total_tasks
            
            category_stats[cat] = {
                "pass_rate": perfect_tasks / total_tasks,
                "avg_completion": avg_completion,
                "avg_steps": avg_steps,
                "total_tasks": total_tasks,
                "perfect_tasks": perfect_tasks
            }
        
        # Overall stats
        total_tasks = len(self.evaluations)
        perfect_tasks = sum(1 for e in self.evaluations if e.is_perfect)
        avg_completion = sum(e.completion_rate for e in self.evaluations) / total_tasks
        
        return {
            "overall_pass_rate": perfect_tasks / total_tasks,
            "overall_avg_completion": avg_completion,
            "total_tasks": total_tasks,
            "perfect_tasks": perfect_tasks,
            "categories": category_stats
        }
    
    def generate_markdown_report(self, summary: Dict) -> str:
        """Generate markdown report for AgentBeats UI"""
        md = "# TheAgentCompany Benchmark Results\n\n"
        
        md += "## Overview\n\n"
        md += f"- **Total Tasks**: {summary['total_tasks']}\n"
        md += f"- **Perfect Completions**: {summary['perfect_tasks']} ({summary['overall_pass_rate']:.1%})\n"
        md += f"- **Average Completion Rate**: {summary['overall_avg_completion']:.1%}\n\n"
        
        md += "## Results by Category\n\n"
        md += "| Category | Total Tasks | Perfect | Pass Rate | Avg Completion | Avg Steps |\n"
        md += "|----------|-------------|---------|-----------|----------------|------------|\n"
        
        for cat, stats in sorted(summary['categories'].items()):
            md += f"| {cat.upper()} | {stats['total_tasks']} | {stats['perfect_tasks']} | "
            md += f"{stats['pass_rate']:.1%} | {stats['avg_completion']:.1%} | {stats['avg_steps']:.1f} |\n"
        
        md += "\n## Task Distribution\n\n"
        for cat, stats in sorted(summary['categories'].items()):
            percentage = stats['total_tasks'] / summary['total_tasks'] * 100
            md += f"- **{cat.upper()}**: {stats['total_tasks']} tasks ({percentage:.1f}%)\n"
        
        return md
    
    async def report_results(self, battle_id: str):
        """
        Report final battle results to AgentBeats backend
        
        Args:
            battle_id: Battle ID received from battle start signal
        """
        # Generate summary and report
        summary = self.generate_summary()
        markdown_content = self.generate_markdown_report(summary)
        
        # Construct BattleResult payload per OpenAPI spec
        result_payload = {
            "is_result": True,  # Mark as final result
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": "TheAgentCompany benchmark results successfully aggregated.",
            "winner": "N/A",  # Not applicable for single-agent evaluation
            "reported_by": "TheAgentCompany Green Agent",
            "detail": summary,  # Structured data
            "markdown_content": markdown_content  # Rich formatted report
        }
        
        logger.info(f"Reporting results for battle {battle_id}")
        logger.info(f"Summary: {json.dumps(summary, indent=2)}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/battles/{battle_id}",
                json=result_payload,
                timeout=30.0
            )
            response.raise_for_status()
        
        logger.info(f"Results reported successfully for battle {battle_id}")
    
    async def handle_battle_start(self, battle_id: str):
        """
        Handle battle start signal from backend
        
        Args:
            battle_id: Unique battle identifier
        """
        logger.info(f"Battle started: {battle_id}")
        
        # Load evaluations if not already loaded
        if not self.evaluations:
            self.evaluations = self.load_evaluations()
        
        # Report results immediately (since they're pre-computed)
        await self.report_results(battle_id)
        
        logger.info(f"Battle {battle_id} completed")
    
    async def run(self):
        """Run the agent server"""
        config = Config(
            app=self.app,
            host=AGENT_HOST,
            port=AGENT_PORT,
            log_level="info"
        )
        server = Server(config)
        await server.serve()


async def main():
    """Main entry point"""
    # Create agent
    agent = TheAgentCompanyGreenAgent(experiments_path=EXPERIMENTS_PATH)
    
    # Note: agent_url and launcher_url should be provided by `ab run`
    # For now, we construct them based on host/port
    agent_url = f"http://{AGENT_HOST}:{AGENT_PORT}"
    launcher_url = agent_url  # Same for standalone mode
    
    # Register agent (this should happen after server starts in production)
    # For now, we'll start the server and registration needs to be manual
    logger.info("=" * 60)
    logger.info("TheAgentCompany Green Agent Starting")
    logger.info("=" * 60)
    logger.info(f"Backend URL: {BACKEND_URL}")
    logger.info(f"Experiments Path: {EXPERIMENTS_PATH}")
    logger.info(f"Agent URL: {agent_url}")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Next steps:")
    logger.info("1. Ensure this agent is running")
    logger.info(f"2. Register manually at {BACKEND_URL}/agents or via UI")
    logger.info("3. Start a battle in the AgentBeats UI")
    logger.info("4. Agent will receive battle_start and report results")
    logger.info("=" * 60)
    
    # Run server
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
