"""Conversational AI Mentor chat interface with structured learning coach responses."""

import os
import html
from typing import Dict, Any, Set, List, Optional
import streamlit as st

from core.config import WELCOME_MESSAGE
from core.state import persist_state
from engine.groq_engine import stream_groq_chat_response, HAS_GROQ
from engine.gemini_engine import stream_gemini_chat_response, HAS_GEMINI
from engine.llm_router import generate_offline_streaming_mentor_reply

SUGGESTED_PROMPTS = [
    "What should I study today?",
    "Why did my roadmap change?",
    "Explain my skill gaps",
    "Adjust my plan for 1 hour"
]

def build_mentor_system_prompt(
    roadmap: Dict[str, Any],
    profile: Dict[str, Any],
    completed_nodes: Set[str],
    adaptation_event: Optional[Dict[str, Any]] = None
) -> str:
    """Constructs a grounded, context-rich system prompt with full roadmap details and adaptation provenance."""
    done = completed_nodes
    total_nodes = sum(len(p.get("nodes", [])) for p in roadmap.get("phases", []))
    
    ctx_lines = [
        f"LEARNING FOCUS: {roadmap.get('role', 'Learner')}",
        f"ORIGINAL GOAL: {roadmap.get('goal', '')}",
        f"EXPERIENCE LEVEL: {profile.get('experience_level', 'Intermediate')} | WEEKLY HOURS: {profile.get('weekly_hours', 15)}",
        f"PROGRESS: {len(done)}/{total_nodes} milestones completed",
        "CURRICULUM ROADMAP:"
    ]

    for phase in roadmap.get("phases", []):
        ctx_lines.append(f"  {phase.get('phase', 'Phase')}")
        for n in phase.get("nodes", []):
            is_done = n["id"] in done
            prereqs = n.get("prereqs", [])
            is_ready = (not prereqs or all(p in done for p in prereqs)) and not is_done
            status_tag = "[COMPLETED]" if is_done else ("[UP-NEXT]" if is_ready else "[LOCKED]")
            ctx_lines.append(
                f"    - {n['id']} {status_tag}: {n['title']} ({n.get('type', 'Course')} via {n.get('provider', 'Provider')}, {n.get('duration', '2w')}) "
                f"prereqs={prereqs} | why={n.get('why', '')}"
            )

    if adaptation_event and adaptation_event.get("adapted"):
        ctx_lines.append("\nADAPTIVE REPLANNING EVENT LOG:")
        ctx_lines.append(f"  - Weakness Skill: {adaptation_event.get('skill_topic')}")
        ctx_lines.append(f"  - Assessment Score: {adaptation_event.get('score')}%")
        ctx_lines.append(f"  - Remedial Nodes Inserted: {adaptation_event.get('inserted_nodes')}")
        ctx_lines.append(f"  - Reason: {adaptation_event.get('reason')}")

    roadmap_context = "\n".join(ctx_lines)

    return f"""You are PathFinder Mentor by Team Cortex — an editorial learning advisor and coach.
The student's complete curriculum roadmap and assessment history is provided below. Answer queries strictly anchored in this roadmap context.

{roadmap_context}

RULES:
1. Reference specific module IDs (e.g. "AI101", "REM101", "AI302") and titles when guiding.
2. Structure responses cleanly with uppercase section labels: TODAY, WHY, NEXT.
3. If asked why the roadmap changed, explain the assessment score and why the remedial milestones were inserted.
4. Keep responses concise, professional, and practical (under 120 words).
5. Never use emojis or decorative symbols.
"""


