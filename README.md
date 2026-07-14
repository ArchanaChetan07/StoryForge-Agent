# StoryForge

**Real-time research briefs and short-form video scripts, powered by Gemini AI and live web search.**

StoryForge takes any topic, fetches the latest web results via Tavily, and uses Google Gemini to produce a concise research brief and a ready-to-shoot 30-second script for YouTube Shorts or Instagram Reels.

---

## Features

- **Planning agent** — plan → search → observe → revise thin queries → brief → (HITL) → script
- **Live web search** — Tavily pulls fresh results (stubbed in `DEMO_MODE`)
- **AI research brief** — Gemini synthesises sources into a sharp summary (stubbed offline)
- **Optional HITL** — approve the brief before script generation
- **Trace spans** — each run records tool spans for debugging
- **MCP server** — wraps the agent (`run_storyforge_agent`, `research_topic`, `create_video_script`)

---

## Quick start

```bash
# 1. Clone and enter the project
git clone <your-repo-url>
cd storyforge-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY and TAVILY_API_KEY

# 4. Run the Streamlit app
streamlit run app.py
```

---

## MCP Server (Claude Desktop integration)

```bash
# Development inspector
mcp dev mcp_server.py

# Install for Claude Desktop
mcp install mcp_server.py
```

### Available MCP tools

| Tool | Description |
|------|-------------|
| `research_topic(query)` | Searches the web and returns a research brief |
| `create_video_script(query)` | Researches a topic and returns a short-form video script |

---

## Project structure

```
storyforge-agent/
├── app.py              # Streamlit UI (HITL + agent loop)
├── mcp_server.py       # MCP tools wrapping the agent
├── agent/              # plan → tool → observe → revise
├── utils/
│   ├── search.py       # Tavily (+ DEMO stubs)
│   ├── generator.py    # Gemini (+ DEMO stubs)
│   ├── config.py
│   ├── tracing.py
│   └── styles.py
├── tests/
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Environment variables

| Variable | Description |
|----------|-------------|
| `DEMO_MODE` | `1` forces stub Tavily/Gemini (also auto when keys missing) |
| `GEMINI_API_KEY` | Google AI Studio API key |
| `TAVILY_API_KEY` | Tavily search API key |
| `HITL_ENABLED` | Optional approve-before-script in the UI (`1` default) |

Get your keys at [aistudio.google.com](https://aistudio.google.com) and [tavily.com](https://tavily.com).

> **Security note:** Never commit your `.env` file. The `.gitignore` in this repo excludes it by default.
