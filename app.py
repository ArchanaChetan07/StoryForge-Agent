"""
StoryForge Agent — Main Streamlit Application
Fetches real-time information and generates AI-powered summaries and video scripts.
"""

import streamlit as st
import os
from dotenv import load_dotenv

from utils.search import fetch_realtime_info
from utils.generator import generate_summary, generate_video_script
from utils.styles import inject_styles

# ─── Configuration ───────────────────────────────────────────────────────────

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

st.set_page_config(
    page_title="StoryForge",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_styles()


# ─── Helpers ─────────────────────────────────────────────────────────────────

def validate_env() -> bool:
    """Return True if required API keys are present."""
    missing = []
    if not GEMINI_API_KEY:
        missing.append("GEMINI_API_KEY")
    if not TAVILY_API_KEY:
        missing.append("TAVILY_API_KEY")
    if missing:
        st.error(
            f"Missing environment variables: **{', '.join(missing)}**\n\n"
            "Add them to your `.env` file and restart the app.",
            icon="🔑",
        )
        return False
    return True


def render_source_cards(sources: list[dict]) -> None:
    """Render individual source reference cards."""
    if not sources:
        return
    st.markdown("<p class='section-label'>SOURCES</p>", unsafe_allow_html=True)
    for src in sources:
        title = src.get("title", "Untitled")
        url = src.get("url", "#")
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        st.markdown(
            f"""
            <a class="source-card" href="{url}" target="_blank">
                <span class="source-title">{title}</span>
                <span class="source-domain">{domain} ↗</span>
            </a>
            """,
            unsafe_allow_html=True,
        )


# ─── Main UI ─────────────────────────────────────────────────────────────────

def main() -> None:
    if not validate_env():
        st.stop()

    # Header
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">LIVE INTELLIGENCE</div>
            <h1 class="hero-title">StoryForge</h1>
            <p class="hero-sub">
                Enter any topic. Get a research brief and a ready-to-shoot video script — 
                powered by live web search and Gemini AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Search input
    st.markdown("<div class='search-wrap'>", unsafe_allow_html=True)
    query = st.text_input(
        label="search",
        placeholder="Try: breakthrough cancer treatments 2025, or Tesla earnings Q3...",
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if not query:
        st.markdown(
            """
            <div class="empty-state">
                <p>Ask about anything — breaking news, research trends, market moves, science discoveries.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # ── Step 1: Fetch sources ────────────────────────────────────────────────
    with st.spinner("Searching the web…"):
        sources, raw_text, search_error = fetch_realtime_info(
            query=query, api_key=TAVILY_API_KEY
        )

    if search_error:
        st.error(f"Search failed: {search_error}", icon="🔍")
        return

    if not sources:
        st.warning(
            "No results found for that query. Try rephrasing or broadening your search.",
            icon="🔎",
        )
        return

    # ── Step 2: Generate summary ─────────────────────────────────────────────
    with st.spinner("Writing your research brief…"):
        summary, summary_error = generate_summary(
            query=query, raw_text=raw_text, api_key=GEMINI_API_KEY
        )

    if summary_error:
        st.error(f"Summary generation failed: {summary_error}", icon="⚡")
        return

    # ── Render summary ───────────────────────────────────────────────────────
    st.markdown("<div class='result-block'>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>RESEARCH BRIEF</p>", unsafe_allow_html=True)
    st.markdown(f"<div class='summary-text'>{summary}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    render_source_cards(sources)

    # ── Step 3: Optional video script ────────────────────────────────────────
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>VIDEO SCRIPT</p>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-desc'>Turn this brief into a punchy 30-second script for Reels or Shorts.</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        generate_btn = st.button("Generate script →", type="primary", use_container_width=True)

    if generate_btn or st.session_state.get("script_generated"):
        if not st.session_state.get("script_generated"):
            with st.spinner("Writing your video script…"):
                script, script_error = generate_video_script(
                    summary=summary, api_key=GEMINI_API_KEY
                )

            if script_error:
                st.error(f"Script generation failed: {script_error}", icon="🎬")
                return

            st.session_state["current_script"] = script
            st.session_state["script_generated"] = True
        else:
            script = st.session_state.get("current_script", "")

        st.markdown("<div class='script-block'>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='script-text'>{script}</div>", unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

        col_a, col_b = st.columns([1, 3])
        with col_a:
            st.download_button(
                label="Download .txt",
                data=script,
                file_name="storyforge_script.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_b:
            if st.button("Regenerate", use_container_width=True):
                st.session_state.pop("current_script", None)
                st.session_state.pop("script_generated", None)
                st.rerun()

    # Reset script state when query changes
    if "last_query" not in st.session_state or st.session_state["last_query"] != query:
        st.session_state.pop("current_script", None)
        st.session_state.pop("script_generated", None)
        st.session_state["last_query"] = query

    # Footer
    st.markdown(
        """
        <div class='footer'>
            StoryForge · Powered by Gemini &amp; Tavily
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
