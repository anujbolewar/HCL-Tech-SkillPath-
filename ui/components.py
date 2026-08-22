"""Editorial, restrained UI presentation components for PathFinder AI."""

import html
from typing import Dict, Any, List, Set, Optional
import streamlit as st

from core.config import TEAM_NAME
from engine.re_router import (
    find_next_recommended_action,
    apply_diagnostic_assessment,
    get_node_status
)
from core.state import persist_state

def clean_html(raw_html: str) -> str:
    """Removes indentation and excess newlines from raw HTML strings."""
    return "".join(line.strip() for line in raw_html.strip().splitlines())

def render_app_header(role_title: str = "AI & ML Engineer") -> None:
    """Renders the editorial 56px application header with minimal SVG path mark."""
    escaped_role = html.escape(role_title)
    
    # PathFinder minimal connected-nodes path mark
    path_mark_svg = """
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="5" cy="18" r="3" fill="#2457D6"/>
        <circle cx="12" cy="6" r="3" fill="#111111"/>
        <circle cx="19" cy="14" r="3" fill="#2F7D5A"/>
        <path d="M7 16L10 8M14 8L17 12" stroke="#DDDCD6" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
    """
    
    header_html = f"""
    <div class="pf-header">
        <div class="pf-header-left">
            <div class="pf-logo-mark">{path_mark_svg}</div>
            <span class="pf-logo-text">PathFinder</span>
            <span class="pf-logo-sub">AI</span>
        </div>
        <div class="pf-header-center">
            <span style="color:#858585; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.06em;">Goal:</span>
            <strong style="color:#111111; font-weight:600;">{escaped_role}</strong>
        </div>
        <div class="pf-header-right">
            <span>Team <strong>{TEAM_NAME}</strong> · Round 2</span>
        </div>
    </div>
    """
    st.markdown(clean_html(header_html), unsafe_allow_html=True)


