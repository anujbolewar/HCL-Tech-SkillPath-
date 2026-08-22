"""Dynamic Skill Competency Radar Chart component."""

from collections import Counter
from typing import Dict, Any, Set, List
import streamlit as st
import plotly.graph_objects as go

def render_dynamic_radar_chart(
    roadmap: Dict[str, Any],
    profile: Dict[str, Any],
    completed_nodes: Set[str]
) -> None:
    """Renders dynamic Polar Radar Chart reflecting real-time skill acquisition."""
    st.markdown("### Skill Competency Radar")
    st.caption("Real-time competency tracking across 6 core skill dimensions derived from your active curriculum.")

    # Extract all skills from this roadmap
    node_skills: List[str] = [
        skill
        for phase in roadmap.get("phases", [])
        for node in phase.get("nodes", [])
        for skill in (node.get("skills") or [])
    ]

    # Pick top 6 most prominent domain competencies
    top_skills_counts = Counter(node_skills).most_common(6)
    top_skills = [s for s, _ in top_skills_counts]

    # Fallback to defaults if no skills found
    if len(top_skills) < 3:
        top_skills = ["Core Theory", "Applied Practice", "Tooling", "Problem Solving", "Domain Synthesis", "Capstone"]

    known_skills = set(profile.get("skills") or [])
    exp_level = profile.get("experience_level", "Intermediate")
    base_level_val = {"Beginner": 15, "Intermediate": 35, "Advanced": 60}.get(exp_level, 30)

    base_vals = []
    current_vals = []

    for skill in top_skills:
        is_known = skill in known_skills or any(k.lower() in skill.lower() for k in known_skills)
        base = max(base_level_val, 50) if is_known else base_level_val
        base_vals.append(base)

        milestones_done = sum(
            1
            for phase in roadmap.get("phases", [])
            for node in phase.get("nodes", [])
            if skill in (node.get("skills") or []) and node["id"] in completed_nodes
        )
        
        boost = min(45, milestones_done * 22)
        current = min(100, base + boost)
        current_vals.append(current)

    # Close the polygon loop for polar plot
    theta_loop = top_skills + [top_skills[0]]
    base_loop = base_vals + [base_vals[0]]
    curr_loop = current_vals + [current_vals[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=base_loop,
        theta=theta_loop,
        fill="toself",
        name="Baseline Profile",
        line_color="#64748b",
        fillcolor="rgba(100, 116, 139, 0.12)",
        line=dict(width=1.5, dash="dot")
    ))

    fig.add_trace(go.Scatterpolar(
        r=curr_loop,
        theta=theta_loop,
        fill="toself",
        name="Current Competency",
        line_color="#6366f1",
        fillcolor="rgba(99, 102, 241, 0.25)",
        line=dict(width=2.5)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#64748b", size=9),
                gridcolor="rgba(255, 255, 255, 0.07)",
                linecolor="rgba(255, 255, 255, 0.07)"
            ),
            angularaxis=dict(
                tickfont=dict(color="#e2e8f0", size=11, family="Outfit"),
                gridcolor="rgba(255, 255, 255, 0.07)",
                linecolor="rgba(255, 255, 255, 0.07)"
            ),
            bgcolor="rgba(0,0,0,0)"
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(color="#94a3b8", size=11)
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=20, b=45),
        height=360
    )

    st.plotly_chart(fig, use_container_width=True)
