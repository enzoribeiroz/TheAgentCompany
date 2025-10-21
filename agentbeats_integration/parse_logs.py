#!/usr/bin/env python3
"""
Standalone utility to parse and analyze TheAgentCompany experiment logs.
Use this for quick analysis without running the full AgentBeats integration.

Example usage:
    python parse_logs.py ../../experiments/evaluation/1.0.0/20250510_OpenHands-0.28.1-gemini-2.5-pro
    python parse_logs.py --category sde --output sde_results.csv
    python parse_logs.py --top 10 --format json
"""

import argparse
import gzip
import json
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class CheckpointScore:
    """Checkpoint evaluation score"""
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


class LogParser:
    """Parser for TheAgentCompany experiment logs"""
    
    def __init__(self, experiments_path: str):
        self.experiments_path = Path(experiments_path)
        self.results_dir = self.experiments_path / "results"
        self.trajectories_dir = self.experiments_path / "trajectories"
        
        if not self.results_dir.exists():
            raise ValueError(f"Results directory not found: {self.results_dir}")
    
    def load_evaluations(self) -> List[TaskEvaluation]:
        """Load all task evaluations from results directory"""
        evaluations = []
        
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
            
            # Parse trajectory for steps and cost
            traj_file = self.trajectories_dir / f"traj_{task_id}-image.json.gz"
            steps, cost = self._parse_trajectory(traj_file)
            
            evaluations.append(TaskEvaluation(
                task_id=task_id,
                checkpoints=checkpoints,
                final_score=final_score,
                total_steps=steps,
                total_cost=cost
            ))
        
        return evaluations
    
    def _parse_trajectory(self, traj_file: Path) -> tuple[int, float]:
        """Parse trajectory file to extract steps and cost"""
        if not traj_file.exists():
            return 0, 0.0
        
        try:
            with gzip.open(traj_file, 'rt') as f:
                traj_data = json.load(f)
            
            # Trajectory is a list of actions
            if isinstance(traj_data, list):
                steps = len(traj_data)
                # Cost calculation not available in trajectory list format
                cost = 0.0
            else:
                # Fallback for dict format
                steps = len(traj_data.get("trajectory", []))
                metrics = traj_data.get("metrics", {})
                cost = metrics.get("accumulated_cost", 0.0)
            
            return steps, cost
        except Exception as e:
            print(f"Warning: Could not parse {traj_file.name}: {e}", file=sys.stderr)
            return 0, 0.0


def generate_summary(evaluations: List[TaskEvaluation], category: Optional[str] = None) -> Dict:
    """Generate summary statistics"""
    if category:
        evaluations = [e for e in evaluations if e.category == category]
    
    if not evaluations:
        return {}
    
    # Aggregate by category
    by_category = defaultdict(list)
    for eval in evaluations:
        by_category[eval.category].append(eval)
    
    category_stats = {}
    for cat, evals in by_category.items():
        total_tasks = len(evals)
        perfect_tasks = sum(1 for e in evals if e.is_perfect)
        avg_completion = sum(e.completion_rate for e in evals) / total_tasks
        total_cost = sum(e.total_cost for e in evals)
        
        category_stats[cat] = {
            "total_tasks": total_tasks,
            "perfect_tasks": perfect_tasks,
            "perfect_rate": perfect_tasks / total_tasks,
            "avg_completion": avg_completion,
            "total_cost": total_cost
        }
    
    return {
        "total_tasks": len(evaluations),
        "perfect_tasks": sum(1 for e in evaluations if e.is_perfect),
        "avg_completion": sum(e.completion_rate for e in evaluations) / len(evaluations),
        "total_cost": sum(e.total_cost for e in evaluations),
        "by_category": category_stats
    }


def print_table(evaluations: List[TaskEvaluation], top_n: Optional[int] = None):
    """Print results as a formatted table"""
    if top_n:
        evaluations = sorted(evaluations, key=lambda e: e.completion_rate, reverse=True)[:top_n]
    
    # Header
    print(f"{'Task ID':<40} {'Category':<10} {'Score':<10} {'Steps':<8} {'Cost ($)':<10}")
    print("-" * 80)
    
    # Rows
    for eval in evaluations:
        score = f"{eval.completion_rate:.2%}"
        cost = f"${eval.total_cost:.4f}"
        print(f"{eval.task_id:<40} {eval.category:<10} {score:<10} {eval.total_steps:<8} {cost:<10}")


def export_csv(evaluations: List[TaskEvaluation], output_file: str):
    """Export results to CSV"""
    import csv
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Task ID', 'Category', 'Completion Rate', 'Perfect', 'Steps', 'Cost'])
        
        for eval in evaluations:
            writer.writerow([
                eval.task_id,
                eval.category,
                f"{eval.completion_rate:.4f}",
                eval.is_perfect,
                eval.total_steps,
                f"{eval.total_cost:.6f}"
            ])
    
    print(f"Results exported to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Parse TheAgentCompany experiment logs")
    parser.add_argument("experiments_path", help="Path to experiments directory")
    parser.add_argument("--category", help="Filter by category (e.g., sde, pm, ds)")
    parser.add_argument("--top", type=int, help="Show only top N tasks by score")
    parser.add_argument("--format", choices=['table', 'json', 'csv'], default='table',
                       help="Output format")
    parser.add_argument("--output", help="Output file (for CSV/JSON)")
    
    args = parser.parse_args()
    
    # Load evaluations
    log_parser = LogParser(args.experiments_path)
    evaluations = log_parser.load_evaluations()
    
    if not evaluations:
        print("No evaluations found!", file=sys.stderr)
        return 1
    
    # Filter by category
    if args.category:
        evaluations = [e for e in evaluations if e.category == args.category]
        if not evaluations:
            print(f"No tasks found for category: {args.category}", file=sys.stderr)
            return 1
    
    # Output
    if args.format == 'table':
        print_table(evaluations, args.top)
        print()
        summary = generate_summary(evaluations)
        print(f"\nSummary:")
        print(f"  Total Tasks: {summary['total_tasks']}")
        print(f"  Perfect Tasks: {summary['perfect_tasks']} ({summary['perfect_tasks']/summary['total_tasks']:.2%})")
        print(f"  Avg Completion: {summary['avg_completion']:.2%}")
        print(f"  Total Cost: ${summary['total_cost']:.2f}")
    
    elif args.format == 'json':
        output = {
            "evaluations": [asdict(e) for e in evaluations],
            "summary": generate_summary(evaluations)
        }
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"Results exported to {args.output}")
        else:
            print(json.dumps(output, indent=2))
    
    elif args.format == 'csv':
        if not args.output:
            print("Error: --output required for CSV format", file=sys.stderr)
            return 1
        export_csv(evaluations, args.output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
