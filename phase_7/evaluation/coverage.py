"""
Coverage metrics to avoid trivial solutions.

Measures:
- Group coverage (fraction of available groups used)
- Parameter diversity (variety in lighting parameters)
"""
from typing import Set


def compute_group_coverage(
    instruction: dict,
    available_groups: Set[str]
) -> float:
    """
    Compute what fraction of available groups were used.
    Helps detect trivial solutions (e.g., only using 1 group).
    """
    if not available_groups:
        return 0.0
    
    used_groups = {g.get("group_id") for g in instruction.get("groups", [])}
    return len(used_groups & available_groups) / len(available_groups)


def compute_parameter_diversity(instruction: dict) -> dict:
    """
    Compute diversity of parameters used.
    Higher diversity = more nuanced lighting decisions.
    """
    groups = instruction.get("groups", [])
    if not groups:
        return {
            "intensity_range": 0.0,
            "transition_types": 0,
            "colors_used": 0,
            "groups_used": 0
        }
    
    intensities = [g.get("parameters", {}).get("intensity", 0) for g in groups]
    transitions = {(g.get("transition") or {}).get("type") for g in groups}
    colors = {g.get("parameters", {}).get("color") for g in groups}
    
    return {
        "intensity_range": max(intensities) - min(intensities),
        "transition_types": len(transitions - {None}),
        "colors_used": len(colors - {None}),
        "groups_used": len(groups)
    }
