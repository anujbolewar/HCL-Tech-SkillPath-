# SkillPath AI

SkillPath AI is a personalized learning recommender built with Streamlit. Type **any** goal — career, hobby, language, fitness, exam — and get a 3-phase, prerequisite-aware learning roadmap with progress tracking and an AI mentor. Powered by **Groq** for instant LLM generation, with a smart offline fallback engine when no API key is set.

By **Team Cortex**

## Features

- ⚡ One-click quick picks or free-text goals for ANY domain (tech, music, fitness, languages, exams...)
- 🔀 Interactive prerequisite DAG canvas (streamlit-flow, graphviz fallback)
- ✅ Milestone completion tracking with prereq locking
- 💬 Roadmap-aware AI Mentor chat (Groq) with offline rule-based fallback
- 💡 Explainable per-module relevance scores (skill gap / prereqs / phase fit)
- 📊 Goal-aware skill radar dashboard + JSON & Markdown export

## Requirements

- Python 3.10+
- A [Groq Cloud](https://console.groq.com/keys) API key (`gsk_...`) — optional; without one the app runs in offline mode

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Configure your Groq key

Either paste it in the app sidebar at runtime, **or** create a `.env` file:

```bash
cp .env.example .env
# then edit .env:
GROQ_API_KEY=gsk_your_key_here
```

### Run tests (optional)

```bash
pip install -r requirements-dev.txt
pytest tests -q
```

## Run

```bash
streamlit run app.py
```

No key? The app still works — quick-pick or type any goal to get an offline-generated roadmap.
