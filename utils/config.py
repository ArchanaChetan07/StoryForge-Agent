"""Application configuration from environment (lazy — no hard fail on import)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "").strip()

# Demo / offline mode when keys are missing (or DEMO_MODE=1)
DEMO_MODE = os.getenv("DEMO_MODE", "").lower() in {"1", "true", "yes"} or (
    not GEMINI_API_KEY or not TAVILY_API_KEY
)

HITL_ENABLED = os.getenv("HITL_ENABLED", "1").lower() in {"1", "true", "yes"}
MAX_AGENT_STEPS = int(os.getenv("MAX_AGENT_STEPS", "8"))
MIN_SOURCES = int(os.getenv("MIN_SOURCES", "2"))
MIN_RAW_CHARS = int(os.getenv("MIN_RAW_CHARS", "80"))


def require_live_keys() -> None:
    """Raise only when a live (non-demo) path needs API credentials."""
    if DEMO_MODE:
        return
    missing = []
    if not GEMINI_API_KEY:
        missing.append("GEMINI_API_KEY")
    if not TAVILY_API_KEY:
        missing.append("TAVILY_API_KEY")
    if missing:
        raise ValueError(
            f"Missing required env vars: {', '.join(missing)}. "
            "Set them in .env or enable DEMO_MODE=1."
        )
