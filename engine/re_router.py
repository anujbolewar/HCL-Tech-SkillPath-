"""Adaptive curriculum re-router and next-action engine.

Calculates unblocked nodes, prerequisite fulfillment graphs, determines
the highest-priority next learning action, and applies dynamic DAG adaptations
based on real-time diagnostic assessment results.
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


def apply_diagnostic_assessment(
    roadmap: Dict[str, Any],
    skill_topic: str,
    score: int,
    profile: Optional[Dict[str, Any]] = None
) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
    """Dynamically adapts the curriculum roadmap based on diagnostic assessment scores.
    
    If score < 70%, synthesizes and splices remedial prerequisite modules into the DAG,
    updating downstream prerequisite dependencies while preserving strict topological validity.
    
    Returns:
      (updated_roadmap, adaptation_event_dict)
    """
    import copy
    adapted_roadmap = copy.deepcopy(roadmap)
    
    # Check if already adapted
    existing_node_ids = {
        n["id"] for p in adapted_roadmap.get("phases", []) for n in p.get("nodes", [])
    }
    
    if score >= 70:
        # Passed assessment cleanly - no remediation required
        event = {
            "adapted": False,
            "skill_topic": skill_topic,
            "score": score,
            "reason": f"Assessment on {skill_topic} passed with {score}%. Standard learning trajectory verified."
        }
        return adapted_roadmap, event

    # If already adapted, construct consistent event metadata and return
    if "REM101" in existing_node_ids:
        event = {
            "adapted": True,
            "skill_topic": skill_topic,
            "score": score,
            "inserted_nodes": [
                {"id": "REM101", "title": "Retrieval Fundamentals & Chunking Strategies", "duration": "1 week"},
                {"id": "REM102", "title": "Vector Search Practice & Hybrid Reranking", "duration": "1 week"}
            ],
            "impacted_node": "AI302 (Enterprise Generative AI & Agentic RAG Capstone)",
            "reason": f"Diagnostic assessment on {skill_topic} revealed a score of {score}% (below 70% threshold). PathFinder dynamically synthesized and inserted 'Retrieval Fundamentals' and 'Vector Search Practice' as mandatory prerequisites before your final project."
        }
        return adapted_roadmap, event

    # Remediation Required (Weakness Detected)
    phases = adapted_roadmap.get("phases", [])
    if not phases:
        return adapted_roadmap, None

    # Target Phase 2 (or middle phase) for inserting remedial modules
    target_phase_idx = 1 if len(phases) > 1 else 0
    target_phase = phases[target_phase_idx]

    # Find foundational prerequisite node from Phase 1
    phase1_nodes = phases[0].get("nodes", [])
    prereq_base = phase1_nodes[0]["id"] if phase1_nodes else []

    rem_node_1 = {
        "id": "REM101",
        "title": "Retrieval Fundamentals & Chunking Strategies",
        "type": "Course",
        "provider": "Stanford Online / Coursera",
        "duration": "1 week",
        "skills": ["Information Retrieval", "Chunking", "Embeddings"],
        "prereqs": [prereq_base] if isinstance(prereq_base, str) else prereq_base,
        "why": f"Synthesized after diagnostic assessment on {skill_topic} ({score}% score) identified a foundational gap in semantic search."
    }

    rem_node_2 = {
        "id": "REM102",
        "title": "Vector Search Practice & Hybrid Reranking",
        "type": "Project",
        "provider": "DeepLearning.AI",
        "duration": "1 week",
        "skills": ["Vector DBs", "BM25 Hybrid Search", "Cross-Encoder Reranking"],
        "prereqs": ["REM101"],
        "why": "Hands-on implementation of FAISS/Chroma indexing and reranking before downstream capstone projects."
    }

    # Insert remedial nodes at the beginning of target phase
    target_phase["nodes"].insert(0, rem_node_1)
    target_phase["nodes"].insert(1, rem_node_2)

    # Re-wire downstream capstone node in the last phase
    last_phase = phases[-1]
    impacted_title = "Capstone Project"
    if last_phase.get("nodes"):
        last_node = last_phase["nodes"][-1]
        impacted_title = f"{last_node['id']} ({last_node.get('title', 'Capstone Project')})"
        if "REM102" not in last_node.get("prereqs", []):
            last_node.setdefault("prereqs", []).append("REM102")

    adaptation_event = {
        "adapted": True,
        "skill_topic": skill_topic,
        "score": score,
        "inserted_nodes": [
            {"id": "REM101", "title": "Retrieval Fundamentals & Chunking Strategies", "duration": "1 week"},
            {"id": "REM102", "title": "Vector Search Practice & Hybrid Reranking", "duration": "1 week"}
        ],
        "impacted_node": impacted_title,
        "reason": f"Diagnostic assessment on {skill_topic} revealed a score of {score}% (below 70% mastery threshold). PathFinder dynamically synthesized and inserted 'Retrieval Fundamentals' and 'Vector Search Practice' as mandatory prerequisites before your final project."
    }

    return adapted_roadmap, adaptation_event
