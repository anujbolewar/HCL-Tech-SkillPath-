"""Editorial, premium learning navigation design system for PathFinder AI.

Palette:
- Canvas: Warm Ivory #F7F6F2 (Subtle section: #F1F0EB)
- Surface: Pure White #FFFFFF
- Primary Ink: #111111
- Secondary Ink: #4B4B4B
- Muted Ink: #858585
- Border: #DDDCD6
- Subtle Border: #EAE9E4
- Primary Path Accent: Deep Cobalt #2457D6 (Highlight: #4A78E8, Deep: #173B8F)
- Success: Muted Forest #2F7D5A
- Warning / Attention: Warm Amber #C58A35
"""

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600;650;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --pf-canvas: #F7F6F2;
        --pf-canvas-subtle: #F1F0EB;
        --pf-surface: #FFFFFF;
        --pf-ink: #111111;
        --pf-ink-secondary: #4B4B4B;
        --pf-ink-muted: #858585;
        --pf-border: #DDDCD6;
        --pf-border-subtle: #EAE9E4;
        --pf-blue: #2457D6;
        --pf-blue-highlight: #4A78E8;
        --pf-blue-deep: #173B8F;
        --pf-green: #2F7D5A;
        --pf-green-bg: #F2F7F4;
        --pf-amber: #C58A35;
        --pf-amber-bg: #FDF9F2;
        --pf-font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --pf-font-serif: 'DM Serif Display', Georgia, serif;
        --pf-font-mono: 'JetBrains Mono', monospace;
    }

    /* Global Warm Ivory Canvas */
    .stApp {
        background-color: var(--pf-canvas) !important;
        color: var(--pf-ink) !important;
    }

    /* Targeted typography without breaking Streamlit material icon fonts */
    .stMarkdown p, .stMarkdown span, .stMarkdown div,
    .pf-header, .pf-card, .pf-next-card, .pf-milestone, .pf-inspector,
    .pf-track-item, .pf-assessment-box, .pf-notification {
        font-family: var(--pf-font-sans);
        color: var(--pf-ink);
    }

    /* Editorial serif classes */
    .pf-serif-headline {
        font-family: var(--pf-font-serif) !important;
        font-weight: 400 !important;
        letter-spacing: -0.01em !important;
        color: var(--pf-ink) !important;
        line-height: 1.15 !important;
    }

    .pf-serif-accent {
        font-family: var(--pf-font-serif) !important;
        font-style: italic !important;
        color: var(--pf-blue) !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: var(--pf-font-sans) !important;
        letter-spacing: -0.02em;
        font-weight: 650 !important;
        color: var(--pf-ink) !important;
    }

    h1 { font-size: 26px !important; }
    h2 { font-size: 20px !important; }
    h3 { font-size: 16px !important; font-weight: 600 !important; }
    h4 { font-size: 14px !important; font-weight: 600 !important; }

    code, pre {
        font-family: var(--pf-font-mono) !important;
    }

    /* Streamlit block container optimization: Max readable width 1260px */
    .block-container {
        padding-top: 0.75rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1260px !important;
    }

    /* =========================================================
       SIDEBAR: QUIET NAVIGATION RAIL (#FFFFFF, BORDER #DDDCD6)
       ========================================================= */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid var(--pf-border) !important;
        box-shadow: none !important;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.25rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }

    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] h4 {
        color: var(--pf-ink) !important;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span:not([class*="material"]),
    section[data-testid="stSidebar"] summary {
        color: var(--pf-ink) !important;
    }

    .pf-sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 18px;
        padding-bottom: 14px;
        border-bottom: 1px solid var(--pf-border-subtle);
    }

    .pf-sidebar-brand-name {
        font-size: 15px;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: var(--pf-ink);
    }

    .pf-sidebar-tag {
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--pf-ink-muted);
        margin-bottom: 4px;
    }

    /* =========================================================
       APPLICATION HEADER (56px, WARM IVORY #F7F6F2, BORDER #DDDCD6)
       ========================================================= */
    .pf-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 56px;
        padding: 0 16px;
        background: var(--pf-canvas);
        border: 1px solid var(--pf-border);
        border-radius: 8px;
        margin-bottom: 20px;
    }

    .pf-header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .pf-logo-mark {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
    }

    .pf-logo-text {
        font-size: 17px;
        font-weight: 650;
        color: var(--pf-ink);
        letter-spacing: -0.02em;
    }

    .pf-logo-sub {
        font-size: 10.5px;
        font-weight: 600;
        color: var(--pf-blue);
        background: #EFF4FE;
        border: 1px solid #D6E4FC;
        padding: 1px 5px;
        border-radius: 3px;
        letter-spacing: 0.04em;
    }

    .pf-header-center {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12.5px;
        color: var(--pf-ink-secondary);
        background: var(--pf-surface);
        padding: 4px 12px;
        border: 1px solid var(--pf-border-subtle);
        border-radius: 4px;
    }

    .pf-header-right {
        font-size: 12px;
        color: var(--pf-ink-muted);
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .pf-header-right strong {
        color: var(--pf-ink);
        font-weight: 600;
    }

    /* =========================================================
       EDITORIAL HERO & GOAL INTAKE BLOCK
       ========================================================= */
    .pf-editorial-intake {
        margin-bottom: 22px;
    }

    .pf-editorial-title {
        font-family: var(--pf-font-serif);
        font-size: 32px;
        line-height: 1.2;
        color: var(--pf-ink);
        margin-bottom: 6px;
        letter-spacing: -0.01em;
    }

    .pf-editorial-meta {
        font-size: 13px;
        color: var(--pf-ink-secondary);
        margin-bottom: 14px;
    }

    .pf-editorial-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--pf-ink-muted);
        margin-bottom: 8px;
    }

    /* =========================================================
       RESTRAINED EDITORIAL CARDS & SECTIONS
       ========================================================= */
    .pf-card {
        background: var(--pf-surface);
        border: 1px solid var(--pf-border);
        border-radius: 8px;
        padding: 20px 22px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(20, 20, 20, 0.02);
        transition: border-color 150ms ease, box-shadow 150ms ease;
    }

    .pf-card:hover {
        border-color: #CFCFC9;
        box-shadow: 0 4px 18px rgba(20, 20, 20, 0.04);
    }

    .pf-section-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 16px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--pf-border-subtle);
    }

    .pf-section-title {
        font-size: 12px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--pf-ink-muted);
    }

    .pf-section-caption {
        font-size: 12.5px;
        color: var(--pf-ink-secondary);
    }

    /* =========================================================
       SKILL POSITION: CURRENT → TARGET TRACK VISUALIZATION
       ========================================================= */
    .pf-track-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .pf-track-item {
        display: grid;
        grid-template-columns: 140px 1fr 100px;
        align-items: center;
        gap: 16px;
        font-size: 13px;
    }

    .pf-track-name {
        font-weight: 550;
        color: var(--pf-ink);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .pf-track-bar-bg {
        position: relative;
        height: 6px;
        background: var(--pf-canvas-subtle);
        border-radius: 3px;
        overflow: hidden;
    }

    .pf-track-bar-target {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        background: #E2E1DA;
        border-radius: 3px;
    }

    .pf-track-bar-current {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        background: var(--pf-ink);
        border-radius: 3px;
        transition: width 400ms ease;
    }

    .pf-track-bar-current.is-gap {
        background: var(--pf-blue);
    }

    .pf-track-value {
        text-align: right;
        font-size: 12px;
        font-weight: 500;
    }

    .pf-badge-mastered {
        color: var(--pf-green);
        font-weight: 600;
    }

    .pf-badge-gap {
        color: var(--pf-amber);
        font-weight: 600;
        background: var(--pf-amber-bg);
        border: 1px solid #F6E6CC;
        padding: 1px 6px;
        border-radius: 3px;
        font-size: 11px;
    }

    /* =========================================================
       NEXT BEST ACTION: SIGNATURE COMPONENT WITH PATH INDICATOR
       ========================================================= */
    .pf-next-card {
        position: relative;
        background: var(--pf-surface);
        border: 1px solid var(--pf-border);
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 18px;
        box-shadow: 0 3px 12px rgba(20, 20, 20, 0.03);
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }

    .pf-next-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 14px;
        bottom: 14px;
        width: 3.5px;
        background: var(--pf-blue);
        border-radius: 0 2px 2px 0;
        transition: top 180ms ease, bottom 180ms ease, width 180ms ease;
    }

    .pf-next-card:hover {
        border-color: #C5C5BF;
        box-shadow: 0 6px 20px rgba(20, 20, 20, 0.05);
    }

    .pf-next-card:hover::before {
        top: 8px;
        bottom: 8px;
        width: 4.5px;
    }

    .pf-next-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }

    .pf-next-step-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--pf-blue);
    }

    .pf-next-step-badge .pf-num {
        font-family: var(--pf-font-mono);
        font-size: 11px;
        background: #EFF4FE;
        border: 1px solid #D6E4FC;
        padding: 1px 5px;
        border-radius: 3px;
    }

    .pf-next-duration {
        font-size: 12px;
        color: var(--pf-ink-muted);
        background: var(--pf-canvas);
        border: 1px solid var(--pf-border-subtle);
        padding: 2px 8px;
        border-radius: 4px;
    }

    .pf-next-title {
        font-size: 18px;
        font-weight: 650;
        color: var(--pf-ink);
        letter-spacing: -0.01em;
        margin-bottom: 4px;
    }

    .pf-next-provider {
        font-size: 13px;
        color: var(--pf-ink-secondary);
        margin-bottom: 12px;
    }

    .pf-next-gaps-block {
        font-size: 12.5px;
        color: var(--pf-ink-secondary);
        margin-bottom: 12px;
        line-height: 1.5;
    }

    .pf-next-gaps-block strong {
        color: var(--pf-ink);
    }

    .pf-next-why-box {
        background: var(--pf-canvas);
        border: 1px solid var(--pf-border-subtle);
        border-radius: 6px;
        padding: 10px 14px;
        font-size: 13px;
        color: var(--pf-ink-secondary);
        line-height: 1.5;
    }

    .pf-next-why-box strong {
        color: var(--pf-ink);
        font-weight: 600;
    }

    /* =========================================================
       PATH UPDATED EDITORIAL NOTIFICATION (ADAPTIVE REPLANNING)
       ========================================================= */
    .pf-notification {
        position: relative;
        background: var(--pf-surface);
        border: 1px solid var(--pf-border);
        border-left: 3.5px solid var(--pf-amber);
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(197, 138, 53, 0.04);
        animation: pfFadeSlideUp 300ms ease forwards;
    }

    .pf-notif-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 11px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--pf-amber);
        margin-bottom: 6px;
    }

    .pf-notif-tag::before {
        content: '';
        width: 6px;
        height: 6px;
        background: var(--pf-amber);
        border-radius: 50%;
    }

    .pf-notif-body {
        font-size: 13px;
        color: var(--pf-ink-secondary);
        line-height: 1.55;
    }

    .pf-notif-body strong {
        color: var(--pf-ink);
    }

    /* =========================================================
       BUTTONS & INK CONTROLS
       ========================================================= */
    /* Primary: Black/Ink Button (#111111 -> Hover Deep Cobalt #2457D6) */
    .stButton > button[kind="primary"] {
        background-color: var(--pf-ink) !important;
        border: 1px solid var(--pf-ink) !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        height: 42px !important;
        transition: background-color 150ms ease, border-color 150ms ease, transform 150ms ease !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: var(--pf-blue) !important;
        border-color: var(--pf-blue) !important;
        color: #FFFFFF !important;
        transform: translateY(-1px);
    }

    /* Secondary: Clean Surface Button */
    .stButton > button,
    .stDownloadButton > button {
        background-color: var(--pf-surface) !important;
        border: 1px solid var(--pf-border) !important;
        color: var(--pf-ink) !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        height: 40px !important;
        transition: background-color 150ms ease, border-color 150ms ease !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background-color: var(--pf-canvas-subtle) !important;
        border-color: #C5C5BF !important;
        color: var(--pf-ink) !important;
    }

    /* Disabled state for locked milestones */
    .stButton > button:disabled,
    .stButton > button[disabled] {
        background-color: var(--pf-canvas-subtle) !important;
        border-color: var(--pf-border) !important;
        color: var(--pf-ink-muted) !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* Form Controls & Baseline Locks */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: var(--pf-surface) !important;
        border: 1px solid var(--pf-border) !important;
        border-radius: 6px !important;
        color: var(--pf-ink) !important;
        font-size: 14px !important;
        height: 42px !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: var(--pf-blue) !important;
        box-shadow: 0 0 0 1px var(--pf-blue) !important;
    }

    /* Clean Streamlit Pills */
    [data-testid="stPills"] {
        gap: 8px !important;
    }

    [data-testid="stPills"] button {
        background-color: #FFFFFF !important;
        border: 1px solid #DDDCD6 !important;
        border-radius: 20px !important;
        font-size: 12px !important;
        color: #4B4B4B !important;
        padding: 3px 12px !important;
        transition: all 150ms ease !important;
    }

    [data-testid="stPills"] button span,
    [data-testid="stPills"] button p {
        color: #4B4B4B !important;
        font-size: 12px !important;
    }

    [data-testid="stPills"] button:hover {
        background-color: var(--pf-canvas-subtle) !important;
        border-color: #C5C5BF !important;
    }

    [data-testid="stPills"] button[aria-selected="true"] {
        background-color: #EFF4FE !important;
        border-color: #D6E4FC !important;
    }

    [data-testid="stPills"] button[aria-selected="true"] span,
    [data-testid="stPills"] button[aria-selected="true"] p {
        color: #2457D6 !important;
        font-weight: 600 !important;
    }

    /* =========================================================
       EDITORIAL TABS (OVERVIEW / LEARNING PATH / PROGRESS / MENTOR)
       ========================================================= */
    .stTabs [data-baseweb="tab-list"] {
        gap: 32px !important;
        background-color: transparent !important;
        border-bottom: 1px solid var(--pf-border) !important;
        padding-bottom: 0px !important;
        margin-bottom: 20px !important;
    }

    .stTabs [data-baseweb="tab"],
    .stTabs [data-baseweb="tab"] div,
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span {
        background-color: transparent !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 8px 4px 12px 4px !important;
        font-size: 14px !important;
        font-weight: 550 !important;
        color: #4B4B4B !important;
        box-shadow: none !important;
        transition: color 150ms ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover,
    .stTabs [data-baseweb="tab"]:hover div,
    .stTabs [data-baseweb="tab"]:hover p,
    .stTabs [data-baseweb="tab"]:hover span {
        color: var(--pf-ink) !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"],
    .stTabs [data-baseweb="tab"][aria-selected="true"] div,
    .stTabs [data-baseweb="tab"][aria-selected="true"] p,
    .stTabs [data-baseweb="tab"][aria-selected="true"] span {
        color: var(--pf-ink) !important;
        font-weight: 700 !important;
        border-bottom: 2px solid var(--pf-ink) !important;
    }

    /* =========================================================
       MILESTONES & NODE INSPECTOR
       ========================================================= */
    .pf-milestone {
        background: var(--pf-surface);
        border: 1px solid var(--pf-border);
        border-radius: 8px;
        padding: 16px 18px;
        margin-bottom: 12px;
        transition: border-color 150ms ease;
    }

    .pf-milestone:hover {
        border-color: #C5C5BF;
    }

    .pf-milestone-completed {
        border-left: 3.5px solid var(--pf-green);
    }

    .pf-milestone-ready {
        border-left: 3.5px solid var(--pf-blue);
    }

    .pf-milestone-locked {
        border-left: 3.5px solid var(--pf-border);
        opacity: 0.7;
    }

    .pf-inspector {
        background: var(--pf-surface);
        border: 1px solid var(--pf-border);
        border-radius: 8px;
        padding: 18px;
        font-size: 13px;
        box-shadow: 0 2px 8px rgba(20, 20, 20, 0.02);
    }

    /* =========================================================
       CHAT & MENTOR STYLES
       ========================================================= */
    [data-testid="stChatMessage"] {
        background-color: var(--pf-surface) !important;
        border: 1px solid var(--pf-border) !important;
        border-radius: 8px !important;
        padding: 14px 18px !important;
        margin-bottom: 10px !important;
        font-size: 13.5px !important;
        color: var(--pf-ink) !important;
        line-height: 1.55 !important;
    }

    [data-testid="stChatInput"] {
        background-color: var(--pf-surface) !important;
        border: 1px solid var(--pf-border) !important;
        border-radius: 8px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: var(--pf-ink) !important;
        font-size: 13.5px !important;
    }

    /* =========================================================
       MOTION SYSTEM & ANIMATIONS
       ========================================================= */
    @keyframes pfFadeSlideUp {
        0% {
            opacity: 0;
            transform: translateY(4px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .pf-animate-fade {
        animation: pfFadeSlideUp 220ms ease forwards;
    }

    /* Accessibility: Respect Reduced Motion */
    @media (prefers-reduced-motion: reduce) {
        *, ::before, ::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }

    /* Remove Streamlit default decorative elements */
    #MainMenu, footer, header {
        visibility: hidden;
    }
</style>
"""

def inject_custom_styles() -> None:
    """Injects the editorial light-mode design system into the active Streamlit session."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
