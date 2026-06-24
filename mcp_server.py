"""
StoryForge MCP Server
Exposes research and script-generation tools via the Model Context Protocol.

Usage:
    mcp dev mcp_server.py        # development inspector
    mcp install mcp_server.py    # install for Claude Desktop
"""

import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from utils.search import fetch_realtime_info
from utils.generator import generate_summary, generate_video_script

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

mcp = FastMCP(
    name="StoryForge",
    description=(
        "Fetches real-time web information on any topic and generates "
        "AI-powered research briefs and short-form video scripts."
    ),
)


@mcp.tool()
async def research_topic(query: str) -> str:
    """
    Search the web for *query* and return an AI-generated research brief (≈200 words).

    Args:
        query: The topic or question to research.

    Returns:
        A concise, factual summary with key developments and trends.
    """
    sources, raw_text, search_err = fetch_realtime_info(
        query=query, api_key=TAVILY_API_KEY
    )
    if search_err:
        return f"Search error: {search_err}"
    if not sources:
        return f"No results found for '{query}'."

    summary, gen_err = generate_summary(
        query=query, raw_text=raw_text, api_key=GEMINI_API_KEY
    )
    if gen_err:
        return f"Summary error: {gen_err}"
    return summary


@mcp.tool()
async def create_video_script(query: str) -> str:
    """
    Research *query* and return a ready-to-shoot 30-second video script
    for YouTube Shorts or Instagram Reels.

    Args:
        query: The topic or question to turn into a video script.

    Returns:
        A punchy, hook-led script (≈110 words) with a call-to-action.
    """
    sources, raw_text, search_err = fetch_realtime_info(
        query=query, api_key=TAVILY_API_KEY
    )
    if search_err:
        return f"Search error: {search_err}"
    if not sources:
        return f"No results found for '{query}'."

    summary, sum_err = generate_summary(
        query=query, raw_text=raw_text, api_key=GEMINI_API_KEY
    )
    if sum_err:
        return f"Summary error: {sum_err}"

    script, script_err = generate_video_script(
        summary=summary, api_key=GEMINI_API_KEY
    )
    if script_err:
        return f"Script error: {script_err}"
    return script


if __name__ == "__main__":
    mcp.run(transport="stdio")
