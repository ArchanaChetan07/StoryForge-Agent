"""Typed structures for the StoryForge planning agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlanStep:
    tool: str
    args: dict[str, Any]
    reason: str = ""


@dataclass
class Plan:
    steps: list[PlanStep]
    notes: str = ""


@dataclass
class Observation:
    tool: str
    ok: bool
    data: Any = None
    error: str | None = None


@dataclass
class AgentState:
    topic: str
    search_query: str = ""
    sources: list[dict] = field(default_factory=list)
    raw_text: str = ""
    brief: str = ""
    script: str = ""
    pending_approval: str | None = None
    approved: bool = False
    search_attempted: bool = False
    brief_done: bool = False
    observations: list[Observation] = field(default_factory=list)
    revisions: int = 0
