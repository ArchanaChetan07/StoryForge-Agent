"""Pytest fixtures — force demo mode for offline green runs."""

import os

import pytest

os.environ["DEMO_MODE"] = "1"
os.environ.setdefault("GEMINI_API_KEY", "")
os.environ.setdefault("TAVILY_API_KEY", "")


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("DEMO_MODE", "1")
    monkeypatch.setenv("GEMINI_API_KEY", "")
    monkeypatch.setenv("TAVILY_API_KEY", "")
