"""Curated course and project recommendation cards component with typographic metadata."""

from typing import Dict, Any, Set
import streamlit as st

from core.state import persist_state
from engine.re_router import get_node_status
from ui.components import clean_html

def render_recommendation_cards(roadmap: Dict[str, Any], completed_nodes: Set[str]) -> None:
    """Renders structured recommendation cards with single status indicators and clean metadata."""
    st.markdown("### Actionable Milestones & Projects")
    st.caption("Curated courses and practical capstone projects sequenced by prerequisite dependencies.")

    for phase in roadmap.get("phases", []):
        st.markdown(f"#### {phase.get('phase', 'Phase')}")

        for node in phase.get("nodes", []):
            node_id = node.get("id", "")
            is_done = node_id in completed_nodes
            status = get_node_status(node, completed_nodes)
            prereqs_met = (status != "locked")

            c_card, c_action = st.columns([4.2, 1], vertical_alignment="center")

            with c_card:
                card_class = (
                    "milestone-card completed" if is_done
                    else "milestone-card active" if prereqs_met
                    else "milestone-card locked"
                )

                status_html = (
                    "<span class=\"status-tag status-completed\">✓ Completed</span>" if is_done
                    else "<span class=\"status-tag status-active\">▶ Unlocked</span>" if prereqs_met
                    else "<span class=\"status-tag status-locked\">🔒 Locked</span>"
                )

                skills_str = " · ".join(node.get("skills", []))
                n_title = node.get('title', '')
                n_prov = node.get('provider', 'Online')
                n_dur = node.get('duration', '2 weeks')
                n_type = node.get('type', 'Course')
                n_why = node.get('why', 'Core required competency on your roadmap.')

                card_html = f"""
                <div class="{card_class}">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <div class="milestone-title">{node_id}: {n_title}</div>
                        {status_html}
                    </div>
                    <div class="milestone-meta">
                        {n_prov} · <strong>{n_dur}</strong> · {n_type}
                    </div>
                    <div class="milestone-why">
                        {n_why}
                    </div>
                    <div style="font-size:0.8rem; color:#64748B; margin-top:4px;">
                        Skills: {skills_str}
                    </div>
                </div>
                """
                st.markdown(clean_html(card_html), unsafe_allow_html=True)

            with c_action:
                if is_done:
                    if st.button("✓ Completed", key=f"rec_undo_{node_id}", use_container_width=True):
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
                        st.session_state["_last_completed_title"] = node.get('title')
                        st.session_state["_show_replan_banner"] = True
                        persist_state()
                        st.rerun()

                if not prereqs_met:
                    st.caption(f"Requires: {', '.join(node.get('prereqs', []))}")
