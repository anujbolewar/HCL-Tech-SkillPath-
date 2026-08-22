import streamlit as st
import plotly.graph_objects as go
import graphviz
import json
import time
import os
import re
from collections import Counter

from dotenv import load_dotenv

load_dotenv()

# Import Groq SDK
try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

# Import streamlit-flow component
try:
    from streamlit_flow import streamlit_flow
    from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
    from streamlit_flow.state import StreamlitFlowState
    from streamlit_flow.layouts import TreeLayout
    HAS_STREAMLIT_FLOW = True
except ImportError:
    HAS_STREAMLIT_FLOW = False

# Fallback list used when the live model catalog cannot be fetched
DEFAULT_GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "llama-3.3-70b-versatile",
]

# ==========================================
# PAGE CONFIGURATION & STYLES
# ==========================================
st.set_page_config(
    page_title="SkillPath AI — Learn Anything",
    page_icon="assets/logo_small.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# shadcn-inspired Pure Black Theme
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Display font for all headings */
    h1, h2, h3, .hero-title, .metric-val, .course-title {
        font-family: 'Space Grotesk', 'Inter', sans-serif !important;
        letter-spacing: -0.02em;
    }

    /* Pure black app surface */
    .stApp {
        background: #09090b;
        color: #fafafa;
    }

    /* Card system: zinc layers on black */
    .hero-card {
        background: #101012;
        border: 1px solid #27272a;
        border-radius: 10px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
    }

    .hero-title {
        background: linear-gradient(92deg, #fafafa 20%, #c7d2fe 60%, #93c5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.4rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: #a1a1aa;
        font-size: 1rem;
        line-height: 1.55;
    }

    /* Metric Cards */
    .metric-container {
        background: #0e0e10;
        border: 1px solid #27272a;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        transition: border-color 0.15s ease, background-color 0.15s ease;
    }

    .metric-container:hover {
        background: #131316;
        border-color: #3f3f46;
    }

    .metric-val {
        font-size: 1.5rem;
        font-weight: 700;
        color: #fafafa;
    }

    .metric-lbl {
        font-size: 0.75rem;
        color: #a1a1aa;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 4px;
    }

    /* Custom Badges — muted zinc variants */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }

    .badge-primary { background: rgba(79, 172, 254, 0.12); color: #7cc4ff; border: 1px solid rgba(79, 172, 254, 0.25); }
    .badge-success { background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.25); }
    .badge-warning { background: rgba(245, 158, 11, 0.12); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.25); }
    .badge-purple { background: rgba(139, 92, 246, 0.12); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.25); }

    /* Course Node Card */
    .course-card {
        background: #0e0e10;
        border: 1px solid #27272a;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 16px;
        transition: border-color 0.15s ease;
    }

    .course-card:hover {
        border-color: #3f3f46;
    }

    .course-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #fafafa;
    }

    /* Sidebar: same pure black, hairline divider */
    section[data-testid="stSidebar"] {
        background-color: #09090b;
        border-right: 1px solid #1f1f23;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# INITIALIZE SESSION STATE (All 6 Pillars)
# ==========================================
DEFAULT_PROFILE = {
    'target_role': 'AI & ML Engineer',
    'experience_level': 'Intermediate',
    'skills': ['Python', 'Basic Math', 'SQL'],
    'completed_courses': ['Python Fundamentals'],
    'weekly_hours': 10
}

WELCOME_MESSAGE = "👋 Hi! I'm your **Groq-Powered SkillPath AI Assistant by Team Cortex**. Tell me your learning goal or ask me anything about your roadmap!"

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = DEFAULT_PROFILE.copy()

if 'roadmap_data' not in st.session_state:
    st.session_state.roadmap_data = None

if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = False

if '_prev_demo' not in st.session_state:
    st.session_state._prev_demo = False

if '_pending_scratch' not in st.session_state:
    st.session_state._pending_scratch = False

if '_pending_demo_off' not in st.session_state:
    st.session_state._pending_demo_off = False

if 'completed_nodes' not in st.session_state:
    st.session_state.completed_nodes = set()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]

# DEFERRED RESETS: must run BEFORE widgets are instantiated this script run,
# because st.session_state[widget_key] cannot be written after widget creation.
if st.session_state.get('_pending_scratch'):
    st.session_state.user_profile = DEFAULT_PROFILE.copy()
    st.session_state.roadmap_data = None
    st.session_state.completed_nodes = set()
    st.session_state.chat_history = [{"role": "assistant", "content": WELCOME_MESSAGE}]
    st.session_state.demo_mode = False
    st.session_state._prev_demo = False
    st.session_state.goal_box = ""
    st.session_state._pending_scratch = False

if st.session_state.get('_pending_demo_off'):
    st.session_state.demo_mode = False
    st.session_state._prev_demo = False
    st.session_state._pending_demo_off = False

# ==========================================
# GROQ LLM ROADMAP GENERATOR & FALLBACK
# ==========================================
def generate_roadmap_with_groq(goal: str, profile: dict, groq_api_key: str, model_name: str):
    """Generates a dynamic multi-phase DAG roadmap JSON using Groq API."""
    try:
        client = Groq(api_key=groq_api_key)
        
        prompt = f"""
You are an expert Learning Path Architect for ANY learning goal — technical careers,
hobbies, languages, music, sports, fitness, arts, academics, or personal growth.
Learner Experience Level: {profile['experience_level']}
Current Skills: {', '.join(profile['skills'])}
Weekly Hours: {profile['weekly_hours']}
Learner Goal: "{goal}"

IMPORTANT: Infer the learning focus directly from the Learner Goal text — it may be a
career (e.g. "software engineer") OR any life skill/hobby/subject (e.g. "learn guitar",
"fluent Spanish", "get fit", "crack JEE", "start a bakery").
In the JSON "role" field use a SHORT, SPECIFIC title naming the subject — like
"Chess Player", "Guitarist", "Spanish Speaker", "Home Baker", "JEE Aspirant".
Never use generic words such as "hobby", "skill" or "interest".

Generate a structured 3-phase learning path in strict JSON format with zero conversational preamble.
JSON Schema:
{{
    "goal": "{goal}",
    "role": "<short learning focus inferred from the goal>",
    "phases": [
        {{
            "phase": "Phase 1: Title",
            "nodes": [
                {{
                    "id": "M101",
                    "title": "Module Title",
                    "type": "Course",
                    "provider": "Provider Name (Coursera/MIT OCW/freeCodeCamp/YouTube/local club/app)",
                    "duration": "2 weeks",
                    "prereqs": [],
                    "why": "Clear rationale explaining why recommended.",
                    "skills": ["Skill1", "Skill2"]
                }}
            ]
        }}
    ]
}}
Ensure node IDs are short strings, prereqs reference prior node IDs, and exactly 6 total nodes across 3 phases are returned.
Adapt providers and module types to the domain (e.g. apps/coaches for fitness, tutors/apps for languages).
"""
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model_name,
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        # Validate schema before accepting the LLM output
        if not isinstance(data.get("phases"), list) or not data["phases"] \
                or not all(isinstance(p.get("nodes"), list) and p["nodes"] for p in data["phases"]) \
                or not data.get("role"):
            raise ValueError("LLM returned an incomplete roadmap schema")

        return data
    except Exception as e:
        st.error(f"⚠️ Live Groq generation failed ({str(e)[:200]}). Showing the smart offline path for your goal instead.")
        return generate_fallback_roadmap(goal, profile)

