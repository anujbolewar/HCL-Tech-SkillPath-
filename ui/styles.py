"""Modern UI stylesheet for PathFinder AI.

Implements a shadcn/zinc pure-black dark aesthetic with glassmorphic cards,
Space Grotesk typography, subtle borders, and comprehensive mobile responsiveness.
"""

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Typography & Headers */
    h1, h2, h3, .hero-title, .metric-val, .course-title, .node-header-title {
        font-family: 'Space Grotesk', 'Inter', sans-serif !important;
        letter-spacing: -0.02em;
    }

    /* Core background */
    .stApp {
        background: #09090b;
        color: #fafafa;
    }

    /* Hero Card */
    .hero-card {
        background: linear-gradient(135deg, #121215 0%, #18181b 100%);
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 26px 30px;
        margin-bottom: 22px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }

    .hero-title {
        background: linear-gradient(92deg, #fafafa 15%, #c7d2fe 60%, #93c5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.3rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: #a1a1aa;
        font-size: 0.98rem;
        line-height: 1.55;
    }

    /* Metric Summary Cards */
    .metric-container {
        background: #111114;
        border: 1px solid #27272a;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }

    .metric-container:hover {
        background: #16161a;
        border-color: #3f3f46;
        transform: translateY(-1px);
    }

    .metric-val {
        font-size: 1.45rem;
        font-weight: 700;
        color: #fafafa;
    }

    .metric-lbl {
        font-size: 0.72rem;
        color: #a1a1aa;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 4px;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.74rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 4px;
    }

    .badge-primary { background: rgba(79, 172, 254, 0.12); color: #7cc4ff; border: 1px solid rgba(79, 172, 254, 0.25); }
    .badge-success { background: rgba(16, 185, 129, 0.12); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.25); }
    .badge-warning { background: rgba(245, 158, 11, 0.12); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.25); }
    .badge-purple { background: rgba(139, 92, 246, 0.12); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.25); }
    .badge-muted { background: rgba(113, 113, 122, 0.15); color: #a1a1aa; border: 1px solid rgba(113, 113, 122, 0.3); }

    /* Course Cards */
    .course-card {
        background: #111114;
        border: 1px solid #27272a;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
        transition: border-color 0.18s ease, box-shadow 0.18s ease;
    }

    .course-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.15);
    }

    .course-card-completed {
        background: #0d1a14;
        border-color: rgba(16, 185, 129, 0.4);
    }

    .course-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #f4f4f5;
        margin: 8px 0 4px 0;
    }

    /* Node Inspector Panel (The "Why" panel on DAG) */
    .node-inspector-card {
        background: #131317;
        border: 1px solid #3b82f6;
        border-radius: 10px;
        padding: 18px 22px;
        margin-top: 14px;
        box-shadow: 0 4px 18px rgba(59, 130, 246, 0.18);
        animation: fadeIn 0.25s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Responsive Mobile Breakpoints */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.7rem;
        }
        .hero-card {
            padding: 18px;
        }
        .metric-val {
            font-size: 1.2rem;
        }
        .metric-container {
            margin-bottom: 8px;
            padding: 12px;
        }
    }
</style>
"""

def inject_custom_styles() -> None:
    """Injects custom CSS styles into the Streamlit app."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
