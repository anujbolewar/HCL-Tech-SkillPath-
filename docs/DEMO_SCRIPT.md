# PathFinder AI — 3–5 Minute Video Demo Script
## HCL Tech Hackathon 2026 (Round 2 Prototype)
**Team Cortex** (Yeshwantrao Chavan College of Engineering)

---

### Video Overview
- **Target Duration**: 3 minutes 45 seconds (within the 3–5 minute hackathon requirement)
- **Goal**: Demonstrate core problem solving, 6-Pillar architecture, interactive DAG flowchart, Explainable AI, streaming mentor, and dynamic radar chart.

---

### Scene-by-Scene Walkthrough

#### ⏱️ 0:00 – 0:40 | Introduction & Problem Statement
- **Screen**: Camera on presenter / Title slide (`docs/pitch_deck.html` or Streamlit app hero).
- **Audio / Script**:
  > *"Hello esteemed judges and HCL leaders. We are Team Cortex from Yeshwantrao Chavan College of Engineering. Today, we're proud to present **PathFinder AI** — an AI-powered personalized learning path recommender designed to eliminate curriculum fragmentation.*
  >
  > *While platforms offer thousands of online courses, over 90% of self-directed learners drop out because they don't know the right sequence of learning, lack prerequisite clarity, and receive black-box suggestions without rationales. PathFinder AI bridges this gap by synthesizing prerequisite-aware Directed Acyclic Graph roadmaps for ANY goal."*

#### ⏱️ 0:40 – 1:30 | Pillar 1 & 2: Goal Intake & Learner Profiling
- **Screen**: Streamlit App (`localhost:8501`). Show the sidebar and Hero header.
- **Action**:
  - Point out the **AI Engine selector** (Groq Cloud Llama 3.3 70B, Google Gemini, and Smart Offline).
  - Open the **Learner Profile expander** and adjust experience level (Intermediate), study hours (15 hrs/week), and mastered skills.
  - Click on a Quick Pick or type a custom goal: `"I want to become an AI & Machine Learning Engineer"`.
  - Click **🚀 Generate Path**.
- **Audio / Script**:
  > *"Notice how PathFinder AI adapts to the student's exact constraints. We can select our AI provider — supporting Groq Cloud with Llama 3.3 70B, Google Gemini, or our instant Smart Offline engine. We configure our current skills and weekly commitment. With one click, PathFinder AI validates topological constraints and builds our personalized 3-phase curriculum."*

#### ⏱️ 1:30 – 2:30 | Pillar 4 & 3: Interactive React Flow DAG & Recommendations
- **Screen**: Tab 1 (**🔀 Pillar 4: Interactive DAG**) & Tab 2 (**📚 Pillar 3: Course Recs**).
- **Action**:
  - Pan and zoom on the 2D React Flow canvas.
  - Click on node `AI101: Mathematics for Machine Learning`.
  - Point out the **Node Inspector ("Why" panel)** that appears on the canvas with the 3-factor Explainable AI score breakdown.
  - Switch to Tab 2, click **Mark Complete** on `AI101`.
  - Switch back to Tab 1 to show `AI101` turn green (`✓ DONE`) and the edge to Phase 2 begin animating as unlocked (`▶ READY`).
- **Audio / Script**:
  > *"Here in Pillar 4, we visualize the curriculum as an interactive 2D Directed Acyclic Graph powered by React Flow. Each node represents a milestone. Notice how clicking any node immediately reveals the 'Why' panel — breaking down the exact skill gap coverage and prerequisite readiness.*
  >
  > *When we mark Phase 1 milestones complete, the DAG dynamically recalculates the topological state — turning completed nodes emerald green and automatically unlocking downstream Phase 2 dependencies."*

#### ⏱️ 2:30 – 3:15 | Pillar 5 & 6: Streaming AI Mentor & Dynamic Radar Chart
- **Screen**: Tab 3 (**💡 Explainable AI & Mentor**) & Tab 4 (**📊 Skill Radar & Analytics**).
- **Action**:
  - In Tab 3, click a suggested prompt chip: `"👉 What should I focus on next?"`.
  - Show the AI Mentor streaming its answer word-by-word with live typewriter animation.
  - Switch to Tab 4 to show the **Plotly Polar Radar Chart** updating baseline vs current mastery in real-time.
  - Click the **📄 Markdown** and **🖨️ Printable HTML/PDF** export buttons to show the generated reports.
- **Audio / Script**:
  > *"In Pillar 5, our AI Mentor is contextually grounded in the active curriculum. It answers queries with real-time word-by-word streaming animation, referencing specific node IDs and scheduling study blocks.*
  >
  > *In Pillar 6, the Skill Competency Radar Chart dynamically recalculates domain proficiencies across 6 dimensions upon every re-render. Finally, learners can export their full personalized curriculum as structured JSON, Markdown checklists, or printable HTML reports for PDF generation."*

#### ⏱️ 3:15 – 3:45 | Conclusion & Summary
- **Screen**: Return to Pitch Deck conclusion slide or app summary.
- **Audio / Script**:
  > *"PathFinder AI features a clean modular architecture, 100% test coverage across 16 automated test suites, and persistent session memory. We are ready to empower thousands of students and corporate professionals at HCL Tech. Thank you for your time!"*
