"""Intelligent multi-model router and unified generation interface."""

import os
from typing import Dict, Any, Generator, List, Optional
import streamlit as st

from engine.groq_engine import generate_roadmap_with_groq, stream_groq_chat_response, HAS_GROQ
from engine.gemini_engine import generate_roadmap_with_gemini, stream_gemini_chat_response, HAS_GEMINI
from engine.fallback_data import generate_fallback_roadmap

def generate_unified_roadmap(
    goal: str,
    profile: Dict[str, Any],
    provider: str,
    model_name: str,
    groq_api_key: Optional[str] = None,
    gemini_api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Generates roadmap by routing to the appropriate engine."""
    g_key = groq_api_key or os.environ.get("GROQ_API_KEY", "")
    gem_key = gemini_api_key or os.environ.get("GEMINI_API_KEY", "")

    if provider == "Groq" and g_key and HAS_GROQ:
        return generate_roadmap_with_groq(goal, profile, g_key, model_name)
    elif provider == "Google Gemini" and gem_key and HAS_GEMINI:
        return generate_roadmap_with_gemini(goal, profile, gem_key, model_name)
    else:
        return generate_fallback_roadmap(goal, profile)


def generate_offline_streaming_mentor_reply(
    user_prompt: str,
    roadmap: Dict[str, Any],
    profile: Dict[str, Any],
    completed_nodes: set
) -> Generator[str, None, None]:
    """Generates a roadmap-grounded response with word-by-word streaming animation when offline."""
    import time
    
    q = user_prompt.lower()
    done = completed_nodes
    next_node, next_phase = None, None

    for phase in roadmap.get("phases", []):
        for n in phase.get("nodes", []):
            if n["id"] not in done and (not n.get("prereqs") or all(p in done for p in n.get("prereqs", []))):
                next_node, next_phase = n, phase.get("phase", "Active Phase")
                break
        if next_node:
            break

    if any(k in q for k in ("why", "recommend", "reason", "rationale")):
        reply = (
            f"Your custom curriculum is precision-calibrated for **{roadmap.get('role', 'your goal')}** "
            f"at **{profile.get('experience_level', 'Intermediate')}** level. "
            f"Each node systematically eliminates skill gaps. Inspect any node in the **Interactive DAG** "
            f"or the **Explainable AI (XAI)** tab for exact scoring breakdowns."
        )
    elif any(k in q for k in ("next", "start", "what now", "todo", "do first", "action")):
        if next_node:
            reply = (
                f"🎯 Your next unblocked milestone is **{next_node['id']}: {next_node['title']}** "
                f"({next_node['duration']}, via *{next_node['provider']}*) in _{next_phase}_.\n\n"
                f"**Why this milestone:** {next_node.get('why', 'Core required competency.')}\n\n"
                f"Recommended weekly pace: dedicate ~{max(2, profile.get('weekly_hours', 15) // 3)} hrs/week."
            )
        else:
            reply = "🎉 **Outstanding achievement!** You have completed all milestones on this learning path! Generate a fresh goal to start your next journey."
    elif any(k in q for k in ("plan", "schedule", "routine", "hours", "time")):
        reply = (
            f"Based on your commitment of **{profile.get('weekly_hours', 15)} hours/week**, we recommend breaking study into "
            f"3-4 focused sessions of 3-4 hours each. Allocate 60% of time to active hands-on projects and 40% to foundational lessons."
        )
    else:
        if next_node:
            reply = (
                f"For **'{user_prompt.strip()}'**: Maintain focus on your current unblocked target: "
                f"**{next_node['id']}: {next_node['title']}** ({next_node['duration']}). "
                f"Completing this milestone directly fulfills prerequisites for downstream Phase 2/3 milestones."
            )
        else:
            reply = f"For **'{user_prompt.strip()}'**: All nodes in this roadmap are mastered! Feel free to pick a new domain or expand your skills."

    # Yield words one-by-one to create a smooth, responsive typewriter animation
    words = reply.split(" ")
    for i, word in enumerate(words):
        yield word + (" " if i < len(words) - 1 else "")
        time.sleep(0.018)  # Natural typing cadence
