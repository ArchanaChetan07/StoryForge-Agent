"""Planner and reviser: search → observe → revise thin results → brief → (HITL) → script."""

from __future__ import annotations

from agent.types import AgentState, Plan, PlanStep
from utils.config import MIN_RAW_CHARS, MIN_SOURCES


def is_thin_results(state: AgentState) -> bool:
    """True when search returned too little usable material."""
    if not state.sources:
        return True
    if len(state.sources) < MIN_SOURCES:
        return True
    if len((state.raw_text or "").strip()) < MIN_RAW_CHARS:
        return True
    return False


def create_initial_plan(state: AgentState) -> Plan:
    """First plan: web search on the topic."""
    q = state.search_query or state.topic
    return Plan(
        steps=[
            PlanStep("search_web", {"query": q}, "Fetch live sources for the topic"),
        ],
        notes="phase=research",
    )


def revise_plan(state: AgentState) -> Plan | None:
    """
    Observe → revise loop:
    - After first search, if thin, revise query once and re-search.
    - Then generate research brief.
    - Script generation is gated by HITL (state.approved); planner stops until approved.
    """
    if not state.search_attempted:
        return create_initial_plan(state)

    if is_thin_results(state) and state.revisions < 1:
        state.revisions += 1
        return Plan(
            steps=[
                PlanStep(
                    "revise_query",
                    {
                        "query": state.search_query or state.topic,
                        "observation_note": (
                            f"Only {len(state.sources)} sources / "
                            f"{len(state.raw_text or '')} chars; broaden or clarify."
                        ),
                    },
                    "Broaden query after thin search results",
                ),
                PlanStep(
                    "search_web",
                    {"query": state.search_query or state.topic},
                    "Re-search with revised query",
                ),
            ],
            notes="phase=revise_thin_search",
        )

    if not state.brief_done:
        return Plan(
            steps=[
                PlanStep(
                    "generate_brief",
                    {
                        "query": state.topic,
                        "raw_text": state.raw_text,
                    },
                    "Synthesize research brief from sources",
                ),
            ],
            notes="phase=brief",
        )

    # Script requires HITL approval
    if not state.approved:
        return None

    if not state.script:
        return Plan(
            steps=[
                PlanStep(
                    "generate_script",
                    {"summary": state.brief},
                    "Write short-form video script from brief",
                ),
            ],
            notes="phase=script",
        )

    return None
