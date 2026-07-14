"""StoryForge unit tests — stub search/generator + MCP tool surface (offline)."""

from agent.tools import TOOLS, call_tool, revise_query
from utils.generator import generate_summary, generate_video_script
from utils.search import fetch_realtime_info


class TestSearchAndGenerate:
    def test_stub_search_structure(self):
        sources, raw_text, err = fetch_realtime_info("AI chips", api_key="")
        assert err is None
        assert sources
        assert all("title" in s and "url" in s for s in sources)
        assert raw_text

    def test_stub_summary_and_script(self):
        _, raw, _ = fetch_realtime_info("climate tech", api_key="")
        summary, err = generate_summary("climate tech", raw, api_key="")
        assert err is None and summary
        script, err2 = generate_video_script(summary, api_key="")
        assert err2 is None and script
        assert "Follow" in script or "follow" in script.lower()

    def test_empty_raw_text_rejected(self):
        text, err = generate_summary("x", "", api_key="")
        assert text == "" and err

    def test_empty_summary_rejected(self):
        text, err = generate_video_script("", api_key="")
        assert text == "" and err


class TestTools:
    def test_tool_registry(self):
        assert "search_web" in TOOLS
        assert "generate_brief" in TOOLS
        assert "generate_script" in TOOLS

    def test_revise_query_broadens(self):
        revised = revise_query("solid state batteries", "Only 0 sources; broaden")
        assert "latest" in revised.lower() or "news" in revised.lower()

    def test_call_search_tool(self):
        data = call_tool("search_web", query="fusion energy")
        assert data["sources"]
        assert data["raw_text"]
