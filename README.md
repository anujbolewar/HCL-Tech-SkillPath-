# SkillPath AI (PathFinder Prototype)
### AI-Powered Personalized Learning Path Recommender
**HCL Tech Hackathon 2026 — Round 2 Prototype Submission**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests Passing](https://img.shields.io/badge/tests-16%20passed%20(100%25)-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 👥 Team Cortex
**Institution**: Yeshwantrao Chavan College of Engineering  
- **Anuj Bolewar** (`bolewara@gmail.com`) — *Lead Architect & AI Engineer*  
- **Lakshya Gupta** (`lakshyagupta9721@gmail.com`) — *Full-Stack & Systems Engineer*  
- **Shaki Gajbhiye** (`gajbhiyeshaki@gmail.com`) — *AI/ML & Data Engineer*  
- **Pranjal Gudadhe** (`pranjalgudadhe59@gmail.com`) — *UX & Frontend Engineer*  
- **Om Ingle** (`omingle71@gmail.com`) — *Research & Evaluation Specialist*  

---

## 🚀 Overview

**SkillPath AI (PathFinder)** is an intelligent curriculum architect that synthesizes personalized, prerequisite-aware **Directed Acyclic Graph (DAG)** learning paths for **ANY** learning goal — technical careers, creative arts, musical instruments, foreign languages, fitness transformations, or competitive exams.

### 🌟 Key Highlights
- **🔀 Prerequisite-Aware DAG Visualizer**: Interactive 2D React Flow canvas (`streamlit-flow`) with node click inspection showing the **"Why"** rationale, target skill gaps, and prerequisites.
- **💡 Deterministic Explainable AI (XAI)**: Multi-factor scoring ledger (`Skill Gap (40%) + Prereq Readiness (30%) + Experience Fit (30%)`) justifying every recommendation.
- **🤖 Word-by-Word Streaming AI Mentor**: Contextually grounded pedagogical mentor with real-time typewriter token streaming (`st.write_stream`) and prompt suggestion chips.
- **🕸️ Dynamic Skill Competency Radar Chart**: Plotly Polar Radar Chart that recalculates baseline vs acquired mastery across 6 dimensions upon every milestone completion.
- **⚡ Multi-Model LLM Router**: Seamless support for **Groq Cloud** (`llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768`), **Google Gemini** (`gemini-2.5-flash`, `gemini-2.5-pro`), and a 100% offline smart knowledge base.
- **💾 Persistent Memory**: State automatically persists across browser refreshes via `.skillpath_state.json`.
- **📁 Multi-Format Exports**: One-click download as structured **JSON**, formatted **Markdown checklists**, and styled **Printable HTML/PDF** reports.

---

## 🏛️ System Architecture & The 6 Pillars

```
hcl/
├── app.py                     # Streamlit orchestrator (<200 lines)
├── core/
│   ├── config.py              # Constants, Demo personas, Quick picks, Model catalog
│   ├── state.py               # State persistence (.skillpath_state.json)
│   └── types.py               # Dataclasses & schema definitions
├── engine/
│   ├── fallback_data.py       # Offline knowledge base (12 domain DAG templates)
│   ├── xai_scorer.py          # Deterministic 3-factor Explainable AI scoring engine
│   ├── re_router.py           # Prerequisite unblocking & adaptive next-action calculator
│   ├── groq_engine.py         # Groq LLM roadmap generator & token stream logic
│   ├── gemini_engine.py       # Google Gemini LLM roadmap generator & stream logic
│   └── llm_router.py          # Unified multi-model routing interface
├── ui/
│   ├── styles.py              # shadcn/zinc dark theme & responsive CSS
│   ├── components.py          # Metrics summary bar, hero cards, node inspector
│   ├── flow_visualizer.py     # Streamlit-Flow React Flow DAG with "Why" inspection
│   ├── radar_chart.py         # Plotly Polar Radar Chart updated on every re-render
│   ├── chat_interface.py      # AI Mentor with word-by-word typewriter streaming
│   ├── recommendations.py     # Curated course cards with Mark Complete / Undo triggers
│   └── export_generator.py    # Markdown, JSON, and Printable HTML/PDF generators
├── docs/
│   ├── DOCUMENTATION.md       # Comprehensive Round 2 Solution Documentation
│   ├── PITCH_DECK.md          # 10-Slide Pitch Deck outline
│   ├── pitch_deck.html        # Interactive HTML presentation slide deck
│   └── DEMO_SCRIPT.md         # 3–5 Minute Video Demo recording script
├── tests/
│   ├── test_app_logic.py      # Legacy test suite compatibility
│   ├── test_modular_engine.py # Router, XAI, persistence, and export test suites
│   └── test_dag_integrity.py  # Topological sorting and cycle detection tests
└── package_submission.py      # Submission ZIP packaging utility
```

---

## 📦 Deliverables Checklist (Round 2)

| Deliverable | Description | Location / Status |
|:------------|:------------|:------------------|
| **1. Source Code (ZIP)** | Complete runnable source code archive | `python3 package_submission.py` → `submission.zip` |
| **2. GitHub Repository** | Public / accessible source repository | [`https://github.com/anujbolewar/HCL-Tech-SkillPath-`](https://github.com/anujbolewar/HCL-Tech-SkillPath-) (branch: `cortex-pathfinder-v2`) |
| **3. Solution Documentation** | Comprehensive technical documentation & slides | [`docs/DOCUMENTATION.md`](docs/DOCUMENTATION.md), [`docs/pitch_deck.html`](docs/pitch_deck.html) |
| **4. Demo Video** | 3–5 minute video recording script & walkthrough | [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md) |
| **5. Local Setup / App Access** | Local execution and deployment guide | See setup instructions below |

---

## 🛠️ Local Setup & Execution Instructions

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14
- Git

### 2. Clone and Branch Setup
```bash
git clone https://github.com/anujbolewar/HCL-Tech-SkillPath-.git
cd HCL-Tech-SkillPath-
git checkout cortex-pathfinder-v2
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment (Optional)
Copy the example environment configuration:
```bash
cp .env.example .env
```
Add your optional API keys for live cloud LLM inference (or use the built-in Smart Offline engine without any keys):
```ini
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIza...
```

### 5. Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running Automated Tests

Run the complete test suite (16 tests verifying curriculum DAGs, topological ordering, XAI scorers, state persistence, and exports):
```bash
python3 -m pytest tests/ -v
```

---

## 🎬 1-Click Interactive Evaluation (Demo Mode)
1. Open the sidebar in the app.
2. Toggle **🎬 Interactive Demo Mode** to `ON`.
3. Choose any pre-configured student persona (e.g. *Alex: AI & ML Aspirant*, *Sarah: Web Switcher*, *Carlos: Guitarist*, *Elena: Spanish Polyglot*, *Rohan: Exam Topper*).
4. Experience instant curriculum generation, topological unblocking, and AI mentoring with zero setup!

---

## 📄 License
Distributed under the MIT License. Developed for HCL Tech Hackathon 2026 by **Team Cortex**.
