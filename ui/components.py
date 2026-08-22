"""Reusable presentation UI components for PathFinder AI."""

from typing import Dict, Any, List, Set, Optional
import streamlit as st

from core.config import APP_TITLE, APP_SUBTITLE, TEAM_NAME, COLLEGE_NAME
from engine.re_router import calculate_progress_stats

def render_hero_header() -> None:
    """Renders the top hero card with team metadata."""
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-title">{APP_TITLE} <span style="font-size:1.05rem;font-weight:500;color:#93c5fd;-webkit-text-fill-color:#93c5fd;">— by Team {TEAM_NAME}</span></div>
        <div class="hero-subtitle">
            AI-powered Directed Acyclic Graph (DAG) curriculum architect. Delivers adaptive, milestone-by-milestone personalized learning paths tailored to your exact skills, schedule, and goals.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metrics_summary_bar(roadmap: Dict[str, Any], completed_nodes: Set[str]) -> None:
    """Renders the top 4-column metric summary bar."""
    stats = calculate_progress_stats(roadmap, completed_nodes)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-val">{roadmap.get('role', 'Learner')}</div>
            <div class="metric-lbl">Target Role / Focus</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-val">{stats['total_nodes']} Nodes</div>
            <div class="metric-lbl">Total Milestones</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-val">{stats['completed_count']} / {stats['total_nodes']}</div>
            <div class="metric-lbl">Completed</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-val">{stats['progress_pct']}%</div>
            <div class="metric-lbl">Curriculum Mastery</div>
        </div>
        """, unsafe_allow_html=True)


def render_node_inspector(node: Dict[str, Any], score: int, breakdown: List[str]) -> None:
    """Renders the transparent Explainable AI 'Why' panel for a clicked node in the DAG."""
    skills_tags = " ".join([f"<span class='badge badge-primary'>#{s}</span>" for s in node.get("skills", [])])
    prereqs_str = ", ".join(node.get("prereqs", [])) if node.get("prereqs") else "None (Entry Point)"
    
    st.markdown(f"""
    <div class="node-inspector-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:1.15rem; font-weight:700; color:#60a5fa;">
                📍 Node Inspector: {node.get('id')}: {node.get('title')}
            </div>
            <span class="badge badge-success">{score}% Relevance Score</span>
        </div>
        <p style="font-size:0.95rem; color:#e4e4e7; margin:6px 0 10px 0;">
            <strong>💡 Why this is recommended:</strong> {node.get('why', 'Core required milestone on your learning path.')}
        </p>
        <div style="margin-bottom:8px;">
            <span class="badge badge-warning">⏱️ {node.get('duration', '2 weeks')}</span>
            <span class="badge badge-purple">🏢 {node.get('provider', 'Online')}</span>
            <span class="badge badge-muted">🔒 Prereqs: {prereqs_str}</span>
        </div>
        <div>
            <strong style="font-size:0.85rem; color:#a1a1aa;">Skills Targeted:</strong> {skills_tags}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 View Relevance Score Breakdown (Chain-of-Thought)", expanded=False):
        st.progress(score / 100, text=f"Total Fit: {score}/100")
        for line in breakdown:
            st.caption(f"• {line}")
