"""SkillPath AI — AI-Powered Personalized Learning Path Recommender (PathFinder Prototype).

Developed by Team Cortex for HCL Tech Hackathon (Round 2).
Sleek, human-crafted Streamlit application with spatial discipline and clean aesthetics.
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
from ui.components import render_hero_header, render_metrics_summary_bar
from ui.flow_visualizer import render_dag_flowchart
from ui.radar_chart import render_dynamic_radar_chart
from ui.chat_interface import render_ai_mentor_chat
from ui.recommendations import render_recommendation_cards
from ui.export_generator import (
    build_markdown_export,
    build_printable_html_export,
)

# ==========================================
# PAGE CONFIGURATION & STYLES
# ==========================================
st.set_page_config(
    page_title="PathFinder AI — Learn Anything",
    page_icon="assets/logo_small.png" if Path("assets/logo_small.png").exists() else "🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_styles()
initialize_session_state()

# ==========================================
# SIDEBAR: SETTINGS, PERSONAS & PROFILING
# ==========================================
with st.sidebar:
    if Path("assets/logo.png").exists():
        st.image("assets/logo.png", width=48)
    st.markdown("### **PathFinder AI**")
    st.caption("Curriculum Architect • Team Cortex")

    # Evaluation Mode & Persona Switcher
    st.markdown("#### Evaluation Mode")
    demo_toggle = st.toggle(
        "Interactive Demo Mode",
        key="demo_mode",
        help="Quickly evaluate pre-configured student personas without manual setup"
    )

    if demo_toggle:
        selected_persona_name = st.selectbox(
            "Select Evaluation Persona:",
            options=list(DEMO_PERSONAS.keys()),
            index=0
        )
        persona_data = DEMO_PERSONAS[selected_persona_name]
        
        # Load persona on selection change
        if st.session_state.get("_loaded_persona") != selected_persona_name:
            st.session_state._loaded_persona = selected_persona_name
            st.session_state.user_profile = persona_data["profile"].copy()
            st.session_state.roadmap_data = generate_fallback_roadmap(
                persona_data["goal"], persona_data["profile"]
            )
            st.session_state.completed_nodes = set(persona_data.get("completed_initial", []))
            st.session_state.selected_node_id = None
            persist_state()
            st.toast(f"Loaded {selected_persona_name}!", icon="🎯")
            st.rerun()

    # Learner Profile Section
    st.divider()
    st.markdown("#### Learner Profile")
    with st.expander("Adjust Profile & Pace", expanded=not demo_toggle):
        role_input = st.selectbox(
            "Primary Domain Focus",
            [
                "AI & ML Engineer", "Full-Stack Web Developer", "Data Scientist",
                "Cybersecurity Analyst", "Cloud & DevOps Engineer", "Musician",
                "Language Learner", "Fitness Enthusiast", "Exam Topper"
            ],
            index=0
        )
        exp_input = st.select_slider(
            "Current Experience Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value=st.session_state.user_profile.get("experience_level", "Intermediate")
        )
        hours_input = st.slider(
            "Weekly Commitment (Hours)",
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
            "target_role": role_input,
            "experience_level": exp_input,
            "weekly_hours": hours_input,
            "skills": known_skills_input
        })

    # Advanced AI Model Settings (Clean, Collapsible)
    st.divider()
    with st.expander("⚙️ Advanced AI Model Settings", expanded=False):
        provider = st.radio(
            "AI Inference Engine",
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
                "Groq Model",
                options=list(GROQ_MODEL_CATALOG.keys()),
                index=0
            )
            active_model = selected_model_key
            if groq_key_input:
                os.environ["GROQ_API_KEY"] = groq_key_input
                st.caption("✅ Groq Key Active")

        elif provider == "Google Gemini":
            gemini_key_input = st.text_input(
                "Gemini API Key",
                type="password",
                placeholder="AIza...",
                value=os.environ.get("GEMINI_API_KEY", "")
            )
            selected_gemini_key = st.selectbox(
                "Gemini Model",
                options=list(GEMINI_MODEL_CATALOG.keys()),
                index=0
            )
            active_model = selected_gemini_key
            if gemini_key_input:
                os.environ["GEMINI_API_KEY"] = gemini_key_input
                st.caption("✅ Gemini Key Active")

        else:
            st.caption("Using offline topological knowledge graphs.")

    # Reset
    st.divider()
    if st.button("Start Fresh", use_container_width=True):
        st.session_state._pending_scratch = True
        st.rerun()

# ==========================================
# MAIN INTERFACE: HERO & GOAL INTAKE
# ==========================================
render_hero_header()

def _execute_roadmap_generation(goal_text: str) -> None:
    """Executes roadmap generation pipeline with spinner and error recovery."""
    if st.session_state.get("demo_mode"):
        st.session_state._pending_demo_off = True

    with st.spinner("Analyzing learning goals, verifying prerequisite constraints, and synthesizing curriculum..."):
        p_name = "Groq" if "Groq" in provider else ("Google Gemini" if "Gemini" in provider else "Offline")
        roadmap = generate_unified_roadmap(
            goal=goal_text,
            profile=st.session_state.user_profile,
            provider=p_name,
            model_name=active_model,
            groq_api_key=groq_key_input,
            gemini_api_key=gemini_key_input
        )
        st.session_state.roadmap_data = roadmap
        st.session_state.completed_nodes = set()
        st.session_state.selected_node_id = None
        
        if st.session_state.get("_pending_demo_off"):
            st.session_state._pending_demo_off = False
            st.session_state.demo_mode = False

        persist_state()
        st.toast("Personalized Learning Pathway Generated!", icon="🚀")
        st.rerun()

# Quick Pick Options
selected_pill = st.pills(
    "Suggested Learning Objectives:",
    options=list(QUICK_PICKS.keys()),
    help="Click any option to instantly synthesize a customized curriculum"
)

if selected_pill and selected_pill != st.session_state.get("_last_pill"):
    st.session_state._last_pill = selected_pill
    st.session_state.goal_box = QUICK_PICKS[selected_pill]
    _execute_roadmap_generation(QUICK_PICKS[selected_pill])

col_query, col_btn = st.columns([3.8, 1])
with col_query:
    goal_query = st.text_input(
        "Describe your learning goal:",
        placeholder="e.g. Become a full-stack AI engineer with PyTorch and Next.js, learn acoustic guitar, or crack JEE",
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
    <div style="background:#0e1320; border:1px solid rgba(255,255,255,0.06); border-radius:14px; padding:32px; text-align:center; margin-top:20px;">
        <div style="font-family:'Outfit',sans-serif; font-size:1.35rem; font-weight:700; color:#f8fafc; margin-bottom:8px;">
            Get Started with PathFinder AI
        </div>
        <p style="color:#94a3b8; font-size:0.95rem; max-width:600px; margin:0 auto 20px auto; line-height:1.6;">
            Select one of the suggested goals above, type your own custom objective, or enable <strong>Interactive Demo Mode</strong> in the sidebar to evaluate pre-configured student personas.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

roadmap = st.session_state.roadmap_data

# ==========================================
# METRICS SUMMARY RIBBON
# ==========================================
render_metrics_summary_bar(roadmap, st.session_state.completed_nodes)

# ==========================================
# MAIN TABS (CLEAN, 3-PART UNIFIED LAYOUT)
# ==========================================
tab_flow, tab_milestones, tab_mentor_analytics = st.tabs([
    "Curriculum DAG Flow",
    "Actionable Milestones",
    "AI Mentor & Analytics"
])

# Tab 1: Interactive Directed Acyclic Graph (DAG)
with tab_flow:
    render_dag_flowchart(roadmap, st.session_state.completed_nodes, st.session_state.user_profile)

# Tab 2: Actionable Milestones & Recs
with tab_milestones:
    render_recommendation_cards(roadmap, st.session_state.completed_nodes)

# Tab 3: AI Mentor + Competency Analytics
with tab_mentor_analytics:
    col_analytics, col_mentor = st.columns([1.1, 1.2])

    with col_analytics:
        render_dynamic_radar_chart(
            roadmap=roadmap,
            profile=st.session_state.user_profile,
            completed_nodes=st.session_state.completed_nodes
        )

        st.markdown("#### Adaptive Next Action")
        next_action_res = find_next_recommended_action(roadmap, st.session_state.completed_nodes)

        if next_action_res:
            next_node, next_phase = next_action_res
            st.info(f"""
            **Next Unlocked Target:**  
            **{next_node['id']}: {next_node['title']}** ({next_node.get('provider', 'Online')})  
            *Pace:* {next_node.get('duration', '2 weeks')} | *Phase:* {next_phase}  
            *Why Now:* Prerequisites unlocked. Mastering this unblocks subsequent modules.
            """)
        else:
            st.success("Curriculum Mastered! All milestones completed.")

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