def render_skill_gap_section(roadmap: Dict[str, Any], profile: Dict[str, Any]) -> None:
    """Renders the signature Current → Target competency track visualization."""
    known_skills = list(profile.get("skills", ["Python", "SQL", "Basic Math"]))
    hours = profile.get("weekly_hours", 15)
    level = profile.get("experience_level", "Intermediate")

    all_roadmap_skills = []
    for phase in roadmap.get("phases", []):
        for node in phase.get("nodes", []):
            for skill in node.get("skills", []):
                if skill not in all_roadmap_skills and skill not in known_skills:
                    all_roadmap_skills.append(skill)

    target_gaps = all_roadmap_skills[:4] if all_roadmap_skills else ["Linear Algebra", "Multivariate Calculus", "Matrix Decompositions", "NumPy"]

    section_html = f"""
    <div class="pf-card">
        <div class="pf-section-header">
            <span class="pf-section-title">Skill Position</span>
            <span class="pf-section-caption">Paced for <strong>{hours} hrs/week</strong> ({level})</span>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 32px;">
            <div>
                <div style="font-size:11px; font-weight:600; text-transform:uppercase; color:#858585; letter-spacing:0.06em; margin-bottom:14px;">
                    Current Baseline
                </div>
                <div class="pf-track-container">
                    {''.join(f'''
                    <div class="pf-track-item">
                        <span class="pf-track-name">{html.escape(skill)}</span>
                        <div class="pf-track-bar-bg">
                            <div class="pf-track-bar-target" style="width: 80%;"></div>
                            <div class="pf-track-bar-current" style="width: 80%;"></div>
                        </div>
                        <span class="pf-track-value pf-badge-mastered">8/10 · Mastered</span>
                    </div>
                    ''' for skill in known_skills[:4])}
                </div>
            </div>
            <div>
                <div style="font-size:11px; font-weight:600; text-transform:uppercase; color:#858585; letter-spacing:0.06em; margin-bottom:14px;">
                    Target Competencies & Gaps
                </div>
                <div class="pf-track-container">
                    {''.join(f'''
                    <div class="pf-track-item">
                        <span class="pf-track-name">{html.escape(gap)}</span>
                        <div class="pf-track-bar-bg">
                            <div class="pf-track-bar-target" style="width: 80%;"></div>
                            <div class="pf-track-bar-current is-gap" style="width: 20%;"></div>
                        </div>
                        <span class="pf-track-value"><span class="pf-badge-gap">Gap · 2/10</span></span>
                    </div>
                    ''' for gap in target_gaps)}
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(clean_html(section_html), unsafe_allow_html=True)


def render_next_best_action_card(roadmap: Dict[str, Any], completed_nodes: Set[str]) -> None:
    """Renders the signature NEXT BEST ACTION card with cobalt path indicator."""
    next_res = find_next_recommended_action(roadmap, completed_nodes)

    if not next_res:
        done_html = """
        <div class="pf-card" style="text-align:center; padding:32px 20px;">
            <div style="font-size:11px; font-weight:650; text-transform:uppercase; letter-spacing:0.08em; color:#2F7D5A; margin-bottom:6px;">All Milestones Mastered</div>
            <div style="font-size:16px; font-weight:600; color:#111111; margin-bottom:6px;">You have completed all prerequisite milestones for this roadmap!</div>
            <div style="font-size:13px; color:#4B4B4B;">Review your completed projects in the Learning Path tab or consult PathFinder Mentor for advanced specialization.</div>
        </div>
        """
        st.markdown(clean_html(done_html), unsafe_allow_html=True)
        return

    next_node, phase_name = next_res
    node_id = next_node.get("id", "01")
    title = html.escape(next_node.get("title", "Next Action"))
    provider = html.escape(next_node.get("provider", "Curated Source"))
    duration = html.escape(next_node.get("duration", "2 weeks"))
    n_type = html.escape(next_node.get("type", "Course"))
    why_text = html.escape(next_node.get("why", "Critical path milestone for closing fundamental prerequisites."))
    skills_list = next_node.get("skills", ["Core Concept"])
    skills_str = " · ".join(html.escape(s) for s in skills_list)

    card_html = f"""
    <div class="pf-next-card">
        <div class="pf-next-header-row">
            <div class="pf-next-step-badge">
                <span class="pf-num">01</span>
                <span>Next Best Action</span>
            </div>
            <span class="pf-next-duration">{duration} · 15 hours</span>
        </div>
        <div class="pf-next-title">{node_id}: {title}</div>
        <div class="pf-next-provider">{n_type} · <strong>{provider}</strong> · {phase_name}</div>
        <div class="pf-next-gaps-block">
            <strong>Closes identified gaps:</strong> {skills_str}
        </div>
        <div class="pf-next-why-box">
            <strong>Why now:</strong> {why_text}
        </div>
    </div>
    """
    st.markdown(clean_html(card_html), unsafe_allow_html=True)


def render_roadmap_updated_banner(adaptation_event: Dict[str, Any]) -> None:
    """Renders the restrained editorial notification when adaptive replanning triggers."""
    if not adaptation_event or not adaptation_event.get("adapted"):
        return

    skill = html.escape(adaptation_event.get("skill_topic", "Domain Skill"))
    score = adaptation_event.get("score", 45)
    
    inserted_raw = adaptation_event.get("inserted_nodes", [])
    if isinstance(inserted_raw, list):
        inserted_names = [
            f"{n['id']}: {n['title']}" if isinstance(n, dict) else str(n)
            for n in inserted_raw
        ]
        inserted = html.escape(", ".join(inserted_names))
    else:
        inserted = html.escape(str(inserted_raw))
        
    reason = html.escape(adaptation_event.get("reason", "Assessment score identified prerequisite gaps."))

    banner_html = f"""
    <div class="pf-notification">
        <div class="pf-notif-tag">Path Updated</div>
        <div class="pf-notif-body">
            Your assessment identified a weakness in <strong>{skill}</strong> ({score}% score).<br/>
            <strong>Added to path:</strong> {inserted}<br/>
            <strong>Reason:</strong> {reason}
        </div>
    </div>
    """
    st.markdown(clean_html(banner_html), unsafe_allow_html=True)


def render_diagnostic_assessment_widget(roadmap: Dict[str, Any], profile: Dict[str, Any]) -> None:
    """Renders a realistic multiple-choice skill check with instant adaptation demo."""
    with st.expander("Skill Check & Diagnostic Assessment", expanded=False):
        st.markdown("""
        <div style="font-size:11px; font-weight:650; text-transform:uppercase; letter-spacing:0.08em; color:#858585; margin-bottom:4px;">
            Skill Check · Retrieval & Vector Search
        </div>
        <div style="font-size:13px; color:#4B4B4B; margin-bottom:14px;">
            Test your current mastery to let PathFinder dynamically verify prerequisites and tailor your roadmap.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Question 1 of 3:** Which retrieval strategy is most appropriate when semantic similarity alone misses exact technical identifiers or SKU codes?")

        selected_option = st.radio(
            "Select Answer:",
            [
                "A. Standard cosine similarity over Dense Embeddings (All-MiniLM-L6-v2)",
                "B. Hybrid Search combining dense vector cosine similarity with Sparse BM25 keyword matching",
                "C. Increasing chunk overlap size to 80% without modifying vector index",
                "D. Using single-token sliding window embedding without re-ranking"
            ],
            index=0,
            label_visibility="collapsed"
        )

        col_submit, col_demo = st.columns([1.5, 2.5], vertical_alignment="center")
        with col_submit:
            submit_quiz = st.button("Submit Assessment", type="primary", use_container_width=True)

        if submit_quiz:
            # If user picks B (correct), score is 90%. If user picks A/C/D, score is 42% (weakness triggers adaptation)
            is_correct = selected_option.startswith("B.")
            simulated_score = 90 if is_correct else 42
            
            with st.spinner("Evaluating response against competency model..."):
                updated_roadmap, event = apply_diagnostic_assessment(
                    st.session_state.roadmap_data,
                    skill_topic="Retrieval & Vector Search",
                    score=simulated_score
                )
                
                st.session_state.roadmap_data = updated_roadmap
                st.session_state.adaptation_event = event
                
                if event and event.get("adapted"):
                    st.session_state.completed_nodes = st.session_state.completed_nodes - {"AI302", "REM101", "REM102"}
                
                persist_state()
                st.rerun()


