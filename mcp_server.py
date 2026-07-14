"""
StoryForge MCP Server
Exposes research / script tools and the full planning-agent entrypoint.

Usage:
    mcp dev mcp_server.py
    mcp install mcp_server.py
"""

from __future__ import annotations

import asyncio

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from agent.loop import run_planning_loop
from utils.config import DEMO_MODE, GEMINI_API_KEY, TAVILY_API_KEY
from utils.generator import generate_summary, generate_video_script
from utils.search import fetch_realtime_info

load_dotenv()

mcp = FastMCP(
    name="StoryForge",
    description=(
        "Planning agent: search → observe → revise thin results → research brief → "
        "optional HITL → short-form video script. Demo stubs when keys are missing."
    ),
)


@mcp.tool()
async def research_topic(query: str) -> str:
    """
    Run research phase (search + revise-if-thin + brief) and return the brief text.

    Args:
        query: Topic or question to research.
    """
    def _run() -> str:
        result = run_planning_loop(query, auto_approve=False)
        if result.state.brief:
            return result.state.brief
        return result.message or f"Research failed for '{query}'."

    return await asyncio.to_thread(_run)


@mcp.tool()
async def create_video_script(query: str) -> str:
    """
    Full agent loop with auto-approve: research → brief → script.

    Args:
        query: Topic to turn into a video script.
    """
    def _run() -> str:
        result = run_planning_loop(query, auto_approve=True)
        if result.state.script:
            return result.state.script
        return result.message or f"Script failed for '{query}'."

    return await asyncio.to_thread(_run)


@mcp.tool()
async def run_storyforge_agent(query: str, auto_approve: bool = True) -> dict:
    """
    Run the plan→search→observe→revise→brief→(HITL)→script agent.

    For unattended MCP use, keep auto_approve=True.
    """
    def _run() -> dict:
        result = run_planning_loop(query, auto_approve=auto_approve)
        return {
            "status": result.status,
            "awaiting_approval": result.awaiting_approval,
            "demo_mode": DEMO_MODE,
            "topic": result.state.topic,
            "search_query": result.state.search_query,
            "brief": result.state.brief,
            "script": result.state.script,
            "sources": result.state.sources,
            "revisions": result.state.revisions,
            "trace": result.trace.to_dict(),
        }

    return await asyncio.to_thread(_run)


@mcp.tool()
async def search_only(query: str) -> str:
    """Low-level web search (Tavily or demo stub). Returns concatenated snippets."""
    sources, raw_text, err = fetch_realtime_info(query=query, api_key=TAVILY_API_KEY)
    if err:
        return f"Search error: {err}"
    if not sources:
        return f"No results for '{query}'."
    return raw_text


@mcp.tool()
async def summarize_only(query: str, raw_text: str) -> str:
    """Low-level brief generation from provided raw text."""
    summary, err = generate_summary(query=query, raw_text=raw_text, api_key=GEMINI_API_KEY)
    if err:
        return f"Summary error: {err}"
    return summary


@mcp.tool()
async def script_only(summary: str) -> str:
    """Low-level script generation from a research brief."""
    script, err = generate_video_script(summary=summary, api_key=GEMINI_API_KEY)
    if err:
        return f"Script error: {err}"
    return script


if __name__ == "__main__":
    mcp.run(transport="stdio")
