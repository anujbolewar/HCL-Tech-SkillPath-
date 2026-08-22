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
    completed_nodes: set,
    adaptation_event: Optional[Dict[str, Any]] = None
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

    has_rem = any(n.get("id") == "REM101" for p in roadmap.get("phases", []) for n in p.get("nodes", []))

    # 1. Direct explanation of dynamic roadmap changes / assessment results
    if any(k in q for k in ("change", "adapted", "updated", "assessment", "weakness", "retrieval")) or "why did" in q:
        if (adaptation_event and adaptation_event.get("adapted")) or has_rem:
            score = adaptation_event.get("score", 42) if adaptation_event else 42
            topic = adaptation_event.get("skill_topic", "Retrieval & Vector Search") if adaptation_event else "Retrieval & Vector Search"
            reply = (
                f"⚡ **Why Your Roadmap Changed:**\n\n"
                f"Your diagnostic assessment on **{topic}** resulted in a score of **{score}%** "
                f"(below the 70% mastery threshold).\n\n"
                f"PathFinder detected a foundational gap and dynamically inserted two remedial milestones:\n"
                f"1. **REM101: Retrieval Fundamentals & Chunking Strategies** (Course · 1 week)\n"
                f"2. **REM102: Vector Search Practice & Hybrid Reranking** (Project · 1 week)\n\n"
                f"These modules must now be completed before unlocking your downstream **Capstone Project**."
            )
        else:
            reply = (
                f"Your roadmap is dynamically generated from your profile goals for **{roadmap.get('role', 'Learner')}**. "
                f"If you take a Diagnostic Assessment on the **Overview** tab, PathFinder will automatically splice in remedial milestones if any skill gap is detected."
            )
    elif any(k in q for k in ("gap", "skill gaps", "weakness", "missing")):
        reply = (
            f"📊 **Skill Gap Diagnosis:**\n\n"
            f"Based on your profile, your verified strengths are **{', '.join(profile.get('skills', ['Foundations']))}**. "
            f"Your primary growth targets across this curriculum are specialized domain competencies in **Phase 2 & Phase 3**. "
            f"Take a diagnostic assessment anytime to test your readiness."
        )
    elif any(k in q for k in ("today", "learn today", "next", "start", "what now", "todo", "do first", "action")):
        if next_node:
            reply = (
                f"🎯 **Your Immediate Focus for Today:**\n\n"
                f"Work on **{next_node['id']}: {next_node['title']}** ({next_node['duration']} via *{next_node['provider']}*) in _{next_phase}_.\n\n"
                f"**Why now:** {next_node.get('why', 'Prerequisites are unlocked and this directly closes a primary skill gap.')}\n\n"
                f"Recommended pace: Dedicate ~{max(2, profile.get('weekly_hours', 15) // 3)} hours today to hands-on exercises."
            )
        else:
            reply = "🎉 **All milestones complete!** You have mastered this entire curriculum roadmap. You can generate a fresh path or adjust your profile."
    elif any(k in q for k in ("plan", "schedule", "routine", "hours", "time")):
        reply = (
            f"📅 **Weekly Study Schedule ({profile.get('weekly_hours', 15)} hrs/week):**\n\n"
            f"- **Mon / Wed (2 hrs each):** Theory and foundational readings.\n"
            f"- **Fri (3 hrs):** Guided coding exercises.\n"
            f"- **Weekend (4 hrs):** Capstone project build & self-assessment."
        )
    else:
        if next_node:
            reply = (
                f"For **'{user_prompt.strip()}'**: Focus on your active unlocked target: "
                f"**{next_node['id']}: {next_node['title']}** ({next_node['duration']}). "
                f"Mastering this module unblocks downstream milestones in your learning tree."
            )
        else:
            reply = f"For **'{user_prompt.strip()}'**: All milestones in this learning path are mastered!"

    # Yield words one-by-one with fast cadence
    words = reply.split(" ")
    for i, word in enumerate(words):
        yield word + (" " if i < len(words) - 1 else "")
        time.sleep(0.005)
