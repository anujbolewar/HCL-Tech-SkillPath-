"""Adaptive curriculum re-router and next-action engine.

Calculates unblocked nodes, prerequisite fulfillment graphs, and determines
the highest-priority next learning action for the learner.
"""

from typing import Dict, Any, Set, List, Optional, Tuple

def get_node_status(node: Dict[str, Any], completed_nodes: Set[str]) -> str:
    """Returns status of a node: 'completed', 'ready', or 'locked'."""
    node_id = node.get("id", "")
    if node_id in completed_nodes:
        return "completed"
    
    prereqs = node.get("prereqs", [])
    if not prereqs or all(p in completed_nodes for p in prereqs):
        return "ready"
    
    return "locked"

def find_next_recommended_action(roadmap: Dict[str, Any], completed_nodes: Set[str]) -> Optional[Tuple[Dict[str, Any], str]]:
    """Identifies the single highest priority unlocked milestone.
    
    Returns:
      (node_dict, phase_title) or None if all are completed.
    """
    for phase in roadmap.get("phases", []):
        for node in phase.get("nodes", []):
            if get_node_status(node, completed_nodes) == "ready":
                return node, phase.get("phase", "Active Phase")
    return None

def calculate_progress_stats(roadmap: Dict[str, Any], completed_nodes: Set[str]) -> Dict[str, Any]:
    """Calculates overall progress metrics, completion percentages, and milestone counts."""
    all_nodes = [n for phase in roadmap.get("phases", []) for n in phase.get("nodes", [])]
    total_count = len(all_nodes)
    completed_count = sum(1 for n in all_nodes if n.get("id") in completed_nodes)
    ready_count = sum(1 for n in all_nodes if get_node_status(n, completed_nodes) == "ready")
    locked_count = total_count - completed_count - ready_count
    
    pct = int((completed_count / total_count) * 100) if total_count > 0 else 0
    
    return {
        "total_nodes": total_count,
        "completed_count": completed_count,
        "ready_count": ready_count,
        "locked_count": locked_count,
        "progress_pct": pct,
        "is_complete": completed_count == total_count and total_count > 0
    }
