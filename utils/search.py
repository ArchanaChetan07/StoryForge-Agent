"""
Search utility — wraps Tavily to fetch live web results.
Returns structured source data and raw text for downstream summarisation.
Includes DEMO_MODE stubs when Tavily key is missing.
"""

from __future__ import annotations

from typing import Optional

from utils.config import DEMO_MODE, TAVILY_API_KEY


def _stub_results(query: str, max_results: int = 4) -> tuple[list[dict], str, None]:
    """Offline stub sources so demos/tests work without Tavily."""
    q = (query or "topic").strip() or "topic"
    sources = [
        {
            "title": f"{q.title()} — key development",
            "url": "https://example.com/storyforge/demo/1",
            "snippet": (
                f"Recent reporting on {q} highlights accelerating progress, "
                "new funding rounds, and expanding public interest across markets."
            ),
        },
        {
            "title": f"Analysis: what {q} means next",
            "url": "https://example.com/storyforge/demo/2",
            "snippet": (
                f"Experts tracking {q} point to measurable gains this year, "
                "naming leading labs and citing early deployment data."
            ),
        },
        {
            "title": f"{q.title()} timeline and figures",
            "url": "https://example.com/storyforge/demo/3",
            "snippet": (
                f"A brief timeline of {q} includes major announcements, "
                "regulatory notes, and a look ahead for the next quarter."
            ),
        },
        {
            "title": f"Community take on {q}",
            "url": "https://example.com/storyforge/demo/4",
            "snippet": (
                f"Creators and analysts summarizing {q} for general audiences, "
                "with clear takeaways and what to watch next."
            ),
        },
    ][:max_results]
    chunks = [f"[{s['title']}]\n{s['snippet']}" for s in sources]
    return sources, "\n\n".join(chunks), None


def fetch_realtime_info(
    query: str,
    api_key: str | None = None,
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
    key = (api_key if api_key is not None else TAVILY_API_KEY) or ""

    if DEMO_MODE or not key:
        return _stub_results(query, max_results=max_results)

    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=key)
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
