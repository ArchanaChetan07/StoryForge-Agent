"""Tool registry for the StoryForge planning agent."""

from __future__ import annotations

from typing import Any, Callable

from utils.config import GEMINI_API_KEY, TAVILY_API_KEY
from utils.generator import generate_summary, generate_video_script
from utils.search import fetch_realtime_info

ToolFn = Callable[..., Any]


def search_web(query: str) -> dict[str, Any]:
    sources, raw_text, err = fetch_realtime_info(query=query, api_key=TAVILY_API_KEY)
    if err:
        raise RuntimeError(err)
    return {"sources": sources, "raw_text": raw_text, "query": query}


def revise_query(query: str, observation_note: str) -> str:
    """Deterministic broaden of a thin query (no LLM required)."""
    q = (query or "").strip()
    note = (observation_note or "").lower()
    if "broad" in note or "thin" in note or "only" in note:
        if "latest" not in q.lower() and "202" not in q:
            return f"{q} latest developments overview".strip()
        return f"{q} news trends analysis".strip()
    return f"{q} key facts and context".strip()


def generate_brief(query: str, raw_text: str) -> str:
    text, err = generate_summary(query=query, raw_text=raw_text, api_key=GEMINI_API_KEY)
    if err:
        raise RuntimeError(err)
    return text


def generate_script(summary: str) -> str:
    text, err = generate_video_script(summary=summary, api_key=GEMINI_API_KEY)
    if err:
        raise RuntimeError(err)
    return text


TOOLS: dict[str, ToolFn] = {
    "search_web": search_web,
    "revise_query": revise_query,
    "generate_brief": generate_brief,
    "generate_script": generate_script,
}


def call_tool(name: str, **kwargs: Any) -> Any:
    if name not in TOOLS:
        raise KeyError(f"Unknown tool: {name}")
    return TOOLS[name](**kwargs)