def generate_fallback_roadmap(goal: str, profile: dict):
    """Smart offline engine: matches the learner's goal to a domain-specific template."""
    goal_l = f" {goal.lower()} "

    ai_ml_phases = [
        {
            "phase": "Phase 1: Core Mathematical Foundations",
            "nodes": [
                {"id": "AI101", "title": "Mathematics for Machine Learning", "type": "Course", "provider": "Imperial College London", "duration": "3 weeks", "prereqs": [], "why": "Establishes linear algebra, multivariate calculus, and PCA foundations.", "skills": ["Linear Algebra", "Calculus"]},
                {"id": "AI102", "title": "Python Data Structures & Algorithms", "type": "Course", "provider": "MIT OCW", "duration": "2 weeks", "prereqs": [], "why": "Optimizes computational complexity and clean object-oriented code.", "skills": ["Data Structures", "Algorithms"]}
            ]
        },
        {
            "phase": "Phase 2: Deep Learning Architectures",
            "nodes": [
                {"id": "AI201", "title": "Deep Learning & PyTorch Modeling", "type": "Course", "provider": "DeepLearning.AI", "duration": "4 weeks", "prereqs": ["AI101", "AI102"], "why": "Hands-on PyTorch modeling, loss optimization, and CNNs/RNNs.", "skills": ["PyTorch", "Neural Networks"]},
                {"id": "AI202", "title": "Transformer Models & LLM Fine-Tuning", "type": "Course", "provider": "Hugging Face", "duration": "3 weeks", "prereqs": ["AI201"], "why": "Teaches self-attention, LoRA/QLoRA fine-tuning, and Hugging Face pipelines.", "skills": ["Transformers", "PEFT", "HuggingFace"]}
            ]
        },
        {
            "phase": "Phase 3: Production MLOps & Autonomous Agents",
            "nodes": [
                {"id": "AI301", "title": "RAG System & Vector Databases", "type": "Project", "provider": "LangChain & Qdrant", "duration": "2 weeks", "prereqs": ["AI202"], "why": "Build enterprise retrieval-augmented generation app with semantic search.", "skills": ["LangChain", "Vector DB", "RAG"]},
                {"id": "AI302", "title": "FastMCP Autonomous Agent Deployment", "type": "Project", "provider": "FastMCP & Docker", "duration": "3 weeks", "prereqs": ["AI301"], "why": "Deploy agentic tool-calling pipeline to production cloud server.", "skills": ["FastMCP", "Docker", "MLOps"]}
            ]
        }
    ]

    domain_templates = [
        {
            "role": "AI & ML Engineer",
            "keywords": ("ai & ml", "ai/ml", "aiml", "mlops"),
            "phases": ai_ml_phases
        },
        {
            "role": "Data Scientist",
            "keywords": ("data scien", "machine learn", "ml engineer", "deep learn", "artificial intelligence"),
            "phases": [
                {"phase": "Phase 1: Mathematical Foundations & Data Tools", "nodes": [
                    {"id": "DS101", "title": "Linear Algebra & Calculus", "type": "Course", "provider": "MIT OCW", "duration": "3 weeks", "prereqs": [], "why": "Essential foundation for matrix transformations & ML optimization.", "skills": ["Linear Algebra", "Calculus"]},
                    {"id": "DS102", "title": "Data Wrangling with Pandas", "type": "Course", "provider": "DataCamp", "duration": "2 weeks", "prereqs": [], "why": "Core stack for cleaning, structuring, and exploring tabular data.", "skills": ["Pandas", "NumPy"]}
                ]},
                {"phase": "Phase 2: Statistical Modeling & ML", "nodes": [
                    {"id": "DS201", "title": "Applied Machine Learning", "type": "Course", "provider": "Coursera (Andrew Ng)", "duration": "4 weeks", "prereqs": ["DS101", "DS102"], "why": "Covers supervised/unsupervised algorithms, cross-validation, and metrics.", "skills": ["Scikit-Learn", "Regression", "Trees"]},
                    {"id": "DS202", "title": "Predictive Analytics Capstone", "type": "Project", "provider": "Portfolio Lab", "duration": "2 weeks", "prereqs": ["DS201"], "why": "Build end-to-end customer churn prediction pipeline.", "skills": ["Feature Engineering", "Model Evaluation"]}
                ]},
                {"phase": "Phase 3: Deep Learning & Production MLOps", "nodes": [
                    {"id": "DS301", "title": "Neural Networks (PyTorch)", "type": "Course", "provider": "DeepLearning.AI", "duration": "4 weeks", "prereqs": ["DS201"], "why": "Teaches PyTorch architecture, backpropagation, and CNNs/RNNs.", "skills": ["PyTorch", "Deep Learning"]},
                    {"id": "DS302", "title": "ML Model Deployment & FastAPI", "type": "Project", "provider": "GitHub Capstone", "duration": "2 weeks", "prereqs": ["DS301"], "why": "Deploy trained model as REST API microservice with Docker.", "skills": ["FastAPI", "Docker", "MLOps"]}
                ]}
            ]
        },
        {
            "role": "Data Analyst",
            "keywords": ("data analy", "business analy", "business intelligence", "power bi", "tableau", "analytics"),
            "phases": [
                {"phase": "Phase 1: Data Querying Foundations", "nodes": [
                    {"id": "BA101", "title": "SQL for Data Analysis", "type": "Course", "provider": "Mode Analytics", "duration": "3 weeks", "prereqs": [], "why": "SQL is the #1 day-to-day tool for analysts querying warehouses.", "skills": ["SQL", "Joins", "Window Functions"]},
                    {"id": "BA102", "title": "Spreadsheets to Power BI", "type": "Course", "provider": "Microsoft Learn", "duration": "2 weeks", "prereqs": [], "why": "Bridges Excel skills into modern BI modeling with DAX basics.", "skills": ["Excel", "Power BI", "DAX"]}
                ]},
                {"phase": "Phase 2: Visualization & Storytelling", "nodes": [
                    {"id": "BA201", "title": "Python for Data Analysis", "type": "Course", "provider": "DataCamp", "duration": "3 weeks", "prereqs": ["BA101"], "why": "Automates cleaning/reporting beyond what spreadsheets can handle.", "skills": ["Pandas", "Matplotlib"]},
                    {"id": "BA202", "title": "Executive Dashboard Project", "type": "Project", "provider": "Portfolio Lab", "duration": "2 weeks", "prereqs": ["BA102", "BA201"], "why": "KPI dashboard demonstrating insight storytelling to stakeholders.", "skills": ["Tableau", "KPI Design"]}
                ]},
                {"phase": "Phase 3: Applied Analytics at Scale", "nodes": [
                    {"id": "BA301", "title": "Statistics for Business Decisions", "type": "Course", "provider": "Coursera (Duke)", "duration": "3 weeks", "prereqs": ["BA201"], "why": "A/B testing and inference prevent wrong conclusions from data.", "skills": ["A/B Testing", "Statistics"]},
                    {"id": "BA302", "title": "End-to-End BI Pipeline Capstone", "type": "Project", "provider": "GitHub Capstone", "duration": "3 weeks", "prereqs": ["BA301"], "why": "Ingestion -> warehouse -> dashboard pipeline mirrors real analytics teams.", "skills": ["ETL", "dbt", "Warehouse"]}
                ]}
            ]
        },
        {
            "role": "Web Developer",
            "keywords": ("web", "frontend", "front-end", "full stack", "fullstack", "react", "mern", "next.js"),
            "phases": [
                {"phase": "Phase 1: Modern Web Foundations", "nodes": [
                    {"id": "WEB101", "title": "TypeScript Syntax", "type": "Course", "provider": "freeCodeCamp", "duration": "2 weeks", "prereqs": [], "why": "Type safety & modern ES6 features required for frontend frameworks.", "skills": ["TypeScript", "ES6+"]},
                    {"id": "WEB102", "title": "React 19 & State Management", "type": "Course", "provider": "Scrimba", "duration": "3 weeks", "prereqs": ["WEB101"], "why": "Master component lifecycles, custom hooks, and Tailwind CSS UI.", "skills": ["React", "Tailwind CSS"]}
                ]},
                {"phase": "Phase 2: Full-Stack Architecture", "nodes": [
                    {"id": "WEB201", "title": "Next.js App Router", "type": "Course", "provider": "Vercel Academy", "duration": "3 weeks", "prereqs": ["WEB102"], "why": "Industry standard for SSR, SEO optimization, and API route handling.", "skills": ["Next.js", "Server Actions"]},
                    {"id": "WEB202", "title": "Full-Stack SaaS Capstone", "type": "Project", "provider": "Portfolio Lab", "duration": "3 weeks", "prereqs": ["WEB201"], "why": "Build production SaaS app with auth, subscription billing, and database.", "skills": ["Prisma", "PostgreSQL", "Stripe"]}
                ]},
                {"phase": "Phase 3: Quality & Deployment", "nodes": [
                    {"id": "WEB301", "title": "Testing (Jest & Cypress)", "type": "Course", "provider": "Frontend Masters", "duration": "2 weeks", "prereqs": ["WEB202"], "why": "Unit/E2E tests are expected in professional web engineering roles.", "skills": ["Jest", "Cypress", "CI"]},
                    {"id": "WEB302", "title": "Ship to Production (Vercel/CDN)", "type": "Project", "provider": "Vercel Academy", "duration": "1 week", "prereqs": ["WEB301"], "why": "Custom domains, env management, and observability in production.", "skills": ["Deployment", "Edge", "Analytics"]}
                ]}
            ]
        },
        {
            "role": "Software Engineer",
            "keywords": ("software", "developer", "programmer", " sde ", "backend", "back-end", "computer science"),
            "phases": [
                {"phase": "Phase 1: Programming & CS Core", "nodes": [
                    {"id": "SE101", "title": "Data Structures & Algorithms", "type": "Course", "provider": "NeetCode", "duration": "4 weeks", "prereqs": [], "why": "DSA fluency drives technical interviews and efficient code.", "skills": ["DSA", "Big-O"]},
                    {"id": "SE102", "title": "Git, Linux & Shell", "type": "Course", "provider": "The Odin Project", "duration": "2 weeks", "prereqs": [], "why": "Version control and CLI fluency are baseline engineering skills.", "skills": ["Git", "Linux", "Bash"]}
                ]},
                {"phase": "Phase 2: Engineering Craft", "nodes": [
                    {"id": "SE201", "title": "OOP & Design Patterns", "type": "Course", "provider": "Refactoring.Guru", "duration": "3 weeks", "prereqs": ["SE101"], "why": "Clean abstractions and patterns keep large codebases maintainable.", "skills": ["OOP", "Design Patterns"]},
                    {"id": "SE202", "title": "Databases: SQL + Redis", "type": "Course", "provider": "CMU Database Group", "duration": "3 weeks", "prereqs": ["SE102"], "why": "Modeling relational data plus caching is core backend knowledge.", "skills": ["PostgreSQL", "Redis", "Indexing"]}
                ]},
                {"phase": "Phase 3: Systems & Ship It", "nodes": [
                    {"id": "SE301", "title": "System Design Basics", "type": "Course", "provider": "ByteByteGo", "duration": "3 weeks", "prereqs": ["SE201"], "why": "Load balancers, queues, and scaling appear in mid-level interviews.", "skills": ["System Design", "Caching", "Queues"]},
                    {"id": "SE302", "title": "Backend API Capstone", "type": "Project", "provider": "GitHub Capstone", "duration": "3 weeks", "prereqs": ["SE202", "SE301"], "why": "Production REST service with auth, tests, Docker, and CI.", "skills": ["REST", "JWT", "CI/CD"]}
                ]}
            ]
        },
        {
            "role": "Cybersecurity Analyst",
            "keywords": ("cyber", "security", "hack", "pentest", "penetration", " soc ", "malware"),
            "phases": [
                {"phase": "Phase 1: Networking & OS Foundations", "nodes": [
                    {"id": "CY101", "title": "Networking Fundamentals (Net+)", "type": "Course", "provider": "Professor Messer", "duration": "3 weeks", "prereqs": [], "why": "TCP/IP, DNS, and firewalls underpin every security control.", "skills": ["TCP/IP", "DNS", "Firewalls"]},
                    {"id": "CY102", "title": "Linux for Security", "type": "Course", "provider": "TryHackMe", "duration": "2 weeks", "prereqs": [], "why": "Most security tooling lives on Linux; permissions and logs matter.", "skills": ["Linux", "Bash", "Permissions"]}
                ]},
                {"phase": "Phase 2: Offensive & Defensive Skills", "nodes": [
                    {"id": "CY201", "title": "Security+ Core Concepts", "type": "Course", "provider": "CompTIA", "duration": "4 weeks", "prereqs": ["CY101"], "why": "Industry-standard coverage of threats, crypto, and IAM.", "skills": ["Threats", "IAM", "Crypto"]},
                    {"id": "CY202", "title": "Hands-on Hacking Labs", "type": "Project", "provider": "TryHackMe/HTB", "duration": "3 weeks", "prereqs": ["CY102", "CY201"], "why": "Legal practice exploiting and hardening vulnerable machines.", "skills": ["Nmap", "Burp", "Metasploit"]}
                ]},
                {"phase": "Phase 3: Blue Team Operations", "nodes": [
                    {"id": "CY301", "title": "SIEM & Log Analysis (Splunk)", "type": "Course", "provider": "LetsDefend", "duration": "3 weeks", "prereqs": ["CY201"], "why": "SOC analysts triage alerts using SIEM queries daily.", "skills": ["Splunk", "SIEM", "Triage"]},
                    {"id": "CY302", "title": "Incident Response Capstone", "type": "Project", "provider": "Blue Team Labs", "duration": "2 weeks", "prereqs": ["CY301"], "why": "Simulated breach investigation end-to-end with report writing.", "skills": ["DFIR", "Reporting"]}
                ]}
            ]
        },
        {
            "role": "Cloud / DevOps Engineer",
            "keywords": ("cloud", "devops", " aws ", "azure", " kubernetes", "docker", " sre ", "terraform", " ci/cd"),
            "phases": [
                {"phase": "Phase 1: Foundations", "nodes": [
                    {"id": "CL101", "title": "Linux Administration", "type": "Course", "provider": "Linux Foundation", "duration": "3 weeks", "prereqs": [], "why": "Servers, systemd, and networking are the substrate of cloud.", "skills": ["Linux", "Networking", "SSH"]},
                    {"id": "CL102", "title": "Scripting: Bash + Python", "type": "Course", "provider": "Automate the Boring Stuff", "duration": "2 weeks", "prereqs": [], "why": "Automation glue for provisioning and operations tasks.", "skills": ["Bash", "Python", "Automation"]}
                ]},
                {"phase": "Phase 2: Cloud & Containers", "nodes": [
                    {"id": "CL201", "title": "AWS Core Services", "type": "Course", "provider": "AWS Skill Builder", "duration": "4 weeks", "prereqs": ["CL101"], "why": "EC2/S3/IAM/VPC knowledge anchors most cloud job descriptions.", "skills": ["EC2", "S3", "IAM", "VPC"]},
                    {"id": "CL202", "title": "Docker & Containers", "type": "Course", "provider": "KodeKloud", "duration": "2 weeks", "prereqs": ["CL102"], "why": "Container images and registries precede orchestration.", "skills": ["Docker", "Registries"]}
                ]},
                {"phase": "Phase 3: Orchestration & IaC", "nodes": [
                    {"id": "CL301", "title": "Kubernetes (CKA Prep)", "type": "Course", "provider": "KodeKloud", "duration": "4 weeks", "prereqs": ["CL202"], "why": "Declarative orchestration is the industry deployment standard.", "skills": ["Kubernetes", "Helm"]},
                    {"id": "CL302", "title": "Terraform + CI/CD Capstone", "type": "Project", "provider": "GitHub Capstone", "duration": "3 weeks", "prereqs": ["CL201", "CL301"], "why": "Infra-as-code pipeline deploying an app automatically on merge.", "skills": ["Terraform", "GitHub Actions", "IaC"]}
                ]}
            ]
        },
        {
            "role": "Mobile Developer",
            "keywords": ("mobile", "android", " ios ", "flutter", "react native", "kotlin", "swift"),
            "phases": [
                {"phase": "Phase 1: Language & Tooling", "nodes": [
                    {"id": "MB101", "title": "Kotlin or Swift Essentials", "type": "Course", "provider": "JetBrains/Apple", "duration": "3 weeks", "prereqs": [], "why": "Native language fluency accelerates everything platform-specific.", "skills": ["Kotlin", "Swift"]},
                    {"id": "MB102", "title": "Android Studio / Xcode", "type": "Course", "provider": "Google/Apple", "duration": "2 weeks", "prereqs": [], "why": "Emulators, debuggers, and project structure daily drivers.", "skills": ["IDE", "Debugging"]}
                ]},
                {"phase": "Phase 2: Building Real Apps", "nodes": [
                    {"id": "MB201", "title": "Modern UI (Compose/SwiftUI)", "type": "Course", "provider": "Google/Apple", "duration": "3 weeks", "prereqs": ["MB101"], "why": "Declarative UI frameworks are how production screens ship today.", "skills": ["Compose", "SwiftUI"]},
                    {"id": "MB202", "title": "Data: APIs + Local Storage", "type": "Course", "provider": "Udacity", "duration": "2 weeks", "prereqs": ["MB102"], "why": "Networking, caching, Room/ CoreData persistence patterns.", "skills": ["REST", "Room", "Offline-first"]}
                ]},
                {"phase": "Phase 3: Release Engineering", "nodes": [
                    {"id": "MB301", "title": "Firebase Backend Integration", "type": "Course", "provider": "Firebase", "duration": "2 weeks", "prereqs": ["MB201"], "why": "Auth, push notifications, and analytics without own server.", "skills": ["Firebase", "FCM"]},
                    {"id": "MB302", "title": "Store Release Capstone", "type": "Project", "provider": "Play Store / App Store", "duration": "3 weeks", "prereqs": ["MB301", "MB202"], "why": "Signed, published app with crash reporting and reviews.", "skills": ["Signing", "Release", "Crashlytics"]}
                ]}
            ]
        },
        {
            "role": "Product Designer (UI/UX)",
            "keywords": (" ui ", " ux ", "figma", "product manager", "product design", "designer", "design thinking"),
            "phases": [
                {"phase": "Phase 1: UX Foundations", "nodes": [
                    {"id": "UX101", "title": "Design Thinking & User Research", "type": "Course", "provider": "Google UX Certificate", "duration": "3 weeks", "prereqs": [], "why": "Problem framing and user interviews anchor good products.", "skills": ["Research", "Personas"]},
                    {"id": "UX102", "title": "Figma Fundamentals", "type": "Course", "provider": "Figma Learn", "duration": "2 weeks", "prereqs": [], "why": "Industry-standard canvas for wireframes through handoff.", "skills": ["Figma", "Wireframing"]}
                ]},
                {"phase": "Phase 2: Interface Craft", "nodes": [
                    {"id": "UX201", "title": "Visual Design & Type/Color", "type": "Course", "provider": "Refactoring UI", "duration": "2 weeks", "prereqs": ["UX102"], "why": "Hierarchy, spacing, and color separate amateur from pro screens.", "skills": ["Typography", "Color", "Layout"]},
                    {"id": "UX202", "title": "Prototype a Mobile App Flow", "type": "Project", "provider": "Portfolio Lab", "duration": "3 weeks", "prereqs": ["UX101", "UX102"], "why": "Clickable prototype demonstrates end-to-end product thinking.", "skills": ["Prototyping", "Flows"]}
                ]},
                {"phase": "Phase 3: Validate & Portfolio", "nodes": [
                    {"id": "UX301", "title": "Usability Testing", "type": "Course", "provider": "NN/g", "duration": "2 weeks", "prereqs": ["UX202"], "why": "Evidence-driven iteration is the designer's superpower.", "skills": ["Usability", "Iteration"]},
                    {"id": "UX302", "title": "Case Study Portfolio Capstone", "type": "Project", "provider": "Portfolio Lab", "duration": "3 weeks", "prereqs": ["UX301"], "why": "Recruiters hire from documented process, not just visuals.", "skills": ["Case Study", "Storytelling"]}
                ]}
            ]
        },
        {
            "role": "Musician",
            "keywords": ("guitar", "piano", "music", "sing", "song", "drum", "violin", "flute", "ukulele"),
            "phases": [
                {"phase": "Phase 1: First Sounds & Rhythm", "nodes": [
                    {"id": "MU101", "title": "Instrument Setup & Care Basics", "type": "Course", "provider": "YouTube (ArtistWorks)", "duration": "1 week", "prereqs": [], "why": "Correct posture and tuning habits prevent bad technique early.", "skills": ["Posture", "Tuning"]},
                    {"id": "MU102", "title": "Rhythm, Timing & Basic Notation", "type": "Course", "provider": "Musictheory.net", "duration": "2 weeks", "prereqs": [], "why": "Internalizing beat and reading simple notation unlocks songs.", "skills": ["Rhythm", "Notation"]}
                ]},
                {"phase": "Phase 2: Chords, Scales & First Songs", "nodes": [
                    {"id": "MU201", "title": "Core Chords & Progressions", "type": "Course", "provider": "JustinGuitar / Simply Piano", "duration": "4 weeks", "prereqs": ["MU101"], "why": "A handful of chords unlocks thousands of popular songs.", "skills": ["Chords", "Changes"]},
                    {"id": "MU202", "title": "Play 3 Full Songs", "type": "Project", "provider": "Ultimate Guitar / Songsterr", "duration": "3 weeks", "prereqs": ["MU201", "MU102"], "why": "Song reps build muscle memory far better than drills alone.", "skills": ["Repertoire", "Muscle Memory"]}
                ]},
                {"phase": "Phase 3: Expression & Performance", "nodes": [
                    {"id": "MU301", "title": "Scales, Improvisation & Dynamics", "type": "Course", "provider": "YouTube (Paul Davids)", "duration": "3 weeks", "prereqs": ["MU201"], "why": "Scales and dynamics turn playing notes into making music.", "skills": ["Improvisation", "Dynamics"]},
                    {"id": "MU302", "title": "Record & Share a Performance", "type": "Project", "provider": "Open Mic / Socials", "duration": "2 weeks", "prereqs": ["MU301"], "why": "Performing cements skills and builds confidence.", "skills": ["Performance", "Recording"]}
                ]}
            ]
        },
        {
            "role": "Language Learner",
            "keywords": ("language", "english speak", "spanish", "french", "german", "japanese", "korean", "chinese", "mandarin", "italian", "ielts", "toefl", "fluent"),
            "phases": [
                {"phase": "Phase 1: Core Vocabulary & Sound System", "nodes": [
                    {"id": "LG101", "title": "Daily App Habit: Top 1000 Words", "type": "Practice", "provider": "Duolingo / Anki", "duration": "4 weeks", "prereqs": [], "why": "High-frequency vocabulary covers most everyday conversation.", "skills": ["Vocabulary", "Listening"]},
                    {"id": "LG102", "title": "Pronunciation & Alphabet Bootcamp", "type": "Course", "provider": "YouTube (native speakers)", "duration": "2 weeks", "prereqs": [], "why": "Training your ear and mouth early prevents fossilized errors.", "skills": ["Pronunciation", "Phonetics"]}
                ]},
                {"phase": "Phase 2: Conversational Foundations", "nodes": [
                    {"id": "LG201", "title": "Grammar Essentials in Context", "type": "Course", "provider": "Language Transfer / Coursera", "duration": "3 weeks", "prereqs": ["LG101"], "why": "Pattern-based grammar beats memorizing rule tables.", "skills": ["Sentence Patterns", "Tenses"]},
                    {"id": "LG202", "title": "Weekly Speaking Sessions", "type": "Project", "provider": "iTalki / Tandem", "duration": "Ongoing", "prereqs": ["LG101", "LG102"], "why": "Speaking from week one is the fastest fluency driver.", "skills": ["Speaking", "Confidence"]}
                ]},
                {"phase": "Phase 3: Immersion & Fluency", "nodes": [
                    {"id": "LG301", "title": "Comprehensible Input Routine", "type": "Practice", "provider": "Netflix + Language Reactor", "duration": "4 weeks", "prereqs": ["LG201"], "why": "Massive enjoyable input builds intuition for phrasing.", "skills": ["Comprehension", "Slang"]},
                    {"id": "LG302", "title": "Milestone: 15-min Conversation Test", "type": "Project", "provider": "iTalki Assessment", "duration": "1 week", "prereqs": ["LG301"], "why": "A measurable checkpoint proves your fluency progress.", "skills": ["Fluency Check", "Goal Review"]}
                ]}
            ]
        },
        {
            "role": "Fitness Enthusiast",
            "keywords": ("fit", " gym ", "workout", "yoga", "weight loss", "weight gain", "diet", "nutrition", "running", "marathon", "calisthenics", "bodybuild", "health"),
            "phases": [
                {"phase": "Phase 1: Baseline & Habits", "nodes": [
                    {"id": "FT101", "title": "Movement Screen & Goal Setting", "type": "Course", "provider": "Nike Training Club", "duration": "1 week", "prereqs": [], "why": "Knowing your baseline keeps training safe and measurable.", "skills": ["Assessment", "SMART Goals"]},
                    {"id": "FT102", "title": "Habit Anchor: 20-min Daily Movement", "type": "Practice", "provider": "Apple Fitness+ / YouTube", "duration": "3 weeks", "prereqs": [], "why": "Consistency beats intensity for lasting results.", "skills": ["Consistency", "Mobility"]}
                ]},
                {"phase": "Phase 2: Structured Training & Fuel", "nodes": [
                    {"id": "FT201", "title": "Strength Training Fundamentals", "type": "Course", "provider": "Stronger by Science", "duration": "4 weeks", "prereqs": ["FT102"], "why": "Progressive overload on compound lifts drives body recomposition.", "skills": ["Squat", "Deadlift", "Press"]},
                    {"id": "FT202", "title": "Nutrition Basics & Meal Framework", "type": "Course", "provider": "Precision Nutrition", "duration": "2 weeks", "prereqs": [], "why": "Protein, portions, and hydration power performance and recovery.", "skills": ["Macros", "Meal Prep"]}
                ]},
                {"phase": "Phase 3: Progressive Challenge", "nodes": [
                    {"id": "FT301", "title": "Cardio Engine: Zone-2 + Intervals", "type": "Practice", "provider": "Couch to 5K / Zwift", "duration": "4 weeks", "prereqs": ["FT201"], "why": "Aerobic base improves energy, recovery, and endurance.", "skills": ["Endurance", "Heart-Rate Zones"]},
                    {"id": "FT302", "title": "Milestone Event or 8-Week PR Block", "type": "Project", "provider": "Local Parkrun / Gym Test", "duration": "2 weeks", "prereqs": ["FT301", "FT202"], "why": "A timed event converts training into a proud achievement.", "skills": ["Peaking", "Tracking"]}
                ]}
            ]
        },
        {
            "role": "Home Chef",
            "keywords": ("cook", "cooking", "baking", "bake", "chef", "cuisine", "recipe", "culinary"),
            "phases": [
                {"phase": "Phase 1: Kitchen Confidence", "nodes": [
                    {"id": "CK101", "title": "Knife Skills & Kitchen Safety", "type": "Course", "provider": "YouTube (Jacob Burton)", "duration": "1 week", "prereqs": [], "why": "Clean cuts and safe habits make cooking faster and calmer.", "skills": ["Knife Work", "Safety"]},
                    {"id": "CK102", "title": "Essential Techniques: Saute, Roast, Braise", "type": "Course", "provider": "MasterClass / America's Test Kitchen", "duration": "3 weeks", "prereqs": [], "why": "Techniques free you from following recipes rigidly.", "skills": ["Saute", "Roasting", "Braising"]}
                ]},
                {"phase": "Phase 2: Flavor & Repertoire", "nodes": [
                    {"id": "CK201", "title": "Sauces, Spices & Seasoning Logic", "type": "Course", "provider": "Salt Fat Acid Heat", "duration": "3 weeks", "prereqs": ["CK102"], "why": "Balancing salt-fat-acid-heat is the core of tasty food.", "skills": ["Seasoning", "Sauces", "Spice Blending"]},
                    {"id": "CK202", "title": "Cook 15 Signature Dishes", "type": "Project", "provider": "Cookbook of Choice", "duration": "4 weeks", "prereqs": ["CK201"], "why": "Repetition across dishes builds instinctive timing.", "skills": ["Repertoire", "Plating"]}
                ]},
                {"phase": "Phase 3: Craft & Hosting", "nodes": [
                    {"id": "CK301", "title": "Baking Science: Bread & Pastry", "type": "Course", "provider": "King Arthur Baking School", "duration": "3 weeks", "prereqs": ["CK201"], "why": "Precision baking teaches measurement and patience.", "skills": ["Bread", "Pastry"]},
                    {"id": "CK302", "title": "Host a Full Dinner Party", "type": "Project", "provider": "Friends & Family", "duration": "2 weeks", "prereqs": ["CK301"], "why": "Planning and executing a menu under time pressure is the real test.", "skills": ["Menu Planning", "Timing"]}
                ]}
            ]
        },
        {
            "role": "Creative Artist",
            "keywords": ("draw", "drawing", "sketch", "paint", "painting", "photograph", "photography", "writing", "write a", "novel", "poetry", "creative"),
            "phases": [
                {"phase": "Phase 1: Seeing Like an Artist", "nodes": [
                    {"id": "AR101", "title": "Fundamentals: Line, Shape, Value", "type": "Course", "provider": "Drawabox / Proko", "duration": "3 weeks", "prereqs": [], "why": "Construction and values are the grammar of visual art.", "skills": ["Line Control", "Values"]},
                    {"id": "AR102", "title": "Daily Sketchbook Habit", "type": "Practice", "provider": "Reddit r/SketchDaily", "duration": "4 weeks", "prereqs": [], "why": "Volume with reflection accelerates hand-eye growth.", "skills": ["Observation", "Consistency"]}
                ]},
                {"phase": "Phase 2: Craft Your Medium", "nodes": [
                    {"id": "AR201", "title": "Color, Composition & Light", "type": "Course", "provider": "Ctrl+Paint / Marc Brunet", "duration": "4 weeks", "prereqs": ["AR101"], "why": "Composition choices decide whether work feels professional.", "skills": ["Color Theory", "Composition"]},
                    {"id": "AR202", "title": "Finish 5 Polished Pieces", "type": "Project", "provider": "Personal Project", "duration": "4 weeks", "prereqs": ["AR201"], "why": "Finished works teach follow-through and reveal style.", "skills": ["Finishing", "Style"]}
                ]},
                {"phase": "Phase 3: Voice & Audience", "nodes": [
                    {"id": "AR301", "title": "Study Masters + Deliberate Copywork", "type": "Practice", "provider": "Library / Museum Archives", "duration": "3 weeks", "prereqs": ["AR202"], "why": "Copying masters internalizes decisions you can't see yet.", "skills": ["Analysis", "Technique"]},
                    {"id": "AR302", "title": "Public Portfolio & Feedback Loop", "type": "Project", "provider": "Instagram / ArtStation", "duration": "2 weeks", "prereqs": ["AR301"], "why": "Sharing invites critique that levels you up fast.", "skills": ["Portfolio", "Critique"]}
                ]}
            ]
        },
        {
            "role": "Entrepreneur / Marketer",
            "keywords": ("business", "entrepreneur", "startup", "marketing", "stock", "invest", "trading", "finance", "sales", "mba", "freelanc"),
            "phases": [
                {"phase": "Phase 1: Money & Market Literacy", "nodes": [
                    {"id": "BZ101", "title": "Personal Finance & Investing 101", "type": "Course", "provider": "Khan Academy / Zerodha Varsity", "duration": "3 weeks", "prereqs": [], "why": "Compounding, risk, and cash flow basics precede business moves.", "skills": ["Budgeting", "Investing Basics"]},
                    {"id": "BZ102", "title": "How Businesses Actually Work", "type": "Course", "provider": "Personal MBA (Book/Course)", "duration": "3 weeks", "prereqs": [], "why": "Value creation, marketing, and delivery form the mental model.", "skills": ["Business Model", "Unit Economics"]}
                ]},
                {"phase": "Phase 2: Build & Validate", "nodes": [
                    {"id": "BZ201", "title": "Marketing Fundamentals & Positioning", "type": "Course", "provider": "Google Digital Garage / HubSpot", "duration": "3 weeks", "prereqs": ["BZ102"], "why": "Attention is the scarcest resource; positioning wins it.", "skills": ["Positioning", "Funnels", "Copywriting"]},
                    {"id": "BZ202", "title": "Launch a Micro-Project for Real Money", "type": "Project", "provider": "Stripe/Gumroad + Socials", "duration": "4 weeks", "prereqs": ["BZ201"], "why": "One real sale teaches more than ten courses.", "skills": ["Landing Page", "Pricing", "Outreach"]}
                ]},
                {"phase": "Phase 3: Scale What Works", "nodes": [
                    {"id": "BZ301", "title": "Analytics & Growth Loops", "type": "Course", "provider": "Reforge (Free Content) / YouTube", "duration": "3 weeks", "prereqs": ["BZ202"], "why": "Metrics tell you which lever to pull next.", "skills": ["KPIs", "Retention", "Experiments"]},
                    {"id": "BZ302", "title": "90-Day Operating Plan Capstone", "type": "Project", "provider": "Notion / Mentor Review", "duration": "2 weeks", "prereqs": ["BZ301"], "why": "Documented strategy turns hustle into a repeatable system.", "skills": ["Planning", "Review Cycles"]}
                ]}
            ]
        },
        {
            "role": "Exam Topper",
            "keywords": ("exam", "jee", "neet", " gate ", "upsc", "cat exam", "board exam", "olympiad", "sat "),
            "phases": [
                {"phase": "Phase 1: Syllabus Mapping & Baseline", "nodes": [
                    {"id": "EX101", "title": "Break Down the Syllabus & Weightage", "type": "Practice", "provider": "Official Syllabus + Past Papers", "duration": "1 week", "prereqs": [], "why": "Studying high-weightage topics first maximizes marks per hour.", "skills": ["Prioritization", "Planning"]},
                    {"id": "EX102", "title": "Diagnostic Mock: Find Gaps", "type": "Practice", "provider": "Previous Year Papers", "duration": "1 week", "prereqs": [], "why": "A scored baseline exposes weak areas to target first.", "skills": ["Self-Assessment"]}
                ]},
                {"phase": "Phase 2: Concept Mastery Loop", "nodes": [
                    {"id": "EX201", "title": "Concept Learning via Best Resources", "type": "Course", "provider": "NPTEL / Khan Academy / Top Faculty", "duration": "6 weeks", "prereqs": ["EX101"], "why": "Understanding concepts once beats re-reading notes thrice.", "skills": ["Concepts", "Notes-Making"]},
                    {"id": "EX202", "title": "Spaced Revision + Active Recall System", "type": "Practice", "provider": "Anki + Revision Planner", "duration": "Ongoing", "prereqs": ["EX201"], "why": "Recall practice doubles retention vs passive review.", "skills": ["Memory Techniques", "Revision"]}
                ]},
                {"phase": "Phase 3: Exam Simulation & Peak", "nodes": [
                    {"id": "EX301", "title": "Full-Length Timed Mock Series", "type": "Practice", "provider": "Test Series (Official/Allen/IMS)", "duration": "4 weeks", "prereqs": ["EX202"], "why": "Simulating pressure builds speed, accuracy, and stamina.", "skills": ["Time Management", "Accuracy"]},
                    {"id": "EX302", "title": "Final Error-Log Sprint", "type": "Project", "provider": "Personal Mistake Notebook", "duration": "2 weeks", "prereqs": ["EX301"], "why": "Fixing YOUR recurring errors yields the biggest score jump.", "skills": ["Error Analysis", "Composure"]}
                ]}
            ]
        }
    ]

    match = next(
        (t for t in domain_templates if any(k in goal_l for k in t["keywords"])),
        None
    )

    if match:
        role = match["role"]
        phases = match["phases"]
    else:
        # Universal scaffold: adapts to ANY learning goal not covered above
        subject = goal.strip().rstrip('.!?,;:') or "Your Learning Goal"
        role = subject if len(subject) <= 42 else subject[:39] + "..."
        phases = [
            {
                "phase": "Phase 1: Foundations & Orientation",
                "nodes": [
                    {"id": "UN101", "title": f"{subject}: Beginner's Guide & Core Concepts", "type": "Course", "provider": "YouTube / Coursera / Local Classes", "duration": "2 weeks", "prereqs": [], "why": "A structured introduction builds correct fundamentals from day one.", "skills": ["Fundamentals", "Key Terminology"]},
                    {"id": "UN102", "title": "Set Up Your Tools, Space & Weekly Routine", "type": "Practice", "provider": "Self-directed + Checklists", "duration": "1 week", "prereqs": [], "why": "The right environment and a fixed schedule make progress automatic.", "skills": ["Habit Design", "Preparation"]}
                ]
            },
            {
                "phase": "Phase 2: Deliberate Practice",
                "nodes": [
                    {"id": "UN201", "title": f"Follow a Guided {subject} Practice Plan", "type": "Course", "provider": "Best-Rated Course / Coach / App", "duration": "4 weeks", "prereqs": ["UN101"], "why": "Deliberate, feedback-driven practice beats random effort every time.", "skills": ["Technique", "Consistency"]},
                    {"id": "UN202", "title": "Join a Community & Seek Expert Feedback", "type": "Project", "provider": "Reddit / Discord / Local Club / Mentor", "duration": "Ongoing", "prereqs": ["UN101"], "why": "External feedback exposes blind spots you cannot see alone.", "skills": ["Feedback Loops", "Networking"]}
                ]
            },
            {
                "phase": "Phase 3: Apply, Showcase & Level Up",
                "nodes": [
                    {"id": "UN301", "title": f"Intermediate Challenge in {subject}", "type": "Practice", "provider": "Community Challenges / Certifications", "duration": "3 weeks", "prereqs": ["UN201"], "why": "Stretch goals convert knowledge into real capability.", "skills": ["Application", "Problem Solving"]},
                    {"id": "UN302", "title": f"Milestone Showcase: {subject} Capstone", "type": "Project", "provider": "Personal Milestone (Event/Exam/Portfolio)", "duration": "2 weeks", "prereqs": ["UN301", "UN202"], "why": "A tangible achievement marks the journey from learner to practitioner.", "skills": ["Mastery Proof", "Confidence"]}
                ]
            }
        ]

    return {
        "goal": goal,
        "role": role,
        "phases": phases
    }