def render_node_inspector(node: Dict[str, Any], score: int, breakdown: Dict[str, Any]) -> None:
    """Renders the side-by-side node inspector with Explainable AI scoring breakdown."""
    node_id = html.escape(node.get("id", ""))
    title = html.escape(node.get("title", ""))
    provider = html.escape(node.get("provider", "Online Provider"))
    duration = html.escape(node.get("duration", "2 weeks"))
    n_type = html.escape(node.get("type", "Course"))
    prereqs = node.get("prereqs", [])
    skills = node.get("skills", [])

    prereq_str = ", ".join(html.escape(p) for p in prereqs) if prereqs else "None (Entry milestone)"
    skills_str = " · ".join(html.escape(s) for s in skills)

    inspector_html = f"""
    <div class="pf-inspector">
        <div style="font-size:11px; font-weight:650; text-transform:uppercase; letter-spacing:0.08em; color:#2457D6; margin-bottom:4px;">
            Milestone Inspector
        </div>
        <div style="font-size:16px; font-weight:650; color:#111111; margin-bottom:4px;">{node_id}: {title}</div>
        <div style="font-size:12.5px; color:#4B4B4B; margin-bottom:12px;">{n_type} · {provider} · {duration}</div>
        
        <div style="border-top:1px solid #EAE9E4; padding-top:10px; margin-bottom:10px; font-size:12.5px; line-height:1.5;">
            <div style="color:#858585; font-size:11px; font-weight:600; text-transform:uppercase; margin-bottom:2px;">Prerequisites</div>
            <div style="color:#111111; font-weight:500;">{prereq_str}</div>
        </div>

        <div style="border-top:1px solid #EAE9E4; padding-top:10px; margin-bottom:12px; font-size:12.5px; line-height:1.5;">
            <div style="color:#858585; font-size:11px; font-weight:600; text-transform:uppercase; margin-bottom:2px;">Target Competencies</div>
            <div style="color:#111111;">{skills_str}</div>
        </div>

        <div style="background:#F7F6F2; border:1px solid #DDDCD6; border-radius:6px; padding:10px 12px; font-size:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-weight:600; color:#111111;">AI Relevance Score</span>
                <strong style="color:#2457D6; font-size:13px;">{score}/100</strong>
            </div>
            <div style="color:#4B4B4B; font-size:11.5px; line-height:1.45;">
                {'<br/>'.join(html.escape(item) for item in breakdown) if isinstance(breakdown, list) else html.escape(str(breakdown))}
            </div>
        </div>
    </div>
    """
    st.markdown(clean_html(inspector_html), unsafe_allow_html=True)
