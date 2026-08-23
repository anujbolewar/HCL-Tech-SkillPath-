"""Editorial presentation components for PathFinder AI.

Includes:
- 52px Compact Header with minimal SVG connected-nodes mark.
- Signature Skill Position track visualization (Current ●━━┆━━● Target).
- Next Best Action card with numbered badge and cobalt indicator.
- Product-level Path Updated event notification with [View updated path →] action.
- Realistic Skill Check diagnostic assessment.
- Module Inspector with Explainable AI multi-factor breakdown.
"""

import html
from typing import Dict, Any, Set, List, Optional
import streamlit as st

from core.config import APP_TITLE, TEAM_NAME
from engine.re_router import find_next_recommended_action, apply_diagnostic_assessment
from core.state import persist_state

def clean_html(raw_html: str) -> str:
    """Removes leading line indents from raw multiline HTML string so Streamlit does not parse as code block."""
    lines = [line.strip() for line in raw_html.strip().split("\n")]
    return "".join(lines)


def render_app_header(role_title: str) -> None:
    """Renders the compact 52px header with minimal SVG path mark and vertical alignment."""
    escaped_role = html.escape(role_title)
    header_html = f"""
    <div class="pf-header">
        <div class="pf-header-left">
            <span class="pf-logo-mark">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="5" cy="18" r="3" fill="#2457D6"/>
                    <circle cx="12" cy="6" r="3" fill="#111111"/>
                    <circle cx="19" cy="14" r="3" fill="#2F7D5A"/>
                    <path d="M7 16L10 8M14 8L17 12" stroke="#DDDCD6" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
            </span>
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
    """Renders PathFinder's signature horizontal Current ●━━┆━━● Target skill tracks."""
    known_skills = list(profile.get("skills", ["Python", "SQL", "Basic Math"]))
    hours = profile.get("weekly_hours", 15)
    level = profile.get("experience_level", "Intermediate")

    all_roadmap_skills = []
    for phase in roadmap.get("phases", []):
        for node in phase.get("nodes", []):
            for skill in node.get("skills", []):
                clean_name = "Matrix Decomposition" if "Matrix" in skill else skill
                if clean_name not in all_roadmap_skills and clean_name not in known_skills:
                    all_roadmap_skills.append(clean_name)

    target_gaps = all_roadmap_skills[:4] if all_roadmap_skills else ["Linear Algebra", "Multivariate Calculus", "Matrix Decomposition", "NumPy"]

    # Baseline rows HTML
    baseline_rows = []
    for skill in known_skills[:3]:
        escaped_s = html.escape(skill)
        baseline_rows.append(f"""
        <div class="pf-track-item">
            <span class="pf-track-name">{escaped_s}</span>
            <div class="pf-track-rail-wrap">
                <div class="pf-track-rail">
                    <div class="pf-track-current-fill" style="width: 80%;"></div>
                    <div class="pf-track-current-dot" style="left: 80%;"></div>
                    <div class="pf-track-target-dot" style="right: 20%;"></div>
                </div>
            </div>
            <span class="pf-track-value pf-badge-mastered">8/10 · Mastered</span>
        </div>
        """)

    # Target gap rows HTML
    gap_rows = []
    for gap in target_gaps:
        escaped_g = html.escape(gap)
        gap_rows.append(f"""
        <div class="pf-track-item">
            <span class="pf-track-name">{escaped_g}</span>
            <div class="pf-track-rail-wrap">
                <div class="pf-track-rail">
                    <div class="pf-track-current-fill" style="width: 20%;"></div>
                    <div class="pf-track-gap-fill" style="left: 20%; width: 60%;"></div>
                    <div class="pf-track-current-dot" style="left: 20%;"></div>
                    <div class="pf-track-target-dot" style="right: 20%;"></div>
                </div>
            </div>
            <span class="pf-track-value"><span class="pf-badge-gap">Gap · 2/10</span></span>
        </div>
        """)

    section_html = f"""
    <div class="pf-card">
        <div class="pf-section-header">
            <span class="pf-section-title">Skill Position</span>
            <span class="pf-section-caption">Paced for <strong>{hours} hrs/week</strong> ({level})</span>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1.1fr; gap: 28px;">
            <div>
                <div style="font-size:10.5px; font-weight:650; text-transform:uppercase; color:#858585; letter-spacing:0.06em; margin-bottom:10px;">
                    Current Baseline
                </div>
                <div class="pf-track-container">
                    {''.join(baseline_rows)}
                </div>
            </div>
            <div>
                <div style="font-size:10.5px; font-weight:650; text-transform:uppercase; color:#858585; letter-spacing:0.06em; margin-bottom:10px;">
                    Target Competencies & Gaps
                </div>
                <div class="pf-track-container">
                    {''.join(gap_rows)}
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
        <div class="pf-card" style="text-align:center; padding:28px 18px;">
            <div style="font-size:10.5px; font-weight:650; text-transform:uppercase; letter-spacing:0.08em; color:#2F7D5A; margin-bottom:4px;">All Milestones Mastered</div>
            <div style="font-size:15px; font-weight:600; color:#111111; margin-bottom:4px;">You have completed all prerequisite milestones for this roadmap!</div>
            <div style="font-size:12.5px; color:#4B4B4B;">Review your completed projects in the Learning Path tab or consult PathFinder Mentor for advanced specialization.</div>
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
    why_text = html.escape(next_node.get("why", "Highest-leverage prerequisite for your target path."))
    skills_list = next_node.get("skills", ["Core Concept"])
    skills_str = " · ".join(html.escape(s) for s in skills_list)

    col_info, col_btn = st.columns([3.8, 1.2], vertical_alignment="center")

    with col_info:
        card_html = f"""
        <div class="pf-next-card">
            <div class="pf-next-header-row">
                <span class="pf-next-step-badge">
                    <span class="pf-num">01</span> NEXT BEST ACTION
                </span>
                <span class="pf-next-duration">{duration} · 15 hours</span>
            </div>
            <div class="pf-next-title">{node_id}: {title}</div>
            <div class="pf-next-provider">{n_type} · <strong>{provider}</strong> · {html.escape(phase_name)}</div>
            <div class="pf-next-gaps-block">
                <strong>Closes:</strong> {skills_str}
            </div>
            <div class="pf-next-why-box">
                <strong>WHY NOW:</strong> {why_text}
            </div>
        </div>
        """
        st.markdown(clean_html(card_html), unsafe_allow_html=True)

    with col_btn:
        if st.button("Start module →", key=f"nba_start_{node_id}", type="primary", use_container_width=True):
            completed_nodes.add(node_id)
            st.session_state["_last_completed_title"] = next_node.get('title')
            st.session_state["_show_replan_banner"] = True
            persist_state()
            st.rerun()


def render_roadmap_updated_banner(adaptation_event: Dict[str, Any]) -> None:
    """Renders the concise, outcome-oriented product-level Path Updated event."""
    if not adaptation_event or not adaptation_event.get("adapted"):
        return

    skill = html.escape(adaptation_event.get("skill_topic", "Retrieval & Vector Search"))
    score = adaptation_event.get("score", 42)
    
    inserted_raw = adaptation_event.get("inserted_nodes", [])
    inserted_items_html = []
    if isinstance(inserted_raw, list):
        for idx, n in enumerate(inserted_raw):
            n_title = html.escape(n.get("title", "")) if isinstance(n, dict) else html.escape(str(n))
            num_str = f"0{idx+1}"
            inserted_items_html.append(f"<div style='margin-bottom:3px;'><strong>{num_str}</strong> &nbsp;{n_title}</div>")
    
    inserted_content = "".join(inserted_items_html) if inserted_items_html else "<div>01 &nbsp;Retrieval Fundamentals<br/>02 &nbsp;Vector Search Practice</div>"

    banner_html = f"""
    <div class="pf-notification">
        <div class="pf-notif-tag">Path Updated</div>
        <div class="pf-notif-body">
            <div style="font-size:13.5px; font-weight:600; color:#111111; margin-bottom:2px;">
                {skill}
            </div>
            <div style="font-size:12px; color:#858585; margin-bottom:8px;">
                Assessment score: {score}%
            </div>
            <div style="font-size:11px; font-weight:650; text-transform:uppercase; letter-spacing:0.06em; color:#858585; margin-bottom:4px;">
                Added to your path
            </div>
            <div style="font-size:12.5px; color:#111111; margin-bottom:8px; line-height:1.45;">
                {inserted_content}
            </div>
            <div style="font-size:12px; color:#5F5F5F; margin-bottom:8px;">
                These prerequisites were added before your next RAG evaluation milestone.
            </div>
        </div>
    </div>
    """
    st.markdown(clean_html(banner_html), unsafe_allow_html=True)


def render_diagnostic_assessment_widget(roadmap: Dict[str, Any], profile: Dict[str, Any]) -> None:
    """Renders a realistic multiple-choice skill check with instant adaptation demo."""
    with st.expander("Skill Check & Diagnostic Assessment", expanded=False):
        st.markdown("""
        <div style="font-size:10.5px; font-weight:650; text-transform:uppercase; letter-spacing:0.08em; color:#858585; margin-bottom:3px;">
            Skill Check · Retrieval & Vector Search
        </div>
        <div style="font-size:12.5px; color:#4B4B4B; margin-bottom:12px;">
            Test your current mastery to verify prerequisites and automatically tailor your roadmap.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:13px; font-weight:550; color:#111111; margin-bottom:8px;">
            Question 1 of 3: Which retrieval strategy is most appropriate when semantic similarity alone misses exact technical identifiers or SKU codes?
        </div>
        """, unsafe_allow_html=True)

        options = [
            "A. Standard cosine similarity over Dense Embeddings (All-MiniLM-L6-v2)",
            "B. Hybrid Search combining dense vector cosine similarity with Sparse BM25 keyword matching",
            "C. Increasing chunk overlap size to 80% without modifying vector index",
            "D. Using single-token sliding window embedding without re-ranking"
        ]

        selected_option = st.radio(
            "Diagnostic Question",
            options=options,
            index=0,
            label_visibility="collapsed",
            key="diag_mcq_radio"
        )

        if st.button("Submit Assessment", type="primary", use_container_width=True, key="diag_submit_btn"):
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


def render_node_inspector(node: Dict[str, Any], score: int, breakdown: List[str]) -> None:
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
        <div style="font-size:10.5px; font-weight:650; text-transform:uppercase; letter-spacing:0.08em; color:#2457D6; margin-bottom:3px;">
            Milestone Inspector
        </div>
        <div style="font-size:15px; font-weight:650; color:#111111; margin-bottom:2px;">{node_id}: {title}</div>
        <div style="font-size:12px; color:#4B4B4B; margin-bottom:10px;">{n_type} · {provider} · {duration}</div>
        
        <div style="border-top:1px solid #EAE9E4; padding-top:8px; margin-bottom:8px; font-size:12px; line-height:1.45;">
            <div style="color:#858585; font-size:10.5px; font-weight:600; text-transform:uppercase; margin-bottom:2px;">Prerequisites</div>
            <div style="color:#111111; font-weight:500;">{prereq_str}</div>
        </div>

        <div style="border-top:1px solid #EAE9E4; padding-top:8px; margin-bottom:10px; font-size:12px; line-height:1.45;">
            <div style="color:#858585; font-size:10.5px; font-weight:600; text-transform:uppercase; margin-bottom:2px;">Target Competencies</div>
            <div style="color:#111111;">{skills_str}</div>
        </div>

        <div style="background:#F7F6F2; border:1px solid #DDDCD6; border-radius:5px; padding:8px 10px; font-size:11.5px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <span style="font-weight:600; color:#111111;">AI Relevance Score</span>
                <strong style="color:#2457D6; font-size:12.5px;">{score}/100</strong>
            </div>
            <div style="color:#4B4B4B; font-size:11px; line-height:1.45;">
                {'<br/>'.join(html.escape(item) for item in breakdown) if isinstance(breakdown, list) else html.escape(str(breakdown))}
            </div>
        </div>
    </div>
    """
    st.markdown(clean_html(inspector_html), unsafe_allow_html=True)
