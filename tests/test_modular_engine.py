"""Comprehensive test suite for modular engine, routing, persistence, and exports."""

import json
from pathlib import Path
import pytest

from core.types import RoadmapNode, RoadmapPhase, RoadmapData, LearnerProfile
from core.config import DEMO_PERSONAS, QUICK_PICKS, GROQ_MODEL_CATALOG, GEMINI_MODEL_CATALOG
from core.state import STATE_FILE, persist_state, clear_persisted_state
from engine.fallback_data import generate_fallback_roadmap, DOMAIN_TEMPLATES
from engine.xai_scorer import compute_node_relevance
from engine.re_router import get_node_status, find_next_recommended_action, calculate_progress_stats
from engine.llm_router import generate_unified_roadmap, generate_offline_streaming_mentor_reply
from ui.export_generator import build_markdown_export, build_printable_html_export

PROFILE = {
    "target_role": "AI & ML Engineer",
    "experience_level": "Intermediate",
    "skills": ["Python", "Basic Math", "SQL"],
    "weekly_hours": 15,
}

def test_all_demo_personas_generate_valid_curriculums():
    """Verify all 5 evaluation personas produce valid roadmaps."""
    for p_name, p_data in DEMO_PERSONAS.items():
        rm = generate_fallback_roadmap(p_data["goal"], p_data["profile"])
        assert "role" in rm
        assert len(rm["phases"]) == 3
        total_nodes = sum(len(p["nodes"]) for p in rm["phases"])
        assert total_nodes == 6

def test_all_quick_picks_generate_valid_curriculums():
    """Verify all 12 quick picks produce valid roadmaps."""
    for label, query in QUICK_PICKS.items():
        rm = generate_fallback_roadmap(query, PROFILE)
        assert len(rm["phases"]) == 3
        total_nodes = sum(len(p["nodes"]) for p in rm["phases"])
        assert total_nodes == 6

def test_node_status_transitions():
    """Verify ready/locked/completed transitions based on prerequisites."""
    rm = generate_fallback_roadmap("AI & ML Engineer", PROFILE)
    phase1_node = rm["phases"][0]["nodes"][0]
    phase2_node = rm["phases"][1]["nodes"][0]  # Requires phase 1

    # Initially phase 1 is ready, phase 2 is locked
    assert get_node_status(phase1_node, set()) == "ready"
    assert get_node_status(phase2_node, set()) == "locked"

    # When phase 1 is completed, phase 1 is completed and phase 2 is ready
    completed = {phase1_node["id"], rm["phases"][0]["nodes"][1]["id"]}
    assert get_node_status(phase1_node, completed) == "completed"
    assert get_node_status(phase2_node, completed) == "ready"

def test_find_next_recommended_action():
    """Verify dynamic next action recommendation correctly identifies the first ready node."""
    rm = generate_fallback_roadmap("AI & ML Engineer", PROFILE)
    
    # Initially recommends the first unblocked Phase 1 node
    first_action = find_next_recommended_action(rm, set())
    assert first_action is not None
    node, phase_title = first_action
    assert node["id"] == rm["phases"][0]["nodes"][0]["id"]

    # When all completed, returns None
    all_node_ids = {n["id"] for p in rm["phases"] for n in p["nodes"]}
    assert find_next_recommended_action(rm, all_node_ids) is None

def test_calculate_progress_stats():
    """Verify progress statistics calculation."""
    rm = generate_fallback_roadmap("AI & ML Engineer", PROFILE)
    stats_empty = calculate_progress_stats(rm, set())
    assert stats_empty["progress_pct"] == 0
    assert stats_empty["is_complete"] is False

    all_node_ids = {n["id"] for p in rm["phases"] for n in p["nodes"]}
    stats_full = calculate_progress_stats(rm, all_node_ids)
    assert stats_full["progress_pct"] == 100
    assert stats_full["is_complete"] is True

def test_offline_streaming_mentor_reply():
    """Verify offline streaming mentor produces words and mentions roadmap context."""
    rm = generate_fallback_roadmap("AI & ML Engineer", PROFILE)
    stream = generate_offline_streaming_mentor_reply(
        "What should I do next?", rm, PROFILE, set()
    )
    full_text = "".join(list(stream))
    assert len(full_text) > 20
    assert "AI101" in full_text or "next" in full_text.lower()

def test_export_generators():
    """Verify Markdown and HTML exports are formatted and complete."""
    rm = generate_fallback_roadmap("AI & ML Engineer", PROFILE)
    completed = {"AI101"}
    
    # Markdown
    md = build_markdown_export(rm, completed, 16)
    assert "# 🎓 Personalized Learning Path" in md
    assert "AI101" in md
    assert "✅ Completed" in md

    # HTML
    html = build_printable_html_export(rm, completed, 16)
    assert "<!DOCTYPE html>" in html
    assert "AI101" in html
    assert "16%" in html
