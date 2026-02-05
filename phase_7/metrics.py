"""
Unified metrics computation engine for Phase 7.

IMPORTANT: This engine is OBSERVATIONAL ONLY.
It does NOT influence execution.
"""
import json
from pathlib import Path
from typing import List, Optional, Set

from .evaluation.consistency import (
    compute_determinism_score,
    compute_drift_score,
    compute_jaccard_similarity,
    extract_group_ids
)
from .evaluation.coverage import (
    compute_group_coverage,
    compute_parameter_diversity
)
from .evaluation.stability import (
    compute_cross_run_stability
)


class MetricsEngine:
    """
    Computes research-grade metrics for lighting decisions.
    
    IMPORTANT: This engine is OBSERVATIONAL ONLY.
    """
    
    def __init__(self, available_groups: Optional[Set[str]] = None):
        self.available_groups = available_groups or set()
    
    def evaluate_instruction(self, instruction: dict) -> dict:
        """Compute all metrics for a single instruction."""
        return {
            "coverage": compute_group_coverage(instruction, self.available_groups),
            "diversity": compute_parameter_diversity(instruction)
        }
    
    def evaluate_pair(
        self,
        instruction_a: dict,
        instruction_b: dict,
        epsilon: float = 0.05
    ) -> dict:
        """Compare two instructions for consistency."""
        score, breakdown = compute_determinism_score(
            instruction_a, instruction_b, epsilon
        )
        return {
            "determinism_score": score,
            "breakdown": breakdown,
            "jaccard_groups": compute_jaccard_similarity(
                extract_group_ids(instruction_a),
                extract_group_ids(instruction_b)
            )
        }
    
    def evaluate_sequence(self, instructions: List[dict]) -> dict:
        """Evaluate a sequence of instructions for drift."""
        return {
            "drift_score": compute_drift_score(instructions),
            "num_instructions": len(instructions)
        }
    
    def evaluate_runs(
        self,
        runs: List[List[dict]],
        epsilon: float = 0.05
    ) -> dict:
        """Evaluate cross-run stability."""
        return compute_cross_run_stability(runs, epsilon)
    
    def generate_report(
        self,
        instructions: List[dict],
        runs: Optional[List[List[dict]]] = None
    ) -> dict:
        """Generate comprehensive metrics report."""
        report = {
            "summary": {
                "num_instructions": len(instructions),
                "available_groups": len(self.available_groups)
            },
            "sequence_metrics": self.evaluate_sequence(instructions),
            "instruction_metrics": []
        }
        
        for i, instr in enumerate(instructions):
            report["instruction_metrics"].append({
                "index": i,
                "scene_id": instr.get("scene_id"),
                **self.evaluate_instruction(instr)
            })
        
        if runs and len(runs) > 1:
            report["stability_metrics"] = self.evaluate_runs(runs)
        
        return report
