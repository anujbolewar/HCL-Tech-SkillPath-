"""Ultra-refined design system and stylesheet for PathFinder AI.

Crafted with aesthetic restraint: deep slate surfaces (#080C14, #0F1626, #162035),
disciplined 8px spatial grid, Outfit & Inter typography, and zero decorative AI fluff.
"""

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global typography & canvas */
    html, body, [class*="css"], .stMarkdown, p, span, label, div {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #F8FAFC;
    }

    h1, h2, h3, h4, h5, h6, .brand-title, .section-heading {
        font-family: 'Outfit', 'Inter', sans-serif !important;
        letter-spacing: -0.02em;
        font-weight: 700;
        color: #F8FAFC;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Core Canvas Background: Clean, deep obsidian (no blobs/gradients) */
    .stApp {
        background-color: #080C14;
        color: #F8FAFC;
    }

    /* Streamlit block container optimization */
    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1320px !important;
    }

    /* Sidebar: Clean Workspace Drawer */
    section[data-testid="stSidebar"] {
        background-color: #0B101D !important;
        border-right: 1px solid #1E293B !important;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
    }

    /* Compact App Header (54px) */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 20px;
        background: #0F1626;
        border: 1px solid #1E293B;
        border-radius: 10px;
        margin-bottom: 16px;
    }

    .app-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Outfit', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: #F8FAFC;
    }

    .app-brand span {
        color: #4F46E5;
        font-weight: 800;
    }

    .app-badge {
        font-size: 0.72rem;
        background: #162035;
        border: 1px solid #334155;
        color: #94A3B8;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 500;
    }

    /* Skill Gap Diagnostic Card */
    .skill-gap-card {
        background: #0F1626;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 16px;
    }

    .skill-gap-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #162035;
    }

    .skill-gap-title {
        font-family: 'Outfit', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8;
    }

    /* Next Best Action Card (Prominent & Actionable) */
    .next-action-card {
        background: #0F1626;
        border: 1px solid #3B82F6;
        border-left: 4px solid #3B82F6;
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 16px;
    }

    .next-action-badge {
        font-family: 'Outfit', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #38BDF8;
        margin-bottom: 4px;
    }

    .next-action-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 6px;
    }

    .next-action-meta {
        font-size: 0.85rem;
        color: #94A3B8;
        margin-bottom: 8px;
    }

    .next-action-why {
        font-size: 0.9rem;
        color: #CBD5E1;
        line-height: 1.5;
        margin-bottom: 12px;
        background: #162035;
        padding: 10px 14px;
        border-radius: 6px;
        border: 1px solid #1E293B;
    }

    /* Adaptive Replanning Banner */
    .replan-banner {
        background: #0D1F2D;
        border: 1px solid #0284C7;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 16px;
        font-size: 0.88rem;
        color: #BAE6FD;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Module / Milestone Items */
    .milestone-card {
        background: #0F1626;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        transition: border-color 0.15s ease;
    }

    .milestone-card:hover {
        border-color: #334155;
    }

    .milestone-card.active {
        border-color: #3B82F6;
        background: #111A2E;
    }

    .milestone-card.completed {
        border-color: #059669;
        background: #0B1917;
    }

    .milestone-card.locked {
        opacity: 0.65;
    }

    .milestone-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        color: #F8FAFC;
        margin-bottom: 4px;
    }

    .milestone-meta {
        font-size: 0.82rem;
        color: #94A3B8;
        margin-bottom: 6px;
    }

    .milestone-why {
        font-size: 0.88rem;
        color: #CBD5E1;
        line-height: 1.5;
    }

    /* Single Status Indicators (Clean, no rainbow) */
    .status-tag {
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
    }

    .status-completed {
        background: rgba(5, 150, 105, 0.15);
        color: #34D399;
        border: 1px solid rgba(5, 150, 105, 0.35);
    }

    .status-active {
        background: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.35);
    }

    .status-locked {
        background: #162035;
        color: #64748B;
        border: 1px solid #334155;
    }

    /* Node Inspector Panel */
    .node-inspector-box {
        background: #0F1626;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 14px;
    }

    /* Button Polish */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
    }

    .stButton > button[kind="primary"] {
        background: #4F46E5 !important;
        border: 1px solid #6366F1 !important;
        color: #FFFFFF !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: #4338CA !important;
    }

    /* Streamlit Tabs Styling (Clean pill navigation) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #0B101D;
        padding: 4px;
        border-radius: 8px;
        border: 1px solid #1E293B;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 6px 14px;
        border-radius: 6px;
        color: #94A3B8;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #162035 !important;
        color: #F8FAFC !important;
        font-weight: 600;
    }
</style>
"""

def inject_custom_styles() -> None:
    """Injects refined CSS into the Streamlit application."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
