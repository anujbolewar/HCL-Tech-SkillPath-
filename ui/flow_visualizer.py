"""Prerequisite-Aware Directed Acyclic Graph (DAG) visualizer using Streamlit Flow."""

from typing import Dict, Any, Set, Optional, List
import streamlit as st
import graphviz

from engine.xai_scorer import compute_node_relevance
from engine.re_router import get_node_status
from ui.components import render_node_inspector

try:
    from streamlit_flow import streamlit_flow
    from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
    from streamlit_flow.state import StreamlitFlowState
    from streamlit_flow.layouts import TreeLayout
    HAS_STREAMLIT_FLOW = True
except ImportError:
    HAS_STREAMLIT_FLOW = False


def render_dag_flowchart(
    roadmap: Dict[str, Any],
    completed_nodes: Set[str],
    profile: Dict[str, Any]
) -> None:
    """Renders the interactive React Flow DAG canvas and node inspector."""
    all_nodes_dict: Dict[str, Dict[str, Any]] = {}
    node_phase_map: Dict[str, int] = {}
    
    total_phases = len(roadmap.get("phases", []))
    for p_idx, phase in enumerate(roadmap.get("phases", [])):
        for node in phase.get("nodes", []):
            all_nodes_dict[node["id"]] = node
            node_phase_map[node["id"]] = p_idx

    selected_node_id = st.session_state.get("selected_node_id")

    # Legend Header
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <span style="font-family:'Outfit',sans-serif; font-size:1.05rem; font-weight:600; color:#F8FAFC;">
            Learning Roadmap (DAG)
        </span>
        <div style="display:flex; gap:14px; font-size:0.78rem; color:#94A3B8;">
            <span><span style="color:#34D399; font-weight:700;">●</span> Completed</span>
            <span><span style="color:#60A5FA; font-weight:700;">●</span> Unlocked / Next</span>
            <span><span style="color:#64748B; font-weight:700;">●</span> Locked (Prereqs Pending)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if HAS_STREAMLIT_FLOW:
        flow_nodes = []
        flow_edges = []

        for phase_idx, phase in enumerate(roadmap.get("phases", [])):
            for node_idx, node in enumerate(phase.get("nodes", [])):
                node_id = node["id"]
                status = get_node_status(node, completed_nodes)
                
                pos_x = phase_idx * 290
                pos_y = node_idx * 130 - 20

                if status == "completed":
                    label = f"✓ {node_id}: {node['title']}\n{node.get('duration', '2w')} [Completed]"
                elif status == "ready":
                    label = f"▶ {node_id}: {node['title']}\n{node.get('duration', '2w')} [Unlocked]"
                else:
                    prereq_info = f"Requires {', '.join(node.get('prereqs', []))}"
                    label = f"🔒 {node_id}: {node['title']}\n{prereq_info}"

                flow_node = StreamlitFlowNode(
                    id=node_id,
                    pos=(pos_x, pos_y),
                    data={"content": label},
                    node_type="input" if not node.get("prereqs") else "output" if phase_idx == total_phases - 1 else "default",
                    source_position="right",
                    target_position="left"
                )
                flow_nodes.append(flow_node)

                for prereq in node.get("prereqs", []):
                    edge_id = f"e_{prereq}_{node_id}"
                    flow_edge = StreamlitFlowEdge(
                        id=edge_id,
                        source=prereq,
                        target=node_id,
                        animated=(status == "ready")
                    )
                    flow_edges.append(flow_edge)

        flow_state = StreamlitFlowState(flow_nodes, flow_edges)

        flow_col, side_ctrl = st.columns([3.5, 1], vertical_alignment="top")
        with side_ctrl:
            node_options = ["None (Click node or select)"] + list(all_nodes_dict.keys())
            curr_idx = 0
            if selected_node_id in all_nodes_dict:
                curr_idx = node_options.index(selected_node_id)
            
            picked = st.selectbox(
                "Inspect Node:",
                node_options,
                index=curr_idx,
                label_visibility="collapsed",
                help="Inspect why PathFinder recommended this milestone."
            )
            if picked != "None (Click node or select)":
                selected_node_id = picked
                st.session_state.selected_node_id = picked

        with flow_col:
            event = streamlit_flow(
                key="learning_path_flow",
                state=flow_state,
                height=380,
                fit_view=True,
                show_minimap=True,
                show_controls=True,
                get_node_on_click=True,
                layout=TreeLayout(direction="right")
            )

        # Catch canvas click event
        if event and hasattr(event, "selected_id") and event.selected_id in all_nodes_dict:
            selected_node_id = event.selected_id
            st.session_state.selected_node_id = event.selected_id

    else:
        # Graphviz fallback
        dot = graphviz.Digraph(comment="Learning Path DAG", graph_attr={"rankdir": "LR", "bgcolor": "transparent"})
        dot.attr("node", shape="box", style="filled,rounded", fontname="Inter", fontsize="10")

        for phase_idx, phase in enumerate(roadmap.get("phases", [])):
            with dot.subgraph(name=f"cluster_{phase_idx}") as c:
                c.attr(label=phase.get("phase", ""), color="#334155", style="dashed", fontcolor="#94A3B8")
                for node in phase.get("nodes", []):
                    status = get_node_status(node, completed_nodes)
                    if status == "completed":
                        bg_color, text_color, border_color, tag = "#064E3B", "#FFFFFF", "#059669", "✓"
                    elif status == "ready":
                        bg_color, text_color, border_color, tag = "#1E293B", "#F8FAFC", "#3B82F6", "▶"
                    else:
                        bg_color, text_color, border_color, tag = "#0F1626", "#64748B", "#334155", "🔒"

                    label_text = f"{tag} {node['id']}: {node['title']}\\n{node.get('duration', '')}"
                    c.node(node["id"], label=label_text, fillcolor=bg_color, fontcolor=text_color, color=border_color, penwidth="1.5")

                    for prereq in node.get("prereqs", []):
                        dot.edge(prereq, node["id"], color="#3B82F6", penwidth="1.2")

        st.graphviz_chart(dot, width="stretch")

        node_options = ["None (Select node)"] + list(all_nodes_dict.keys())
        picked = st.selectbox("Inspect Node:", node_options, index=0)
        if picked != "None (Select node)":
            selected_node_id = picked
            st.session_state.selected_node_id = picked

    # Node Inspector
    if selected_node_id and selected_node_id in all_nodes_dict:
        node_obj = all_nodes_dict[selected_node_id]
        p_idx = node_phase_map.get(selected_node_id, 0)
        score, breakdown = compute_node_relevance(
            node_obj, profile, completed_nodes, p_idx, total_phases
        )
        render_node_inspector(node_obj, score, breakdown)
