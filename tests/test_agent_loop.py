"""Agent loop and HITL tests (offline / DEMO_MODE)."""

from agent.hitl import apply_approval, request_script_approval
from agent.loop import run_planning_loop, run_research_phase, run_script_phase
from agent.planner import is_thin_results, revise_plan
from agent.types import AgentState
from utils.search import fetch_realtime_info


TOPIC = "breakthrough battery technology 2025"


def test_research_phase_awaits_approval():
    result = run_research_phase(TOPIC)
    assert result.awaiting_approval is True
    assert result.state.brief
    assert result.state.sources
    assert result.trace.spans
    assert any(s.name.startswith("tool:search_web") for s in result.trace.spans)
    assert any(s.name.startswith("tool:generate_brief") for s in result.trace.spans)


def test_full_loop_auto_approve_returns_script():
    result = run_planning_loop(TOPIC, auto_approve=True)
    assert result.status == "ok"
    assert result.state.brief
    assert result.state.script
    assert any(s.name.startswith("tool:generate_script") for s in result.trace.spans)


def test_hitl_helpers():
    req = request_script_approval("A short brief about batteries.")
    assert "Approve" in req.message
    assert apply_approval(True) is True
    assert apply_approval(False) is False


def test_script_requires_approval():
    research = run_research_phase(TOPIC)
    try:
        run_script_phase(research.state)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_demo_search_stub():
    sources, raw_text, err = fetch_realtime_info("quantum computing", api_key="")
    assert err is None
    assert len(sources) >= 2
    assert "quantum" in raw_text.lower()


def test_revise_plan_on_thin_results():
    state = AgentState(topic=TOPIC, search_query=TOPIC, search_attempted=True)
    state.sources = [{"title": "only one", "url": "https://example.com", "snippet": "x"}]
    state.raw_text = "too short"
    assert is_thin_results(state) is True
    plan = revise_plan(state)
    assert plan is not None
    assert plan.notes == "phase=revise_thin_search"
    assert any(s.tool == "revise_query" for s in plan.steps)
    assert any(s.tool == "search_web" for s in plan.steps)


def test_revise_triggered_when_first_search_empty(monkeypatch):
    calls = {"n": 0}

    def fake_fetch(query, api_key=None, max_results=4):
        calls["n"] += 1
        if calls["n"] == 1:
            return [], "", None
        return (
            [
                {"title": "A", "url": "https://example.com/a", "snippet": "alpha " * 20},
                {"title": "B", "url": "https://example.com/b", "snippet": "beta " * 20},
            ],
            "alpha " * 20 + "\n\n" + "beta " * 20,
            None,
        )

    monkeypatch.setattr("agent.tools.fetch_realtime_info", fake_fetch)
    result = run_research_phase("obscure niche topic xyz")
    assert result.state.revisions >= 1
    assert result.state.brief
    assert "latest" in (result.state.search_query or "").lower() or result.state.search_query != "obscure niche topic xyz"
