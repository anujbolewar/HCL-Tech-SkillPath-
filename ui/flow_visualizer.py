"""Prerequisite-Aware Directed Acyclic Graph (DAG) visualizer using Streamlit Flow."""

from typing import Dict, Any, Set, Optional, List
import streamlit as st
import graphviz

from engine.xai_scorer import compute_node_relevance
from engine.re_router import get_node_status
from ui.components import render_node_inspector, clean_html

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
    """Renders the interactive React Flow DAG canvas with side-by-side node inspector in editorial light mode."""
    all_nodes_dict: Dict[str, Dict[str, Any]] = {}
    node_phase_map: Dict[str, int] = {}
    
    total_phases = len(roadmap.get("phases", []))
    for p_idx, phase in enumerate(roadmap.get("phases", [])):
        for node in phase.get("nodes", []):
            all_nodes_dict[node["id"]] = node
            node_phase_map[node["id"]] = p_idx

    selected_node_id = st.session_state.get("selected_node_id")

    # Legend Header
    legend_html = """
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #EAE9E4; padding-bottom:10px;">
        <span style="font-size:14px; font-weight:650; text-transform:uppercase; letter-spacing:0.06em; color:#858585;">
            Learning Path (Prerequisite DAG)
        </span>
        <div style="display:flex; gap:16px; font-size:12px; color:#4B4B4B;">
            <span><span style="color:#2F7D5A; font-weight:700;">●</span> Completed</span>
            <span><span style="color:#2457D6; font-weight:700;">●</span> Up Next / Unlocked</span>
            <span><span style="color:#858585; font-weight:700;">●</span> Locked (Prerequisites Pending)</span>
        </div>
    </div>
    """
    st.markdown(clean_html(legend_html), unsafe_allow_html=True)

    flow_col, side_ctrl = st.columns([2.3, 1.1], vertical_alignment="top")

    if HAS_STREAMLIT_FLOW:
        flow_nodes = []
        flow_edges = []

        for phase_idx, phase in enumerate(roadmap.get("phases", [])):
            for node_idx, node in enumerate(phase.get("nodes", [])):
                node_id = node["id"]
                status = get_node_status(node, completed_nodes)
                
                pos_x = phase_idx * 260
                pos_y = node_idx * 120 - 20

                if status == "completed":
                    label = f"{node_id}: {node['title']}\n{node.get('duration', '2w')} [Completed]"
                    node_style = {
                        "backgroundColor": "#FFFFFF",
                        "color": "#111111",
                        "border": "1px solid #DDDCD6",
                        "borderLeft": "3.5px solid #2F7D5A",
                        "borderRadius": "6px",
                        "fontSize": "11px",
                        "fontWeight": "500",
                        "padding": "8px 10px",
                        "boxShadow": "0 2px 6px rgba(20,20,20,0.02)"
                    }
                elif status == "ready":
                    label = f"{node_id}: {node['title']}\n{node.get('duration', '2w')} [Up Next]"
                    node_style = {
                        "backgroundColor": "#FFFFFF",
                        "color": "#111111",
                        "border": "1px solid #DDDCD6",
                        "borderLeft": "3.5px solid #2457D6",
                        "borderRadius": "6px",
                        "fontSize": "11px",
                        "fontWeight": "600",
                        "padding": "8px 10px",
                        "boxShadow": "0 3px 10px rgba(36,87,214,0.06)"
                    }
                else:
                    prereq_info = f"Requires {', '.join(node.get('prereqs', []))}"
                    label = f"{node_id}: {node['title']}\n{prereq_info} [Locked]"
                    node_style = {
                        "backgroundColor": "#FAF9F5",
                        "color": "#858585",
                        "border": "1px solid #DDDCD6",
                        "borderRadius": "6px",
                        "fontSize": "11px",
                        "padding": "8px 10px"
                    }

                flow_node = StreamlitFlowNode(
                    id=node_id,
                    pos=(pos_x, pos_y),
                    data={"content": label},
                    node_type="input" if not node.get("prereqs") else "output" if phase_idx == total_phases - 1 else "default",
                    source_position="right",
                    target_position="left",
                    style=node_style
                )
                flow_nodes.append(flow_node)

                for prereq in node.get("prereqs", []):
                    edge_id = f"e_{prereq}_{node_id}"
                    flow_edge = StreamlitFlowEdge(
                        id=edge_id,
                        source=prereq,
                        target=node_id,
                        animated=(status == "ready"),
                        style={"stroke": "#2457D6" if status == "ready" else "#DDDCD6", "strokeWidth": "1.5px"}
                    )
                    flow_edges.append(flow_edge)

        flow_state = StreamlitFlowState(flow_nodes, flow_edges)

        with flow_col:
            event = streamlit_flow(
                key="learning_path_flow",
                state=flow_state,
                height=390,
                fit_view=True,
                show_minimap=True,
                show_controls=True,
                get_node_on_click=True,
                layout=TreeLayout(direction="right"),
                style={"backgroundColor": "#F7F6F2", "border": "1px solid #DDDCD6", "borderRadius": "8px"}
            )

        # Catch canvas click event
        if event and hasattr(event, "selected_id") and event.selected_id in all_nodes_dict:
            selected_node_id = event.selected_id
            st.session_state.selected_node_id = event.selected_id

        with side_ctrl:
            st.markdown("<div style='font-size:11px; font-weight:650; color:#858585; text-transform:uppercase; margin-bottom:6px; letter-spacing:0.06em;'>Module Inspector</div>", unsafe_allow_html=True)
            node_options = ["None (Select or click node)"] + list(all_nodes_dict.keys())
            curr_idx = 0
            if selected_node_id in all_nodes_dict:
                curr_idx = node_options.index(selected_node_id)
            
            picked = st.selectbox(
                "Choose Node:",
                node_options,
                index=curr_idx,
                label_visibility="collapsed",
                help="Inspect rationale and prerequisite requirements for any node."
            )
            if picked != "None (Select or click node)":
                selected_node_id = picked
                st.session_state.selected_node_id = picked

            # Render inspector inside side_ctrl
            if selected_node_id and selected_node_id in all_nodes_dict:
                node_obj = all_nodes_dict[selected_node_id]
                p_idx = node_phase_map.get(selected_node_id, 0)
                score, breakdown = compute_node_relevance(
                    node_obj, profile, completed_nodes, p_idx, total_phases
                )
                render_node_inspector(node_obj, score, breakdown)
            else:
                placeholder_html = """
                <div class="pf-inspector" style="text-align:center; padding:28px 16px; color:#858585;">
                    <div style="font-size:13px; font-weight:600; color:#111111; margin-bottom:4px;">Node Inspector</div>
                    <div style="font-size:12px; line-height:1.45;">Click any node on the roadmap canvas or select from the dropdown to view its prerequisite chain, provider, and relevance score.</div>
                </div>
                """
                st.markdown(clean_html(placeholder_html), unsafe_allow_html=True)

    else:
        # Graceful fallback with Graphviz (Editorial Theme)
        dot = graphviz.Digraph(comment="Learning Path", format="svg")
        dot.attr(rankdir="LR", bgcolor="#F7F6F2", splines="ortho")
        dot.attr("node", fontname="Inter, sans-serif", fontsize="11", style="filled,rounded", shape="box", margin="0.15,0.1")
        dot.attr("edge", color="#DDDCD6", arrowsize="0.75")

        for phase in roadmap.get("phases", []):
            for node in phase.get("nodes", []):
                node_id = node["id"]
                status = get_node_status(node, completed_nodes)
                if status == "completed":
                    dot.node(node_id, f"{node_id}\n{node['title']}", fillcolor="#FFFFFF", color="#2F7D5A", fontcolor="#2F7D5A")
                elif status == "ready":
                    dot.node(node_id, f"{node_id}\n{node['title']}", fillcolor="#FFFFFF", color="#2457D6", fontcolor="#2457D6")
                else:
                    dot.node(node_id, f"{node_id}\n{node['title']}", fillcolor="#FAF9F5", color="#DDDCD6", fontcolor="#858585")

                for prereq in node.get("prereqs", []):
                    edge_color = "#2457D6" if status == "ready" else "#DDDCD6"
                    dot.edge(prereq, node_id, color=edge_color)

        with flow_col:
            st.graphviz_chart(dot, use_container_width=True)
