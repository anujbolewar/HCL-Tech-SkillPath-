"""Explainable AI (XAI) transparent relevance scoring engine.

Provides deterministic, multi-factor transparent scoring (0-100) explaining
why each node is recommended for a given learner profile and current progress.
"""

from typing import Dict, Any, Set, Tuple, List

def compute_node_relevance(
    node: Dict[str, Any],
    profile: Dict[str, Any],
    completed_nodes: Set[str],
    phase_idx: int,
    total_phases: int
) -> Tuple[int, List[str]]:
    """Deterministic, explainable relevance score (0-100) for a roadmap node.

    Three Key Transparent Factors:
      1. Skill-gap coverage (/40): Rewards teaching skills the learner does NOT already master.
      2. Prerequisite readiness (/30): Measures how many required prerequisites are completed.
      3. Experience-phase fit (/30): Matches learner level with curriculum depth (Phase 1 vs 2 vs 3).
      
    Returns:
      score (int): Normalized 0-100 score.
      breakdown (list[str]): Human-readable Chain-of-Thought explanation bullet points.
    """
    skills = node.get("skills") or []
    prereqs = node.get("prereqs") or []
    breakdown = []

    # Factor 1 - Skill-Gap Coverage (max 40)
    known_skills = set(profile.get("skills") or [])
    gap_skills = [s for s in skills if s not in known_skills]
    
    if skills:
        f_gap = round((len(gap_skills) / len(skills)) * 40, 1)
        breakdown.append(
            f"Skill-Gap Coverage: +{f_gap:.0f}/40 ({len(gap_skills)} of {len(skills)} skills are new to your profile)"
        )
    else:
        f_gap = 20.0
        breakdown.append("Skill-Gap Coverage: +20/40 (General competency milestone)")

    # Factor 2 - Prerequisite Readiness (max 30)
    if prereqs:
        met = sum(1 for p in prereqs if p in completed_nodes)
        f_prereq = round((met / len(prereqs)) * 30, 1)
        if met == len(prereqs):
            breakdown.append(f"Prerequisite Readiness: +{f_prereq:.0f}/30 (All {len(prereqs)} prerequisites unlocked)")
        else:
            breakdown.append(f"Prerequisite Readiness: +{f_prereq:.0f}/30 ({met} of {len(prereqs)} prerequisites completed)")
    else:
        f_prereq = 30.0
        breakdown.append("Prerequisite Readiness: +30/30 (Entry point — no prerequisites required)")

    # Factor 3 - Experience-Phase Fit (max 30)
    depth = (phase_idx + 1) / max(total_phases, 1)
    level = profile.get("experience_level") or "Beginner"
    fit_target = {"Beginner": 0.25, "Intermediate": 0.5, "Advanced": 0.85}.get(level, 0.5)
    closeness = max(0.0, 1.0 - abs(depth - fit_target))
    f_fit = round(closeness * 30, 1)
    phase_no = phase_idx + 1
    breakdown.append(
        f"Experience-Phase Alignment: +{f_fit:.0f}/30 ({level} level vs Phase {phase_no} of {total_phases})"
    )

    total_score = min(100, max(0, round(f_gap + f_prereq + f_fit)))
    return total_score, breakdown
