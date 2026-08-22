"""PathFinder AI — AI-Powered Personalized Learning Path Recommender.

Developed by Team Cortex for HCL Tech Hackathon (Round 2).
Restrained, editorial light-mode learning platform prioritizing the core learner journey:
GOAL → CURRENT SKILLS → SKILL GAPS → ROADMAP → NEXT BEST ACTION → ADAPTIVE REPLANNING.
"""

import os
import json
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
# PAGE CONFIGURATION & RESTRAINED STYLES
# ==========================================
st.set_page_config(
    page_title="PathFinder AI — Personalized Learning Path",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_styles()
initialize_session_state()

# ==========================================
# SIDEBAR: CLEAN LEARNER PANEL
# ==========================================
with st.sidebar:
    st.markdown("### PathFinder Workspace")
    st.caption("AI-Powered Curriculum Architect")

    # Evaluation Mode & Persona Presets
    st.markdown("#### Evaluation Presets")
    selected_persona_name = st.selectbox(
        "Load Student Persona:",
        options=["Custom Goal"] + list(DEMO_PERSONAS.keys()),
        index=0,
        help="Quickly evaluate pre-configured student personas"
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

    st.divider()

    # Learner Profile Summary in Sidebar
    active_role = st.session_state.user_profile.get("target_role", "AI & ML Engineer")
    active_level = st.session_state.user_profile.get("experience_level", "Intermediate")
    active_hours = st.session_state.user_profile.get("weekly_hours", 15)

    st.markdown(f"""
    <div style="font-size:11px; font-weight:600; text-transform:uppercase; color:#8A8A8A; letter-spacing:0.04em; margin-bottom:4px;">Your Learning Goal</div>
    <div style="font-size:14px; font-weight:600; color:#171717; margin-bottom:12px;">{active_role}</div>
    <div style="font-size:11px; font-weight:600; text-transform:uppercase; color:#8A8A8A; letter-spacing:0.04em; margin-bottom:4px;">Profile</div>
    <div style="font-size:13px; color:#666666; margin-bottom:12px;">{active_level} · {active_hours} hrs/week</div>
    """, unsafe_allow_html=True)

    with st.expander("Edit Background & Pace", expanded=False):
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

    # Collapsed Developer & Engine Settings
    st.divider()
    with st.expander("Settings & Engine", expanded=False):
        provider = st.radio(
            "Inference Engine",
            ["Smart Offline (Default)", "Groq Cloud (Llama 3.3)", "Google Gemini"],
            index=0
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
                st.caption("Connected to Groq")

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
                st.caption("Connected to Gemini")
        else:
            st.caption("Using offline topological knowledge graphs.")

    # Reset Action
    st.divider()
    if st.button("Start Fresh", use_container_width=True):
        st.session_state._pending_scratch = True
        st.rerun()

# ==========================================
# MAIN INTERFACE: COMPACT HEADER & INTAKE
# ==========================================
roadmap = st.session_state.roadmap_data
role_title = roadmap.get("role", "Curriculum") if roadmap else "Personalized Path"
render_app_header(role_title)

def _execute_roadmap_generation(goal_text: str) -> None:
    """Executes roadmap generation pipeline with validation and state update."""
    with st.spinner("Assessing skills, mapping gaps, and synthesizing learning path..."):
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

# Goal intake section
st.markdown("<div style='font-size:12px; font-weight:600; text-transform:uppercase; color:#8A8A8A; letter-spacing:0.04em; margin-bottom:8px;'>What do you want to become?</div>", unsafe_allow_html=True)

col_query, col_btn = st.columns([4.2, 1.2], vertical_alignment="center")
with col_query:
    goal_query = st.text_input(
        "What do you want to become?",
        placeholder="e.g. Become an AI Product Engineer, Full-Stack Developer, or Data Scientist",
        key="goal_box",
        label_visibility="collapsed"
    )
with col_btn:
    btn_generate = st.button("Build learning path", type="primary", use_container_width=True)

# Clean single-line popular goals pills
popular_goals = {
    "AI Engineering": "I want to become an AI & Machine Learning Engineer",
    "Full-Stack Web": "I want to become a Full-Stack Web Developer",
    "Data Science": "I want to master Data Science and Predictive Analytics",
    "Cybersecurity": "I want to become a Cybersecurity Analyst and Ethical Hacker",
    "Cloud & DevOps": "I want to become a Cloud Solutions Architect with Docker and Kubernetes"
}

selected_pop = st.pills(
    "Popular goals:",
    options=list(popular_goals.keys()),
    label_visibility="visible"
)

if selected_pop and selected_pop != st.session_state.get("_last_pop_pill"):
    st.session_state._last_pop_pill = selected_pop
    st.session_state.goal_box = popular_goals[selected_pop]
    _execute_roadmap_generation(popular_goals[selected_pop])

if btn_generate and goal_query.strip():
    _execute_roadmap_generation(goal_query.strip())

# Empty State Guard
if not st.session_state.roadmap_data:
    empty_html = """
    <div class="content-card" style="text-align:center; padding:48px 24px; margin-top:20px;">
        <h3 style="font-size:18px; color:#171717; margin-bottom:8px;">
            Tell PathFinder what you want to achieve.
        </h3>
        <p style="color:#666666; font-size:14px; max-width:540px; margin:0 auto; line-height:1.6;">
            Select a popular goal above, enter any custom objective, or choose an evaluation persona in the sidebar to generate your prerequisite-aware learning roadmap.
        </p>
    </div>
    """
    st.markdown(clean_html(empty_html), unsafe_allow_html=True)
    st.stop()

# ==========================================
# 3-TAB RESTRAINED ARCHITECTURE
# ==========================================
roadmap = st.session_state.roadmap_data

tab_overview, tab_learning_path, tab_mentor = st.tabs([
    "Overview",
    "Learning Path",
    "Mentor"
])

# ------------------------------------------
# TAB 1: OVERVIEW & NEXT STEPS
# ------------------------------------------
with tab_overview:
    # 1. Dynamic Adaptive Replanning Banner (when triggered by assessment or completion)
    if st.session_state.get("adaptation_event"):
        render_roadmap_updated_banner(st.session_state.adaptation_event)
    elif st.session_state.get("_show_replan_banner"):
        last_title = st.session_state.get("_last_completed_title", "milestone")
        banner_html = f"""
        <div class="path-updated-banner">
            <strong>Path Updated:</strong> Verified mastery of <em>{last_title}</em>. Downstream prerequisites have been dynamically unlocked.
        </div>
        """
        st.markdown(clean_html(banner_html), unsafe_allow_html=True)

    # 2. Skill Gap Diagnostic Section (Horizontal Competency Comparison)
    render_skill_gap_section(roadmap, st.session_state.user_profile)

    # 3. Prominent NEXT UP Card
    render_next_best_action_card(roadmap, st.session_state.completed_nodes)

    # 4. Interactive Skill Check Assessment (Adaptive Loop Demo)
    render_diagnostic_assessment_widget(roadmap, st.session_state.user_profile)

    # 5. Compact Curriculum Progress Summary
    stats = calculate_progress_stats(roadmap, st.session_state.completed_nodes)
    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #E5E5E2; border-radius:8px; padding:14px 18px; margin-top:14px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 1px 2px rgba(0,0,0,0.02);">
        <span style="font-size:13px; color:#666666;">
            Curriculum Progress: <strong style="color:#171717;">{stats['completed_count']} / {stats['total_nodes']} Modules Mastered</strong> ({stats['progress_pct']}%)
        </span>
        <span style="font-size:12.5px; color:#2563EB;">
            Switch to <strong>Learning Path</strong> tab to view interactive DAG canvas.
        </span>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: LEARNING PATH & MILESTONES
# ------------------------------------------
with tab_learning_path:
    # Top: Streamlit Flow React Flow DAG with Side-by-Side Node Inspector
    render_dag_flowchart(roadmap, st.session_state.completed_nodes, st.session_state.user_profile)
    
    st.divider()
    # Bottom: Detailed Actionable Milestones & Projects
    render_recommendation_cards(roadmap, st.session_state.completed_nodes)

# ------------------------------------------
# TAB 3: MENTOR & EXPORTS
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
        # Collapsible Radar Chart (Secondary Visualization)
        with st.expander("Competency Radar Analysis", expanded=False):
            render_dynamic_radar_chart(
                roadmap=roadmap,
                profile=st.session_state.user_profile,
                completed_nodes=st.session_state.completed_nodes
            )

        st.markdown("#### Export Curriculum")
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
