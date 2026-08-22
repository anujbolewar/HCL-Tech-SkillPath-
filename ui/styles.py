"""Restrained, editorial light-mode design system for PathFinder AI.

Palette:
- Canvas: #F7F7F5
- Primary Surface: #FFFFFF
- Secondary Surface: #F1F2F0
- Primary Text: #171717
- Secondary Text: #666666
- Muted: #8A8A8A
- Borders: #E5E5E2
- Primary Accent: #2563EB
- Accent Hover: #1D4ED8
- Success: #15803D
- Warning: #B45309
- Locked: #A3A3A3
"""

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;650;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global canvas */
    .stApp {
        background-color: #F7F7F5 !important;
        color: #171717 !important;
    }

    /* Targeted typography without breaking Streamlit material icon fonts */
    .stMarkdown p, .stMarkdown span, .stMarkdown div, 
    .app-header, .content-card, .next-action-card, .milestone-item, .node-inspector-box {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.02em;
        font-weight: 650 !important;
        color: #171717 !important;
    }

    h1 { font-size: 24px !important; }
    h2 { font-size: 19px !important; }
    h3 { font-size: 16px !important; font-weight: 600 !important; }
    h4 { font-size: 14px !important; font-weight: 600 !important; }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Streamlit block container optimization */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1280px !important;
    }

    /* Sidebar: Clean White Learner Panel */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E5E2 !important;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.25rem !important;
    }

    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] h4 {
        color: #171717 !important;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span:not([class*="material"]),
    section[data-testid="stSidebar"] summary {
        color: #171717 !important;
    }

    /* Compact Application Header (56px) */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 18px;
        background: #FFFFFF;
        border: 1px solid #E5E5E2;
        border-radius: 8px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }

    .app-brand {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 18px;
        font-weight: 650;
        color: #171717;
        letter-spacing: -0.01em;
    }

    .app-brand .ai-tag {
        font-size: 11px;
        font-weight: 600;
        background: #F1F2F0;
        color: #2563EB;
        padding: 2px 6px;
        border-radius: 4px;
        border: 1px solid #E5E5E2;
        letter-spacing: 0.02em;
    }

    .app-badge {
        font-size: 12px;
        background: #F1F2F0;
        border: 1px solid #E5E5E2;
        color: #404040;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 500;
    }

    .app-meta {
        font-size: 12px;
        color: #8A8A8A;
        font-weight: 400;
        text-align: right;
    }

    .app-meta strong {
        color: #171717;
        font-weight: 600;
    }

    /* Section Cards & Panels */
    .content-card {
        background: #FFFFFF;
        border: 1px solid #E5E5E2;
        border-radius: 8px;
        padding: 18px 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }

    .card-header-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #8A8A8A;
        margin-bottom: 12px;
    }

    /* Next Best Action / Next Up Card */
    .next-action-card {
        background: #FFFFFF;
        border: 1px solid #E5E5E2;
        border-left: 3px solid #2563EB;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }

    .next-action-badge {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #2563EB;
        margin-bottom: 4px;
    }

    .next-action-title {
        font-size: 17px;
        font-weight: 650;
        color: #171717;
        margin-bottom: 4px;
        letter-spacing: -0.01em;
    }

    .next-action-meta {
        font-size: 13px;
        color: #666666;
        margin-bottom: 10px;
    }

    .next-action-why {
        font-size: 13px;
        color: #404040;
        line-height: 1.5;
        background: #F7F7F5;
        padding: 10px 14px;
        border-radius: 6px;
        border: 1px solid #E5E5E2;
    }

    /* Path Updated Banner (Adaptive Replanning) */
    .path-updated-banner {
        background: #F0F7FF;
        border: 1px solid #BFDBFE;
        border-left: 3px solid #2563EB;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 16px;
        font-size: 13px;
        color: #1E3A8A;
        line-height: 1.5;
    }

    .path-updated-title {
        font-size: 13px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        color: #1D4ED8;
        margin-bottom: 4px;
    }

    /* Status Tags */
    .status-tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 500;
    }

    .status-active {
        background: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #DBEAFE;
    }

    .status-completed {
        background: #F0FDF4;
        color: #15803D;
        border: 1px solid #DCFCE7;
    }

    .status-locked {
        background: #F1F2F0;
        color: #8A8A8A;
        border: 1px solid #E5E5E2;
    }

    /* Form Controls & Baseline Locks */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E5E2 !important;
        border-radius: 6px !important;
        color: #171717 !important;
        font-size: 14px !important;
        height: 42px !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 1px #2563EB !important;
    }

    /* Primary & Secondary Buttons */
    .stButton > button,
    .stDownloadButton > button {
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        height: 42px !important;
        transition: background-color 150ms ease, border-color 150ms ease !important;
        border: 1px solid #E5E5E2 !important;
        background-color: #FFFFFF !important;
        color: #171717 !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background-color: #F1F2F0 !important;
        border-color: #D4D4D0 !important;
        color: #171717 !important;
    }

    .stButton > button[kind="primary"] {
        background-color: #2563EB !important;
        border-color: #2563EB !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }

    /* Clean Light Mode Streamlit Pills */
    [data-testid="stPills"] {
        gap: 8px !important;
    }

    [data-testid="stPills"] button {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E5E2 !important;
        border-radius: 20px !important;
        font-size: 12px !important;
        color: #404040 !important;
        padding: 3px 12px !important;
    }

    [data-testid="stPills"] button span,
    [data-testid="stPills"] button p {
        color: #404040 !important;
        font-size: 12px !important;
    }

    [data-testid="stPills"] button:hover {
        background-color: #F1F2F0 !important;
        border-color: #D4D4D0 !important;
    }

    [data-testid="stPills"] button[aria-selected="true"] {
        background-color: #EFF6FF !important;
        border-color: #BFDBFE !important;
    }

    [data-testid="stPills"] button[aria-selected="true"] span,
    [data-testid="stPills"] button[aria-selected="true"] p {
        color: #1D4ED8 !important;
        font-weight: 600 !important;
    }

    /* Restrained Clean Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px !important;
        background-color: transparent !important;
        border-bottom: 1px solid #E5E5E2 !important;
        padding-bottom: 0px !important;
        margin-bottom: 18px !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 8px 4px 12px 4px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #666666 !important;
        box-shadow: none !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #171717 !important;
    }

    .stTabs [aria-selected="true"] {
        color: #2563EB !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #2563EB !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E5E2 !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #171717 !important;
    }

    .streamlit-expanderContent {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E5E2 !important;
        border-top: none !important;
        border-radius: 0 0 6px 6px !important;
    }

    /* Milestone Progression Cards */
    .milestone-item {
        background: #FFFFFF;
        border: 1px solid #E5E5E2;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
        transition: border-color 150ms ease;
    }

    .milestone-item:hover {
        border-color: #D4D4D0;
    }

    .milestone-item-completed {
        border-left: 3px solid #15803D;
    }

    .milestone-item-ready {
        border-left: 3px solid #2563EB;
    }

    .milestone-item-locked {
        border-left: 3px solid #E5E5E2;
        opacity: 0.75;
    }

    /* Node Inspector Panel */
    .node-inspector-box {
        background: #FFFFFF;
        border: 1px solid #E5E5E2;
        border-radius: 8px;
        padding: 16px;
        font-size: 13px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }

    /* Chat Messages & Inputs */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E5E2 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        margin-bottom: 8px !important;
        font-size: 13.5px !important;
        color: #171717 !important;
    }

    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E5E2 !important;
        border-radius: 8px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #171717 !important;
        font-size: 13.5px !important;
    }

    /* Remove Streamlit default decorative headers */
    #MainMenu, footer, header {
        visibility: hidden;
    }
</style>
"""

def inject_custom_styles() -> None:
    """Injects the light-mode editorial stylesheet into the active Streamlit app."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
