"""DAG integrity and topological validation tests."""

from collections import defaultdict, deque
import pytest

from engine.fallback_data import DOMAIN_TEMPLATES, generate_fallback_roadmap

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
