"""
StoryForge UI styles.
Design direction: editorial dark, ink-black background, warm amber accent,
Space Grotesk display / Inter body. Signature element: a thin amber left-rule
on every result block — like a journalist's markup.
"""

import streamlit as st

_CSS = """
/* ── Google Fonts ───────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;450;500&display=swap');

/* ── Reset / Base ───────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #0C0C0E !important;
    color: #E8E6E1 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

.block-container {
    max-width: 780px !important;
    padding: 2.5rem 1.5rem 5rem !important;
}

/* ── Hero ───────────────────────────────────────────── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
}

.hero-badge {
    display: inline-block;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    color: #E8A838;
    border: 1px solid #E8A83850;
    border-radius: 100px;
    padding: 0.3rem 0.85rem;
    margin-bottom: 1.25rem;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(2.6rem, 6vw, 4rem) !important;
    font-weight: 700 !important;
    color: #F2EFE9 !important;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin: 0 0 1.1rem !important;
}

.hero-sub {
    font-size: 1.05rem;
    color: #7A7775;
    line-height: 1.65;
    max-width: 560px;
    margin: 0 auto;
}

/* ── Search input ───────────────────────────────────── */
.search-wrap { margin-bottom: 0.25rem; }

[data-testid="stTextInput"] input {
    background-color: #141416 !important;
    border: 1.5px solid #2A2A2E !important;
    border-radius: 10px !important;
    color: #E8E6E1 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.1rem !important;
    transition: border-color 0.2s ease;
    caret-color: #E8A838;
}
[data-testid="stTextInput"] input:focus {
    border-color: #E8A838 !important;
    box-shadow: 0 0 0 3px #E8A83818 !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #3E3E44 !important; }

/* ── Empty state ────────────────────────────────────── */
.empty-state {
    text-align: center;
    color: #3E3E44;
    font-size: 0.95rem;
    padding: 3rem 0;
}

/* ── Section labels ─────────────────────────────────── */
.section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    color: #E8A838;
    text-transform: uppercase;
    margin: 2rem 0 0.75rem !important;
}

.section-desc {
    font-size: 0.9rem;
    color: #5A5A60;
    margin: -0.25rem 0 1rem !important;
}

/* ── Result / summary block ─────────────────────────── */
.result-block {
    border-left: 2px solid #E8A838;
    padding: 1.25rem 1.5rem;
    background: #111113;
    border-radius: 0 10px 10px 0;
    margin-top: 0.5rem;
}

.summary-text {
    font-size: 1.05rem;
    line-height: 1.8;
    color: #C8C5BF;
}

/* ── Source cards ───────────────────────────────────── */
.source-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.65rem 0.9rem;
    background: #111113;
    border: 1px solid #1E1E22;
    border-radius: 8px;
    text-decoration: none !important;
    margin-bottom: 0.5rem;
    transition: border-color 0.2s, background 0.2s;
}
.source-card:hover {
    border-color: #E8A83855;
    background: #16161A;
}
.source-title {
    font-size: 0.88rem;
    color: #9A9793;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 76%;
}
.source-domain {
    font-size: 0.78rem;
    color: #E8A838;
    flex-shrink: 0;
    font-family: 'Space Grotesk', sans-serif;
}

/* ── Divider ────────────────────────────────────────── */
.divider {
    height: 1px;
    background: #1E1E22;
    margin: 2.5rem 0 0;
}

/* ── Script block ───────────────────────────────────── */
.script-block {
    border-left: 2px solid #3B82F6;
    padding: 1.25rem 1.5rem;
    background: #0E1118;
    border-radius: 0 10px 10px 0;
    margin: 0.75rem 0 1.25rem;
}

.script-text {
    font-size: 1.05rem;
    line-height: 1.85;
    color: #BFC3CF;
    white-space: pre-wrap;
}

/* ── Buttons ────────────────────────────────────────── */
div.stButton > button[kind="primary"] {
    background: #E8A838 !important;
    color: #0C0C0E !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 0.6rem 1.4rem !important;
    letter-spacing: 0.01em;
    transition: background 0.2s, transform 0.15s !important;
}
div.stButton > button[kind="primary"]:hover {
    background: #F5BC50 !important;
    transform: translateY(-1px);
}

div.stButton > button[kind="secondary"],
div.stButton > button:not([kind]) {
    background: transparent !important;
    color: #5A5A60 !important;
    border: 1px solid #2A2A2E !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1.2rem !important;
    transition: border-color 0.2s, color 0.2s !important;
}
div.stButton > button:not([kind]):hover {
    border-color: #5A5A60 !important;
    color: #9A9793 !important;
}

/* Download button */
[data-testid="stDownloadButton"] button {
    background: transparent !important;
    color: #E8A838 !important;
    border: 1px solid #E8A83850 !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: #E8A83812 !important;
    border-color: #E8A838 !important;
}

/* ── Spinner ────────────────────────────────────────── */
[data-testid="stSpinner"] > div {
    color: #E8A838 !important;
}

/* ── Alerts ─────────────────────────────────────────── */
[data-testid="stAlert"] {
    background: #111113 !important;
    border-radius: 8px !important;
    border-left-color: #E8A838 !important;
    color: #C8C5BF !important;
    font-size: 0.93rem !important;
}

/* ── Footer ─────────────────────────────────────────── */
.footer {
    text-align: center;
    font-size: 0.78rem;
    color: #2A2A2E;
    margin-top: 4rem;
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: 0.05em;
}
"""


def inject_styles() -> None:
    """Inject all custom CSS into the Streamlit page."""
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)
