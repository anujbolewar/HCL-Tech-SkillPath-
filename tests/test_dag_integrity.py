"""DAG integrity and topological validation tests."""

from collections import defaultdict, deque
import pytest

from engine.fallback_data import DOMAIN_TEMPLATES, generate_fallback_roadmap
from engine.re_router import apply_diagnostic_assessment

def has_cycle(nodes_dict: dict) -> bool:
    """Detects if a directed graph contains a cycle using Kahn's algorithm."""
    in_degree = {k: 0 for k in nodes_dict}
    adj = defaultdict(list)

    for node_id, node in nodes_dict.items():
        for prereq in node.get("prereqs", []):
            if prereq in in_degree:
                adj[prereq].append(node_id)
                in_degree[node_id] += 1

    queue = deque([k for k, d in in_degree.items() if d == 0])
    visited_count = 0

    while queue:
        curr = queue.popleft()
        visited_count += 1
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return visited_count != len(nodes_dict)


def test_all_domain_templates_are_strict_dags():
    """Verify all domain templates form strict acyclic graphs without cycles or dangling edges."""
    for template in DOMAIN_TEMPLATES:
        nodes = {n["id"]: n for phase in template["phases"] for n in phase["nodes"]}
        assert len(nodes) == 6, f"{template['role']}: Must have exactly 6 nodes"
        
        # Verify no dangling prereqs
        for node_id, node in nodes.items():
            for prereq in node.get("prereqs", []):
                assert prereq in nodes, f"{template['role']}: Dangling prereq {prereq} in {node_id}"

        # Verify no cycles
        assert not has_cycle(nodes), f"{template['role']}: Contains a cyclic dependency"


def test_universal_scaffolds_are_strict_dags():
    """Verify random custom goal scaffolds form valid acyclic DAGs."""
    test_goals = [
        "Learn Origami art",
        "Master Japanese Kanji",
        "Build a Woodworking Table",
        "Learn Speedcubing 3x3",
        "Train for Ironman Triathlon"
    ]
    for goal in test_goals:
        rm = generate_fallback_roadmap(goal, {"weekly_hours": 12})
        nodes = {n["id"]: n for phase in rm["phases"] for n in phase["nodes"]}
        assert len(nodes) == 6
        assert not has_cycle(nodes)


def test_apply_diagnostic_assessment_inserts_valid_dag_nodes():
    """Verify adaptive assessment weakness splices valid remedial nodes into DAG without cycles."""
    base_roadmap = generate_fallback_roadmap("Become an AI & Machine Learning Engineer", {"weekly_hours": 15})
    
    adapted_rm, event = apply_diagnostic_assessment(
        roadmap=base_roadmap,
        skill_topic="Retrieval & Vector Search",
        score=42,
        profile={"weekly_hours": 15}
    )

    assert event is not None
    assert event["adapted"] is True
    assert event["score"] == 42
    assert len(event["inserted_nodes"]) == 2

    # Verify total nodes increased by 2
    nodes = {n["id"]: n for phase in adapted_rm["phases"] for n in phase["nodes"]}
    assert len(nodes) == 8
    assert "REM101" in nodes
    assert "REM102" in nodes

    # Verify no dangling prereqs
    for node_id, node in nodes.items():
        for prereq in node.get("prereqs", []):
            assert prereq in nodes, f"Dangling prereq {prereq} in {node_id}"

    # Verify no cycles exist in adapted DAG
    assert not has_cycle(nodes), "Adapted roadmap contains a cyclic dependency"


def test_apply_diagnostic_assessment_high_score_no_remediation():
    """Verify passing diagnostic assessment does not splice unnecessary nodes."""
    base_roadmap = generate_fallback_roadmap("Become an AI & Machine Learning Engineer", {"weekly_hours": 15})
    
    adapted_rm, event = apply_diagnostic_assessment(
        roadmap=base_roadmap,
        skill_topic="Retrieval & Vector Search",
        score=88,
        profile={"weekly_hours": 15}
    )

    assert event is not None
    assert event["adapted"] is False
    nodes = {n["id"]: n for phase in adapted_rm["phases"] for n in phase["nodes"]}
    assert len(nodes) == 6
    assert "REM101" not in nodes
