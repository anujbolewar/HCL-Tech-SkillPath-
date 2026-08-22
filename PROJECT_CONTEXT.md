# Project Context: PathFinder AI (SkillPath)
**Team Cortex** — HCL Tech Hackathon 2026 (Round 2)

## 1. Domain & Purpose
AI-Powered Personalized Learning Path Recommender (PathFinder Prototype). Generates structured, prerequisite-aware Directed Acyclic Graph (DAG) curriculums for any career or learning goal.

## 2. Core Architecture
- **Streamlit Frontend**: `app.py`, `ui/` (`styles.py`, `components.py`, `flow_visualizer.py`, `radar_chart.py`, `chat_interface.py`, `recommendations.py`, `export_generator.py`).
- **Core Layer**: `core/` (`config.py`, `types.py`, `state.py`).
- **Intelligence Engine**: `engine/` (`llm_router.py`, `groq_engine.py`, `gemini_engine.py`, `fallback_data.py`, `xai_scorer.py`, `re_router.py`).
- **Multi-Model LLM Routing**: Groq (Llama 3.3 70B & 3.1 8B), Google Gemini (2.5 Flash / Pro), and Smart Offline Knowledge Graph.
- **Topological Integrity**: Kahn's algorithm DAG validation ensuring zero circular loops.
- **Persistence**: `.skillpath_state.json` ensuring progress persists across browser refresh.

## 3. Team Details
- **Team**: Cortex (Yeshwantrao Chavan College of Engineering)
- **Members**: Anuj Bolewar, Lakshya Gupta, Shaki Gajbhiye, Pranjal Gudadhe, Om Ingle
- **Active Branch**: `cortex-pathfinder-v2`

## 4. Key Commands
- Run app: `streamlit run app.py`
- Run tests: `python3 -m pytest tests/ -v`
- Package submission: `python3 package_submission.py`
