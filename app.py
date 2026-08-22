"""SkillPath AI — AI-Powered Personalized Learning Path Recommender (PathFinder Prototype).

Developed by Team Cortex for HCL Tech Hackathon (Round 2).
Modular, production-ready Streamlit application.
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
    page_title="SkillPath AI — Learn Anything",
    page_icon="assets/logo_small.png" if Path("assets/logo_small.png").exists() else "🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_styles()
initialize_session_state()

# ==========================================
# SIDEBAR: SETTINGS, LLM ROUTER & PROFILING
# ==========================================
with st.sidebar:
    if Path("assets/logo.png").exists():
        st.image("assets/logo.png", width=64)
    st.title("Settings & Profile")
    st.caption(f"Team {TEAM_NAME} • PathFinder AI")

    # LLM Provider & Model Selection
    st.subheader("⚡ AI Engine & Models")
    provider = st.radio(
        "Select AI Provider",
        ["Groq Cloud", "Google Gemini", "Smart Offline (No Key)"],
        index=0,
        help="Choose between high-speed Groq inference, Google Gemini reasoning, or fast offline templates."
    )

    active_model = "llama-3.3-70b-versatile"
    groq_key_input = ""
    gemini_key_input = ""

    if provider == "Groq Cloud":
        groq_key_input = st.text_input(
            "Groq API Key (`gsk_...`)",
            type="password",
            placeholder="gsk_...",
            value=os.environ.get("GROQ_API_KEY", ""),
            help="Get your free API key at console.groq.com"
        )
        
        # Model dropdown with suitability recommendation
        model_display_names = {k: f"{v['name']} ({v['tag']})" for k, v in GROQ_MODEL_CATALOG.items()}
        selected_model_key = st.selectbox(
            "Groq LLM Model",
            options=list(GROQ_MODEL_CATALOG.keys()),
            format_func=lambda k: model_display_names.get(k, k),
            index=0,
            help="Selected model determines reasoning depth and DAG complexity."
        )
        active_model = selected_model_key
        st.caption(f"ℹ️ {GROQ_MODEL_CATALOG[selected_model_key]['desc']}")

        if groq_key_input:
            os.environ["GROQ_API_KEY"] = groq_key_input
            if groq_key_input.startswith("gsk_"):
                st.success("⚡ Groq API Key Active!", icon="✅")
            else:
                st.warning("Key should start with `gsk_`")

    elif provider == "Google Gemini":
        gemini_key_input = st.text_input(
            "Gemini API Key (`AIza...`)",
            type="password",
            placeholder="AIza...",
            value=os.environ.get("GEMINI_API_KEY", ""),
            help="Get your API key at aistudio.google.com"
        )
        gemini_display_names = {k: f"{v['name']} ({v['tag']})" for k, v in GEMINI_MODEL_CATALOG.items()}
        selected_gemini_key = st.selectbox(
            "Gemini LLM Model",
            options=list(GEMINI_MODEL_CATALOG.keys()),
            format_func=lambda k: gemini_display_names.get(k, k),
            index=0
        )
        active_model = selected_gemini_key
        st.caption(f"ℹ️ {GEMINI_MODEL_CATALOG[selected_gemini_key]['desc']}")

        if gemini_key_input:
            os.environ["GEMINI_API_KEY"] = gemini_key_input
            st.success("✨ Gemini API Key Active!", icon="✅")

    else:
        st.info("🛡️ Smart Offline Engine active. Generates rich 3-phase DAG curriculums instantly without any API keys.")

    st.divider()

    # Mode Controls: Demo Mode & Persona Switcher
    st.caption("Evaluation Mode")
    demo_toggle = st.toggle(
        "🎬 Interactive Demo Mode",
        key="demo_mode",
        help="Quickly evaluate pre-built personas without typing a goal"
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
            st.toast(f"Loaded {selected_persona_name}!", icon="🎬")
            st.rerun()

    btn_scratch = st.button("🔄 Start from Scratch", use_container_width=True)
    if btn_scratch:
        st.session_state._pending_scratch = True
        st.rerun()

    st.divider()

    # Pillar 2: Learner Profiling Engine
    st.caption("Pillar 2: Learner Profiling Engine")
    with st.expander("👤 Learner Profile & Constraints", expanded=True):
        role_input = st.selectbox(
            "Primary Domain Interest",
            [
                "AI & ML Engineer", "Full-Stack Web Developer", "Data Scientist",
                "Cybersecurity Analyst", "Cloud & DevOps Engineer", "Musician",
                "Language Learner", "Fitness Enthusiast", "Exam Topper"
            ],
            index=0,
            help="Context hint for personalized curriculum framing"
        )
        exp_input = st.select_slider(
            "Current Experience Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value=st.session_state.user_profile.get("experience_level", "Intermediate")
        )
        hours_input = st.slider(
            "Weekly Study Commitment",
            min_value=5,
            max_value=40,
            value=st.session_state.user_profile.get("weekly_hours", 15),
            help="Hours per week allocated for learning"
        )
        style_input = st.selectbox(
            "Preferred Learning Style",
            ["Hands-on Projects", "Video Courses", "Reading & Docs", "Interactive Labs"],
            index=0
        )
        known_skills_input = st.multiselect(
            "Verified Mastered Skills",
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
            "preferred_learning_style": style_input,
            "skills": known_skills_input
        })

# ==========================================
# MAIN INTERFACE: HERO & GOAL INTAKE (PILLAR 1)
# ==========================================
render_hero_header()

def _execute_roadmap_generation(goal_text: str) -> None:
    """Executes roadmap generation pipeline with spinner and error recovery."""
    if st.session_state.get("demo_mode"):
        st.session_state._pending_demo_off = True

    with st.spinner("⚡ Analyzing learning goals, verifying prerequisite constraints, and synthesizing DAG curriculum..."):
        provider_name = "Groq" if provider == "Groq Cloud" else ("Google Gemini" if provider == "Google Gemini" else "Offline")
        roadmap = generate_unified_roadmap(
            goal=goal_text,
            profile=st.session_state.user_profile,
            provider=provider_name,
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
        st.toast("🎉 Personalized Learning Pathway Generated!", icon="🚀")
        st.rerun()

# Pillar 1: Quick Picks + Natural Language Goal Input
selected_pill = st.pills(
    "⚡ One-Click Career / Goal Quick Picks:",
    options=list(QUICK_PICKS.keys()),
    help="Click any option to instantly synthesize a customized curriculum"
)

if selected_pill and selected_pill != st.session_state.get("_last_pill"):
    st.session_state._last_pill = selected_pill
    st.session_state.goal_box = QUICK_PICKS[selected_pill]
    _execute_roadmap_generation(QUICK_PICKS[selected_pill])

col_query, col_btn = st.columns([3.5, 1])
with col_query:
    goal_query = st.text_input(
        "💬 Describe ANY Learning Goal — career, technical stack, hobby, instrument, exam, or fitness:",
        placeholder="e.g. Become a full-stack AI engineer with PyTorch and Next.js in 3 months",
        key="goal_box"
    )
with col_btn:
    st.write(" ")
    st.write(" ")
    btn_generate = st.button("🚀 Generate Path", type="primary", use_container_width=True)

if btn_generate and goal_query.strip():
    _execute_roadmap_generation(goal_query.strip())

# Empty State Guard
if not st.session_state.roadmap_data:
    st.info(
        "👋 **Welcome to SkillPath AI (PathFinder Prototype by Team Cortex)!**\n\n"
        "1. ⚡ **Click any Quick Pick** above for instant curriculum synthesis,\n"
        "2. ✏️ **Type any custom goal** (e.g. *learn guitar, deep learning, fluent Spanish, crack JEE*) and click **Generate Path**, or\n"
        "3. 🎬 Enable **Interactive Demo Mode** in the sidebar to evaluate pre-configured student personas."
    )
    st.stop()

roadmap = st.session_state.roadmap_data

# ==========================================
# METRICS SUMMARY BAR
# ==========================================
render_metrics_summary_bar(roadmap, st.session_state.completed_nodes)
st.divider()

# ==========================================
# MAIN TABS (ALL 6 PILLARS VISUALIZED)
# ==========================================
tab_dag, tab_recs, tab_xai, tab_dash = st.tabs([
    "🔀 Pillar 4: Interactive DAG (React Flow)",
    "📚 Pillar 3: Course & Project Recs",
    "💡 Pillar 5: Explainable AI & AI Mentor",
    "📊 Pillar 6: Skill Radar & Analytics"
])

# Tab 1: Prerequisite-Aware Directed Acyclic Graph (DAG) Visualizer
with tab_dag:
    render_dag_flowchart(roadmap, st.session_state.completed_nodes, st.session_state.user_profile)

# Tab 2: Curated Course & Project Recommendations
with tab_recs:
    render_recommendation_cards(roadmap, st.session_state.completed_nodes)

# Tab 3: Explainable AI (XAI) Ledger & Real-Time Streaming Mentor
with tab_xai:
    col_xai_left, col_xai_right = st.columns([1, 1])

    with col_xai_left:
        st.markdown("### 🔍 Transparent Rationale Ledger")
        st.caption("Multi-factor Explainable AI scoring breakdown justifying every curriculum recommendation.")
        
        total_p = len(roadmap.get("phases", []))
        for p_idx, phase in enumerate(roadmap.get("phases", [])):
            for node in phase.get("nodes", []):
                score, breakdown = compute_node_relevance(
                    node,
                    st.session_state.user_profile,
                    st.session_state.completed_nodes,
                    p_idx,
                    total_p
                )
                with st.expander(f"Why {node['id']}: {node['title']}? ({score}% match)", expanded=False):
                    st.markdown(f"**Target Skill Gap:** *{', '.join(node.get('skills', ['General']))}*")
                    st.markdown(f"**Prerequisite Rationale:** {node.get('why', 'Foundational milestone.')}")
                    st.progress(score / 100, text=f"Relevance Score: {score}/100")
                    for line in breakdown:
                        st.caption(f"• {line}")

    with col_xai_right:
        render_ai_mentor_chat(
            roadmap=roadmap,
            profile=st.session_state.user_profile,
            completed_nodes=st.session_state.completed_nodes,
            provider="Groq" if provider == "Groq Cloud" else ("Google Gemini" if provider == "Google Gemini" else "Offline"),
            model_name=active_model,
            groq_api_key=groq_key_input,
            gemini_api_key=gemini_key_input
        )

# Tab 4: Skill Competency Radar Chart, Next Actions & Exports
with tab_dash:
    col_radar, col_actions = st.columns([1.1, 1])

    with col_radar:
        render_dynamic_radar_chart(
            roadmap=roadmap,
            profile=st.session_state.user_profile,
            completed_nodes=st.session_state.completed_nodes
        )

    with col_actions:
        st.markdown("### 🎯 Adaptive Next Action")
        next_action_res = find_next_recommended_action(roadmap, st.session_state.completed_nodes)

        if next_action_res:
            next_node, next_phase = next_action_res
            st.info(f"""
            👉 **Highest Priority Milestone:**  
            **{next_node['id']}: {next_node['title']}** ({next_node.get('provider', 'Online')})  
            *Duration:* {next_node.get('duration', '2 weeks')} | *Phase:* {next_phase}  
            *Why Now:* Prerequisites unlocked! Completing this unlocks subsequent Phase 2/3 milestones.
            """)
        else:
            st.balloons()
            st.success("🏆 **Curriculum Mastered!** You have completed all milestones on this learning path!")

        st.markdown("#### 📁 Roadmap Export & Download")
        stats = calculate_progress_stats(roadmap, st.session_state.completed_nodes)

        exp_c1, exp_c2, exp_c3 = st.columns(3)
        with exp_c1:
            st.download_button(
                "📥 JSON",
                data=json.dumps(roadmap, indent=2),
                file_name="learning_path_roadmap.json",
                mime="application/json",
                use_container_width=True
            )
        with exp_c2:
            st.download_button(
                "📄 Markdown",
                data=build_markdown_export(roadmap, st.session_state.completed_nodes, stats["progress_pct"]),
                file_name="learning_path.md",
                mime="text/markdown",
                use_container_width=True
            )
        with exp_c3:
            st.download_button(
                "🖨️ Printable HTML/PDF",
                data=build_printable_html_export(roadmap, st.session_state.completed_nodes, stats["progress_pct"]),
                file_name="learning_path_report.html",
                mime="text/html",
                use_container_width=True
            )
