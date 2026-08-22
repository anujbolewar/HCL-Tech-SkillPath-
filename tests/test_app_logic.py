"""Unit tests for SkillPath AI core logic.

app.py is a Streamlit script (executes UI code on import), so we extract
the pure functions we need via the AST instead of importing the module.
"""
import ast
from pathlib import Path

import pytest

APP = Path(__file__).resolve().parent.parent / "app.py"


def _extract(name):
    """Return the named function from app.py, or None if not defined there."""
    tree = ast.parse(APP.read_text(encoding="utf-8"))
    fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name), None)
    if fn is None:
        return None
    ns = {}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(APP), "exec"), ns)
    return ns[name]


generate_fallback_roadmap = _extract("generate_fallback_roadmap")
compute_node_relevance = _extract("compute_node_relevance")
prioritize_models_for_task = _extract("prioritize_models_for_task")
format_mentor_reply = _extract("format_mentor_reply")
stream_mentor_reply = _extract("stream_mentor_reply")

needs_scorer = pytest.mark.skipif(
    compute_node_relevance is None, reason="scorer lands with the XAI feature branch"
)

needs_model_prioritizer = pytest.mark.skipif(
    prioritize_models_for_task is None, reason="model prioritizer is not available"
)

PROFILE = {
    "target_role": "AI & ML Engineer",
    "experience_level": "Intermediate",
    "skills": ["Python", "Basic Math", "SQL"],
    "weekly_hours": 10,
}


# ---------- fallback roadmap engine ----------

def test_guitar_goal_matches_musician_template():
    rm = generate_fallback_roadmap("I want to learn guitar from scratch", PROFILE)
    assert rm["role"] == "Musician"


def test_unknown_goal_gets_universal_scaffold():
    rm = generate_fallback_roadmap("learn origami cranes", PROFILE)
    assert len(rm["phases"]) == 3
    titles = [n["title"] for p in rm["phases"] for n in p["nodes"]]
    assert any("origami" in t.lower() for t in titles)


def test_roadmap_structure_is_valid_dag():
    for goal in ("data scientist", "web developer", "learn cooking"):
        rm = generate_fallback_roadmap(goal, PROFILE)
        nodes = {n["id"] for p in rm["phases"] for n in p["nodes"]}
        assert len(nodes) == 6, f"{goal}: expected 6 nodes"
        for p in rm["phases"]:
            for n in p["nodes"]:
                for pre in n.get("prereqs", []):
                    assert pre in nodes, f"{goal}: dangling prereq {pre}"


# ---------- relevance scorer ----------

def _score(node, level="Beginner", done=frozenset(), phase_idx=0, total=3):
    return compute_node_relevance(node, {"skills": ["Python"], "experience_level": level}, set(done), phase_idx, total)


@needs_model_prioritizer
def test_roadmap_model_priority_prefers_best_reasoning_model_first():
    ranked, recommended = prioritize_models_for_task(
        ["openai/gpt-oss-20b", "llama-3.3-70b-versatile", "openai/gpt-oss-120b"],
        "roadmap",
    )
    assert ranked[0] == "openai/gpt-oss-120b"
    assert recommended == "openai/gpt-oss-120b"


@needs_model_prioritizer
def test_mentor_model_priority_prefers_faster_chat_model_first():
    ranked, recommended = prioritize_models_for_task(
        ["openai/gpt-oss-120b", "llama-3.3-70b-versatile", "openai/gpt-oss-20b"],
        "mentor",
    )
    assert ranked[0] == "openai/gpt-oss-20b"
    assert recommended == "openai/gpt-oss-20b"


@needs_model_prioritizer
def test_model_priority_keeps_unknown_models_after_preferred_ones():
    ranked, _ = prioritize_models_for_task(["custom/model-x", "openai/gpt-oss-20b"], "mentor")
    assert ranked[0] == "openai/gpt-oss-20b"
    assert ranked[-1] == "custom/model-x"


def test_mentor_message_formatter_adds_clear_structure():
    assert format_mentor_reply is not None
    output = format_mentor_reply(
        "Start with Python basics and keep a 30-minute daily streak.",
        next_step="Python Fundamentals",
        goal="AI & ML Engineer",
    )
    assert "### Next move" in output
    assert "### Why this matters" in output
    assert "### Quick plan" in output
    assert "Python Fundamentals" in output


def test_live_stream_words_are_emitted_in_order():
    assert stream_mentor_reply is not None
    words = list(stream_mentor_reply("Start with Python basics today."))
    assert words[0].startswith("Start")
    assert words[-1].startswith("today.") or words[-1].startswith("today")


@needs_scorer
def test_score_within_bounds_and_int():
    score, breakdown = _score({"id": "X", "skills": ["A"], "prereqs": []})
    assert isinstance(score, int) and 0 <= score <= 100
    assert len(breakdown) == 3


@needs_scorer
def test_entry_node_scores_higher_for_beginners_than_late_locked_nodes():
    early = _score({"skills": ["Linear Algebra"], "prereqs": []}, phase_idx=0)[0]
    late = _score({"skills": [], "prereqs": ["M1"]}, phase_idx=2)[0]
    assert early > late


@needs_scorer
def test_completed_prereqs_raise_readiness_factor():
    locked = _score({"skills": ["Python"], "prereqs": ["M1"]}, done=set())[0]
    ready = _score({"skills": ["Python"], "prereqs": ["M1"]}, done={"M1"})[0]
    assert ready > locked


@needs_scorer
def test_missing_keys_do_not_crash():
    score, breakdown = _score({"id": "Bare"})
    assert 0 <= score <= 100 and len(breakdown) == 3
