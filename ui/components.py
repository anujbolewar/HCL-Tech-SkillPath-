"""Presentation components for PathFinder AI with spatial discipline and clean typography."""

from typing import Dict, Any, List, Set, Optional
import streamlit as st

from core.config import APP_TITLE, TEAM_NAME
from engine.re_router import calculate_progress_stats, get_node_status, find_next_recommended_action

def clean_html(html_str: str) -> str:
    """Strips all leading and trailing whitespace from each line to prevent Markdown codeblock parsing."""
    return "\n".join([line.strip() for line in html_str.strip().splitlines()])


def render_app_header(role_title: str = "Personalized Curriculum") -> None:
    """Renders a compact, functional application header (54px tall)."""
    raw_html = f"""
    <div class="app-header">
        <div class="app-brand">
            🎓 PathFinder <span>AI</span>
            <span class="app-badge">{role_title}</span>
        </div>
        <div style="font-size:0.8rem; color:#94A3B8;">
            Team Cortex • HCL Tech Hackathon
        </div>
    </div>
    """
    st.markdown(clean_html(raw_html), unsafe_allow_html=True)


def render_skill_gap_section(roadmap: Dict[str, Any], profile: Dict[str, Any]) -> None:
    """Renders the explicit 'Where I Am vs Where I Need To Be' skill gap diagnostic using atomic CSS Grid."""
    known_skills = list(set(profile.get("skills") or []))
    
    # Collect all skills targeted across the roadmap
    target_skills = []
    for phase in roadmap.get("phases", []):
        for node in phase.get("nodes", []):
            for s in (node.get("skills") or []):
                if s not in target_skills:
                    target_skills.append(s)

    identified_gaps = [s for s in target_skills if s not in known_skills]

    # Baseline rows
    baseline_items = []
    if known_skills:
        for s in known_skills[:4]:
            baseline_items.append(f"""
            <div style="margin-bottom: 10px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
                    <span style="color:#F8FAFC; font-weight:500;">{s}</span>
                    <span style="color:#34D399; font-weight:600; font-size:0.75rem;">Verified Mastered (85%)</span>
                </div>
                <div style="background:#162035; border-radius:999px; height:6px; width:100%; overflow:hidden;">
                    <div style="background:#10B981; width:85%; height:100%; border-radius:999px;"></div>
                </div>
            </div>
            """)
        baseline_html = "".join(baseline_items)
    else:
        baseline_html = "<div style='color:#64748B; font-size:0.85rem; padding: 12px 0;'>No prior skills declared (Foundational beginner track).</div>"

    # Gaps rows
    gaps_items = []
    if identified_gaps:
        for s in identified_gaps[:4]:
            gaps_items.append(f"""
            <div style="margin-bottom: 10px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
                    <span style="color:#F8FAFC; font-weight:500;">{s}</span>
                    <span style="color:#60A5FA; font-weight:600; font-size:0.75rem;">Gap Target (20%)</span>
                </div>
                <div style="background:#162035; border-radius:999px; height:6px; width:100%; overflow:hidden;">
                    <div style="background:#3B82F6; width:20%; height:100%; border-radius:999px;"></div>
                </div>
            </div>
            """)
        gaps_html = "".join(gaps_items)
    else:
        gaps_html = "<div style='color:#64748B; font-size:0.85rem; padding: 12px 0;'>All targeted skills align with your baseline profile.</div>"

    hours = profile.get('weekly_hours', 15)
    exp = profile.get('experience_level', 'Intermediate')

    card_html = f"""
    <div style="background:#0F1626; border:1px solid #1E293B; border-radius:10px; padding:18px 22px; margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #1E293B; padding-bottom:8px;">
            <span style="font-family:'Outfit',sans-serif; font-size:0.92rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#94A3B8;">
                Learner Diagnostic & Skill Gap Map
            </span>
            <span style="font-size:0.82rem; color:#94A3B8;">
                Paced for <strong>{hours} hrs/week</strong> (Level: {exp})
            </span>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 28px;">
            <div>
                <div style="font-size:0.78rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:10px;">
                    Current Baseline
                </div>
                {baseline_html}
            </div>
            <div>
                <div style="font-size:0.78rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:10px;">
                    Identified Gaps to Bridge
                </div>
                {gaps_html}
            </div>
        </div>
    </div>
    """
    st.markdown(clean_html(card_html), unsafe_allow_html=True)


