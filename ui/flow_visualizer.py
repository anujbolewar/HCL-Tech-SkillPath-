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
    st.subheader("🔀 Prerequisite-Aware Directed Acyclic Graph (DAG) Canvas")
    st.caption("Interactive 2D React Flow canvas powered by `streamlit-flow-component` with drag, pan, zoom, and prerequisite animations.")

    all_nodes_dict: Dict[str, Dict[str, Any]] = {}
    node_phase_map: Dict[str, int] = {}
    
    total_phases = len(roadmap.get("phases", []))
    for p_idx, phase in enumerate(roadmap.get("phases", [])):
        for node in phase.get("nodes", []):
            all_nodes_dict[node["id"]] = node
            node_phase_map[node["id"]] = p_idx

    selected_node_id = st.session_state.get("selected_node_id")

    if HAS_STREAMLIT_FLOW:
        flow_nodes = []
        flow_edges = []

        for phase_idx, phase in enumerate(roadmap.get("phases", [])):
            for node_idx, node in enumerate(phase.get("nodes", [])):
                node_id = node["id"]
                status = get_node_status(node, completed_nodes)
                
                pos_x = phase_idx * 300
                pos_y = node_idx * 140 - 30

                if status == "completed":
                    status_tag = "✓ DONE"
                elif status == "ready":
                    status_tag = "▶ READY"
                else:
                    status_tag = "🔒 LOCKED"

                label = f"{node_id}: {node['title']}\n({node.get('duration', '2w')}) [{status_tag}]"

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

        flow_col, side_ctrl = st.columns([3, 1])
        with side_ctrl:
            st.markdown("#### 🎯 Quick Node Picker")
            node_options = ["None (Select a node)"] + list(all_nodes_dict.keys())
            curr_idx = 0
            if selected_node_id in all_nodes_dict:
                curr_idx = node_options.index(selected_node_id)
            
            picked = st.selectbox(
                "Inspect Node 'Why':",
                node_options,
                index=curr_idx,
                help="Select any node to view its Explainable AI rationale and skill gap breakdown."
            )
            if picked != "None (Select a node)":
                selected_node_id = picked
                st.session_state.selected_node_id = picked

        with flow_col:
            event = streamlit_flow(
                key="learning_path_flow",
                state=flow_state,
                height=450,
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
        # Fallback to Graphviz visualization
        dot = graphviz.Digraph(comment="Learning Path DAG", graph_attr={"rankdir": "LR", "bgcolor": "transparent"})
        dot.attr("node", shape="box", style="filled,rounded", fontname="Inter", fontsize="11")

        for phase_idx, phase in enumerate(roadmap.get("phases", [])):
            with dot.subgraph(name=f"cluster_{phase_idx}") as c:
                c.attr(label=phase.get("phase", ""), color="#4facfe", style="dashed", fontcolor="#00f2fe")
                for node in phase.get("nodes", []):
                    status = get_node_status(node, completed_nodes)
                    if status == "completed":
                        bg_color, text_color, border_color, tag = "#10b981", "#ffffff", "#34d399", "✓ DONE"
                    elif status == "ready":
                        bg_color, text_color, border_color, tag = "#1e293b", "#f3f4f6", "#38bdf8", "▶ READY"
                    else:
                        bg_color, text_color, border_color, tag = "#0f172a", "#94a3b8", "#475569", "🔒 LOCKED"

                    label_text = f"{node['id']}: {node['title']}\\n({node.get('duration', '')}) [{tag}]"
                    c.node(node["id"], label=label_text, fillcolor=bg_color, fontcolor=text_color, color=border_color, penwidth="2")

                    for prereq in node.get("prereqs", []):
                        dot.edge(prereq, node["id"], color="#38bdf8", penwidth="1.5")

        st.graphviz_chart(dot, width="stretch")

        node_options = ["None (Select a node)"] + list(all_nodes_dict.keys())
        picked = st.selectbox("Inspect Node 'Why':", node_options, index=0)
        if picked != "None (Select a node)":
            selected_node_id = picked
            st.session_state.selected_node_id = picked

    # Render Node Inspector ("Why" is prominently visible upon node selection)
    if selected_node_id and selected_node_id in all_nodes_dict:
        node_obj = all_nodes_dict[selected_node_id]
        p_idx = node_phase_map.get(selected_node_id, 0)
        score, breakdown = compute_node_relevance(
            node_obj, profile, completed_nodes, p_idx, total_phases
        )
        render_node_inspector(node_obj, score, breakdown)
    else:
        st.info("💡 **Click any node in the DAG above** or select from the dropdown to instantly reveal its **Explainable AI (Why)** rationale, prerequisite dependencies, and skill gap coverage!")