# ==========================================
# XAI: TRANSPARENT NODE RELEVANCE SCORING
# ==========================================
def compute_node_relevance(node: dict, profile: dict, completed_nodes: set, phase_idx: int, total_phases: int):
    """Deterministic, explainable relevance score (0-100) for a roadmap node.

    Factors:
      - Skill-gap coverage (/40): rewards teaching skills the learner does NOT have
      - Prerequisite readiness (/30): how many prereqs are already completed
      - Experience-phase fit (/30): early phases suit beginners, late phases suit advanced
    Returns (score:int, breakdown:list[str]).
    """
    skills = node.get("skills") or []
    prereqs = node.get("prereqs") or []
    breakdown = []

    # Factor 1 - Skill-gap coverage (max 40)
    known_skills = profile.get("skills") or []
    gap = sum(1 for s in skills if s not in known_skills)
    if skills:
        f_gap = round((gap / len(skills)) * 40, 1)
        breakdown.append(f"Skill-gap coverage: +{f_gap:.0f}/40 ({gap} of {len(skills)} skills new to you)")
    else:
        f_gap = 20.0
        breakdown.append(f"Skill-gap coverage: +{f_gap:.0f}/40 (no skill tags on this module)")

    # Factor 2 - Prerequisite readiness (max 30)
    if prereqs:
        met = sum(1 for p in prereqs if p in completed_nodes)
        f_prereq = round((met / len(prereqs)) * 30, 1)
        breakdown.append(f"Prerequisite readiness: +{f_prereq:.0f}/30 ({met}/{len(prereqs)} completed)")
    else:
        f_prereq = 30.0
        breakdown.append("Prerequisite readiness: +30/30 (entry point — no prerequisites)")

    # Factor 3 - Experience-phase fit (max 30)
    depth = (phase_idx + 1) / max(total_phases, 1)
    level = profile.get("experience_level") or "Beginner"
    fit_target = {"Beginner": 0.25, "Intermediate": 0.5, "Advanced": 0.85}.get(level, 0.5)
    closeness = max(0.0, 1.0 - abs(depth - fit_target))
    f_fit = round(closeness * 30, 1)
    phase_no = phase_idx + 1
    breakdown.append(f"Experience-phase fit: +{f_fit:.0f}/30 ({level} level vs Phase {phase_no} of {total_phases})")

    score = min(100, round(f_gap + f_prereq + f_fit))
    return score, breakdown