def render_next_best_action_card(roadmap: Dict[str, Any], completed_nodes: Set[str]) -> None:
    """Renders the prominent 'Next Best Action' recommendation block."""
    next_action_res = find_next_recommended_action(roadmap, completed_nodes)

    if next_action_res:
        next_node, next_phase = next_action_res
        n_id = next_node.get('id', '')
        n_title = next_node.get('title', '')
        n_dur = next_node.get('duration', '2 weeks')
        n_type = next_node.get('type', 'Course')
        n_prov = next_node.get('provider', 'Online')
        n_why = next_node.get('why', 'Prerequisites are unlocked. Completing this milestone directly closes an identified skill gap.')

        card_html = f"""
        <div class="next-action-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:4px;">
                <div class="next-action-badge">▶ Next Best Action</div>
                <span class="status-tag status-active">{n_dur}</span>
            </div>
            <div class="next-action-title">{n_id}: {n_title}</div>
            <div class="next-action-meta">
                {n_type} · <em>{n_prov}</em> · {next_phase}
            </div>
            <div class="next-action-why">
                <strong>Why PathFinder recommended this now:</strong> {n_why}
            </div>
        </div>
        """
        st.markdown(clean_html(card_html), unsafe_allow_html=True)
    else:
        completed_html = """
        <div class="next-action-card" style="border-color:#059669; border-left-color:#059669;">
            <div class="next-action-badge" style="color:#34D399;">✓ Curriculum Completed</div>
            <div class="next-action-title">All Milestones Mastered!</div>
            <div class="next-action-meta">You have completed all prerequisite pathways in this personalized curriculum.</div>
        </div>
        """
        st.markdown(clean_html(completed_html), unsafe_allow_html=True)


def render_node_inspector(node: Dict[str, Any], score: int, breakdown: List[str]) -> None:
    """Renders a clean module rationale inspector near the roadmap."""
    prereqs_str = ", ".join(node.get("prereqs", [])) if node.get("prereqs") else "None (Entry Point)"
    skills_str = " · ".join(node.get("skills", ["General"]))
    n_id = node.get('id', '')
    n_title = node.get('title', '')
    n_prov = node.get('provider', 'Online')
    n_dur = node.get('duration', '2 weeks')
    n_why = node.get('why', 'Key required competency.')

    inspector_html = f"""
    <div class="node-inspector-box">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="font-family:'Outfit',sans-serif; font-size:1.05rem; color:#F8FAFC;">
                {n_id}: {n_title}
            </strong>
            <span class="status-tag status-active">{score}% Match</span>
        </div>
        <div style="font-size:0.82rem; color:#94A3B8; margin-bottom:8px;">
            {n_prov} · {n_dur}
        </div>
        <div style="font-size:0.82rem; color:#94A3B8; margin-bottom:8px;">
            Prerequisites: <strong style="color:#F8FAFC;">{prereqs_str}</strong>
        </div>
        <div style="font-size:0.88rem; color:#CBD5E1; line-height:1.45; margin-bottom:8px; background:#162035; padding:8px 12px; border-radius:6px;">
            <strong>Why This Module:</strong> {n_why}
        </div>
        <div style="font-size:0.8rem; color:#94A3B8;">
            <strong>Skills:</strong> {skills_str}
        </div>
    </div>
    """
    st.markdown(clean_html(inspector_html), unsafe_allow_html=True)
