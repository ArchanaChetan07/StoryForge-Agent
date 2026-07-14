"""Plan → tool → observe → revise loop for StoryForge."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from agent.planner import create_initial_plan, is_thin_results, revise_plan
from agent.tools import call_tool
from agent.types import AgentState, Observation, Plan
from utils.config import MAX_AGENT_STEPS
from utils.tracing import Trace, new_run_id, span


@dataclass
class AgentResult:
    state: AgentState
    trace: Trace
    status: str
    message: str = ""
    awaiting_approval: bool = False
    extras: dict[str, Any] = field(default_factory=dict)


def _apply_observation(state: AgentState, obs: Observation) -> None:
    state.observations.append(obs)
    if obs.tool == "search_web":
        state.search_attempted = True
    if not obs.ok:
        return
    if obs.tool == "search_web":
        data = obs.data or {}
        state.sources = list(data.get("sources") or [])
        state.raw_text = str(data.get("raw_text") or "")
        if data.get("query"):
            state.search_query = str(data["query"])
    elif obs.tool == "revise_query":
        state.search_query = str(obs.data or "").strip() or state.search_query
        # Clear prior search so re-search is meaningful
        state.sources = []
        state.raw_text = ""
    elif obs.tool == "generate_brief":
        state.brief = str(obs.data or "")
        state.brief_done = True
    elif obs.tool == "generate_script":
        state.script = str(obs.data or "")


def _execute_plan(state: AgentState, plan: Plan, trace: Trace) -> None:
    for step in plan.steps:
        with span(trace, f"tool:{step.tool}", reason=step.reason) as s:
            try:
                args = dict(step.args)
                # Keep search/brief args in sync after revise
                if step.tool == "search_web" and state.search_query:
                    args["query"] = state.search_query
                if step.tool == "generate_brief":
                    args["query"] = state.topic
                    args["raw_text"] = state.raw_text
                if step.tool == "generate_script":
                    args["summary"] = state.brief
                result = call_tool(step.tool, **args)
                obs = Observation(tool=step.tool, ok=True, data=result)
                s.attrs["ok"] = True
            except Exception as e:
                obs = Observation(tool=step.tool, ok=False, error=str(e))
                s.attrs["ok"] = False
                s.status = "error"
                s.error = str(e)
            _apply_observation(state, obs)


def run_research_phase(topic: str) -> AgentResult:
    """Search (with revise-if-thin) → generate brief; stop for HITL before script."""
    state = AgentState(topic=topic, search_query=topic)
    trace = Trace(run_id=new_run_id())
    steps_used = 0

    with span(trace, "phase:research"):
        plan = create_initial_plan(state)
        _execute_plan(state, plan, trace)
        steps_used += len(plan.steps)

        while steps_used < MAX_AGENT_STEPS:
            plan = revise_plan(state)
            if plan is None:
                break
            # Stop before script phase — script needs HITL
            if plan.notes == "phase=script":
                break
            _execute_plan(state, plan, trace)
            steps_used += len(plan.steps)
            if state.brief_done:
                # One more revise_plan call may request script; leave for HITL
                break

    state.pending_approval = state.brief or None
    thin = is_thin_results(state) and not state.brief
    status = "awaiting_approval" if state.brief_done else ("thin_results" if thin else "error")
    return AgentResult(
        state=state,
        trace=trace,
        status=status,
        message=(
            "Approve brief to generate video script."
            if state.brief_done
            else "Research incomplete."
        ),
        awaiting_approval=bool(state.brief_done),
        extras={
            "sources_count": len(state.sources),
            "revisions": state.revisions,
            "search_query": state.search_query,
        },
    )


def run_script_phase(state: AgentState, previous_trace: Trace | None = None) -> AgentResult:
    """After HITL approval: generate the video script."""
    if not state.approved:
        raise ValueError("Cannot generate script without HITL approval.")
    if not state.brief:
        raise ValueError("Cannot generate script without a research brief.")

    trace = previous_trace or Trace(run_id=new_run_id())
    with span(trace, "phase:script"):
        plan = revise_plan(state)
        if plan is None or plan.notes != "phase=script":
            # Force script step if planner already considered it done
            from agent.types import PlanStep

            plan = Plan(
                steps=[
                    PlanStep(
                        "generate_script",
                        {"summary": state.brief},
                        "Write short-form video script from brief",
                    )
                ],
                notes="phase=script",
            )
        _execute_plan(state, plan, trace)

    status = "ok" if state.script else "error"
    return AgentResult(
        state=state,
        trace=trace,
        status=status,
        message="Script ready." if state.script else "Script generation failed.",
        awaiting_approval=False,
    )


def run_planning_loop(
    topic: str,
    *,
    auto_approve: bool = False,
) -> AgentResult:
    """
    Full loop for non-UI callers / MCP / tests.
    If auto_approve=False, returns after brief for HITL.
    """
    research = run_research_phase(topic)
    if not auto_approve:
        return research
    if not research.state.brief_done:
        return research
    state = research.state
    state.approved = True
    return run_script_phase(state, previous_trace=research.trace)