# ==========================================
# SIDEBAR: PILLAR 2 & GROQ CONFIGURATION
# ==========================================
with st.sidebar:
    st.image("assets/logo.png", width=64)
    st.title("Settings & Profile")
    
    # GROQ API INPUT SECTION
    st.subheader("🔑 Groq API Key")
    groq_key_input = st.text_input(
        "Enter Groq API Key (`gsk_...`)",
        type="password",
        placeholder="gsk_...",
        help="Paste your Groq Cloud API Key starting with gsk_"
    )
    
    # Fetch the live model catalog for this key (cached per session)
    _key_for_models = groq_key_input or os.environ.get("GROQ_API_KEY", "")
    available_models = list(DEFAULT_GROQ_MODELS)
    if _key_for_models and HAS_GROQ:
        _cache_key = f"_groq_models_{_key_for_models[:10]}"
        if _cache_key not in st.session_state:
            try:
                _models_client = Groq(api_key=_key_for_models)
                st.session_state[_cache_key] = sorted(
                    m.id for m in _models_client.models.list().data
                )
            except Exception:
                st.session_state[_cache_key] = list(DEFAULT_GROQ_MODELS)
        available_models = st.session_state[_cache_key]

    groq_model_choice = st.selectbox(
        "Select Groq LLM Model",
        available_models,
        index=0,
        help="Models fetched live from your Groq account; falls back to defaults if unreachable"
    )
    
    if groq_key_input:
        if groq_key_input.startswith("gsk_"):
            os.environ["GROQ_API_KEY"] = groq_key_input
            st.success("⚡ Groq API Key Active!", icon="✅")
        else:
            st.warning("Key should start with `gsk_`")
    elif os.environ.get("GROQ_API_KEY", "").startswith("gsk_"):
        st.caption("Using GROQ_API_KEY loaded from environment (.env)")
            
    st.divider()

    # MODE CONTROLS: DEMO TOGGLE & SCRATCH RESET
    st.caption("Mode")
    demo_toggle = st.toggle(
        "🎬 Demo Mode",
        key="demo_mode",
        help="Preview a pre-built sample roadmap without entering a goal"
    )
    btn_scratch = st.button("🔄 Start from Scratch", width="stretch")

    if btn_scratch:
        st.session_state._pending_scratch = True
        st.rerun()

    if demo_toggle != st.session_state._prev_demo:
        if demo_toggle:
            st.session_state.roadmap_data = generate_fallback_roadmap(
                "AI & ML Engineer", st.session_state.user_profile)
            st.session_state.completed_nodes = set()
            st.toast("🎬 Demo Mode ON — sample roadmap loaded!", icon="🎬")
        else:
            st.session_state.roadmap_data = None
            st.session_state.completed_nodes = set()
            st.toast("Demo Mode OFF — enter your own goal to begin.", icon="✏️")
        st.session_state._prev_demo = demo_toggle

    st.divider()
    
    # PILLAR 2: LEARNER PROFILING ENGINE
    st.caption("Pillar 2: Learner Profiling Engine")
    with st.expander("👤 Learner Attributes", expanded=True):
        role_input = st.selectbox(
            "Primary Interest Area (context hint)",
            ["AI & ML Engineer", "Data Scientist", "Full-Stack Web Developer", "Cloud Architect",
             "Cybersecurity Analyst", "Musician", "Language Learner", "Fitness Enthusiast",
             "Home Chef", "Creative Artist", "Entrepreneur / Marketer", "Exam Topper"],
            index=0,
            help="Optional context — your typed goal drives the actual roadmap"
        )
        exp_input = st.select_slider(
            "Current Experience Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Intermediate"
        )
        hours_input = st.slider("Weekly Study Commitment", 5, 40, 15, help="Hours per week dedicated to learning")
        
        known_skills = st.multiselect(
            "Verified Mastered Skills",
            ["Python", "Basic Math", "SQL", "Git", "HTML/CSS", "Linear Algebra", "JavaScript", "Docker"],
            default=["Python", "Basic Math", "SQL"]
        )
        
        st.session_state.user_profile.update({
            'target_role': role_input,
            'experience_level': exp_input,
            'weekly_hours': hours_input,
            'skills': known_skills
        })

