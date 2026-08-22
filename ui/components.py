"""Presentation components for PathFinder AI with restrained typography and spatial discipline."""

from typing import Dict, Any, List, Set, Optional, Tuple
import streamlit as st

from core.config import APP_TITLE, TEAM_NAME
from engine.re_router import (
    calculate_progress_stats,
    get_node_status,
    find_next_recommended_action,
    apply_diagnostic_assessment,
)

def clean_html(html_str: str) -> str:
    """Strips all leading and trailing whitespace from each line to prevent Markdown codeblock parsing."""
    return "\n".join([line.strip() for line in html_str.strip().splitlines()])


def render_app_header(role_title: str = "Personalized Curriculum") -> None:
    """Renders a compact, professional application header (56px tall) in clean light mode."""
    raw_html = f"""
    <div class="app-header">
        <div class="app-brand">
            PathFinder <span class="ai-tag">AI</span>
            <span class="app-badge">{role_title}</span>
        </div>
        <div class="app-meta">
            <strong>Cortex</strong> · HCL Tech Hackathon
        </div>
    </div>
    """
    st.markdown(clean_html(raw_html), unsafe_allow_html=True)


def render_skill_gap_section(roadmap: Dict[str, Any], profile: Dict[str, Any]) -> None:
    """Renders the explicit 'Where I Am vs Where I Need To Be' skill gap comparison in editorial format."""
    known_skills = list(set(profile.get("skills") or []))
    
    # Collect all skills targeted across the roadmap
    target_skills = []
    for phase in roadmap.get("phases", []):
        for node in phase.get("nodes", []):
            for s in (node.get("skills") or []):
                if s not in target_skills:
                    target_skills.append(s)

    identified_gaps = [s for s in target_skills if s not in known_skills]

    # Baseline rows with neutral gray bars
    baseline_items = []
    if known_skills:
        for s in known_skills[:4]:
            baseline_items.append(f"""
            <div style="margin-bottom: 12px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:13px;">
                    <span style="color:#171717; font-weight:500;">{s}</span>
                    <span style="color:#15803D; font-weight:500; font-size:12px;">8/10 · Mastered</span>
                </div>
                <div style="background:#F1F2F0; border-radius:4px; height:6px; width:100%; overflow:hidden;">
                    <div style="background:#8A8A8A; width:80%; height:100%; border-radius:4px;"></div>
                </div>
            </div>
            """)
        baseline_html = "".join(baseline_items)
    else:
        baseline_html = "<div style='color:#8A8A8A; font-size:13px; padding: 8px 0;'>No baseline skills declared (Foundational beginner).</div>"

    # Gaps rows with blue accent target bars
    gaps_items = []
    if identified_gaps:
        for s in identified_gaps[:4]:
            gaps_items.append(f"""
            <div style="margin-bottom: 12px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:13px;">
                    <span style="color:#171717; font-weight:500;">{s}</span>
                    <span style="color:#2563EB; font-weight:500; font-size:12px;">Target (2/10)</span>
                </div>
                <div style="background:#F1F2F0; border-radius:4px; height:6px; width:100%; overflow:hidden;">
                    <div style="background:#2563EB; width:20%; height:100%; border-radius:4px;"></div>
                </div>
            </div>
            """)
        gaps_html = "".join(gaps_items)
    else:
        gaps_html = "<div style='color:#8A8A8A; font-size:13px; padding: 8px 0;'>All targeted competencies match your baseline profile.</div>"

    hours = profile.get('weekly_hours', 15)
    exp = profile.get('experience_level', 'Intermediate')

    card_html = f"""
    <div class="content-card">
        <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:14px; border-bottom:1px solid #E5E5E2; padding-bottom:8px;">
            <span class="card-header-label" style="margin-bottom:0;">
                Skill Gap Analysis
            </span>
            <span style="font-size:12px; color:#666666;">
                Paced for <strong>{hours} hrs/week</strong> ({exp})
            </span>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 32px;">
            <div>
                <div style="font-size:12px; font-weight:600; color:#8A8A8A; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:10px;">
                    Current Baseline
                </div>
                {baseline_html}
            </div>
            <div>
                <div style="font-size:12px; font-weight:600; color:#8A8A8A; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:10px;">
                    Target Competencies & Gaps
                </div>
                {gaps_html}
            </div>
        </div>
    </div>
    """
    st.markdown(clean_html(card_html), unsafe_allow_html=True)


