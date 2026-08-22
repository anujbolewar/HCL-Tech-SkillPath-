"""Google Gemini LLM Engine for roadmap generation and streaming AI mentoring."""

import json
import os
from typing import Dict, Any, Generator, List, Optional
import streamlit as st

from engine.fallback_data import generate_fallback_roadmap

try:
    from google import genai
    from google.genai import types
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

def generate_roadmap_with_gemini(
    goal: str,
    profile: Dict[str, Any],
    gemini_api_key: str,
    model_name: str = "gemini-2.5-flash"
) -> Dict[str, Any]:
    """Generates a structured 3-phase DAG roadmap JSON using Google Gemini API."""
    if not HAS_GEMINI:
        st.warning("⚠️ Google GenAI package not installed. Using offline fallback engine.")
        return generate_fallback_roadmap(goal, profile)

    try:
        client = genai.Client(api_key=gemini_api_key)

        prompt = f"""
You are an expert Learning Path Architect and Curriculum Designer.
Generate a tailored, prerequisite-aware 3-phase Directed Acyclic Graph (DAG) learning roadmap for the goal: "{goal}".

Learner Profile:
- Target Experience Level: {profile.get('experience_level', 'Intermediate')}
- Mastered Skills: {', '.join(profile.get('skills', ['None']))}
- Weekly Study Commitment: {profile.get('weekly_hours', 15)} hours/week
- Preferred Style: {profile.get('preferred_learning_style', 'Hands-on Projects')}

Instructions:
1. In the "role" field, provide a concise, high-impact title (e.g. "Full-Stack AI Engineer", "Classical Guitarist", "Spanish Polyglot").
2. Generate exactly 3 sequential phases with exactly 2 milestone nodes per phase (total 6 nodes).
3. Phase 1 has empty prereqs `[]`. Phase 2 nodes reference Phase 1 IDs. Phase 3 nodes reference Phase 2 IDs.
4. In "why", provide an explicit, clear explanation of the pedagogical necessity of this milestone.
5. Return strictly valid JSON conforming to this schema:
{{
    "goal": "{goal}",
    "role": "<Role Title>",
    "phases": [
        {{
            "phase": "Phase 1: Foundations & Core Principles",
            "nodes": [
                {{
                    "id": "M101",
                    "title": "Module Title",
                    "type": "Course",
                    "provider": "Provider Name",
                    "duration": "2 weeks",
                    "prereqs": [],
                    "why": "Clear reason why this node is vital.",
                    "skills": ["Skill1", "Skill2"],
                    "difficulty": "Beginner"
                }}
            ]
        }}
    ]
}}
"""
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            )
        )

        content = response.text
        data = json.loads(content)

        if not isinstance(data.get("phases"), list) or len(data["phases"]) < 1:
            raise ValueError("Invalid schema returned by Gemini")

        return data

    except Exception as e:
        err_msg = str(e)
        st.error(f"⚠️ Gemini Generation Notice: {err_msg[:160]}... Loading optimized offline curriculum instead.")
        return generate_fallback_roadmap(goal, profile)


def stream_gemini_chat_response(
    messages: List[Dict[str, str]],
    gemini_api_key: str,
    model_name: str = "gemini-2.5-flash"
) -> Generator[str, None, None]:
    """Streams responses from Google Gemini models."""
    if not HAS_GEMINI:
        yield "Gemini package is unavailable. Please check your installation."
        return

    try:
        client = genai.Client(api_key=gemini_api_key)
        
        # Format history for Gemini
        conversation_text = ""
        for m in messages:
            role = "User" if m["role"] == "user" else "Assistant" if m["role"] == "assistant" else "System"
            conversation_text += f"{role}: {m['content']}\n\n"
        conversation_text += "Assistant: "

        response_stream = client.models.generate_content_stream(
            model=model_name,
            contents=conversation_text,
            config=types.GenerateContentConfig(temperature=0.5)
        )
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"⚠️ Gemini API connection issue: {str(e)}"
