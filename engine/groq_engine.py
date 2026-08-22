"""Groq LLM Engine for roadmap generation and real-time streaming AI mentoring."""

import json
import os
import time
from typing import Dict, Any, Generator, Optional, List
import streamlit as st

from engine.fallback_data import generate_fallback_roadmap

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

def generate_roadmap_with_groq(
    goal: str,
    profile: Dict[str, Any],
    groq_api_key: str,
    model_name: str = "llama-3.3-70b-versatile"
) -> Dict[str, Any]:
    """Generates a dynamic 3-phase DAG roadmap JSON using Groq LLMs."""
    if not HAS_GROQ:
        st.warning("⚠️ Groq package not installed. Using offline fallback engine.")
        return generate_fallback_roadmap(goal, profile)

    try:
        client = Groq(api_key=groq_api_key)
        
        prompt = f"""
You are an expert Learning Path Architect and Curriculum Designer.
Generate a tailored, prerequisite-aware 3-phase Directed Acyclic Graph (DAG) learning roadmap for ANY goal.

Learner Profile:
- Goal: "{goal}"
- Target Experience Level: {profile.get('experience_level', 'Intermediate')}
- Mastered Skills: {', '.join(profile.get('skills', ['None']))}
- Weekly Study Commitment: {profile.get('weekly_hours', 15)} hours/week
- Preferred Style: {profile.get('preferred_learning_style', 'Hands-on Projects')}

Instructions:
1. Infer the exact subject/focus directly from the goal.
2. In the "role" field, give a SHORT, SPECIFIC professional or skill title (e.g. "Full-Stack AI Engineer", "Classical Guitarist", "Spanish Speaker", "JEE Topper").
3. Generate exactly 3 phases with exactly 2 milestone nodes per phase (total 6 nodes).
4. Node IDs should be short alphanumeric (e.g., M101, M102, M201, M202, M301, M302 or domain specific like AI101, WEB101).
5. Ensure prerequisite graph is strictly acyclic. Phase 1 nodes have empty prereqs `[]`. Phase 2 nodes reference Phase 1 nodes. Phase 3 nodes reference Phase 2 nodes.
6. Provide real, high-quality course/project providers (Coursera, MIT OCW, YouTube, freeCodeCamp, Fast.ai, official docs, etc.).
7. In the "why" field, write an explicit, compelling rationale explaining why this node is recommended and how it builds on earlier prerequisites.

Output strict JSON only conforming to this schema:
{{
    "goal": "{goal}",
    "role": "<Short specific title>",
    "phases": [
        {{
            "phase": "Phase 1: Foundations & Core Concepts",
            "nodes": [
                {{
                    "id": "M101",
                    "title": "Module Title",
                    "type": "Course",
                    "provider": "Provider Name",
                    "duration": "2 weeks",
                    "prereqs": [],
                    "why": "Clear explanation of prerequisite necessity and foundational value.",
                    "skills": ["Skill1", "Skill2"],
                    "difficulty": "Beginner"
                }}
            ]
        }}
    ]
}}
"""
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model_name,
            temperature=0.25,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        # Validate schema completeness
        if not isinstance(data.get("phases"), list) or len(data["phases"]) < 1:
            raise ValueError("Incomplete phases schema returned")
        
        for phase in data["phases"]:
            if not isinstance(phase.get("nodes"), list) or len(phase["nodes"]) < 1:
                raise ValueError("Incomplete nodes schema in phase")
            for node in phase["nodes"]:
                if not node.get("id") or not node.get("title"):
                    raise ValueError("Node missing id or title")

        return data

    except Exception as e:
        err_msg = str(e)
        st.error(f"⚠️ Groq Generation Notice: {err_msg[:160]}... Loading optimized offline curriculum instead.")
        return generate_fallback_roadmap(goal, profile)


def stream_groq_chat_response(
    messages: List[Dict[str, str]],
    groq_api_key: str,
    model_name: str = "llama-3.1-8b-instant"
) -> Generator[str, None, None]:
    """Streams Groq chat responses token by token for smooth typewriter UI effect."""
    if not HAS_GROQ:
        yield "Groq package is unavailable. Please check your installation."
        return

    try:
        client = Groq(api_key=groq_api_key)
        stream = client.chat.completions.create(
            messages=messages,
            model=model_name,
            temperature=0.5,
            max_tokens=600,
            stream=True
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except Exception as e:
        yield f"⚠️ Groq API connection issue: {str(e)}"