# ==========================================
# MAIN INTERFACE: HERO & GOAL INTAKE (PILLAR 1)
# ==========================================
st.markdown("""
<div class="hero-card">
    <div class="hero-title">SkillPath AI <span style="font-size:1.1rem;font-weight:500;color:#a1a1aa;-webkit-text-fill-color:#a1a1aa;">— by Team Cortex</span></div>
    <div class="hero-subtitle">Any goal. One clear path. Get a personalized, milestone-by-milestone learning roadmap for anything you want to master — careers, languages, music, fitness, exams and beyond.</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# PILLAR 1: GOAL INTAKE — QUICK PICKS + INPUT
# ==========================================
QUICK_PICKS = {
    "💻 Software Engineer": "I want to become a Software Engineer",
    "🌐 Web Developer": "I want to become a Web Developer",
    "🧪 Data Scientist": "I want to become a Data Scientist",
    "🛡️ Cybersecurity Analyst": "I want to become a Cybersecurity Analyst",
    "☁️ Cloud / DevOps Engineer": "I want to become a Cloud / DevOps Engineer",
    "🎸 Learn Guitar": "I want to learn guitar from scratch",
    "🗣️ Speak a New Language": "I want to become fluent in Spanish",
    "💪 Get Fit & Healthy": "I want to improve my fitness and health",
    "🍳 Learn Cooking": "I want to learn cooking and baking",
    "✏️ Learn Drawing": "I want to learn drawing and sketching",
    "📈 Start a Business": "I want to start a business and learn marketing",
    "📚 Crack Competitive Exams": "I want to crack competitive exams with a study routine",
}

def _generate_roadmap(goal_text: str):
    """Shared roadmap generation routine (used by Generate button + quick picks)."""
    active_key = groq_key_input or os.environ.get("GROQ_API_KEY", "")
    if st.session_state.demo_mode:
        st.session_state._pending_demo_off = True
    with st.spinner("⚡ Analyzing your goal, checking skill gaps, and building the DAG roadmap..."):
        if active_key and HAS_GROQ:
            st.session_state.roadmap_data = generate_roadmap_with_groq(
                goal_text, st.session_state.user_profile, active_key, groq_model_choice)
        else:
            st.session_state.roadmap_data = generate_fallback_roadmap(
                goal_text, st.session_state.user_profile)
        st.session_state.completed_nodes = set()
        if st.session_state._pending_demo_off:
            st.rerun()
        st.toast("🎉 Personal Learning Pathway Generated!", icon="🚀")

# One-click domain selection: fills the input and generates instantly
selected_pill = st.pills(
    "⚡ Quick pick a career:",
    options=list(QUICK_PICKS.keys()),
    help="Click any option to instantly generate a tailored roadmap — or type your own goal below"
)

if selected_pill and selected_pill != st.session_state.get("_last_pill"):
    st.session_state._last_pill = selected_pill
    st.session_state.goal_box = QUICK_PICKS[selected_pill]
    _generate_roadmap(QUICK_PICKS[selected_pill])

col_input, col_preset = st.columns([3, 1])

with col_input:
    goal_query = st.text_input(
        "💬 Or describe ANY learning goal — career, hobby, language, sport, subject...",
        placeholder="e.g. learn guitar basics in 2 months, fluent French, crack JEE, get fit, become a data scientist",
        key="goal_box"
    )

with col_preset:
    st.write(" ")
    st.write(" ")
    btn_generate = st.button("🚀 Generate Path", type="primary", width="stretch")

if btn_generate and goal_query.strip():
    _generate_roadmap(goal_query.strip())

# EMPTY STATE GUARD: scratch mode until a roadmap exists
if not st.session_state.roadmap_data:
    st.info(
        "👋 **Welcome to SkillPath AI — built for ANY learning goal!**\n\n"
        "1. ⚡ **Quick pick** a goal above (tech, music, fitness, languages...) for instant results,\n"
        "2. ✏️ Type literally any goal — *guitar, French, marathon, baking, JEE...* — and hit **Generate Path**, or\n"
        "3. 🎬 Enable **Demo Mode** in the sidebar to preview a sample roadmap."
    )
    st.stop()

roadmap = st.session_state.roadmap_data

# ==========================================
# METRIC SUMMARY BAR
# ==========================================
all_nodes = [n for phase in roadmap["phases"] for n in phase["nodes"]]
total_nodes = len(all_nodes)
completed_count = len(st.session_state.completed_nodes)
progress_pct = int((completed_count / total_nodes) * 100) if total_nodes > 0 else 0

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-val">{roadmap['role']}</div>
        <div class="metric-lbl">Learning Focus</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-val">{total_nodes} Nodes</div>
        <div class="metric-lbl">Total Milestones</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-val">{completed_count} / {total_nodes}</div>
        <div class="metric-lbl">Completed</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-val">{progress_pct}%</div>
        <div class="metric-lbl">Roadmap Mastery</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==========================================
# MAIN TABS: ALL 6 PILLARS VISUALIZED
# ==========================================
tab_dag, tab_recs, tab_xai, tab_dash = st.tabs([
    "🔀 Pillar 4: Streamlit-Flow DAG (React Flow)",
    "📚 Pillar 3: Course & Project Recs",
    "💡 Pillar 5: Explainable AI (XAI)",
    "📊 Pillar 6: Skill Radar & Progress"
])

# ------------------------------------------
# TAB 1: PILLAR 4 - VISUAL DAG FLOWCHART (STREAMLIT-FLOW)
# ------------------------------------------
with tab_dag:
    st.subheader("🔀 Prerequisite-Aware Directed Acyclic Graph (DAG) Canvas")
    st.caption("Interactive 2D React Flow canvas powered by `streamlit-flow-component` with drag, pan, zoom, and prerequisite animations.")
    
    if HAS_STREAMLIT_FLOW:
        flow_nodes = []
        flow_edges = []

        for phase_idx, phase in enumerate(roadmap["phases"]):
            for node_idx, node in enumerate(phase["nodes"]):
                is_done = node["id"] in st.session_state.completed_nodes

                pos_x = phase_idx * 280
                pos_y = node_idx * 120 - 40

                label = f"{node['id']}: {node['title']}\n({node['duration']}) [{'✓ DONE' if is_done else 'READY'}]"

                flow_node = StreamlitFlowNode(
                    id=node["id"],
                    pos=(pos_x, pos_y),
                    data={'content': label},
                    node_type='input' if not node['prereqs'] else 'output' if phase_idx == len(roadmap["phases"]) - 1 else 'default',
                    source_position='right',
                    target_position='left'
                )
                flow_nodes.append(flow_node)

                for prereq in node["prereqs"]:
                    edge_id = f"e_{prereq}_{node['id']}"
                    flow_edge = StreamlitFlowEdge(
                        id=edge_id,
                        source=prereq,
                        target=node["id"],
                        animated=True
                    )
                    flow_edges.append(flow_edge)

        # v1.6.1 API: requires StreamlitFlowState as 2nd arg
        flow_state = StreamlitFlowState(flow_nodes, flow_edges)

        event = streamlit_flow(
            key="learning_path_flow",
            state=flow_state,
            height=450,
            fit_view=True,
            show_minimap=True,
            show_controls=True,
            get_node_on_click=True,
            layout=TreeLayout(direction='right')
        )

        if event and event.selected_id:
            st.info(f"📍 Interactive Node Selected: **{event.selected_id}** — View details in the **Explainable AI (XAI)** tab!")
    else:
        dot = graphviz.Digraph(comment="Learning Path DAG", graph_attr={'rankdir': 'LR', 'bgcolor': 'transparent'})
        dot.attr('node', shape='box', style='filled,rounded', fontname='Inter', fontsize='11')
        
        for phase_idx, phase in enumerate(roadmap["phases"]):
            with dot.subgraph(name=f"cluster_{phase_idx}") as c:
                c.attr(label=phase["phase"], color='#4facfe', style='dashed', fontcolor='#00f2fe')
                for node in phase["nodes"]:
                    is_done = node["id"] in st.session_state.completed_nodes
                    bg_color = "#10b981" if is_done else "#1e293b"
                    text_color = "#ffffff" if is_done else "#f3f4f6"
                    border_color = "#34d399" if is_done else "#00f2fe"
                    
                    label_text = f"{node['id']}: {node['title']}\n({node['duration']}) [{'✓ DONE' if is_done else 'READY'}]"
                    c.node(node["id"], label=label_text, fillcolor=bg_color, fontcolor=text_color, color=border_color, penwidth='2')
                    
                    for prereq in node["prereqs"]:
                        dot.edge(prereq, node["id"], color='#4facfe', penwidth='1.5')

        st.graphviz_chart(dot, width="stretch")

# ------------------------------------------
# TAB 2: PILLAR 3 - RECOMMENDATION ENGINE
# ------------------------------------------
with tab_recs:
    st.subheader("📚 Pillar 3: Curated Course & Project Recommendations")
    st.caption("Intelligent course nodes curated with provider details, duration, and direct interactive action checkpoints.")
    
    for phase in roadmap["phases"]:
        st.markdown(f"### {phase['phase']}")
        
        for node in phase["nodes"]:
            is_done = node["id"] in st.session_state.completed_nodes
            prereqs_met = not node["prereqs"] or all(p in st.session_state.completed_nodes for p in node["prereqs"])
            
            c_card, c_action = st.columns([4, 1])
            
            with c_card:
                badge_type = "badge-success" if node["type"] == "Course" else "badge-purple"
                st.markdown(f"""
                <div class="course-card">
                    <span class="badge {badge_type}">{node['type']}</span>
                    <span class="badge badge-primary">{node['provider']}</span>
                    <span class="badge badge-warning">⏱️ {node['duration']}</span>
                    <div class="course-title" style="margin-top: 8px;">{node['id']}: {node['title']}</div>
                    <p style="color: #9ca3af; font-size: 0.9rem; margin-top: 4px;">{node['why']}</p>
                    <div>
                        {' '.join([f'<span class="badge badge-primary">#{s}</span>' for s in node['skills']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with c_action:
                st.write(" ")
                st.write(" ")
                if is_done:
                    if st.button("✓ Completed", key=f"btn_undo_{node['id']}", width="stretch"):
                        st.session_state.completed_nodes.remove(node["id"])
                        st.rerun()
                else:
                    if st.button("Mark Complete", key=f"btn_done_{node['id']}", type="primary", disabled=not prereqs_met, width="stretch"):
                        st.session_state.completed_nodes.add(node["id"])
                        st.toast(f"🎉 Milestone Completed: {node['title']}!", icon="✅")
                        st.rerun()
                
                if not prereqs_met:
                    st.caption(f"🔒 Prereqs required: {', '.join(node['prereqs'])}")

# ------------------------------------------
# TAB 3: PILLAR 5 - EXPLAINABLE AI (XAI) & GROQ CHAT
# ------------------------------------------
with tab_xai:
    st.subheader("💡 Pillar 5: Explainable AI (XAI) & Groq Mentor Assistant")
    st.caption("Transparent Chain-of-Thought rationales explaining why each course was recommended + Groq Llama-3.3 chat.")
    
    col_xai_left, col_xai_right = st.columns([1, 1])
    
    with col_xai_left:
        st.markdown("### 🔍 Rationale Transparency Ledger")
        total_phases = len(roadmap["phases"])
        for phase_idx, phase in enumerate(roadmap["phases"]):
            for node in phase["nodes"]:
                score, breakdown = compute_node_relevance(
                    node, st.session_state.user_profile,
                    st.session_state.completed_nodes, phase_idx, total_phases)
                with st.expander(f"Why {node['id']}: {node['title']}? ({score}% relevant)", expanded=False):
                    st.markdown(f"**Target Skill Gap:** Replaces deficiency in *{', '.join(node.get('skills') or ['—'])}*")
                    st.markdown(f"**Prerequisite Rationale:** {node.get('why', 'Core milestone on your learning path.')}")
                    st.markdown(f"**Goal Alignment:** Supports your learning focus as **{roadmap['role']}**")
                    st.progress(score / 100, text=f"Relevance Score: {score}/100")
                    for line in breakdown:
                        st.caption(f"• {line}")
    
    with col_xai_right:
        st.markdown("### 🤖 AI Mentor — knows your roadmap")
        
        chat_box = st.container(height=350)
        with chat_box:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
        
        user_prompt = st.chat_input("Ask Groq AI about prerequisites, project guidance, or career advice...")
        if user_prompt:
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            
            active_key = groq_key_input or os.environ.get("GROQ_API_KEY", "")

            if active_key and HAS_GROQ:
                client = Groq(api_key=active_key)
                try:
                    # Build full roadmap context so the mentor answers from REAL data
                    done = st.session_state.completed_nodes
                    ctx_lines = [f"LEARNING FOCUS: {roadmap['role']}",
                                 f"ORIGINAL GOAL: {roadmap['goal']}",
                                 f"EXPERIENCE: {st.session_state.user_profile['experience_level']} | WEEKLY HOURS: {st.session_state.user_profile['weekly_hours']}",
                                 f"PROGRESS: {len(done)}/{sum(len(p['nodes']) for p in roadmap['phases'])} modules completed",
                                 "ROADMAP:"]
                    for phase in roadmap["phases"]:
                        ctx_lines.append(f"  {phase['phase']}")
                        for n in phase["nodes"]:
                            mark = "[DONE]" if n["id"] in done else (
                                "[NEXT-UNBLOCKED]" if (not n["prereqs"] or all(p in done for p in n["prereqs"])) and n["id"] not in done else "[LOCKED]")
                            ctx_lines.append(f"    - {n['id']} {mark}: {n['title']} ({n['type']} via {n['provider']}, {n['duration']}) prereqs={n['prereqs']} why={n['why']}")
                    roadmap_context = "\n".join(ctx_lines)

                    system_prompt = f"""You are SkillPath AI Mentor by Team Cortex — a warm, expert learning mentor.
The learner's COMPLETE roadmap is below. Answer STRICTLY from it.

{roadmap_context}

RULES:
1. Reference specific module IDs/titles when giving guidance (e.g. "start with SE201 next").
2. If they ask what to do next, point to the FIRST [NEXT-UNBLOCKED] module and explain its 'why'.
3. Adapt advice to the domain (music practice, language drills, exam strategy...) — never assume coding.
4. Keep replies under 150 words, friendly and actionable.
5. Off-topic questions: answer briefly, then steer back to their learning goal."""
                    messages = [{"role": "system", "content": system_prompt}]
                    # Cap context window: last 20 turns keeps tokens bounded
                    messages.extend(st.session_state.chat_history[-20:])

                    response = client.chat.completions.create(
                        messages=messages,
                        model=groq_model_choice,
                        max_tokens=500,
                        temperature=0.5
                    )
                    reply = response.choices[0].message.content
                except Exception as e:
                    reply = f"Groq response error: {str(e)}"
            else:
                # Roadmap-aware offline mentor (no API key needed)
                q = user_prompt.lower()
                done = st.session_state.completed_nodes
                next_node, next_phase = None, None
                for phase in roadmap["phases"]:
                    for n in phase["nodes"]:
                        if n["id"] not in done and (not n["prereqs"] or all(p in done for p in n["prereqs"])):
                            next_node, next_phase = n, phase["phase"]
                            break
                    if next_node:
                        break

                if any(k in q for k in ("why", "recommend", "reason")):
                    reply = (f"Your path targets **{roadmap['role']}** at **{st.session_state.user_profile['experience_level']}** level. "
                             f"Each module fills a skill gap toward that goal — open the **Explainable AI** tab on the left for per-module rationale.")
                elif any(k in q for k in ("next", "start", "what now", "todo", "do first")):
                    if next_node:
                        reply = (f"Your next step is **{next_node['id']}: {next_node['title']}** ({next_node['duration']}, via *{next_node['provider']}*) "
                                 f"in _{next_phase}_. **Why:** {next_node['why']} Budget ~{max(2, st.session_state.user_profile['weekly_hours'] // 3)} hrs/week on it.")
                    else:
                        reply = "🎉 Every module is complete! Generate a new goal or enable Demo Mode to keep learning."
                else:
                    if next_node:
                        reply = (f"For **{user_prompt.strip()}**: stay anchored to your plan — focus on **{next_node['id']}: {next_node['title']}** "
                                 f"({next_node['duration']}) across your **{st.session_state.user_profile['weekly_hours']} weekly hours**, and log progress in the Module Checklist. "
                                 f"Add a Groq key in the sidebar for fully personalized AI mentoring!")
                    else:
                        reply = f"All modules done 🎉 For **{user_prompt.strip()}**, generate a fresh goal to keep the momentum going."
            
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            # Keep stored history bounded too (welcome msg + last 39 turns)
            st.session_state.chat_history = st.session_state.chat_history[-40:]
            st.rerun()

# ------------------------------------------
# TAB 4: PILLAR 6 - DASHBOARD & RADAR
# ------------------------------------------
with tab_dash:
    st.subheader("📊 Pillar 6: Visual Dashboard & Adaptive Skill Growth")
    st.caption("Real-time skill development radar chart, milestone checklist, and next recommended actions.")
    
    col_radar, col_checklist = st.columns([1, 1])
    
    with col_radar:
        st.markdown("### 🕸️ Skill Competency Radar Chart")

        # Derive axes from THIS roadmap's skills so a guitar path shows
        # Chords/Repertoire instead of ML jargon
        node_skills = [
            s for phase in roadmap["phases"]
            for n in phase["nodes"] for s in (n.get("skills") or [])
        ]
        top_skills = [s for s, _ in Counter(node_skills).most_common(6)] or ["Fundamentals"]
        known = set(st.session_state.user_profile.get("skills") or [])
        base_vals = [45 if s in known else 15 for s in top_skills]

        current_vals = []
        for skill, base in zip(top_skills, base_vals):
            trained = any(
                skill in (n.get("skills") or []) and n["id"] in st.session_state.completed_nodes
                for p in roadmap["phases"] for n in p["nodes"]
            )
            current_vals.append(min(100, base + (18 if trained else 0)))
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=base_vals,
            theta=top_skills,
            fill='toself',
            name='Baseline Profile',
            line_color='#4facfe'
        ))
        fig.add_trace(go.Scatterpolar(
            r=current_vals,
            theta=top_skills,
            fill='toself',
            name='Current Competency',
            line_color='#10b981'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f3f4f6'),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        st.plotly_chart(fig, width="stretch")

    with col_checklist:
        st.markdown("### 🎯 Adaptive Re-Routing & Next Actions")
        
        next_node = None
        for phase in roadmap["phases"]:
            for node in phase["nodes"]:
                if node["id"] not in st.session_state.completed_nodes:
                    prereqs_met = not node["prereqs"] or all(p in st.session_state.completed_nodes for p in node["prereqs"])
                    if prereqs_met:
                        next_node = node
                        break
            if next_node:
                break
                
        if next_node:
            st.info(f"""
            👉 **Next Action Recommended for You:**  
            **{next_node['id']}: {next_node['title']}** ({next_node['provider']})  
            *Estimated Time:* {next_node['duration']}  
            *Why Now:* Prerequisites met! Mastering this unlocks downstream nodes.
            """)
        else:
            st.balloons()
            st.success("🏆 Congratulations! You have completed all milestones on your learning path!")
            
        st.markdown("#### 📁 Roadmap Export")
        c_exp1, c_exp2 = st.columns(2)
        with c_exp1:
            st.download_button(
                "📥 Export JSON Roadmap",
                data=json.dumps(roadmap, indent=2),
                file_name="learning_path_roadmap.json",
                mime="application/json",
                width="stretch"
            )
        with c_exp2:
            st.download_button(
                "📄 Export Markdown Summary",
                data=f"# Learning Path: {roadmap['role']}\nGoal: {roadmap['goal']}\nProgress: {progress_pct}%",
                file_name="learning_path.md",
                mime="text/markdown",
                width="stretch"
            )
