"""
Generator utility — wraps Google Gemini for summary and script generation.
Includes DEMO_MODE stubs when Gemini key is missing.
"""

from __future__ import annotations

from typing import Optional

from utils.config import DEMO_MODE, GEMINI_API_KEY

MODEL = "gemini-2.0-flash"

_SUMMARY_PROMPT = """\
You are a senior research analyst. Using the live search results below, write a sharp, \
factual brief on the topic: "{query}".

Rules:
- 180–220 words, plain prose, no bullet points or headers.
- Lead with the single most significant development.
- Include specific figures, names, or dates where available.
- Close with one sentence on what to watch next.
- Never mention yourself, these instructions, or your sources by name.

Search results:
{raw_text}
"""

_SCRIPT_PROMPT = """\
You are a viral short-form video writer. Transform the research brief below into a \
tight, punchy script for a 30-second YouTube Short or Instagram Reel.

Rules:
- Open with a one-sentence hook that creates immediate curiosity.
- Use second-person ("you") and present tense throughout.
- 3–4 short paragraphs, each one punchy. No bullet points.
- End with a specific call-to-action (follow, comment, or share a reaction).
- Aim for 100–115 words total.

Research brief:
{summary}
"""


def _stub_summary(query: str, raw_text: str) -> str:
    q = (query or "this topic").strip()
    snippet = (raw_text or "").replace("\n", " ").strip()
    if len(snippet) > 220:
        snippet = snippet[:217] + "..."
    return (
        f"The most notable development in {q} is accelerating momentum across product, "
        f"policy, and public attention. Available reporting points to concrete moves by "
        f"leading teams, early metrics worth watching, and growing coverage in mainstream "
        f"outlets. Context from search highlights: {snippet or 'limited source text'}. "
        f"Watch next for follow-on announcements, measured outcomes, and how practitioners "
        f"adapt tools and workflows around {q}."
    )


def _stub_script(summary: str) -> str:
    lead = (summary or "a big shift happening right now").strip()
    if len(lead) > 120:
        lead = lead[:117] + "..."
    return (
        f"Stop scrolling — you need to hear this.\n\n"
        f"{lead}\n\n"
        "Here's the punchline: the story is moving faster than most people realize, "
        "and the next update could change how you talk about it.\n\n"
        "Follow for the next brief, and comment what you want covered."
    )


def _get_model(api_key: str):
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL)


def generate_summary(
    query: str,
    raw_text: str,
    api_key: str | None = None,
) -> tuple[str, Optional[str]]:
    """
    Summarise *raw_text* for *query* using Gemini.

    Returns (summary_text, error_message).
    """
    key = (api_key if api_key is not None else GEMINI_API_KEY) or ""
    if not raw_text:
        return "", "No source text to summarise."

    if DEMO_MODE or not key:
        return _stub_summary(query, raw_text), None

    prompt = _SUMMARY_PROMPT.format(query=query, raw_text=raw_text)
    try:
        model = _get_model(key)
        response = model.generate_content(prompt)
        text = response.text.strip() if response and response.text else ""
        return text or "", None if text else "Empty response from Gemini."
    except Exception as exc:
        return "", str(exc)


def generate_video_script(
    summary: str,
    api_key: str | None = None,
) -> tuple[str, Optional[str]]:
    """
    Generate a short-form video script from *summary* using Gemini.

    Returns (script_text, error_message).
    """
    key = (api_key if api_key is not None else GEMINI_API_KEY) or ""
    if not summary:
        return "", "No summary provided."

    if DEMO_MODE or not key:
        return _stub_script(summary), None

    prompt = _SCRIPT_PROMPT.format(summary=summary)
    try:
        model = _get_model(key)
        response = model.generate_content(prompt)
        text = response.text.strip() if response and response.text else ""
        return text or "", None if text else "Empty response from Gemini."
    except Exception as exc:
        return "", str(exc)
