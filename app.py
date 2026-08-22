"""PathFinder AI — AI-Powered Personalized Learning Path Recommender.

Developed by Team Cortex for HCL Tech Hackathon (Round 2).
Streamlined, human-crafted educational platform prioritizing the core learner journey:
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
# SIDEBAR: LEARNER WORKSPACE & SETTINGS
# ==========================================
with st.sidebar:
    st.markdown("### 🎓 **PathFinder Workspace**")
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
            st.session_state._show_replan_banner = False
            persist_state()
            st.rerun()

    # Learner Profile Section
    st.divider()
    st.markdown("#### Learner Profile")
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

    # Collapsed Developer Settings (API Keys)
    st.divider()
    with st.expander("⚙️ Developer Settings", expanded=False):
        provider = st.radio(
            "Inference Provider",
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
                st.caption("✅ Groq Active")

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
                st.caption("✅ Gemini Active")
        else:
            st.caption("Using offline topological knowledge graphs.")

    # Reset
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
    with st.spinner("Assessing skills, mapping gaps, and synthesizing DAG curriculum..."):
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
        st.session_state._show_replan_banner = False
        persist_state()
        st.rerun()

# One-Click Quick Pick Options
selected_pill = st.pills(
    "Quick Goal Suggestions:",
    options=list(QUICK_PICKS.keys()),
    help="Click any goal to instantly synthesize a tailored curriculum"
)

if selected_pill and selected_pill != st.session_state.get("_last_pill"):
    st.session_state._last_pill = selected_pill
    st.session_state.goal_box = QUICK_PICKS[selected_pill]
    _execute_roadmap_generation(QUICK_PICKS[selected_pill])

col_query, col_btn = st.columns([4, 1])
with col_query:
    goal_query = st.text_input(
        "Enter your learning goal:",
        placeholder="e.g. Become an AI & Machine Learning Engineer, learn guitar, or crack JEE",
        key="goal_box",
        label_visibility="collapsed"
    )
with col_btn:
    btn_generate = st.button("Build Roadmap", type="primary", use_container_width=True)

if btn_generate and goal_query.strip():
    _execute_roadmap_generation(goal_query.strip())

# Empty State Guard
if not st.session_state.roadmap_data:
    st.markdown("""
    <div style="background:#0F1626; border:1px solid #1E293B; border-radius:10px; padding:36px; text-align:center; margin-top:20px;">
        <h3 style="font-family:'Outfit',sans-serif; font-size:1.4rem; color:#F8FAFC; margin-bottom:8px;">
            Tell PathFinder what you want to become.
        </h3>
        <p style="color:#94A3B8; font-size:0.95rem; max-width:560px; margin:0 auto 20px auto; line-height:1.6;">
            Select a suggested goal above, enter any custom objective, or pick an evaluation persona in the sidebar to generate your personalized, prerequisite-aware learning roadmap.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ==========================================
# CORE PRODUCT STORY (FIRST VIEWPORT)
# ==========================================
roadmap = st.session_state.roadmap_data

# 1. Skill Gap Diagnostic Section ("Where I Am" vs "Where I Need To Be")
render_skill_gap_section(roadmap, st.session_state.user_profile)

# 2. Adaptive Replanning Indicator (when a milestone completion updates downstream state)
if st.session_state.get("_show_replan_banner"):
    last_title = st.session_state.get("_last_completed_title", "milestone")
    st.markdown(f"""
    <div class="replan-banner">
        <strong>⚡ ROADMAP ADAPTED:</strong> Verified mastery of <em>{last_title}</em>. Downstream prerequisites have been dynamically unlocked.
    </div>
    """, unsafe_allow_html=True)

# 3. Prominent NEXT BEST ACTION Card
render_next_best_action_card(roadmap, st.session_state.completed_nodes)

# ==========================================
# MAIN WORKSPACE: ROADMAP, MILESTONES & MENTOR
# ==========================================
tab_roadmap, tab_mentor_analytics = st.tabs([
    "🗺️ Interactive Learning Roadmap",
    "🤖 PathFinder Mentor & Competency Progress"
])

with tab_roadmap:
    # Top: Streamlit Flow React Flow DAG
    render_dag_flowchart(roadmap, st.session_state.completed_nodes, st.session_state.user_profile)
    
    st.divider()
    # Bottom: Detailed Actionable Milestones
    render_recommendation_cards(roadmap, st.session_state.completed_nodes)

with tab_mentor_analytics:
    col_analytics, col_mentor = st.columns([1.1, 1.2])

    with col_analytics:
        # Dynamic Skill Competency Polar Radar
        render_dynamic_radar_chart(
            roadmap=roadmap,
            profile=st.session_state.user_profile,
            completed_nodes=st.session_state.completed_nodes
        )

        st.markdown("#### Export Curriculum")
        stats = calculate_progress_stats(roadmap, st.session_state.completed_nodes)

        exp_c1, exp_c2, exp_c3 = st.columns(3)
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

    with col_mentor:
        p_name = "Groq" if "Groq" in provider else ("Google Gemini" if "Gemini" in provider else "Offline")
        render_ai_mentor_chat(
            roadmap=roadmap,
            profile=st.session_state.user_profile,
            completed_nodes=st.session_state.completed_nodes,
            provider=p_name,
            model_name=active_model,
            groq_api_key=groq_key_input,
            gemini_api_key=gemini_key_input
        )
