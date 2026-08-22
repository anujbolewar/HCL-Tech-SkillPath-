"""Engine package initialization for PathFinder AI."""

from engine.fallback_data import generate_fallback_roadmap, DOMAIN_TEMPLATES
from engine.xai_scorer import compute_node_relevance
from engine.re_router import (
    get_node_status,
    find_next_recommended_action,
    calculate_progress_stats,
)
from engine.groq_engine import (
    generate_roadmap_with_groq,
    stream_groq_chat_response,
    HAS_GROQ,
)
from engine.gemini_engine import (
    generate_roadmap_with_gemini,
    stream_gemini_chat_response,
    HAS_GEMINI,
)
from engine.llm_router import (
    generate_unified_roadmap,
    generate_offline_streaming_mentor_reply,
)

__all__ = [
    "generate_fallback_roadmap",
    "DOMAIN_TEMPLATES",
    "compute_node_relevance",
    "get_node_status",
    "find_next_recommended_action",
    "calculate_progress_stats",
    "generate_roadmap_with_groq",
    "stream_groq_chat_response",
    "HAS_GROQ",
    "generate_roadmap_with_gemini",
    "stream_gemini_chat_response",
    "HAS_GEMINI",
    "generate_unified_roadmap",
    "generate_offline_streaming_mentor_reply",
]
