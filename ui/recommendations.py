"""Curated course and project recommendation cards with editorial metadata."""

import html
from typing import Dict, Any, Set
import streamlit as st

from core.state import persist_state
from engine.re_router import get_node_status
from ui.components import clean_html

def render_recommendation_cards(roadmap: Dict[str, Any], completed_nodes: Set[str]) -> None:
    """Renders structured curriculum milestones sequenced by prerequisite dependencies."""
    st.markdown("""
    <div style="font-size:11px; font-weight:650; text-transform:uppercase; letter-spacing:0.08em; color:#858585; margin: 16px 0 4px 0;">
        Actionable Curriculum Milestones
    </div>
    <div style="font-size:12.5px; color:#4B4B4B; margin-bottom:14px;">
        Curated courses and practical projects sequenced by prerequisite dependencies.
    </div>
    """, unsafe_allow_html=True)

    for phase in roadmap.get("phases", []):
        p_name = html.escape(phase.get('phase', 'Phase'))
        st.markdown(f"<div style='font-size:14px; font-weight:650; color:#111111; margin: 14px 0 8px 0; letter-spacing:-0.01em;'>{p_name}</div>", unsafe_allow_html=True)

        for node in phase.get("nodes", []):
            node_id = html.escape(node.get("id", ""))
            is_done = node_id in completed_nodes
            is_remedial = node_id.startswith("REM")
            status = get_node_status(node, completed_nodes)
            prereqs_met = (status != "locked")

            c_card, c_action = st.columns([4.2, 1.2], vertical_alignment="center")

            with c_card:
                card_class = (
                    "pf-milestone pf-milestone-completed" if is_done
                    else "pf-milestone pf-milestone-new" if is_remedial
                    else "pf-milestone pf-milestone-ready" if prereqs_met
                    else "pf-milestone pf-milestone-locked"
                )

                status_html = (
                    "<span style=\"color:#2F7D5A; font-weight:600; font-size:11px; background:#F2F7F4; border:1px solid #D1E7DD; padding:1px 7px; border-radius:3px;\">Completed</span>" if is_done
                    else "<span style=\"color:#C58A35; font-weight:600; font-size:11px; background:#FDF9F2; border:1px solid #F6E6CC; padding:1px 7px; border-radius:3px;\">NEW</span>" if is_remedial
                    else "<span style=\"color:#2457D6; font-weight:600; font-size:11px; background:#EFF4FE; border:1px solid #D6E4FC; padding:1px 7px; border-radius:3px;\">Up Next</span>" if prereqs_met
                    else "<span style=\"color:#858585; font-size:11px; background:#F7F6F2; border:1px solid #DDDCD6; padding:1px 7px; border-radius:3px;\">Locked</span>"
                )

                skills_str = " · ".join(html.escape(s) for s in node.get("skills", []))
                n_title = html.escape(node.get('title', ''))
                n_prov = html.escape(node.get('provider', 'Online'))
                n_dur = html.escape(node.get('duration', '2 weeks'))
                n_type = html.escape(node.get('type', 'Course'))
                n_why = html.escape(node.get('why', 'Core required competency on your roadmap.'))

                card_html = f"""
                <div class="{card_class}">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <strong style="font-size:13.5px; color:#111111;">{node_id}: {n_title}</strong>
                        {status_html}
                    </div>
                    <div style="font-size:12px; color:#4B4B4B; margin-bottom:4px;">
                        {n_prov} · <strong>{n_dur}</strong> · {n_type}
                    </div>
                    <div style="font-size:12.5px; color:#4B4B4B; line-height:1.45; margin-bottom:4px;">
                        {n_why}
                    </div>
                    <div style="font-size:11.5px; color:#858585;">
                        Competencies: {skills_str}
                    </div>
                </div>
                """
                st.markdown(clean_html(card_html), unsafe_allow_html=True)

            with c_action:
                if is_done:
                    if st.button("Completed", key=f"rec_undo_{node_id}", use_container_width=True):
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
