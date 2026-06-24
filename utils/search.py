"""
Search utility — wraps Tavily to fetch live web results.
Returns structured source data and raw text for downstream summarisation.
"""

from __future__ import annotations
from typing import Optional
from tavily import TavilyClient


def fetch_realtime_info(
    query: str,
    api_key: str,
    max_results: int = 4,
) -> tuple[list[dict], str, Optional[str]]:
    """
    Fetch live search results for *query* using the Tavily API.

    Returns
    -------
    sources : list[dict]
        Each item has keys: title, url, snippet.
    raw_text : str
        Concatenated plain-text snippets for the LLM.
    error : str | None
        Error message if the call failed, else None.
    """
    if not api_key:
        return [], "", "TAVILY_API_KEY is not set."

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(
            query=query,
            max_results=max_results,
            topic="general",
            include_answer=False,
        )
    except Exception as exc:
        return [], "", str(exc)

    results = response.get("results") if response else []
    if not results:
        return [], "", None

    sources: list[dict] = []
    chunks: list[str] = []

    for r in results:
        title = r.get("title", "").strip()
        url = r.get("url", "").strip()
        snippet = r.get("content", r.get("snippet", "")).strip()

        sources.append({"title": title, "url": url, "snippet": snippet})
        if snippet:
            chunks.append(f"[{title}]\n{snippet}")

    raw_text = "\n\n".join(chunks)
    return sources, raw_text, None
