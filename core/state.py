"""State persistence manager for PathFinder AI.

Ensures user profile, roadmap data, completed milestone set, chat history,
and adaptive assessment events persist seamlessly across browser reruns and page refreshes.
"""

import json
from pathlib import Path
from typing import Dict, Any, Set, List
import streamlit as st

from core.config import DEFAULT_PROFILE, WELCOME_MESSAGE

STATE_FILE = Path(".skillpath_state.json")

def persist_state() -> bool:
    """Snapshot user profile, roadmap, completed nodes and chat history to disk."""
    try:
        completed = sorted(list(st.session_state.get("completed_nodes", set())))
        payload = {
            "user_profile": st.session_state.get("user_profile", DEFAULT_PROFILE),
            "roadmap_data": st.session_state.get("roadmap_data"),
            "completed_nodes": completed,
            "chat_history": st.session_state.get("chat_history", [])[-40:],
            "active_persona": st.session_state.get("active_persona", "Custom"),
            "selected_node_id": st.session_state.get("selected_node_id"),
            "adaptation_event": st.session_state.get("adaptation_event"),
        }
        STATE_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except Exception:
        return False

def load_persisted_state() -> bool:
    """Load persistent state from disk into session_state on initial startup."""
    try:
        if not STATE_FILE.exists():
            return False
        content = STATE_FILE.read_text(encoding="utf-8")
        data = json.loads(content)

        if isinstance(data.get("user_profile"), dict):
            st.session_state.user_profile = {**DEFAULT_PROFILE, **data["user_profile"]}
        if isinstance(data.get("roadmap_data"), dict) and data["roadmap_data"].get("phases"):
            st.session_state.roadmap_data = data["roadmap_data"]
        if isinstance(data.get("completed_nodes"), list):
            st.session_state.completed_nodes = set(data["completed_nodes"])
        if isinstance(data.get("chat_history"), list) and data["chat_history"]:
            st.session_state.chat_history = data["chat_history"]
        if "selected_node_id" in data:
            st.session_state.selected_node_id = data["selected_node_id"]
        if "adaptation_event" in data:
            st.session_state.adaptation_event = data["adaptation_event"]
        return True
    except Exception:
        return False

def clear_persisted_state() -> None:
    """Wipe disk snapshot and reset session state to clean state."""
    try:
        if STATE_FILE.exists():
            STATE_FILE.unlink(missing_ok=True)
    except Exception:
        pass

def initialize_session_state() -> None:
    """Initializes default session_state values if unassigned."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.user_profile = DEFAULT_PROFILE.copy()
        st.session_state.roadmap_data = None
        st.session_state.completed_nodes = set()
        st.session_state.selected_node_id = None
        st.session_state.adaptation_event = None
        st.session_state._show_replan_banner = False
        st.session_state._last_completed_title = ""
        st.session_state.chat_history = [{
            "role": "assistant",
            "content": WELCOME_MESSAGE
        }]
        # Try loading previous session state if available
        load_persisted_state()

    # Handle scratch wipe request
    if st.session_state.get("_pending_scratch"):
        clear_persisted_state()
        st.session_state.clear()
        st.session_state.initialized = True
        st.session_state.user_profile = DEFAULT_PROFILE.copy()
        st.session_state.roadmap_data = None
        st.session_state.completed_nodes = set()
        st.session_state.selected_node_id = None
        st.session_state.adaptation_event = None
        st.session_state._show_replan_banner = False
        st.session_state.chat_history = [{
            "role": "assistant",
            "content": WELCOME_MESSAGE
        }]
        persist_state()
