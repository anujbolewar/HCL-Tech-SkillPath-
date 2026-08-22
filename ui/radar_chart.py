"""Dynamic Skill Competency Radar Chart component.

Recalculates competency metrics in real-time based on the active learning goal,
the user's baseline skills, and completed milestones upon every re-render.
"""

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
    st.markdown("### 🕸️ Adaptive Skill Competency Radar")
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
        top_skills = ["Foundations", "Problem Solving", "Applied Practice", "Tooling", "Domain Theory", "Capstone"]

    known_skills = set(profile.get("skills") or [])
    exp_level = profile.get("experience_level", "Intermediate")
    base_level_val = {"Beginner": 15, "Intermediate": 35, "Advanced": 60}.get(exp_level, 30)

    base_vals = []
    current_vals = []

    for skill in top_skills:
        # Base value: higher if skill was in user's profile
        is_known = skill in known_skills or any(k.lower() in skill.lower() for k in known_skills)
        base = max(base_level_val, 50) if is_known else base_level_val
        base_vals.append(base)

        # Increment competency based on completed nodes teaching this skill
        milestones_done = sum(
            1
            for phase in roadmap.get("phases", [])
            for node in phase.get("nodes", [])
            if skill in (node.get("skills") or []) and node["id"] in completed_nodes
        )
        
        # Skill boost per completed milestone
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
        line_color="#38bdf8",
        fillcolor="rgba(56, 189, 248, 0.15)",
        line=dict(width=2, dash="dot")
    ))

    fig.add_trace(go.Scatterpolar(
        r=curr_loop,
        theta=theta_loop,
        fill="toself",
        name="Current Mastery",
        line_color="#10b981",
        fillcolor="rgba(16, 185, 129, 0.28)",
        line=dict(width=2.5)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#a1a1aa", size=9),
                gridcolor="#27272a",
                linecolor="#27272a"
            ),
            angularaxis=dict(
                tickfont=dict(color="#f4f4f5", size=11, family="Space Grotesk"),
                gridcolor="#27272a",
                linecolor="#27272a"
            ),
            bgcolor="rgba(0,0,0,0)"
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color="#d4d4d8", size=11)
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=35, r=35, t=30, b=50),
        height=380
    )

    st.plotly_chart(fig, use_container_width=True)
