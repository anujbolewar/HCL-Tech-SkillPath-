"""Presentation components for PathFinder AI with spatial discipline and clean typography."""

from typing import Dict, Any, List, Set, Optional
import streamlit as st

from core.config import APP_TITLE, TEAM_NAME
from engine.re_router import calculate_progress_stats

def render_hero_header() -> None:
    """Renders the top hero card with refined typography and team badge."""
    st.markdown(f"""
    <div class="hero-container">
        <div class="brand-badge">HCL Tech Hackathon 2026 • Round 2 Prototype</div>
        <div class="brand-title">PathFinder <span>AI</span></div>
        <div class="hero-desc">
            Personalized, milestone-by-milestone curriculum architect. Transforms any learning objective into an adaptive, prerequisite-aware Directed Acyclic Graph (DAG) roadmap.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metrics_summary_bar(roadmap: Dict[str, Any], completed_nodes: Set[str]) -> None:
    """Renders the clean 4-column metric summary ribbon."""
    stats = calculate_progress_stats(roadmap, completed_nodes)
    
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-lbl">Target Focus</div>
            <div class="metric-num" style="font-size:1.15rem; color:#93c5fd;">{roadmap.get('role', 'Learner')}</div>
        </div>
        <div class="metric-card">
            <div class="metric-lbl">Total Milestones</div>
            <div class="metric-num">{stats['total_nodes']} Modules</div>
        </div>
        <div class="metric-card">
            <div class="metric-lbl">Completed</div>
            <div class="metric-num" style="color:#34d399;">{stats['completed_count']} of {stats['total_nodes']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-lbl">Curriculum Mastery</div>
            <div class="metric-num">{stats['progress_pct']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_node_inspector(node: Dict[str, Any], score: int, breakdown: List[str]) -> None:
    """Renders the refined Explainable AI 'Why' inspector card."""
    skills_tags = " ".join([f"<span class='tag tag-blue'>#{s}</span>" for s in node.get("skills", [])])
    prereqs_str = ", ".join(node.get("prereqs", [])) if node.get("prereqs") else "None (Entry Point)"
    
    st.markdown(f"""
    <div class="inspector-panel">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-family:'Outfit',sans-serif; font-size:1.15rem; font-weight:700; color:#818cf8;">
                Module Rationale: {node.get('id')}: {node.get('title')}
            </div>
            <span class="tag tag-emerald" style="font-size:0.8rem; padding:4px 10px;">{score}% Match Score</span>
        </div>
        <p style="font-size:0.92rem; color:#cbd5e1; margin:8px 0 12px 0; line-height:1.55;">
            <strong>Pedagogical Value:</strong> {node.get('why', 'Core required competency on this learning path.')}
        </p>
        <div style="margin-bottom:10px;">
            <span class="tag tag-amber">⏱️ {node.get('duration', '2 weeks')}</span>
            <span class="tag tag-indigo">🏢 {node.get('provider', 'Online')}</span>
            <span class="tag tag-slate">Prerequisites: {prereqs_str}</span>
        </div>
        <div>
            <span style="font-size:0.8rem; color:#94a3b8; margin-right:6px;">Target Competencies:</span>
            {skills_tags}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("View 3-Factor Relevance Scoring Breakdown", expanded=False):
        st.progress(score / 100, text=f"Total Alignment: {score}/100")
        for line in breakdown:
            st.caption(f"• {line}")
