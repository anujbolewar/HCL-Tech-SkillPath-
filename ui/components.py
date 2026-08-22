"""Presentation components for PathFinder AI with spatial discipline and clean typography."""

from typing import Dict, Any, List, Set, Optional
import streamlit as st

from core.config import APP_TITLE, TEAM_NAME
from engine.re_router import calculate_progress_stats, get_node_status, find_next_recommended_action

def render_app_header(role_title: str = "Personalized Curriculum") -> None:
    """Renders a compact, functional application header (54px tall)."""
    st.markdown(f"""
    <div class="app-header">
        <div class="app-brand">
            🎓 PathFinder <span>AI</span>
            <span class="app-badge">{role_title}</span>
        </div>
        <div style="font-size:0.8rem; color:#94A3B8;">
            Team Cortex • HCL Tech Hackathon
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_skill_gap_section(roadmap: Dict[str, Any], profile: Dict[str, Any]) -> None:
    """Renders the explicit 'Where I Am vs Where I Need To Be' skill gap diagnostic using native container."""
    known_skills = set(profile.get("skills") or [])
    
    # Collect all skills targeted across the roadmap
    target_skills = []
    for phase in roadmap.get("phases", []):
        for node in phase.get("nodes", []):
            for s in (node.get("skills") or []):
                if s not in target_skills:
                    target_skills.append(s)

    identified_gaps = [s for s in target_skills if s not in known_skills]
    
    with st.container(border=True):
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border-bottom:1px solid #1E293B; padding-bottom:8px;">
            <span style="font-family:'Outfit',sans-serif; font-size:0.92rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#94A3B8;">
                Learner Diagnostic & Skill Gap Map
            </span>
            <span style="font-size:0.82rem; color:#94A3B8;">
                Paced for <strong>{profile.get('weekly_hours', 15)} hrs/week</strong> (Level: {profile.get('experience_level', 'Intermediate')})
            </span>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div style='font-size:0.82rem; font-weight:700; color:#94A3B8; margin-bottom:8px;'>CURRENT BASELINE:</div>", unsafe_allow_html=True)
            if known_skills:
                for s in list(known_skills)[:4]:
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; margin-bottom:2px; font-size:0.85rem;">
                        <span>{s}</span>
                        <span style="color:#34D399; font-weight:600;">Verified Mastered</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(0.85)
            else:
                st.caption("No prior skills declared (Foundational beginner track).")

        with col2:
            st.markdown("<div style='font-size:0.82rem; font-weight:700; color:#94A3B8; margin-bottom:8px;'>IDENTIFIED GAPS TO BRIDGE:</div>", unsafe_allow_html=True)
            if identified_gaps:
                for s in identified_gaps[:4]:
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; margin-bottom:2px; font-size:0.85rem;">
                        <span>{s}</span>
                        <span style="color:#60A5FA; font-weight:500;">Gap Target</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(0.20)
            else:
                st.caption("All targeted skills align with your baseline.")


def render_next_best_action_card(roadmap: Dict[str, Any], completed_nodes: Set[str]) -> None:
    """Renders the prominent 'Next Best Action' recommendation block."""
    next_action_res = find_next_recommended_action(roadmap, completed_nodes)

    if next_action_res:
        next_node, next_phase = next_action_res
        st.markdown(f"""
        <div class="next-action-card">
            <div class="next-action-badge">▶ Next Best Action</div>
            <div class="next-action-title">{next_node.get('id')}: {next_node.get('title')}</div>
            <div class="next-action-meta">
                <strong>{next_node.get('duration', '2 weeks')}</strong> · {next_node.get('type', 'Course')} · <em>{next_node.get('provider', 'Online')}</em> · {next_phase}
            </div>
            <div class="next-action-why">
                <strong>Why PathFinder recommended this now:</strong> {next_node.get('why', 'Prerequisites are unlocked. Completing this milestone directly closes an identified skill gap.')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="next-action-card" style="border-color:#059669; border-left-color:#059669;">
            <div class="next-action-badge" style="color:#34D399;">✓ Curriculum Completed</div>
            <div class="next-action-title">All Milestones Mastered!</div>
            <div class="next-action-meta">You have completed all prerequisite pathways in this personalized curriculum.</div>
        </div>
        """, unsafe_allow_html=True)


def render_node_inspector(node: Dict[str, Any], score: int, breakdown: List[str]) -> None:
    """Renders a clean module rationale inspector near the roadmap."""
    prereqs_str = ", ".join(node.get("prereqs", [])) if node.get("prereqs") else "None (Entry Point)"
    skills_str = " · ".join(node.get("skills", ["General"]))

    st.markdown(f"""
    <div class="node-inspector-box">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <strong style="font-family:'Outfit',sans-serif; font-size:1.1rem; color:#F8FAFC;">
                {node.get('id')}: {node.get('title')}
            </strong>
            <span class="status-tag status-active">{score}% Match Score</span>
        </div>
        <div style="font-size:0.85rem; color:#94A3B8; margin-bottom:10px;">
            {node.get('provider', 'Online')} · {node.get('duration', '2 weeks')} · Prerequisites: <strong>{prereqs_str}</strong>
        </div>
        <div style="font-size:0.9rem; color:#CBD5E1; line-height:1.5; margin-bottom:10px;">
            <strong>Why This Module:</strong> {node.get('why', 'Key required competency.')}
        </div>
        <div style="font-size:0.82rem; color:#94A3B8;">
            <strong>Target Competencies:</strong> {skills_str}
        </div>
    </div>
    """, unsafe_allow_html=True)
