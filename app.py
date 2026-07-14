"""
StoryForge Agent — Streamlit UI
Planning agent: search → observe → revise → brief → HITL → script.
"""

from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

from agent.hitl import apply_approval, request_script_approval
from agent.loop import run_research_phase, run_script_phase
from utils.config import DEMO_MODE, HITL_ENABLED
from utils.styles import inject_styles

load_dotenv()

st.set_page_config(
    page_title="StoryForge",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_styles()


def render_source_cards(sources: list[dict]) -> None:
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


def main() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">LIVE INTELLIGENCE</div>
            <h1 class="hero-title">StoryForge</h1>
            <p class="hero-sub">
                Enter any topic. The agent plans research, revises thin searches,
                writes a brief, then — after optional approval — a ready-to-shoot script.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if DEMO_MODE:
        st.info("Running in **DEMO_MODE** (missing keys or DEMO_MODE=1). Using stub search & generation.")

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

    if "last_query" not in st.session_state or st.session_state["last_query"] != query:
        st.session_state.pop("agent_research", None)
        st.session_state.pop("agent_script", None)
        st.session_state["last_query"] = query

    if "agent_research" not in st.session_state:
        with st.spinner("Agent researching (plan → search → revise if thin → brief)…"):
            st.session_state["agent_research"] = run_research_phase(query)

    research = st.session_state["agent_research"]
    state = research.state

    if not state.brief:
        st.error(research.message or "Research failed.", icon="🔍")
        if research.trace.spans:
            with st.expander("Trace"):
                st.json(research.trace.to_dict())
        return

    st.markdown("<div class='result-block'>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>RESEARCH BRIEF</p>", unsafe_allow_html=True)
    st.markdown(f"<div class='summary-text'>{state.brief}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    render_source_cards(state.sources)

    if research.extras.get("revisions"):
        st.caption(
            f"Query revised once after thin results → `{research.extras.get('search_query')}`"
        )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>VIDEO SCRIPT</p>", unsafe_allow_html=True)

    if HITL_ENABLED and "agent_script" not in st.session_state:
        approval = request_script_approval(state.brief)
        st.markdown(
            "<p class='section-desc'>HITL — approve before the agent spends a generation step on the script.</p>",
            unsafe_allow_html=True,
        )
        st.write(approval.message)
        col1, col2 = st.columns([1, 3])
        with col1:
            approve = st.button("Approve script →", type="primary", use_container_width=True)
        with col2:
            skip = st.button("Skip script", use_container_width=True)
        if skip:
            st.info("Script skipped. Edit the topic or re-run to continue.")
            with st.expander("Trace"):
                st.json(research.trace.to_dict())
            return
        if not approve:
            with st.expander("Trace"):
                st.json(research.trace.to_dict())
            return
        if not apply_approval(True):
            return
        state.approved = True
        with st.spinner("Writing your video script…"):
            st.session_state["agent_script"] = run_script_phase(
                state, previous_trace=research.trace
            )
    elif "agent_script" not in st.session_state:
        # HITL disabled — auto-approve
        state.approved = True
        with st.spinner("Writing your video script…"):
            st.session_state["agent_script"] = run_script_phase(
                state, previous_trace=research.trace
            )

    script_result = st.session_state.get("agent_script")
    if script_result:
        script = script_result.state.script
        if not script:
            st.error(script_result.message or "Script generation failed.", icon="🎬")
            return

        st.markdown("<div class='script-block'>", unsafe_allow_html=True)
        st.markdown(f"<div class='script-text'>{script}</div>", unsafe_allow_html=True)
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
                st.session_state.pop("agent_script", None)
                st.rerun()

        with st.expander("Trace"):
            st.json(script_result.trace.to_dict())

    st.markdown(
        """
        <div class='footer'>
            StoryForge · Planning agent · Gemini &amp; Tavily
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
