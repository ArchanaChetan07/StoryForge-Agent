"""
Generator utility — wraps Google Gemini for summary and script generation.
"""

from __future__ import annotations
from typing import Optional
import google.generativeai as genai

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


def _get_model(api_key: str) -> genai.GenerativeModel:
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL)


def generate_summary(
    query: str,
    raw_text: str,
    api_key: str,
) -> tuple[str, Optional[str]]:
    """
    Summarise *raw_text* for *query* using Gemini.

    Returns (summary_text, error_message).
    """
    if not api_key:
        return "", "GEMINI_API_KEY is not set."
    if not raw_text:
        return "", "No source text to summarise."

    prompt = _SUMMARY_PROMPT.format(query=query, raw_text=raw_text)
    try:
        model = _get_model(api_key)
        response = model.generate_content(prompt)
        text = response.text.strip() if response and response.text else ""
        return text or "", None if text else "Empty response from Gemini."
    except Exception as exc:
        return "", str(exc)


def generate_video_script(
    summary: str,
    api_key: str,
) -> tuple[str, Optional[str]]:
    """
    Generate a short-form video script from *summary* using Gemini.

    Returns (script_text, error_message).
    """
    if not api_key:
        return "", "GEMINI_API_KEY is not set."
    if not summary:
        return "", "No summary provided."

    prompt = _SCRIPT_PROMPT.format(summary=summary)
    try:
        model = _get_model(api_key)
        response = model.generate_content(prompt)
        text = response.text.strip() if response and response.text else ""
        return text or "", None if text else "Empty response from Gemini."
    except Exception as exc:
        return "", str(exc)
