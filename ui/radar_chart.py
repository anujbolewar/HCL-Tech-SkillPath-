"""Progress & Competency Radar Analytics component styled for editorial light mode."""

from collections import Counter
import html
from typing import Dict, Any, Set, List
import streamlit as st
import plotly.graph_objects as go

from engine.re_router import calculate_progress_stats

def render_dynamic_radar_chart(
    roadmap: Dict[str, Any],
    profile: Dict[str, Any],
    completed_nodes: Set[str]
) -> None:
    """Renders the comprehensive Progress Analytics section with competency gains and polar chart."""
    stats = calculate_progress_stats(roadmap, completed_nodes)
    pct = stats.get("progress_pct", 0)

    st.markdown(f"""
    <div style="margin-bottom:16px;">
        <div style="font-size:11px; font-weight:650; text-transform:uppercase; letter-spacing:0.08em; color:#858585; margin-bottom:4px;">
            Your Progress
        </div>
        <div style="display:flex; align-items:baseline; gap:10px;">
            <span class="pf-serif-headline" style="font-size:36px; color:#111111;">{pct}%</span>
            <span style="font-size:14px; color:#4B4B4B;">Target Competency Mastered</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Extract all skills from this roadmap
    node_skills: List[str] = [
        skill
        for phase in roadmap.get("phases", [])
        for node in phase.get("nodes", [])
        for skill in (node.get("skills") or [])
    ]

    top_skills_counts = Counter(node_skills).most_common(6)
    top_skills = [s for s, _ in top_skills_counts]
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

    # Competency Gains Grid
    gains_cols = st.columns(3)
    for idx, skill in enumerate(top_skills[:3]):
        gain = (current_vals[idx] - base_vals[idx]) / 10.0
        with gains_cols[idx]:
            st.markdown(f"""
            <div style="background:#FFFFFF; border:1px solid #DDDCD6; border-radius:6px; padding:10px 14px; margin-bottom:12px;">
                <div style="font-size:11px; color:#858585; text-transform:uppercase; font-weight:600; letter-spacing:0.04em;">{html.escape(skill)}</div>
                <div style="font-size:16px; font-weight:650; color:{'#2F7D5A' if gain > 0 else '#111111'};">
                    +{gain:.1f} pts
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Polar Chart
    theta_loop = top_skills + [top_skills[0]]
    base_loop = base_vals + [base_vals[0]]
    curr_loop = current_vals + [current_vals[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=base_loop,
        theta=theta_loop,
        fill="toself",
        name="Baseline",
        line_color="#858585",
        fillcolor="rgba(133, 133, 133, 0.08)",
        line=dict(width=1.5, dash="dot")
    ))

    fig.add_trace(go.Scatterpolar(
        r=curr_loop,
        theta=theta_loop,
        fill="toself",
        name="Current Position",
        line_color="#2457D6",
        fillcolor="rgba(36, 87, 214, 0.12)",
        line=dict(width=2.5)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#858585", size=9),
                gridcolor="#EAE9E4",
                linecolor="#EAE9E4"
            ),
            angularaxis=dict(
                tickfont=dict(color="#111111", size=11, family="Inter"),
                gridcolor="#EAE9E4",
                linecolor="#EAE9E4"
            ),
            bgcolor="#FFFFFF"
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(color="#111111", size=11)
        ),
        margin=dict(l=24, r=24, t=14, b=24),
        height=260
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