def render_roadmap_updated_banner(adaptation_event: Dict[str, Any]) -> None:
    """Renders the clean, restrained 'PATH UPDATED' inline change summary."""
    if not adaptation_event or not adaptation_event.get("adapted"):
        return

    skill = adaptation_event.get("skill_topic", "Retrieval & Vector Search")
    score = adaptation_event.get("score", 42)
    inserted = adaptation_event.get("inserted_nodes", [])
    impacted = adaptation_event.get("impacted_node", "Capstone Project")

    inserted_items = "".join([
        f"<div style='margin-bottom:4px;'><strong style='color:#171717;'>{n.get('id')}: {n.get('title')}</strong> <span style='color:#666666;'>({n.get('duration', '1 week')})</span></div>"
        for n in inserted
    ])

    banner_html = f"""
    <div class="path-updated-banner">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span class="path-updated-title">Path Updated</span>
            <span class="status-tag status-active">Assessment Score: {score}%</span>
        </div>
        <div style="font-size:13.5px; color:#171717; margin-bottom:10px; line-height:1.5;">
            Your diagnostic check identified a prerequisite gap in <strong>{skill}</strong>. PathFinder dynamically updated your learning sequence with foundational coursework:
        </div>
        <div style="background:#FFFFFF; border:1px solid #BFDBFE; border-radius:6px; padding:10px 14px; margin-bottom:8px; font-size:13px;">
            <div style="font-size:11px; font-weight:600; text-transform:uppercase; color:#2563EB; margin-bottom:6px; letter-spacing:0.03em;">Added to your path:</div>
            {inserted_items}
        </div>
        <div style="font-size:12px; color:#1E3A8A;">
            These newly inserted modules now unlock <strong>{impacted}</strong>.
        </div>
    </div>
    """
    st.markdown(clean_html(banner_html), unsafe_allow_html=True)


