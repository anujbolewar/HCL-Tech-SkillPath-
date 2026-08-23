"""Regression and interaction state tests for PathFinder AI."""

import json
from pathlib import Path
from core.config import DEFAULT_PROFILE, WELCOME_MESSAGE
from core.state import STATE_FILE, persist_state, load_persisted_state, clear_persisted_state
from engine.fallback_data import generate_fallback_roadmap
from engine.llm_router import generate_offline_streaming_mentor_reply
from ui.chat_interface import build_mentor_system_prompt
from engine.re_router import apply_diagnostic_assessment, calculate_progress_stats, find_next_recommended_action

def test_mentor_system_prompt_builder():
    """Verify context-rich system prompt incorporates goal, profile, and adaptation event."""
    rm = generate_fallback_roadmap("AI & ML Engineer", DEFAULT_PROFILE)
    event = {
        "adapted": True,
        "skill_topic": "Retrieval & Vector Search",
        "score": 42,
        "inserted_nodes": [{"id": "REM101", "title": "Retrieval Fundamentals"}],
        "reason": "Score 42% below threshold"
    }
    prompt = build_mentor_system_prompt(rm, DEFAULT_PROFILE, {"AI101"}, event)
    
    assert "AI & ML Engineer" in prompt
    assert "AI101 [COMPLETED]" in prompt
    assert "ADAPTIVE REPLANNING EVENT LOG:" in prompt
    assert "Retrieval & Vector Search" in prompt
    assert "42%" in prompt

def test_mentor_reply_categories():
    """Verify mentor handles different question intents accurately."""
    rm = generate_fallback_roadmap("AI & ML Engineer", DEFAULT_PROFILE)
    
    # 1. Why changed / adaptation
    event = {
        "adapted": True,
        "skill_topic": "Retrieval & Vector Search",
        "score": 42,
        "inserted_nodes": [{"id": "REM101", "title": "Retrieval Fundamentals"}],
        "impacted_node": "AI302",
        "reason": "Below threshold"
    }
    reply_why = "".join(list(generate_offline_streaming_mentor_reply("Why did my roadmap change?", rm, DEFAULT_PROFILE, set(), event)))
    assert "Why Your Roadmap Changed" in reply_why or "42%" in reply_why
    assert "REM101" in reply_why

    # 2. Skill gaps
    reply_gaps = "".join(list(generate_offline_streaming_mentor_reply("Explain my skill gaps", rm, DEFAULT_PROFILE, set(), None)))
    assert "Skill Gap" in reply_gaps or "Phase" in reply_gaps

    # 3. Schedule / study hours
    reply_plan = "".join(list(generate_offline_streaming_mentor_reply("Adjust my plan for 1 hour", rm, DEFAULT_PROFILE, set(), None)))
    assert "Study Schedule" in reply_plan or "hrs/week" in reply_plan

def test_diagnostic_and_progress_recalculation():
    """Verify that applying diagnostic updates progress statistics and unblocks remedial nodes."""
    rm = generate_fallback_roadmap("AI & ML Engineer", DEFAULT_PROFILE)
    updated_rm, event = apply_diagnostic_assessment(rm, "Retrieval & Vector Search", 42)
    
    assert event["adapted"] is True
    node_ids = [n["id"] for p in updated_rm["phases"] for n in p["nodes"]]
    assert "REM101" in node_ids
    assert "REM102" in node_ids

    # Progress stats before and after completing REM101
    stats_0 = calculate_progress_stats(updated_rm, set())
    assert stats_0["completed_count"] == 0

    stats_1 = calculate_progress_stats(updated_rm, {"AI101", "REM101"})
    assert stats_1["completed_count"] == 2
    assert stats_1["progress_pct"] > 0