def render_ai_mentor_chat(
    roadmap: Dict[str, Any],
    profile: Dict[str, Any],
    completed_nodes: Set[str],
    provider: str,
    model_name: str,
    groq_api_key: str = "",
    gemini_api_key: str = "",
    adaptation_event: Optional[Dict[str, Any]] = None
) -> None:
    """Renders the PathFinder Mentor conversational window with rock-solid state preservation."""
    # Ensure chat history is canonically initialized
    if "chat_history" not in st.session_state or not st.session_state.chat_history:
        st.session_state.chat_history = [{
            "role": "assistant",
            "content": WELCOME_MESSAGE
        }]

    # Header and Clear Chat control
    head_c1, head_c2 = st.columns([3.5, 1.2], vertical_alignment="center")
    with head_c1:
        st.markdown("""
        <div style="font-size:11px; font-weight:650; text-transform:uppercase; letter-spacing:0.08em; color:#858585; margin-bottom:2px;">
            PathFinder Mentor
        </div>
        <div style="font-size:12.5px; color:#4B4B4B;">
            Context-aware learning advisor grounded in your active roadmap.
        </div>
        """, unsafe_allow_html=True)
    with head_c2:
        if st.button("Clear History", key="btn_clear_chat", use_container_width=True):
            st.session_state.chat_history = [{
                "role": "assistant",
                "content": WELCOME_MESSAGE
            }]
            persist_state()
            st.rerun()

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # Action prompt links (Suggested chips)
    chip_cols = st.columns(len(SUGGESTED_PROMPTS))
    prompt_to_send = None
    for idx, prompt_text in enumerate(SUGGESTED_PROMPTS):
        with chip_cols[idx]:
            if st.button(prompt_text, key=f"chip_{idx}", use_container_width=True):
                prompt_to_send = prompt_text

    # Form with input + submit button
    with st.form("mentor_chat_form", clear_on_submit=True):
        f_col1, f_col2 = st.columns([4.2, 1.1], vertical_alignment="center")
        with f_col1:
            typed_prompt = st.text_input(
                "Ask PathFinder Mentor",
                placeholder="Ask about prerequisites, study plans, or skill gaps...",
                label_visibility="collapsed"
            )
        with f_col2:
            send_clicked = st.form_submit_button("Send →", type="primary", use_container_width=True)

    active_prompt = prompt_to_send or (typed_prompt.strip() if send_clicked and typed_prompt and typed_prompt.strip() else None)

    # Process prompt before rendering message history
    if active_prompt:
        st.session_state.chat_history.append({"role": "user", "content": active_prompt})

        system_prompt = build_mentor_system_prompt(roadmap, profile, completed_nodes, adaptation_event)
        g_key = groq_api_key or os.environ.get("GROQ_API_KEY", "")
        gem_key = gemini_api_key or os.environ.get("GEMINI_API_KEY", "")

        assistant_reply = ""
        try:
            if provider == "Groq" and g_key and HAS_GROQ:
                messages = [{"role": "system", "content": system_prompt}]
                messages.extend(st.session_state.chat_history[-15:])
                stream_gen = stream_groq_chat_response(messages, g_key, model_name)
                assistant_reply = "".join(list(stream_gen))
            elif provider == "Google Gemini" and gem_key and HAS_GEMINI:
                messages = [{"role": "system", "content": system_prompt}]
                messages.extend(st.session_state.chat_history[-15:])
                stream_gen = stream_gemini_chat_response(messages, gem_key, model_name)
                assistant_reply = "".join(list(stream_gen))
            else:
                stream_gen = generate_offline_streaming_mentor_reply(
                    active_prompt, roadmap, profile, completed_nodes, adaptation_event
                )
                assistant_reply = "".join(list(stream_gen))
        except Exception:
            assistant_reply = f"I am guiding your learning path for **{roadmap.get('role', 'your chosen role')}**. Focus on your immediate unlocked prerequisites in the Learning Path tab."

        if not assistant_reply:
            assistant_reply = f"I am guiding your learning path for **{roadmap.get('role', 'your chosen role')}**. Focus on your immediate unlocked prerequisites in the Learning Path tab."

        st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
        st.session_state.chat_history = st.session_state.chat_history[-40:]
        persist_state()

    # Render complete chat history in container
    chat_container = st.container(height=340)
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
