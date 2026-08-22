"""Curated course and project recommendation cards component."""

from typing import Dict, Any, Set
import streamlit as st

from core.state import persist_state
from engine.re_router import get_node_status

def render_recommendation_cards(roadmap: Dict[str, Any], completed_nodes: Set[str]) -> None:
    """Renders structured recommendation cards with interactive completion toggles."""
    st.subheader("📚 Pillar 3: Curated Course & Project Recommendations")
    st.caption("Structured course modules and hands-on projects with provider details, duration, prerequisite status, and completion triggers.")

    for phase in roadmap.get("phases", []):
        st.markdown(f"### {phase.get('phase', 'Phase')}")

        for node in phase.get("nodes", []):
            node_id = node.get("id", "")
            is_done = node_id in completed_nodes
            status = get_node_status(node, completed_nodes)
            prereqs_met = (status != "locked")

            c_card, c_action = st.columns([4, 1])

            with c_card:
                badge_type = "badge-success" if node.get("type") == "Course" else "badge-purple"
                card_class = "course-card course-card-completed" if is_done else "course-card"
                skills_html = " ".join([f"<span class='badge badge-primary'>#{s}</span>" for s in node.get("skills", [])])
                
                status_badge = (
                    "<span class='badge badge-success'>✓ Completed</span>" if is_done
                    else "<span class='badge badge-primary'>▶ Ready to Start</span>" if prereqs_met
                    else "<span class='badge badge-muted'>🔒 Locked</span>"
                )

                st.markdown(f"""
                <div class="{card_class}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span class="badge {badge_type}">{node.get('type', 'Course')}</span>
                            <span class="badge badge-warning">🏢 {node.get('provider', 'Online')}</span>
                            <span class="badge badge-warning">⏱️ {node.get('duration', '2 weeks')}</span>
                        </div>
                        {status_badge}
                    </div>
                    <div class="course-title">{node_id}: {node.get('title', '')}</div>
                    <p style="color: #a1a1aa; font-size: 0.92rem; margin: 6px 0 8px 0; line-height: 1.5;">
                        {node.get('why', 'Key milestone on your personalized learning pathway.')}
                    </p>
                    <div style="margin-top: 4px;">
                        {skills_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c_action:
                st.write(" ")
                st.write(" ")
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
                        persist_state()
                        st.toast(f"🎉 Milestone Completed: {node.get('title')}!", icon="✅")
                        st.rerun()

                if not prereqs_met:
                    st.caption(f"🔒 Prereqs required: {', '.join(node.get('prereqs', []))}")
