"""PathFinder AI — Editorial Learning Navigation & Intelligence System.

Developed by Team Cortex for HCL Tech Hackathon (Round 2).
Restrained, editorial light-mode learning platform prioritizing the core learner journey:
GOAL → CURRENT SKILLS → SKILL GAPS → ROADMAP → NEXT BEST ACTION → ADAPTIVE REPLANNING.
"""

import os
import json
import html
from pathlib import Path
from typing import Dict, Any, Set, Tuple, List, Optional
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Core modules
from core.config import (
    APP_TITLE,
    APP_SUBTITLE,
    TEAM_NAME,
    TEAM_MEMBERS,
    DEFAULT_PROFILE,
    QUICK_PICKS,
    DEMO_PERSONAS,
    GROQ_MODEL_CATALOG,
    GEMINI_MODEL_CATALOG,
    DEFAULT_GROQ_MODELS,
    DEFAULT_GEMINI_MODELS,
)
from core.state import (
    initialize_session_state,
    persist_state,
    clear_persisted_state,
)

# Engine modules
from engine.fallback_data import generate_fallback_roadmap
from engine.xai_scorer import compute_node_relevance
from engine.re_router import (
    find_next_recommended_action,
    calculate_progress_stats,
    apply_diagnostic_assessment,
)
from engine.groq_engine import generate_roadmap_with_groq, HAS_GROQ
from engine.gemini_engine import generate_roadmap_with_gemini, HAS_GEMINI
from engine.llm_router import generate_unified_roadmap

# UI components
from ui.styles import inject_custom_styles
from ui.components import (
    render_app_header,
    render_skill_gap_section,
    render_next_best_action_card,
    render_node_inspector,
    render_roadmap_updated_banner,
    render_diagnostic_assessment_widget,
    clean_html,
)
from ui.flow_visualizer import render_dag_flowchart
from ui.radar_chart import render_dynamic_radar_chart
from ui.chat_interface import render_ai_mentor_chat
from ui.recommendations import render_recommendation_cards
from ui.export_generator import (
    build_markdown_export,
    build_printable_html_export,
)

