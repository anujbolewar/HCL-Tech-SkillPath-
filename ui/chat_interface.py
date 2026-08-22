"""Conversational AI Mentor chat interface with word-by-word streaming animations."""

import os
from typing import Dict, Any, Set, List
import streamlit as st

from core.state import persist_state
from engine.groq_engine import stream_groq_chat_response, HAS_GROQ
from engine.gemini_engine import stream_gemini_chat_response, HAS_GEMINI
from engine.llm_router import generate_offline_streaming_mentor_reply

SUGGESTED_PROMPTS = [
    "👉 What should I learn today?",
    "💡 Why was my Phase 2 project chosen?",
    "🔍 Explain my skill gaps",
    "📅 Plan weekly study schedule"
]

def build_mentor_system_prompt(roadmap: Dict[str, Any], profile: Dict[str, Any], completed_nodes: Set[str]) -> str:
    """Constructs a grounded, context-rich system prompt with full roadmap details."""
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
            status_tag = "[COMPLETED]" if is_done else ("[NEXT-UNBLOCKED]" if is_ready else "[LOCKED]")
            ctx_lines.append(
                f"    - {n['id']} {status_tag}: {n['title']} ({n.get('type', 'Course')} via {n.get('provider', 'Provider')}, {n.get('duration', '2w')}) "
                f"prereqs={prereqs} | why={n.get('why', '')}"
            )

    roadmap_context = "\n".join(ctx_lines)

    return f"""You are PathFinder Mentor by Team Cortex — an expert, pragmatic curriculum tutor.
The student's COMPLETE personalized roadmap is provided below. Answer queries STRICTLY anchored in this roadmap context.

{roadmap_context}

RULES:
1. Reference specific module IDs (e.g. "AI101", "FS201") and titles when guiding.
2. If asked what to do next, point directly to the FIRST [NEXT-UNBLOCKED] milestone and explain its rationale.
3. Keep responses compact, friendly, and practical (under 120 words).
4. Use clean Markdown bullet points where appropriate.
"""


def render_ai_mentor_chat(
    roadmap: Dict[str, Any],
    profile: Dict[str, Any],
    completed_nodes: Set[str],
    provider: str,
    model_name: str,
    groq_api_key: str = "",
    gemini_api_key: str = ""
) -> None:
    """Renders the PathFinder Mentor conversational window with real-time streaming."""
    st.markdown("### PathFinder Mentor")
    st.caption("Context-aware AI tutor grounded in your active roadmap and prerequisite progression.")

    # Contextual action chips
    st.markdown("<div style='margin-bottom:8px;'>", unsafe_allow_html=True)
    chip_cols = st.columns(len(SUGGESTED_PROMPTS))
    prompt_to_send = None
    for idx, prompt_text in enumerate(SUGGESTED_PROMPTS):
        with chip_cols[idx]:
            if st.button(prompt_text, key=f"chip_{idx}", use_container_width=True):
                prompt_to_send = prompt_text
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat history display container
    chat_container = st.container(height=320)
    with chat_container:
        for msg in st.session_state.get("chat_history", []):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # User input
    typed_prompt = st.chat_input("Ask PathFinder Mentor about prerequisites or study plans...")
    active_prompt = prompt_to_send or typed_prompt

    if active_prompt:
        st.session_state.chat_history.append({"role": "user", "content": active_prompt})
        
        with st.chat_message("user"):
            st.markdown(active_prompt)

        with st.chat_message("assistant"):
            system_prompt = build_mentor_system_prompt(roadmap, profile, completed_nodes)
            
            g_key = groq_api_key or os.environ.get("GROQ_API_KEY", "")
            gem_key = gemini_api_key or os.environ.get("GEMINI_API_KEY", "")

            # Stream response word-by-word
            if provider == "Groq" and g_key and HAS_GROQ:
                messages = [{"role": "system", "content": system_prompt}]
                messages.extend(st.session_state.chat_history[-15:])
                stream_generator = stream_groq_chat_response(messages, g_key, model_name)
                full_reply = st.write_stream(stream_generator)
            elif provider == "Google Gemini" and gem_key and HAS_GEMINI:
                messages = [{"role": "system", "content": system_prompt}]
                messages.extend(st.session_state.chat_history[-15:])
                stream_generator = stream_gemini_chat_response(messages, gem_key, model_name)
                full_reply = st.write_stream(stream_generator)
            else:
                stream_generator = generate_offline_streaming_mentor_reply(
                    active_prompt, roadmap, profile, completed_nodes
                )
                full_reply = st.write_stream(stream_generator)

        st.session_state.chat_history.append({"role": "assistant", "content": full_reply})
        st.session_state.chat_history = st.session_state.chat_history[-40:]
        persist_state()
        st.rerun()
