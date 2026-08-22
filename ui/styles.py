"""Editorial, premium learning navigation design system for PathFinder AI.

Palette:
- Canvas: Warm Ivory #F7F6F2 (Subtle section: #F1F0EB)
- Surface: Pure White #FFFFFF
- Primary Ink: #111111
- Secondary Ink: #4B4B4B
- Muted Ink: #5F5F5F / #858585
- Border: #DDDCD6
- Subtle Border: #EAE9E4
- Primary Path Accent: Deep Cobalt #2457D6 (Highlight: #4A78E8, Deep: #173B8F)
- Success: Muted Forest #2F7D5A
- Warning / Skill Gap / Adaptation: Warm Amber #C58A35
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
        --pf-ink-muted: #5F5F5F;
        --pf-ink-faint: #858585;
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
    .pf-track-item, .pf-assessment-box, .pf-notification, .pf-sidebar-brand {
        font-family: var(--pf-font-sans);
        color: var(--pf-ink);
    }

    /* Editorial serif headline ONLY for the main hero statement */
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

    h1 { font-size: 22px !important; }
    h2 { font-size: 18px !important; }
    h3 { font-size: 15px !important; font-weight: 600 !important; }
    h4 { font-size: 13px !important; font-weight: 600 !important; }

    code, pre {
        font-family: var(--pf-font-mono) !important;
    }

    /* Streamlit block container density optimization */
    .block-container {
        padding-top: 0.35rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 1260px !important;
    }

    /* =========================================================
       SIDEBAR: CLEAN LEARNER RAIL (#FFFFFF, BORDER #DDDCD6)
       ========================================================= */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid var(--pf-border) !important;
        box-shadow: none !important;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.85rem !important;
        padding-left: 1.15rem !important;
        padding-right: 1.15rem !important;
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
        gap: 9px;
        margin-bottom: 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--pf-border-subtle);
    }

    .pf-sidebar-brand-name {
        font-size: 14.5px;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: var(--pf-ink);
    }

    .pf-sidebar-tag {
        font-size: 10px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--pf-ink-faint);
        margin-bottom: 3px;
    }

    .pf-sidebar-goal-box {
        background: var(--pf-canvas);
        border: 1px solid var(--pf-border-subtle);
        border-radius: 6px;
        padding: 8px 10px;
        margin-bottom: 12px;
    }

    /* =========================================================
       APPLICATION HEADER (52px, WARM IVORY #F7F6F2, BORDER #DDDCD6)
       ========================================================= */
    .pf-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 52px;
        padding: 0 16px;
        background: var(--pf-canvas);
        border: 1px solid var(--pf-border);
        border-radius: 6px;
        margin-bottom: 14px;
    }

    .pf-header-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .pf-logo-mark {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 22px;
        height: 22px;
    }

    .pf-logo-text {
        font-size: 16px;
        font-weight: 650;
        color: var(--pf-ink);
        letter-spacing: -0.02em;
    }

    .pf-logo-sub {
        font-size: 10px;
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
        font-size: 12px;
        color: var(--pf-ink-secondary);
        background: var(--pf-surface);
        padding: 3px 10px;
        border: 1px solid var(--pf-border-subtle);
        border-radius: 4px;
    }

    .pf-header-right {
        font-size: 12px;
        color: var(--pf-ink-secondary);
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .pf-header-right strong {
        color: var(--pf-ink);
        font-weight: 600;
    }

    /* =========================================================
       EDITORIAL HERO & GOAL INTAKE BLOCK (COMPACT DENSITY)
       ========================================================= */
    .pf-editorial-intake {
        margin-bottom: 10px;
    }

    .pf-editorial-title {
        font-family: var(--pf-font-serif);
        font-size: 26px;
        line-height: 1.15;
        color: var(--pf-ink);
        margin-bottom: 2px;
        letter-spacing: -0.01em;
    }

    .pf-editorial-meta {
        font-size: 12px;
        color: var(--pf-ink-muted);
        margin-bottom: 8px;
    }

    .pf-editorial-label {
        font-size: 10.5px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--pf-ink-faint);
        margin-bottom: 4px;
    }

    /* Refined Textual Popular Paths Row Overrides */
    div[class*="st-key-pop_btn_"] button,
    div[class*="st-key-pop_btn_"] button:focus,
    div[class*="st-key-pop_btn_"] button:active {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        border-color: transparent !important;
        box-shadow: none !important;
        padding: 0px 2px !important;
        height: 22px !important;
        min-height: 22px !important;
        border-radius: 0px !important;
    }

    div[class*="st-key-pop_btn_"] button p,
    div[class*="st-key-pop_btn_"] button span {
        color: #5F5F5F !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        transition: color 150ms ease, text-decoration 150ms ease !important;
    }

    div[class*="st-key-pop_btn_"] button:hover p,
    div[class*="st-key-pop_btn_"] button:hover span {
        color: var(--pf-blue) !important;
        text-decoration: underline !important;
    }

    /* =========================================================
       EDITORIAL TABS (HIGH CONTRAST & 2PX COBALT INDICATOR)
       ========================================================= */
    div[data-testid="stTabs"] [role="tablist"] {
        gap: 28px !important;
        background-color: transparent !important;
        border-bottom: 1px solid var(--pf-border) !important;
        padding-bottom: 0px !important;
        margin-bottom: 14px !important;
    }

    div[data-testid="stTabs"] button[role="tab"],
    button[role="tab"],
    [data-testid="stTab"] {
        background-color: transparent !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 6px 4px 10px 4px !important;
        box-shadow: none !important;
        opacity: 1 !important;
    }

    div[data-testid="stTabs"] button[role="tab"] p,
    div[data-testid="stTabs"] button[role="tab"] span,
    div[data-testid="stTabs"] button[role="tab"] div,
    button[role="tab"] p,
    button[role="tab"] span,
    button[role="tab"] div,
    [data-testid="stTab"] p,
    [data-testid="stTab"] span,
    [data-testid="stTab"] div {
        color: #5F5F5F !important;
        font-size: 13.5px !important;
        font-weight: 550 !important;
        opacity: 1 !important;
        transition: color 150ms ease !important;
    }

    div[data-testid="stTabs"] button[role="tab"]:hover p,
    div[data-testid="stTabs"] button[role="tab"]:hover span,
    button[role="tab"]:hover p,
    button[role="tab"]:hover span {
        color: #111111 !important;
    }

    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p,
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] span,
    button[role="tab"][aria-selected="true"] p,
    button[role="tab"][aria-selected="true"] span {
        color: var(--pf-blue) !important;
        font-weight: 650 !important;
    }

    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
    button[role="tab"][aria-selected="true"] {
        border-bottom: 2px solid var(--pf-blue) !important;
    }

    /* =========================================================
       RESTRAINED EDITORIAL CARDS & SECTIONS
       ========================================================= */
    .pf-card {
        background: var(--pf-surface);
        border: 1px solid var(--pf-border);
        border-radius: 6px;
        padding: 16px 18px;
        margin-bottom: 14px;
        box-shadow: 0 1px 4px rgba(20, 20, 20, 0.02);
        transition: border-color 150ms ease, box-shadow 150ms ease;
    }

    .pf-card:hover {
        border-color: #CFCFC9;
        box-shadow: 0 3px 12px rgba(20, 20, 20, 0.03);
    }

    .pf-section-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--pf-border-subtle);
    }

    .pf-section-title {
        font-size: 11px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--pf-ink-faint);
    }

    .pf-section-caption {
        font-size: 12px;
        color: var(--pf-ink-secondary);
    }

    /* =========================================================
       SKILL POSITION: SIGNATURE HORIZONTAL TRACK VISUALIZATION
       WHERE I AM → WHAT I NEED → HOW FAR I HAVE TO GO
       ========================================================= */
    .pf-track-container {
        display: flex;
        flex-direction: column;
        gap: 11px;
    }

    .pf-track-item {
        display: grid;
        grid-template-columns: 165px 1fr 95px;
        align-items: center;
        gap: 16px;
        font-size: 12.5px;
    }

    .pf-track-name {
        font-weight: 550;
        color: var(--pf-ink);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .pf-track-rail-wrap {
        position: relative;
        height: 16px;
        display: flex;
        align-items: center;
    }

    .pf-track-rail {
        position: relative;
        width: 100%;
        height: 3px;
        background: #E5E4DE;
        border-radius: 1.5px;
    }

    .pf-track-current-fill {
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        background: var(--pf-ink);
        border-radius: 1.5px;
    }

    .pf-track-gap-fill {
        position: absolute;
        top: 0;
        height: 100%;
        background: var(--pf-amber);
        opacity: 0.85;
        border-radius: 1.5px;
    }

    .pf-track-current-dot {
        position: absolute;
        top: 50%;
        transform: translate(-50%, -50%);
        width: 8px;
        height: 8px;
        background: var(--pf-ink);
        border-radius: 50%;
        z-index: 2;
    }

    .pf-track-target-dot {
        position: absolute;
        top: 50%;
        transform: translate(50%, -50%);
        width: 8px;
        height: 8px;
        background: var(--pf-blue);
        border-radius: 50%;
        z-index: 2;
        transition: background-color 150ms ease, transform 150ms ease;
    }

    .pf-track-item:hover .pf-track-target-dot {
        background: var(--pf-blue-highlight);
        transform: translate(50%, -50%) scale(1.15);
    }

    .pf-track-value {
        text-align: right;
        font-size: 11.5px;
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
       NEXT BEST ACTION: SIGNATURE COMPONENT WITH COBALT PATH
       ========================================================= */
    .pf-next-card {
        position: relative;
        background: var(--pf-surface);
        border: 1px solid var(--pf-border);
        border-left: 3px solid var(--pf-blue);
        border-radius: 6px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 1px 6px rgba(20, 20, 20, 0.02);
        transition: transform 150ms ease, box-shadow 150ms ease, border-color 150ms ease;
    }

    .pf-next-card:hover {
        transform: translateY(-1px);
        border-color: #C5C5BF;
        box-shadow: 0 4px 14px rgba(20, 20, 20, 0.04);
    }

    .pf-next-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }

    .pf-next-step-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 10.5px;
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
        font-size: 11.5px;
        color: var(--pf-ink-muted);
        background: var(--pf-canvas);
        border: 1px solid var(--pf-border-subtle);
        padding: 2px 7px;
        border-radius: 3px;
    }

    .pf-next-title {
        font-size: 16.5px;
        font-weight: 650;
        color: var(--pf-ink);
        letter-spacing: -0.01em;
        margin-bottom: 2px;
    }

    .pf-next-provider {
        font-size: 12.5px;
        color: var(--pf-ink-secondary);
        margin-bottom: 8px;
    }

    .pf-next-gaps-block {
        font-size: 12px;
        color: var(--pf-ink-secondary);
        margin-bottom: 8px;
        line-height: 1.45;
    }

    .pf-next-gaps-block strong {
        color: var(--pf-ink);
    }

    .pf-next-why-box {
        background: var(--pf-canvas);
        border: 1px solid var(--pf-border-subtle);
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 12px;
        color: var(--pf-ink-secondary);
        line-height: 1.45;
        margin-bottom: 10px;
    }

    .pf-next-why-box strong {
        color: var(--pf-ink);
        font-weight: 600;
    }

    /* =========================================================
       PATH UPDATED EDITORIAL NOTIFICATION (PRODUCT-LEVEL EVENT)
       ========================================================= */
    .pf-notification {
        position: relative;
        background: var(--pf-surface);
        border: 1px solid var(--pf-border);
        border-left: 3px solid var(--pf-amber);
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 14px;
        box-shadow: 0 1px 6px rgba(197, 138, 53, 0.03);
        animation: pfFadeSlideUp 250ms ease forwards;
    }

    .pf-notif-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 10.5px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--pf-amber);
        margin-bottom: 4px;
    }

    .pf-notif-tag::before {
        content: '';
        width: 5px;
        height: 5px;
        background: var(--pf-amber);
        border-radius: 50%;
    }

    .pf-notif-body {
        font-size: 12.5px;
        color: var(--pf-ink-secondary);
        line-height: 1.5;
    }

    .pf-notif-body strong {
        color: var(--pf-ink);
    }

    /* =========================================================
       BUTTONS & INK CONTROLS (WITH ARROW MICRO-INTERACTION)
       ========================================================= */
    /* Primary: Black/Ink Button (#111111 -> Hover Deep Cobalt #2457D6) */
    .stButton > button[kind="primary"] {
        background-color: var(--pf-ink) !important;
        border: 1px solid var(--pf-ink) !important;
        color: #FFFFFF !important;
        border-radius: 5px !important;
        font-size: 12.5px !important;
        font-weight: 600 !important;
        height: 38px !important;
        transition: background-color 150ms ease, border-color 150ms ease, transform 150ms ease !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: var(--pf-blue) !important;
        border-color: var(--pf-blue) !important;
        color: #FFFFFF !important;
    }

    /* Secondary: Clean Surface Button */
    .stButton > button,
    .stDownloadButton > button {
        background-color: var(--pf-surface) !important;
        border: 1px solid var(--pf-border) !important;
        color: var(--pf-ink) !important;
        border-radius: 5px !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        height: 36px !important;
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
        color: var(--pf-ink-faint) !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* Form Controls */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: var(--pf-surface) !important;
        border: 1px solid var(--pf-border) !important;
        border-radius: 5px !important;
        color: var(--pf-ink) !important;
        font-size: 13px !important;
        height: 38px !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: var(--pf-blue) !important;
        box-shadow: 0 0 0 1px var(--pf-blue) !important;
    }

    /* =========================================================
       MILESTONES & NODE INSPECTOR
       ========================================================= */
    .pf-milestone {
        background: var(--pf-surface);
        border: 1px solid var(--pf-border);
        border-radius: 6px;
        padding: 14px 16px;
        margin-bottom: 10px;
        transition: border-color 150ms ease;
    }

    .pf-milestone:hover {
        border-color: #C5C5BF;
    }

    .pf-milestone-completed {
        border-left: 3px solid var(--pf-green);
    }

    .pf-milestone-ready {
        border-left: 3px solid var(--pf-blue);
    }

    .pf-milestone-new {
        border-left: 3px solid var(--pf-amber);
        background: #FDFCF9;
    }

    .pf-milestone-locked {
        border-left: 3px solid var(--pf-border);
        opacity: 0.75;
    }

    .pf-inspector {
        background: var(--pf-surface);
        border: 1px solid var(--pf-border);
        border-radius: 6px;
        padding: 16px;
        font-size: 12.5px;
        box-shadow: 0 1px 6px rgba(20, 20, 20, 0.02);
    }

    /* =========================================================
       CHAT & MENTOR STYLES
       ========================================================= */
    [data-testid="stChatMessage"] {
        background-color: var(--pf-surface) !important;
        border: 1px solid var(--pf-border) !important;
        border-radius: 6px !important;
        padding: 12px 16px !important;
        margin-bottom: 8px !important;
        font-size: 13px !important;
        color: var(--pf-ink) !important;
        line-height: 1.5 !important;
    }

    [data-testid="stChatInput"] {
        background-color: var(--pf-surface) !important;
        border: 1px solid var(--pf-border) !important;
        border-radius: 6px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: var(--pf-ink) !important;
        font-size: 13px !important;
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
        animation: pfFadeSlideUp 250ms ease forwards;
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
