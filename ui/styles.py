"""Ultra-refined design system and stylesheet for PathFinder AI.

Crafted with high-end taste: deep slate surfaces, Outfit & Inter typography,
subtle glowing borders, refined spatial discipline, and zero visual clutter.
"""

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global reset & typography */
    html, body, [class*="css"], .stMarkdown, p, span, label, div {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #e2e8f0;
    }

    h1, h2, h3, h4, h5, h6, .brand-title, .metric-num, .card-heading {
        font-family: 'Outfit', 'Inter', sans-serif !important;
        letter-spacing: -0.025em;
        font-weight: 700;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Core Canvas Background */
    .stApp {
        background-color: #080b11;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.07) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(56, 189, 248, 0.05) 0px, transparent 50%);
        background-attachment: fixed;
    }

    /* Remove Streamlit default top padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem !important;
    }

    /* Hero Header */
    .hero-container {
        background: linear-gradient(180deg, rgba(18, 24, 38, 0.8) 0%, rgba(13, 18, 30, 0.6) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 32px 36px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.6), rgba(56, 189, 248, 0.6), transparent);
    }

    .brand-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(99, 102, 241, 0.25);
        color: #a5b4fc;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 12px;
        letter-spacing: 0.02em;
    }

    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
        line-height: 1.15;
    }

    .brand-title span {
        background: linear-gradient(135deg, #818cf8 0%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-desc {
        color: #94a3b8;
        font-size: 0.98rem;
        line-height: 1.6;
        max-width: 780px;
    }

    /* Metric Summary Ribbon */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }

    .metric-card {
        background: #0f1523;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 16px 20px;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .metric-card:hover {
        background: #141c2e;
        border-color: rgba(99, 102, 241, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }

    .metric-lbl {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748b;
        margin-bottom: 4px;
    }

    .metric-num {
        font-size: 1.45rem;
        font-weight: 700;
        color: #f8fafc;
    }

    /* Glassmorphic Section Cards */
    .glass-card {
        background: #0e1320;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 22px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }

    /* Course / Module Milestone Cards */
    .module-item {
        background: #111726;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
        transition: all 0.2s ease;
        position: relative;
    }

    .module-item:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.08);
    }

    .module-item.completed {
        background: rgba(16, 185, 129, 0.04);
        border-color: rgba(16, 185, 129, 0.3);
    }

    .module-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }

    .module-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.08rem;
        font-weight: 600;
        color: #f1f5f9;
        margin: 6px 0;
    }

    .module-why {
        color: #94a3b8;
        font-size: 0.88rem;
        line-height: 1.5;
        margin-bottom: 10px;
    }

    /* Clean Pill Tags */
    .tag {
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 500;
        margin-right: 6px;
        margin-bottom: 4px;
    }

    .tag-blue { background: rgba(56, 189, 248, 0.1); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.2); }
    .tag-emerald { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }
    .tag-amber { background: rgba(245, 158, 11, 0.1); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.2); }
    .tag-indigo { background: rgba(99, 102, 241, 0.1); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.2); }
    .tag-slate { background: rgba(148, 163, 184, 0.1); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.2); }

    /* Node Inspector Panel */
    .inspector-panel {
        background: #111728;
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 16px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
        animation: fadeIn 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(4px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Buttons & Inputs Polish */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        transition: all 0.15s ease !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%) !important;
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.45) !important;
        transform: translateY(-1px);
    }

    /* Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0b0f19;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        font-size: 0.92rem;
        padding: 8px 16px;
        border-radius: 6px;
        color: #94a3b8;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
        font-weight: 600;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .metric-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        .hero-container {
            padding: 20px;
        }
        .brand-title {
            font-size: 1.65rem;
        }
    }
</style>
"""

def inject_custom_styles() -> None:
    """Injects refined CSS into the Streamlit application."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
