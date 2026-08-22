"""Dynamic Skill Competency Radar Chart component styled for light mode."""

from collections import Counter
from typing import Dict, Any, Set, List
import streamlit as st
import plotly.graph_objects as go

def render_dynamic_radar_chart(
    roadmap: Dict[str, Any],
    profile: Dict[str, Any],
    completed_nodes: Set[str]
) -> None:
    """Renders dynamic Polar Radar Chart reflecting real-time skill acquisition in clean light mode."""
    st.markdown("### Competency Radar Analysis")
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
        line_color="#8A8A8A",
        fillcolor="rgba(138, 138, 138, 0.08)",
        line=dict(width=1.5, dash="dot")
    ))

    fig.add_trace(go.Scatterpolar(
        r=curr_loop,
        theta=theta_loop,
        fill="toself",
        name="Current Competency",
        line_color="#2563EB",
        fillcolor="rgba(37, 99, 235, 0.15)",
        line=dict(width=2.5)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#8A8A8A", size=9),
                gridcolor="#E5E5E2",
                linecolor="#E5E5E2"
            ),
            angularaxis=dict(
                tickfont=dict(color="#171717", size=11, family="Inter"),
                gridcolor="#E5E5E2",
                linecolor="#E5E5E2"
            ),
            bgcolor="#FFFFFF"
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color="#171717", size=11)
        ),
        margin=dict(l=30, r=30, t=20, b=30),
        height=280
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