def render_diagnostic_assessment_widget(roadmap: Dict[str, Any], profile: Dict[str, Any]) -> None:
    """Renders a realistic Skill Check assessment experience to test the adaptive learning loop."""
    from core.state import persist_state

    with st.expander("Skill Check & Diagnostic Assessment", expanded=False):
        st.markdown(
            "<div style='font-size:13px; color:#666666; margin-bottom:12px;'>"
            "Assess your competency in key domain prerequisites. If a foundational weakness is detected, "
            "PathFinder automatically re-sequences your learning path."
            "</div>",
            unsafe_allow_html=True
        )

        q_col1, q_col2 = st.columns([1.8, 1], vertical_alignment="top")
        with q_col1:
            quiz_topic = st.selectbox(
                "Skill Domain:",
                ["Retrieval & Vector Search", "Model Evaluation & Metrics", "Production FastAPI & Docker"],
                index=0
            )

            st.markdown(
                f"<div style='background:#F7F7F5; border:1px solid #E5E5E2; border-radius:6px; padding:12px 14px; margin: 10px 0; font-size:13px; color:#171717;'>"
                f"<strong>Scenario Question (1 of 3):</strong><br>"
                f"In semantic search with dense vector embeddings, what primary failure occurs when chunk sizes are too large (>2000 tokens)?"
                f"</div>",
                unsafe_allow_html=True
            )

            selected_answer = st.radio(
                "Select response:",
                [
                    "A. Embedding vectors dilute specific factual nuances into broad centroid averages.",
                    "B. Cosine similarity calculations crash due to matrix dimensionality limits.",
                    "C. Tokenizers reject documents with more than 512 total characters."
                ],
                index=0,
                label_visibility="collapsed"
            )

        with q_col2:
            st.markdown("<div style='font-size:12px; font-weight:600; color:#8A8A8A; text-transform:uppercase; margin-bottom:6px;'>Diagnostic Evaluation Mode</div>", unsafe_allow_html=True)
            mode_choice = st.radio(
                "Simulated Test Outcome:",
                ["Detect Weakness (Score: 42%)", "Demonstrate Mastery (Score: 88%)"],
                index=0,
                help="Select score profile to test PathFinder's adaptive re-planning loop"
            )
            simulated_score = 42 if "42%" in mode_choice else 88

            st.markdown("<div style='margin-top:14px;'>", unsafe_allow_html=True)
            btn_run_quiz = st.button("Submit Assessment", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if btn_run_quiz:
            with st.spinner("Analyzing knowledge boundaries and updating learning tree..."):
                updated_roadmap, adapt_event = apply_diagnostic_assessment(
                    roadmap=roadmap,
                    skill_topic=quiz_topic,
                    score=simulated_score,
                    profile=profile
                )
                st.session_state.roadmap_data = updated_roadmap
                if adapt_event:
                    st.session_state.adaptation_event = adapt_event
                    if adapt_event.get("adapted"):
                        st.toast("Assessment complete: Learning path adapted with remedial modules.", icon="ℹ️")
                    else:
                        st.toast("Assessment passed: Standard trajectory confirmed.", icon="✅")
                persist_state()
                st.rerun()


def render_next_best_action_card(roadmap: Dict[str, Any], completed_nodes: Set[str]) -> None:
    """Renders the clean, restrained 'Next Up' learning action block."""
    next_action_res = find_next_recommended_action(roadmap, completed_nodes)

    if next_action_res:
        next_node, next_phase = next_action_res
        n_id = next_node.get('id', '')
        n_title = next_node.get('title', '')
        n_dur = next_node.get('duration', '2 weeks')
        n_type = next_node.get('type', 'Course')
        n_prov = next_node.get('provider', 'Online')
        n_why = next_node.get('why', 'Prerequisites are unlocked. Completing this milestone directly closes an identified skill gap.')
        skills_closed = " · ".join(next_node.get("skills", ["Core Foundation"]))

        card_html = f"""
        <div class="next-action-card">
            <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:4px;">
                <div class="next-action-badge">Next Up</div>
                <span class="status-tag status-active">{n_dur}</span>
            </div>
            <div class="next-action-title">{n_id}: {n_title}</div>
            <div class="next-action-meta">
                {n_type} · <strong>{n_prov}</strong> · {next_phase}
            </div>
            <div style="font-size:12px; color:#666666; margin-bottom:8px;">
                <strong>Closes skill gaps in:</strong> {skills_closed}
            </div>
            <div class="next-action-why">
                <strong>Why this milestone now:</strong> {n_why}
            </div>
        </div>
        """
        st.markdown(clean_html(card_html), unsafe_allow_html=True)
    else:
        completed_html = """
        <div class="next-action-card" style="border-left-color:#15803D;">
            <div class="next-action-badge" style="color:#15803D;">Curriculum Completed</div>
            <div class="next-action-title">All Milestones Mastered</div>
            <div class="next-action-meta">You have completed all prerequisite pathways in this personalized curriculum.</div>
        </div>
        """
        st.markdown(clean_html(completed_html), unsafe_allow_html=True)


def render_node_inspector(node: Dict[str, Any], score: int, breakdown: List[str]) -> None:
    """Renders a clean module rationale inspector in editorial light mode."""
    prereqs_str = ", ".join(node.get("prereqs", [])) if node.get("prereqs") else "None (Entry Point)"
    skills_str = " · ".join(node.get("skills", ["General"]))
    n_id = node.get('id', '')
    n_title = node.get('title', '')
    n_prov = node.get('provider', 'Online')
    n_dur = node.get('duration', '2 weeks')
    n_why = node.get('why', 'Key required competency.')

    inspector_html = f"""
    <div class="node-inspector-box">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; border-bottom:1px solid #E5E5E2; padding-bottom:6px;">
            <strong style="font-size:14px; color:#171717;">
                {n_id}: {n_title}
            </strong>
            <span class="status-tag status-active">{score}% Match</span>
        </div>
        <div style="font-size:12.5px; color:#666666; margin-bottom:6px;">
            <strong>Provider:</strong> {n_prov} · {n_dur}
        </div>
        <div style="font-size:12.5px; color:#666666; margin-bottom:8px;">
            <strong>Prerequisites:</strong> <span style="color:#171717;">{prereqs_str}</span>
        </div>
        <div style="font-size:13px; color:#404040; line-height:1.45; margin-bottom:8px; background:#F7F7F5; padding:8px 10px; border-radius:6px; border:1px solid #E5E5E2;">
            <strong>Why This Module:</strong> {n_why}
        </div>
        <div style="font-size:12px; color:#8A8A8A;">
            <strong>Competencies:</strong> {skills_str}
        </div>
    </div>
    """
    st.markdown(clean_html(inspector_html), unsafe_allow_html=True)