# ==========================================
# PAGE CONFIGURATION & EDITORIAL STYLES
# ==========================================
st.set_page_config(
    page_title="PathFinder AI — Learning Navigation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_styles()
initialize_session_state()

# ==========================================
# SIDEBAR: CLEAN LEARNER RAIL
# ==========================================
with st.sidebar:
    st.markdown("""
    <div class="pf-sidebar-brand">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="5" cy="18" r="3" fill="#2457D6"/>
            <circle cx="12" cy="6" r="3" fill="#111111"/>
            <circle cx="19" cy="14" r="3" fill="#2F7D5A"/>
            <path d="M7 16L10 8M14 8L17 12" stroke="#DDDCD6" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <div>
            <div class="pf-sidebar-brand-name">PathFinder</div>
            <div style="font-size:10.5px; color:#858585;">Curriculum Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Learner Profile & Active Target
    active_role = st.session_state.user_profile.get("target_role", "AI & ML Engineer")
    active_level = st.session_state.user_profile.get("experience_level", "Intermediate")
    active_hours = st.session_state.user_profile.get("weekly_hours", 15)
    known_skills = st.session_state.user_profile.get("skills", ["Python", "SQL", "Basic Math"])
    known_str = " · ".join(html.escape(s) for s in known_skills[:4])

    st.markdown(f"""
    <div class="pf-sidebar-tag">Current Goal</div>
    <div style="font-size:13.5px; font-weight:600; color:#111111; margin-bottom:10px;">{html.escape(active_role)}</div>
    <div class="pf-sidebar-tag">Profile</div>
    <div style="font-size:12.5px; color:#4B4B4B; margin-bottom:4px;">{html.escape(active_level)} · {active_hours} hrs / week</div>
    <div style="font-size:11.5px; color:#858585; margin-bottom:14px;">{known_str}</div>
    """, unsafe_allow_html=True)

    st.divider()

    # Settings Expander (Learner Settings + Collapsed Developer/Demo Mode)
    with st.expander("Settings", expanded=False):
        st.markdown("<div class='pf-sidebar-tag'>Learner Pace & Profile</div>", unsafe_allow_html=True)
        exp_input = st.select_slider(
            "Experience Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value=st.session_state.user_profile.get("experience_level", "Intermediate")
        )
        hours_input = st.slider(
            "Weekly Study Hours",
            min_value=5,
            max_value=40,
            value=st.session_state.user_profile.get("weekly_hours", 15)
        )
        known_skills_input = st.multiselect(
            "Mastered Skills",
            [
                "Python", "Basic Math", "SQL", "Git", "HTML/CSS", "Linear Algebra",
                "JavaScript", "TypeScript", "Docker", "Linux", "React", "Calculus"
            ],
            default=st.session_state.user_profile.get("skills", ["Python", "Basic Math", "SQL"])
        )

        st.session_state.user_profile.update({
            "experience_level": exp_input,
            "weekly_hours": hours_input,
            "skills": known_skills_input
        })

        st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
        
        # Sub-expander: Developer / Demo Mode
        with st.expander("Developer / Demo Mode", expanded=False):
            st.markdown("<div class='pf-sidebar-tag'>Evaluation Persona Presets</div>", unsafe_allow_html=True)
            selected_persona_name = st.selectbox(
                "Load Student Persona:",
                options=["Custom Goal"] + list(DEMO_PERSONAS.keys()),
                index=0,
                label_visibility="collapsed"
            )

            if selected_persona_name != "Custom Goal":
                persona_data = DEMO_PERSONAS[selected_persona_name]
                if st.session_state.get("_loaded_persona") != selected_persona_name:
                    st.session_state._loaded_persona = selected_persona_name
                    st.session_state.user_profile = persona_data["profile"].copy()
                    st.session_state.roadmap_data = generate_fallback_roadmap(
                        persona_data["goal"], persona_data["profile"]
                    )
                    st.session_state.completed_nodes = set(persona_data.get("completed_initial", []))
                    st.session_state.selected_node_id = None
                    st.session_state.adaptation_event = None
                    st.session_state._show_replan_banner = False
                    persist_state()
                    st.rerun()

            st.markdown("<div class='pf-sidebar-tag' style='margin-top:10px;'>Inference Engine</div>", unsafe_allow_html=True)
            provider = st.radio(
                "Inference Engine",
                ["Smart Offline (Default)", "Groq Cloud (Llama 3.3)", "Google Gemini"],
                index=0,
                label_visibility="collapsed"
            )

            active_model = "llama-3.3-70b-versatile"
            groq_key_input = ""
            gemini_key_input = ""

            if provider == "Groq Cloud (Llama 3.3)":
                groq_key_input = st.text_input(
                    "Groq API Key",
                    type="password",
                    placeholder="gsk_...",
                    value=os.environ.get("GROQ_API_KEY", "")
                )
                selected_model_key = st.selectbox(
                    "Model",
                    options=list(GROQ_MODEL_CATALOG.keys()),
                    index=0
                )
                active_model = selected_model_key
                if groq_key_input:
                    os.environ["GROQ_API_KEY"] = groq_key_input

            elif provider == "Google Gemini":
                gemini_key_input = st.text_input(
                    "Gemini API Key",
                    type="password",
                    placeholder="AIza...",
                    value=os.environ.get("GEMINI_API_KEY", "")
                )
                selected_gemini_key = st.selectbox(
                    "Model",
                    options=list(GEMINI_MODEL_CATALOG.keys()),
                    index=0
                )
                active_model = selected_gemini_key
                if gemini_key_input:
                    os.environ["GEMINI_API_KEY"] = gemini_key_input

            st.markdown("<div class='pf-sidebar-tag' style='margin-top:10px;'>State Reset</div>", unsafe_allow_html=True)
            if st.button("Start Fresh", use_container_width=True):
                st.session_state._pending_scratch = True
                st.rerun()

# Default provider values when demo mode is collapsed
if "provider" not in locals():
    provider = "Smart Offline (Default)"
    active_model = "llama-3.3-70b-versatile"
    groq_key_input = ""
    gemini_key_input = ""

# ==========================================
# MAIN INTERFACE: COMPACT EDITORIAL HERO & INTAKE
# ==========================================
roadmap = st.session_state.roadmap_data
role_title = roadmap.get("role", "AI & ML Engineer") if roadmap else "AI & ML Engineer"
render_app_header(role_title)

def _execute_roadmap_generation(goal_text: str) -> None:
    """Executes roadmap generation pipeline with validation and state update."""
    with st.spinner("Analyzing skill prerequisites and synthesizing learning path..."):
        p_name = "Groq" if "Groq" in provider else ("Google Gemini" if "Gemini" in provider else "Offline")
        new_roadmap = generate_unified_roadmap(
            goal=goal_text,
            profile=st.session_state.user_profile,
            provider=p_name,
            model_name=active_model,
            groq_api_key=groq_key_input,
            gemini_api_key=gemini_key_input
        )
        st.session_state.roadmap_data = new_roadmap
        st.session_state.completed_nodes = set()
        st.session_state.selected_node_id = None
        st.session_state.adaptation_event = None
        st.session_state._show_replan_banner = False
        persist_state()
        st.rerun()

# Compact Editorial intake block
st.markdown(f"""
<div class="pf-editorial-intake">
    <div class="pf-editorial-label">What are you working toward?</div>
    <div class="pf-editorial-title">Your path to <span class="pf-serif-accent">{html.escape(role_title)}.</span></div>
    <div class="pf-editorial-meta">{html.escape(active_level)} · {active_hours} hours per week pace</div>
</div>
""", unsafe_allow_html=True)

col_query, col_btn = st.columns([4.2, 1.2], vertical_alignment="center")
with col_query:
    goal_query = st.text_input(
        "Search Goal",
        placeholder="e.g. Become an AI Product Engineer, Full-Stack Developer, or Data Scientist",
        key="goal_box",
        label_visibility="collapsed"
    )
with col_btn:
    btn_generate = st.button("Build path →", type="primary", use_container_width=True)

# Refined textual popular path selector (NO black pills, NO emojis)
popular_goals = {
    "AI Engineering": "I want to become an AI & Machine Learning Engineer",
    "Full-Stack": "I want to become a Full-Stack Web Developer",
    "Data Science": "I want to master Data Science and Predictive Analytics",
    "Cybersecurity": "I want to become a Cybersecurity Analyst and Ethical Hacker",
    "Cloud & DevOps": "I want to become a Cloud Solutions Architect with Docker and Kubernetes"
}

st.markdown("<div style='margin-top:2px;'></div>", unsafe_allow_html=True)
pop_cols = st.columns([1.1, 1.2, 0.15, 1.0, 0.15, 1.2, 0.15, 1.2, 0.15, 1.4], vertical_alignment="center")
with pop_cols[0]:
    st.markdown("<span style='font-size:11px; font-weight:650; text-transform:uppercase; letter-spacing:0.06em; color:#858585;'>Popular paths</span>", unsafe_allow_html=True)

col_map = {0: 1, 1: 3, 2: 5, 3: 7, 4: 9}
sep_map = [2, 4, 6, 8]

for s_idx in sep_map:
    with pop_cols[s_idx]:
        st.markdown("<span style='color:#D0CFCA; font-size:11px; user-select:none;'>·</span>", unsafe_allow_html=True)

for p_idx, (p_label, p_prompt) in enumerate(popular_goals.items()):
    c_idx = col_map[p_idx]
    with pop_cols[c_idx]:
        st.markdown('<div class="pf-text-btn">', unsafe_allow_html=True)
        if st.button(p_label, key=f"pop_btn_{p_idx}", use_container_width=True):
            _execute_roadmap_generation(p_prompt)
        st.markdown('</div>', unsafe_allow_html=True)

if btn_generate and goal_query.strip():
    _execute_roadmap_generation(goal_query.strip())

# Empty State Guard
if not st.session_state.roadmap_data:
    empty_html = """
    <div class="pf-card" style="text-align:center; padding:36px 20px; margin-top:14px;">
        <h3 style="font-size:16px; color:#111111; margin-bottom:6px;">
            Tell PathFinder what you want to achieve.
        </h3>
        <p style="color:#4B4B4B; font-size:13px; max-width:500px; margin:0 auto; line-height:1.5;">
            Select a popular path above or enter any custom objective to generate your prerequisite-aware learning roadmap.
        </p>
    </div>
    """
    st.markdown(clean_html(empty_html), unsafe_allow_html=True)
    st.stop()

# ==========================================
# 4-TAB EDITORIAL ARCHITECTURE
# ==========================================
roadmap = st.session_state.roadmap_data

tab_overview, tab_learning_path, tab_progress, tab_mentor = st.tabs([
    "Overview",
    "Learning Path",
    "Progress",
    "Mentor"
])

# ------------------------------------------
# TAB 1: OVERVIEW & NEXT STEPS
# ------------------------------------------
with tab_overview:
    # 1. Product-Level Path Updated Event (When Adaptive Replanning Triggers)
    if st.session_state.get("adaptation_event"):
        render_roadmap_updated_banner(st.session_state.adaptation_event)
    elif st.session_state.get("_show_replan_banner"):
        last_title = st.session_state.get("_last_completed_title", "milestone")
        banner_html = f"""
        <div class="pf-notification">
            <div class="pf-notif-tag">Path Updated</div>
            <div class="pf-notif-body">
                Verified mastery of <strong>{last_title}</strong>. Downstream prerequisites have been dynamically unlocked.
            </div>
        </div>
        """
        st.markdown(clean_html(banner_html), unsafe_allow_html=True)

    # 2. Signature Skill Position Track Visualization (WHERE I AM → WHAT I NEED → HOW FAR I HAVE TO GO)
    render_skill_gap_section(roadmap, st.session_state.user_profile)

    # 3. Signature NEXT BEST ACTION Card
    render_next_best_action_card(roadmap, st.session_state.completed_nodes)

    # 4. Realistic Skill Check Assessment
    render_diagnostic_assessment_widget(roadmap, st.session_state.user_profile)

# ------------------------------------------
# TAB 2: LEARNING PATH (ROADMAP SIGNATURE)
# ------------------------------------------
with tab_learning_path:
    # Top: Streamlit Flow React Flow DAG with Side-by-Side Node Inspector
    render_dag_flowchart(roadmap, st.session_state.completed_nodes, st.session_state.user_profile)
    
    st.divider()
    # Bottom: Detailed Actionable Milestones & Projects
    render_recommendation_cards(roadmap, st.session_state.completed_nodes)

# ------------------------------------------
# TAB 3: PROGRESS ANALYTICS
# ------------------------------------------
with tab_progress:
    render_dynamic_radar_chart(
        roadmap=roadmap,
        profile=st.session_state.user_profile,
        completed_nodes=st.session_state.completed_nodes
    )

# ------------------------------------------
# TAB 4: MENTOR & EXPORTS
# ------------------------------------------
with tab_mentor:
    col_chat, col_side = st.columns([1.3, 1], vertical_alignment="top")

    with col_chat:
        p_name = "Groq" if "Groq" in provider else ("Google Gemini" if "Gemini" in provider else "Offline")
        render_ai_mentor_chat(
            roadmap=roadmap,
            profile=st.session_state.user_profile,
            completed_nodes=st.session_state.completed_nodes,
            provider=p_name,
            model_name=active_model,
            groq_api_key=groq_key_input,
            gemini_api_key=gemini_key_input,
            adaptation_event=st.session_state.get("adaptation_event")
        )

    with col_side:
        st.markdown("<div style='font-size:11px; font-weight:650; text-transform:uppercase; letter-spacing:0.08em; color:#858585; margin-bottom:10px;'>Export Curriculum</div>", unsafe_allow_html=True)
        stats = calculate_progress_stats(roadmap, st.session_state.completed_nodes)

        exp_c1, exp_c2, exp_c3 = st.columns(3, vertical_alignment="center")
        with exp_c1:
            st.download_button(
                "JSON",
                data=json.dumps(roadmap, indent=2),
                file_name="learning_path_roadmap.json",
                mime="application/json",
                use_container_width=True
            )
        with exp_c2:
            st.download_button(
                "Markdown",
                data=build_markdown_export(roadmap, st.session_state.completed_nodes, stats["progress_pct"]),
                file_name="learning_path.md",
                mime="text/markdown",
                use_container_width=True
            )
        with exp_c3:
            st.download_button(
                "HTML Report",
                data=build_printable_html_export(roadmap, st.session_state.completed_nodes, stats["progress_pct"]),
                file_name="learning_path_report.html",
                mime="text/html",
                use_container_width=True
            )
