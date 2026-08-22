"""UI package initialization for PathFinder AI."""

from ui.styles import inject_custom_styles, CUSTOM_CSS
from ui.components import (
    render_app_header,
    render_skill_gap_section,
    render_next_best_action_card,
    render_node_inspector,
    render_roadmap_updated_banner,
    render_diagnostic_assessment_widget,
    clean_html,
)
from ui.flow_visualizer import render_dag_flowchart
from ui.radar_chart import render_dynamic_radar_chart
from ui.chat_interface import render_ai_mentor_chat
from ui.recommendations import render_recommendation_cards
from ui.export_generator import (
    build_markdown_export,
    build_printable_html_export,
)

# Backward-compatible aliases
render_hero_header = render_app_header

__all__ = [
    "inject_custom_styles",
    "CUSTOM_CSS",
    "render_app_header",
    "render_hero_header",
    "render_skill_gap_section",
    "render_next_best_action_card",
    "render_node_inspector",
    "render_roadmap_updated_banner",
    "render_diagnostic_assessment_widget",
    "render_dag_flowchart",
    "render_dynamic_radar_chart",
    "render_ai_mentor_chat",
    "render_recommendation_cards",
    "build_markdown_export",
    "build_printable_html_export",
    "clean_html",
]
