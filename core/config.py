"""Application configuration, demo personas, model catalogs, and default settings."""

from typing import Dict, List, Any

# App Metadata & Team Info
APP_TITLE = "SkillPath AI — Learn Anything"
APP_SUBTITLE = "AI-Powered Personalized Learning Path Recommender (PathFinder Prototype)"
TEAM_NAME = "Cortex"
COLLEGE_NAME = "Yeshwantrao Chavan College of Engineering"
TEAM_MEMBERS = [
    {"name": "Anuj Bolewar", "email": "bolewara@gmail.com", "role": "Lead Architect & AI Engineer"},
    {"name": "Lakshya Gupta", "email": "lakshyagupta9721@gmail.com", "role": "Full-Stack & Systems Engineer"},
    {"name": "Shaki Gajbhiye", "email": "gajbhiyeshaki@gmail.com", "role": "AI/ML & Data Engineer"},
    {"name": "Pranjal Gudadhe", "email": "pranjalgudadhe59@gmail.com", "role": "UX & Frontend Engineer"},
    {"name": "Om Ingle", "email": "omingle71@gmail.com", "role": "Research & Evaluation Specialist"},
]

WELCOME_MESSAGE = (
    "👋 Hi! I'm your **SkillPath AI Mentor by Team Cortex**.\n\n"
    "I can help you explore your customized roadmap, break down complex prerequisites, "
    "recommend top resources, or guide your weekly schedule. How can I help you today?"
)

# Default Learner Profile
DEFAULT_PROFILE: Dict[str, Any] = {
    "target_role": "AI & ML Engineer",
    "experience_level": "Intermediate",
    "weekly_hours": 15,
    "skills": ["Python", "Basic Math", "SQL"],
    "completed_courses": [],
    "preferred_learning_style": "Hands-on Projects"
}

# 12 Universal Quick Picks
QUICK_PICKS: Dict[str, str] = {
    "🤖 AI & ML Engineer": "I want to become an AI & Machine Learning Engineer",
    "🌐 Full-Stack Web Developer": "I want to become a Full-Stack Web Developer",
    "📊 Data Scientist": "I want to master Data Science and Predictive Analytics",
    "🛡️ Cybersecurity Analyst": "I want to become a Cybersecurity Analyst and Ethical Hacker",
    "☁️ Cloud & DevOps Engineer": "I want to become a Cloud Solutions Architect with Docker and Kubernetes",
    "🎸 Learn Guitar": "I want to learn guitar from scratch and play my favorite songs",
    "🗣️ Speak Fluent Spanish": "I want to become conversational and fluent in Spanish",
    "💪 Fitness & Strength Transformation": "I want to build strength, improve stamina, and optimize nutrition",
    "🍳 Gourmet Cooking & Baking": "I want to master culinary knife skills, flavor pairing, and baking",
    "✏️ Digital Art & Illustration": "I want to learn digital drawing, anatomy, and color theory",
    "📈 Startup Founder & Marketing": "I want to validate, build, and launch a profitable tech startup",
    "📚 Crack JEE / Competitive Exam": "I want to crack competitive entrance exams with a structured daily study plan"
}

# Rich Demo Personas for 1-Click Evaluation
DEMO_PERSONAS: Dict[str, Dict[str, Any]] = {
    "🤖 Persona 1: AI & ML Aspirant (Alex)": {
        "goal": "I want to become an AI & Machine Learning Engineer",
        "profile": {
            "target_role": "AI & ML Engineer",
            "experience_level": "Intermediate",
            "weekly_hours": 15,
            "skills": ["Python", "Basic Math", "SQL", "Git"],
            "preferred_learning_style": "Hands-on Projects"
        },
        "completed_initial": ["AI101"]
    },
    "🌐 Persona 2: Web Dev Switcher (Sarah)": {
        "goal": "I want to transition into Full-Stack Web Development",
        "profile": {
            "target_role": "Full-Stack Web Developer",
            "experience_level": "Beginner",
            "weekly_hours": 20,
            "skills": ["HTML/CSS", "Basic Math"],
            "preferred_learning_style": "Interactive"
        },
        "completed_initial": []
    },
    "🎸 Persona 3: Music Hobbyist (Carlos)": {
        "goal": "I want to learn acoustic and electric guitar from scratch",
        "profile": {
            "target_role": "Musician",
            "experience_level": "Beginner",
            "weekly_hours": 7,
            "skills": [],
            "preferred_learning_style": "Video Courses"
        },
        "completed_initial": ["MU101"]
    },
    "🗣️ Persona 4: Global Polyglot (Elena)": {
        "goal": "I want to become fluent in Spanish for business and travel",
        "profile": {
            "target_role": "Language Learner",
            "experience_level": "Beginner",
            "weekly_hours": 10,
            "skills": ["English"],
            "preferred_learning_style": "Hands-on Projects"
        },
        "completed_initial": ["LG101"]
    },
    "📚 Persona 5: High-Score Exam Topper (Rohan)": {
        "goal": "I want to crack national engineering entrance exams with top rank",
        "profile": {
            "target_role": "Exam Topper",
            "experience_level": "Intermediate",
            "weekly_hours": 30,
            "skills": ["Basic Math", "Physics", "Chemistry"],
            "preferred_learning_style": "Hands-on Projects"
        },
        "completed_initial": ["EX101", "EX102"]
    }
}

# Groq Supported Models with Suitability Annotations
GROQ_MODEL_CATALOG: Dict[str, Dict[str, str]] = {
    "llama-3.3-70b-versatile": {
        "name": "Llama 3.3 70B Versatile",
        "tag": "⭐ Recommended for Roadmap Generation",
        "desc": "Best for complex prerequisite DAG planning, structured JSON extraction, and deep domain reasoning."
    },
    "llama-3.1-8b-instant": {
        "name": "Llama 3.1 8B Instant",
        "tag": "⚡ Ultra-Fast for Live Chat",
        "desc": "Sub-100ms latency, ideal for real-time conversational mentoring and immediate Q&A."
    },
    "mixtral-8x7b-32768": {
        "name": "Mixtral 8x7B (MoE)",
        "tag": "🧠 Extended Context",
        "desc": "32k token window, robust for multi-turn learning roadmap reviews and large skill portfolios."
    },
    "gemma2-9b-it": {
        "name": "Gemma 2 9B Instruct",
        "tag": "🎯 Precise & Concise",
        "desc": "Google's lightweight model optimized for concise instructional explanations."
    },
    "qwen-2.5-32b": {
        "name": "Qwen 2.5 32B",
        "tag": "🌐 Multilingual & Math",
        "desc": "Superior performance in technical STEM domains, coding, and multilingual path generation."
    }
}

# Google Gemini Models Catalog
GEMINI_MODEL_CATALOG: Dict[str, Dict[str, str]] = {
    "gemini-2.5-flash": {
        "name": "Gemini 2.5 Flash",
        "tag": "⭐ Recommended for Gemini",
        "desc": "State-of-the-art fast reasoning model with high JSON fidelity and multimodal understanding."
    },
    "gemini-2.5-pro": {
        "name": "Gemini 2.5 Pro",
        "tag": "🔬 Deep Architectural Reasoning",
        "desc": "Complex thinking and curriculum design with large context windows."
    }
}

DEFAULT_GROQ_MODELS = list(GROQ_MODEL_CATALOG.keys())
DEFAULT_GEMINI_MODELS = list(GEMINI_MODEL_CATALOG.keys())
