"""Conversational AI Mentor chat interface with structured learning coach responses."""

import os
from typing import Dict, Any, Set, List, Optional
import streamlit as st

from core.state import persist_state
from engine.groq_engine import stream_groq_chat_response, HAS_GROQ
from engine.gemini_engine import stream_gemini_chat_response, HAS_GEMINI
from engine.llm_router import generate_offline_streaming_mentor_reply

SUGGESTED_PROMPTS = [
    "Today's Study Focus",
    "Why Roadmap Changed",
    "Explain Skill Gaps",
    "Weekly Study Plan"
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

    return f"""You are PathFinder Mentor by Team Cortex — a precise, pragmatic learning coach.
The student's complete curriculum roadmap and assessment history is provided below. Answer queries strictly anchored in this roadmap context.

{roadmap_context}

RULES:
1. Reference specific module IDs (e.g. "AI101", "REM101", "AI302") and titles when guiding.
2. Structure responses cleanly with uppercase section labels where helpful (e.g. TODAY'S FOCUS, WHY, NEXT STEP).
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
    """Renders the PathFinder Mentor conversational window in clean light mode."""
    st.markdown("### Mentor")
    st.caption("Context-aware learning coach grounded in your active roadmap and prerequisite progression.")

    # Contextual action chips
    st.markdown("<div style='margin-bottom:8px;'>", unsafe_allow_html=True)
    chip_cols = st.columns(len(SUGGESTED_PROMPTS))
    prompt_to_send = None
    for idx, prompt_text in enumerate(SUGGESTED_PROMPTS):
        with chip_cols[idx]:
            if st.button(prompt_text, key=f"chip_{idx}", use_container_width=True):
                prompt_to_send = prompt_text
    st.markdown("</div>", unsafe_allow_html=True)

    # Capture prompt before container rendering
    typed_prompt = st.chat_input("Ask PathFinder Mentor about prerequisites or study plans...")
    active_prompt = prompt_to_send or typed_prompt

    if active_prompt:
        st.session_state.chat_history.append({"role": "user", "content": active_prompt})

    # Scrollable chat history & active streaming container
    chat_container = st.container(height=340)
    with chat_container:
        for msg in st.session_state.get("chat_history", []):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if active_prompt:
            with st.chat_message("assistant"):
                system_prompt = build_mentor_system_prompt(roadmap, profile, completed_nodes, adaptation_event)
                
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
                        active_prompt, roadmap, profile, completed_nodes, adaptation_event
                    )
                    full_reply = st.write_stream(stream_generator)

            st.session_state.chat_history.append({"role": "assistant", "content": full_reply})
            st.session_state.chat_history = st.session_state.chat_history[-40:]
            persist_state()
