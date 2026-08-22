"""Curated course and project recommendation cards component."""

from typing import Dict, Any, Set
import streamlit as st

from core.state import persist_state
from engine.re_router import get_node_status

def render_recommendation_cards(roadmap: Dict[str, Any], completed_nodes: Set[str]) -> None:
    """Renders structured recommendation cards with interactive completion toggles."""
    st.markdown("### Actionable Milestones & Projects")
    st.caption("Curated courses, practical projects, and assessments sequenced by prerequisite readiness.")

    for phase in roadmap.get("phases", []):
        st.markdown(f"#### {phase.get('phase', 'Phase')}")

        for node in phase.get("nodes", []):
            node_id = node.get("id", "")
            is_done = node_id in completed_nodes
            status = get_node_status(node, completed_nodes)
            prereqs_met = (status != "locked")

            c_card, c_action = st.columns([4.2, 1])

            with c_card:
                card_class = "module-item completed" if is_done else "module-item"
                skills_html = " ".join([f"<span class='tag tag-blue'>#{s}</span>" for s in node.get("skills", [])])
                
                status_tag = (
                    "<span class='tag tag-emerald'>✓ Mastered</span>" if is_done
                    else "<span class='tag tag-indigo'>▶ Unlocked</span>" if prereqs_met
                    else "<span class='tag tag-slate'>🔒 Locked</span>"
                )

                st.markdown(f"""
                <div class="{card_class}">
                    <div class="module-header">
                        <div>
                            <span class="tag tag-indigo">{node.get('type', 'Course')}</span>
                            <span class="tag tag-amber">⏱️ {node.get('duration', '2 weeks')}</span>
                            <span class="tag tag-slate">🏢 {node.get('provider', 'Online')}</span>
                        </div>
                        {status_tag}
                    </div>
                    <div class="module-title">{node_id}: {node.get('title', '')}</div>
                    <div class="module-why">{node.get('why', 'Key competency on your customized roadmap.')}</div>
                    <div>{skills_html}</div>
                </div>
                """, unsafe_allow_html=True)

            with c_action:
                st.write(" ")
                st.write(" ")
                if is_done:
                    if st.button("✓ Mastered", key=f"rec_undo_{node_id}", use_container_width=True):
                        completed_nodes.remove(node_id)
                        persist_state()
                        st.rerun()
                else:
                    if st.button(
                        "Mark Complete",
                        key=f"rec_done_{node_id}",
                        type="primary",
                        disabled=not prereqs_met,
                        use_container_width=True
                    ):
                        completed_nodes.add(node_id)
                        persist_state()
                        st.toast(f"Milestone Mastered: {node.get('title')}!", icon="🎉")
                        st.rerun()

                if not prereqs_met:
                    st.caption(f"Requires: {', '.join(node.get('prereqs', []))}")
