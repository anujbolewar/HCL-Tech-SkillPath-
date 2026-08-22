"""UI package initialization for PathFinder AI."""

from ui.styles import inject_custom_styles, CUSTOM_CSS
from ui.components import (
    render_hero_header,
    render_metrics_summary_bar,
    render_node_inspector,
)
from ui.flow_visualizer import render_dag_flowchart
from ui.radar_chart import render_dynamic_radar_chart
from ui.chat_interface import render_ai_mentor_chat
from ui.recommendations import render_recommendation_cards
from ui.export_generator import (
    build_markdown_export,
    build_printable_html_export,
)

__all__ = [
    "inject_custom_styles",
    "CUSTOM_CSS",
    "render_hero_header",
    "render_metrics_summary_bar",
    "render_node_inspector",
    "render_dag_flowchart",
    "render_dynamic_radar_chart",
    "render_ai_mentor_chat",
    "render_recommendation_cards",
    "build_markdown_export",
    "build_printable_html_export",
]
